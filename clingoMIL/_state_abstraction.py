import clingo
from copy import copy
from typing import List
from collections import defaultdict
import importlib.resources as pkg_resources

from . import encodings
from . import metarules as metarules_resource


class IDMaker:
    def __init__(self):
        self._ids = defaultdict(dict)

    def get(self, obj, table=None) -> int:
        if table is None:
            table = type(obj)
        if obj not in self._ids[table]:
            self._ids[table][obj] = max([-1, *self._ids[table].values()]) + 1
        return self._ids[table][obj]


class StateSequence:
    class StateVisitedException(Exception):
        pass

    def __init__(self, start, fluents, goal):
        self.states = [start]
        self.fluents = [fluents]
        self.actions = []
        self.goal = goal

    def extend(self, state, fluents, action) -> object:
        if state in self.states:
            raise StateSequence.StateVisitedException()
        successor = self._copy()
        successor.states.append(state)
        successor.fluents.append(fluents)
        successor.actions.append(action)
        return successor

    def _copy(self) -> object:
        successor = StateSequence(None, None, self._copy_symbol(self.goal))
        successor.states = [self._copy_symbol(s) for s in self.states]
        successor.fluents = [copy(fs) for fs in self.fluents]
        successor.actions = copy(self.actions)
        return successor

    def _copy_symbol(self, symbol) -> clingo.Symbol:
        if symbol.type == clingo.SymbolType.String:
            return clingo.String(symbol.string)
        elif symbol.type == clingo.SymbolType.Number:
            return clingo.Number(symbol.number)
        raise NotImplementedError(
            "_copy_symbol for symbol type {}".format(symbol.type)
        )

    def current(self) -> clingo.Symbol:
        return self.states[-1]

    def ended(self) -> bool:
        return self.current() == self.goal


def state_sequences(fluents, actions, start, goal) -> List[StateSequence]:
    def successor_states(state):
        for action in actions:
            for succ in action(state):
                yield (action, succ)

    # perform breadth first search for paths from start to goal
    sequences = []
    frontier = [StateSequence(start, [f for f in fluents if f(start)], goal)]
    while frontier != []:
        search_state = frontier.pop(0)
        for action, succ in successor_states(search_state.current()):
            try:
                succ_fluents = [f for f in fluents if f(succ)]
                search_succ = search_state.extend(succ, succ_fluents, action)

                # if the goal state has not been reached, look at successor
                # states by appending them to the frontier and continue
                if not search_succ.ended():
                    frontier.append(search_succ)
                    continue
                # else, yield the successor state as it has reached the goal
                sequences.append(search_succ)
            except StateSequence.StateVisitedException:
                # if the state has already been visited, do not look at it
                pass
    return sequences


def check_deduced(sequences, metarules, assigned_meta_symbols) -> bool:
    unary_bk, binary_bk = set(), set()
    for seq in sequences:
        for i in range(len(seq.states)):
            for f in seq.fluents[i]:
                unary_bk.add((clingo.Function(f.__name__), seq.states[i]))
            if i < len(seq.actions):
                action = seq.actions[i]
                [c1, c2] = seq.states[i : i + 2]
                binary_bk.add((clingo.Function(action.__name__), c1, c2))

    class FailNegContext:
        def unary(self):
            yield from unary_bk

        def binary(self):
            yield from binary_bk

        def meta(self):
            for meta in assigned_meta_symbols:
                yield tuple(meta.arguments)

    models = []
    ctl = clingo.Control()
    with pkg_resources.path(encodings, "check_deduced.lp") as path:
        ctl.load(str(path))
    ctl.ground([("base", [])], context=FailNegContext())
    with ctl.solve(yield_=True) as handle:
        for m in handle:
            models.append(m.symbols(shown=True))

    if len(models) != 1:
        raise RuntimeError(
            "the number of models found was not equal to one while checking "
            + "for failneg"
        )

    return models[0]


def _make_sa_context(self, ids) -> object:
    # create and return context object for grounding with mode ="sa"
    # maybe this should be public so it can be overwritten to provide bk in
    # certain order?
    pos_ex_seqs = {}
    for ex in self.examples:
        [start, goal] = tuple(ex.arguments[1:3])
        if ex.match("pos_ex", 3):
            pos_ex_seqs[ex] = state_sequences(
                self._unary_bk_functions(),
                self._binary_bk_functions(),
                start,
                goal,
            )

    class SAContext:
        def unary(inner_self):
            for pos_ex in pos_ex_seqs.keys():
                for seq in pos_ex_seqs[pos_ex]:
                    for i, fluents in enumerate(seq.fluents):
                        for fluent in fluents:
                            yield (
                                clingo.Function(fluent.__name__),
                                (ids.get(pos_ex), ids.get(seq), i + 1),
                            )

        def binary(inner_self):
            for pos_ex in pos_ex_seqs.keys():
                for seq in pos_ex_seqs[pos_ex]:
                    for i, f in enumerate(seq.actions):
                        yield (
                            clingo.Function(f.__name__),
                            (ids.get(pos_ex), ids.get(seq), i + 1),
                            (ids.get(pos_ex), ids.get(seq), i + 2),
                        )

        def checkpos(inner_self):
            for pos_ex in pos_ex_seqs.keys():
                for seq in pos_ex_seqs[pos_ex]:
                    yield (
                        ids.get(pos_ex),
                        clingo.Function(pos_ex.arguments[0].name),
                        (ids.get(pos_ex), ids.get(seq), 1),
                        (ids.get(pos_ex), ids.get(seq), len(seq.states)),
                    )

    return SAContext


def _make_sa_propagator(self, functional) -> object:
    # create and return propagator for solving with mode="sa"
    # functional means that only positive example are allowed to be derived

    # generating sequences for positive and negative examples
    sequences = {}
    for example in self.examples:
        [start, goal] = tuple(example.arguments[1:])
        if example.match("neg_ex" if not functional else "pos_ex", 3):
            sequences[example] = state_sequences(
                self._unary_bk_functions(),
                self._binary_bk_functions(),
                start,
                goal,
            )

    class SAPropagator:
        def __init__(inner_self):
            inner_self.meta_symbolic_atoms = {}
            inner_self.assigned_metas = []

        def init(inner_self, init):
            init.check_mode = clingo.PropagatorCheckMode.Total

            for a in init.symbolic_atoms:
                if a.symbol.match("meta", 4):
                    # a.literal is a program literal
                    solver_literal = init.solver_literal(a.literal)
                    inner_self.meta_symbolic_atoms[solver_literal] = a
                    # add_watch wants solver literal
                    init.add_watch(solver_literal)

        def propagate(inner_self, control, changes):
            # changes are solver literal
            inner_self.assigned_metas.extend(changes)

        def undo(inner_self, thread_id, assignment, changes):
            for meta in changes:
                inner_self.assigned_metas.remove(meta)

        def check(inner_self, control):
            # for every example we have to check if the hypothesis fails
            # either by deriving the example (non-functional, negative example)
            # or by deriving something other than the example (functional,
            # positive example)

            metas = []
            for c in inner_self.assigned_metas:
                symbolic_atom = inner_self.meta_symbolic_atoms[c]
                metas.append(symbolic_atom.symbol)

            for example in sequences.keys():
                deduced = check_deduced(
                    sequences[example], self.metarules, metas
                )

                ex_name = example.arguments[0]
                ex_args = example.arguments[1:]
                for symbol in deduced:
                    sym_name = symbol.arguments[0]
                    sym_args = symbol.arguments[1:]

                    if sym_name != ex_name:
                        continue

                    # if sym_args == ex_args:
                    #     print(sym_args)

                    if (ex_args == sym_args and not functional) or (
                        ex_args != sym_args and functional
                    ):
                        # as we return after adding the nogood, we dont have to
                        # check for its return value (on False we MUST return,
                        # but we do eitherway)
                        # print(inner_self.assigned_metas)
                        control.add_nogood(
                            inner_self.assigned_metas, lock=True
                        )
                        return

    return SAPropagator


def _ground_sa(self, functional) -> None:
    ids = IDMaker()
    propagator = self._make_sa_propagator(functional)
    self.control.register_propagator(propagator())

    id_examples = []
    for ex in self.examples:
        if ex.match("pos_ex", 3):
            s = clingo.Function(ex.name, [ids.get(ex), *ex.arguments])
            id_examples.append(s)

    example_strs = ["{}.".format(str(e)) for e in id_examples]
    self.control.add("examples", [], "".join(example_strs))
    for rule in self.metarules:
        with pkg_resources.path(metarules_resource, f"{rule}.lp") as path:
            self.control.load(str(path))

    with pkg_resources.path(encodings, "clingomil_sa.lp") as path:
        self.control.load(str(path))

    context = self._make_sa_context(ids)
    self.control.ground(
        [
            ("base", []),
            ("substitution", []),
            ("deduction", []),
            ("examples", []),
        ],
        context=context(),
    )

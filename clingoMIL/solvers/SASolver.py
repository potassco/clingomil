import clingo
from copy import copy
from typing import List
from collections import defaultdict
import importlib.resources as pkg_resources

from . import MILSolver
from .. import _encodings as encodings_resource


class IDMaker:
    def __init__(self):
        self._ids = defaultdict(dict)

    def get(self, obj, table=None) -> int:
        if table is None:
            table = type(obj)
        if obj not in self._ids[table]:
            self._ids[table][obj] = max([0, *self._ids[table].values()]) + 1
        return self._ids[table][obj]


class StateSequence:
    class StateVisitedException(Exception):
        pass

    def __init__(self, start, fluents, goal):
        self.states = [start]
        self.fluents = [fluents]
        self.actions = []
        self.goal = goal

    def extend(self, state, fluents, action):
        if state in self.states:
            raise StateSequence.StateVisitedException()
        successor = self._copy()
        successor.states.append(state)
        successor.fluents.append(fluents)
        successor.actions.append(action)
        return successor

    def _copy(self):
        successor = StateSequence(None, None, self._copy_symbol(self.goal))
        successor.states = [self._copy_symbol(s) for s in self.states]
        successor.fluents = [copy(fs) for fs in self.fluents]
        successor.actions = copy(self.actions)
        return successor

    def _copy_symbol(self, symbol):
        if symbol.type == clingo.SymbolType.String:
            return clingo.String(symbol.string)
        elif symbol.type == clingo.SymbolType.Number:
            return clingo.Number(symbol.number)
        raise NotImplementedError("_copy_symbol for symbol type {}".format(symbol.type))

    def current(self):
        return self.states[-1]

    def ended(self):
        return self.current() == self.goal


def state_sequences(fluents, actions, start, goal):
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


def _make_sa_context(ids, background, examples):
    # create and return context object for grounding with mode ="sa"
    # maybe this should be public so it can be overwritten to provide bk in
    # certain order?
    pos_ex_seqs = {}
    for ex in examples:
        [start, goal] = tuple(ex.arguments[1:3])
        if ex.match("pos_ex", 3):
            pos_ex_seqs[ex] = state_sequences(
                background.unary_functions, background.binary_functions, start, goal,
            )

    class SAContext:
        def unary(self):
            for pos_ex in pos_ex_seqs.keys():
                for seq in pos_ex_seqs[pos_ex]:
                    for i, fluents in enumerate(seq.fluents):
                        for fluent in fluents:
                            yield (
                                clingo.Function(fluent.__name__),
                                (ids.get(pos_ex), ids.get(seq), i + 1),
                            )

        def binary(self):
            for pos_ex in pos_ex_seqs.keys():
                for seq in pos_ex_seqs[pos_ex]:
                    for i, f in enumerate(seq.actions):
                        yield (
                            clingo.Function(f.__name__),
                            (ids.get(pos_ex), ids.get(seq), i + 1),
                            (ids.get(pos_ex), ids.get(seq), i + 2),
                        )

        def checkpos(self):
            for pos_ex in pos_ex_seqs.keys():
                for seq in pos_ex_seqs[pos_ex]:
                    yield (
                        ids.get(pos_ex),
                        clingo.Function(pos_ex.arguments[0].name),
                        (ids.get(pos_ex), ids.get(seq), 1),
                        (ids.get(pos_ex), ids.get(seq), len(seq.states)),
                    )

    return SAContext


def expand(meta_assignment_fs, function):
    # returns predicates that need to be true for rule body of rule with the
    # functions predicate as head to be satisfied

    def convert(sym):
        if sym.type == clingo.SymbolType.Number:
            return sym.number
        if sym.type == clingo.SymbolType.Function:
            return sym.name
        raise RuntimeError(
            f"predicate symbol was neither {clingo.SymbolType.Function} "
            + f"nor {clingo.SymbolType.Number}"
        )

    expansions = []

    for ass in meta_assignment_fs:
        args = [convert(sym) for sym in ass.arguments]
        if args[1] != function:
            continue
        if args[0] in ["precon", "postcon", "chain"]:
            expansions.append([args[2], args[3]])
        if args[0] in ["tailrec"]:
            expansions.append([args[2], args[1]])

    return expansions


def check_fail(example, meta_assignments, background, functional):
    # check if negative example is induced if not functional
    # check if something different than positive example is induced if
    # functional
    # seen is protection against infinite loops (e.g. switch in strings)
    queue = [([example.arguments[0].name], example.arguments[1])]
    seen = []

    # this function appends to the queue, while appending a copy to seen
    def append(x):
        if x in seen:
            return
        (functions, state) = x
        queue.append((functions, state))
        # here, we have to copy because functions are popped within queue
        seen.append((copy(functions), state))

    while len(queue) > 0:
        (functions, state) = queue.pop(0)
        if functions == []:
            if functional and state != example.arguments[2]:
                return True
            elif not functional and state == example.arguments[2]:
                return True
            else:
                continue

        skip_expansion = False
        function = functions.pop(0)

        # function is "n" because of n in tailrec (3rd predicate unused)
        if function == "n":
            append((functions, state))
            skip_expansion = True

        for unary_f in background.unary_functions:
            if unary_f.__name__ == function and unary_f(state):
                append((functions, state))
                skip_expansion = True

        for binary_f in background.binary_functions:
            if binary_f.__name__ == function:
                for successor in binary_f(state):
                    append((functions, successor))
                skip_expansion = True

        # expansion if the predicate (function) is untrue for the state by bk,
        # so it is checked which rules can make it true
        if not skip_expansion:
            for successors in expand(meta_assignments, function):
                append((successors + functions, state))

    return False


def _make_sa_propagator(background, examples, functional):
    # create and return propagator for solving with mode="sa"
    # functional means that only positive example are allowed to be derived

    class SAPropagator:
        def __init__(self):
            self.meta_symbolic_atoms = {}
            self.assigned_metas = []

        def init(self, init):
            init.check_mode = clingo.PropagatorCheckMode.Total

            for a in init.symbolic_atoms:
                if a.symbol.match("meta", 4):
                    # a.literal is a program literal
                    solver_literal = init.solver_literal(a.literal)
                    self.meta_symbolic_atoms[solver_literal] = a
                    # add_watch wants solver literal
                    init.add_watch(solver_literal)

        def propagate(self, control, changes):
            # changes are solver literal
            self.assigned_metas.extend(changes)

        def undo(self, thread_id, assignment, changes):
            for meta in changes:
                self.assigned_metas.remove(meta)

        def check(self, control):
            # for every example we have to check if the hypothesis fails
            # either by deriving the example (non-functional, negative example)
            # or by deriving something other than the example (functional,
            # positive example)

            metas = []
            for c in self.assigned_metas:
                symbolic_atom = self.meta_symbolic_atoms[c]
                metas.append(symbolic_atom.symbol)

            relevant_examples = (
                examples.positive() if functional else examples.negative()
            )

            # as we return after adding the nogood, we dont have to
            # check for its return value (on False we MUST return,
            # but we do eitherway)
            for example in relevant_examples:
                if check_fail(example, metas, background, functional):
                    control.add_nogood(self.assigned_metas, lock=True)
                    return

    return SAPropagator


class SASolver(MILSolver):
    def ground(self, background, examples, functional):
        ids = IDMaker()
        propagator = _make_sa_propagator(background, examples, functional)
        self.control.register_propagator(propagator())

        id_examples = []
        for ex in examples:
            if ex.match("pos_ex", 3):
                s = clingo.Function(ex.name, [ids.get(ex), *ex.arguments])
                id_examples.append(s)

        example_strs = ["{}.".format(str(e)) for e in id_examples]
        self.control.add("examples", [], "".join(example_strs))

        with pkg_resources.path(encodings_resource, "clingomil_sa.lp") as path:
            self.control.load(str(path))

        context = _make_sa_context(ids, background, examples)
        self.control.ground(
            [("base", []), ("examples", [])], context=context(),
        )

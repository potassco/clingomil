import clingo
from collections import defaultdict
from collections.abc import Iterable


def from_symbol(symbol):
    if symbol.type == clingo.SymbolType.Number:
        return symbol.number
    if symbol.type == clingo.SymbolType.String:
        return symbol.string
    raise ValueError(f"conversion of {clingo.Symbol} of {symbol.type} not supported")


def to_symbol(obj):
    if isinstance(obj, int):
        return clingo.Number(obj)
    if isinstance(obj, str):
        return clingo.String(obj)
    raise ValueError(f"conversion of {type(obj)} to {clingo.Symbol} not supported")


class Background:
    def __init__(self):
        self.unary_functions = []
        self.binary_functions = []

    def register(self, unary=[], binary=[]):
        # calls decorators manually
        if not isinstance(unary, Iterable):
            unary = [unary]
        if not isinstance(binary, Iterable):
            binary = [binary]

        for fun in unary:
            self.unary_bg(fun)

        for fun in binary:
            self.binary_bg(fun)

    def unary_bg(self, function):
        # The function which is to be used as background knowledge should take exactly one argument, which is X
        # Unary background functions should return a boolean
        def unary_wrapper(symbol):
            var = from_symbol(symbol)
            return function(var)

        self.unary_functions.append(unary_wrapper)
        return unary_wrapper

    def binary_bg(self, function):
        # binary background functions return lists of y for that p(x, y) holds. Is converted to clingo symbols
        def binary_wrapper(symbol):
            var = from_symbol(symbol)
            arguments = function(var)
            for argument in arguments:
                # Yes, I know the clingo does this conversion itself
                yield to_symbol(argument)

        self.binary_functions.append(binary_wrapper)
        return binary_wrapper

    def _extend_background(self, model):
        # create functions for unary background functions. They return a boolean signalling that p(x) is in the background
        unary_bg = defaultdict(list)
        for symbol in filter(lambda s: s.match("unary_bg", 2), model):
            unary_bg[symbol.arguments[0]].append(symbol.arguments[1])

        for predicate, arguments in unary_bg.items():

            def unary_bg_function(x):
                return x in arguments

            unary_bg_function.__name__ = predicate.name
            self.unary_functions.append(unary_bg_function)

        # create binary background functions. They yield all ys for that p(x, y) holds
        binary_bg = defaultdict(lambda: defaultdict(list))
        for symbol in filter(lambda s: s.match("binary_bg", 3), model):
            binary_bg[symbol.arguments[0]][symbol.arguments[1]].append(
                symbol.arguments[2]
            )

        for predicate, argument_dicts in binary_bg.items():

            def binary_bg_function(x):
                if x in argument_dicts.keys():
                    yield from argument_dicts[x]

            binary_bg_function.__name__ = predicate.name
            self.binary_functions.append(binary_bg_function)

    # TODO: this is essentially the same function as _add_load in the Examples class. Remove duplication
    def _add_load(self, add=None, load=None):
        # Examples are expected to be in the base subprogram
        if add is None and load is None:
            return

        control = clingo.Control()
        if add is not None:
            control.add("base", [], add)
        if load is not None:
            control.load(load)
        control.ground([("base", [])])

        model = []
        result = control.solve(on_model=lambda m: model.extend(m.symbols(shown=True)))

        if not result.satisfiable:
            raise RuntimeError("added or loaded background knowledge was unsatisfiable")

        self._extend_background(model)

    def load(self, filename):
        self._add_load(load=filename)
        return self

    def add(self, program):
        self._add_load(add=program)
        return self


# bk = Background()
# bk.add(
#     """
# unary_bg(test,1).
# unary_bg(test, X+1) :- unary_bg(test, X), X < 10.
# binary_bg(test, 3, "test").
# """
# )


# @bk.unary_bg
# def odd(x):
#     return x % 2 == 1


# print(bk.unary_functions[0](clingo.Number(10)))
# print(list(bk.binary_functions[0](clingo.Number(3))))
# print(bk.unary_functions[1](clingo.Number(2)), bk.unary_functions[1](clingo.Number(3)))

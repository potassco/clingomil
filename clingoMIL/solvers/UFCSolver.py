import clingo
from itertools import count
import importlib.resources as pkg_resources

from .MILSolver import MILSolver
from .. import _encodings as encodings_resource


def _make_fc_context(background):
    class FCContext:
        def unary(self, symbol):
            for f in background.unary_functions:
                if f(symbol):
                    yield clingo.Function(f.__name__)

        def binary(self, symbol):
            for f in background.binary_functions:
                for result in f(symbol):
                    yield (clingo.Function(f.__name__), result)

    return FCContext


class UFCSolver(MILSolver):
    def ground(self, background, examples, functional):
        example_strs = [f"{e}." for e in examples]
        self.control.add("examples", [], "".join(example_strs))

        with pkg_resources.path(encodings_resource, "clingomil_ufc.lp") as path:
            self.control.load(str(path))

        context = _make_fc_context(background)
        self.control.ground(
            [("base", []), ("examples", [])], context=context(),
        )

        self.control.assign_external(clingo.Function("functional"), functional)

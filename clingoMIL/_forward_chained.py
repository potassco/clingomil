import clingo
import importlib.resources as pkg_resources

from . import encodings
from . import metarules as metarules_resource


def _make_fc_context(self) -> object:
    # create and return context object for grounding with mode="fc"
    class FCContext:
        def unary(inner_self, symbol):
            # return all unary bk functions that evaluate to true with
            # given symbol
            for f in self._unary_bk_functions():
                if f(symbol):
                    yield clingo.Function(f.__name__)

        def binary(inner_self, symbol):
            for f in self._binary_bk_functions():
                for result in f(symbol):
                    yield (clingo.Function(f.__name__), result)

    return FCContext


def _ground_fc(self, functional) -> None:
    example_strs = ["{}.".format(str(e)) for e in self.examples]
    self.control.add("examples", [], "".join(example_strs))

    with pkg_resources.path(encodings, "clingomil_fc.lp") as path:
        self.control.load(str(path))

    for rule in self.metarules:
        with pkg_resources.path(metarules_resource, f"{rule}.lp") as path:
            self.control.load(str(path))

    context = self._make_fc_context()
    self.control.ground(
        [
            ("base", []),
            ("substitution", []),
            ("deduction", []),
            ("examples", []),
        ],
        context=context(),
    )

    self.control.assign_external("functional", functional)

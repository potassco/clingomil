import clingo
from itertools import count
import importlib.resources as pkg_resources

from . import SolverAbstract
from .FCSolver import _make_fc_context
from .. import _encodings as encodings_resource


class UFCSolver(SolverAbstract):
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

import clingo
from itertools import count
import importlib.resources as pkg_resources

from . import SolverAbstract
from .FCSolver import _make_fc_context
from .SASolver import _make_sa_propagator
from .. import _encodings as encodings_resource


class PFCSolver(SolverAbstract):
    def ground(self, background, examples, functional):
        propagator = _make_sa_propagator(background, examples, functional)
        self.control.register_propagator(propagator())

        example_strs = [f"{e}." for e in examples]
        self.control.add("examples", [], "".join(example_strs))

        with pkg_resources.path(encodings_resource, "clingomil_pfc.lp") as path:
            self.control.load(str(path))

        context = _make_fc_context(background)
        self.control.ground(
            [("base", []), ("examples", [])], context=context(),
        )

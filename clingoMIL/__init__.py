import clingo
import importlib.resources as pkg_resources

from . import metarules as metarules_resource
from ._functions import induced_program, solve_incrementally


class clingoMIL:

    from ._forward_chained import _make_fc_context, _ground_fc
    from ._state_abstraction import (
        _make_sa_context,
        _make_sa_propagator,
        _ground_sa,
    )
    from ._background import (
        unary_bk,
        binary_bk,
        _unary_bk_functions,
        _binary_bk_functions,
    )

    def __init__(self, *args, **kwargs):
        # initialize examples and metarules
        self.examples = []
        self.use_metarules(metarules=None)

        # create clingo control object
        self.control = None
        self.reset_control(0, 0, *args, **kwargs)

    def reset_control(self, size, skolems, *args, **kwargs) -> None:
        # resets the control, but with size and skolems added to arguments in
        # any case
        del self.control
        if "arguments" not in kwargs:
            kwargs["arguments"] = []
        kwargs["arguments"].extend(
            ["-c size={}".format(size), "-c skolems={}".format(skolems)]
        )
        self.control = clingo.Control(*args, **kwargs)
        self.solve = self.control.solve

    def use_metarules(self, metarules=None) -> None:
        # load (and verify?) metarules used during grounding
        # if metarules is None, all provided are used
        provided = []
        for file in pkg_resources.contents(metarules_resource):
            if (
                not pkg_resources.is_resource(metarules_resource, file)
                or file == "__init__.py"
            ):
                continue
            provided.append(file[:-3])

        if metarules is None:
            self.metarules = provided
            return

        for rule in metarules:
            if rule not in provided:
                raise ValueError(f"metarule {rule} does not exist")
        self.metarules = metarules

    def load_examples(self, file) -> None:
        # load examples from file, convert into internal representation
        # they must be in the "base" subprogram
        ctl = clingo.Control(arguments=["--warn=none"])
        ctl.load(file)
        ctl.add("base", [], "#show pos_ex/3. #show neg_ex/3.")
        ctl.ground([("base", [])])
        ctl.solve(
            on_model=lambda m: self.examples.extend(m.symbols(shown=True))
        )

    def ground(self, mode="fc", functional=False) -> None:
        if mode not in ["fc", "sa"]:
            raise ValueError("illegal mode, must be either 'fc' or 'sa'")
        elif mode == "fc":
            self._ground_fc(functional)
        elif mode == "sa":
            self._ground_sa(functional)

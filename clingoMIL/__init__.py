import clingo as _clingo

from ._functions import (
    induced_program,
    solve_incrementally,
    from_symbol,
    to_symbol,
)


__all__ = [
    "clingoMIL",
    "induced_program",
    "solve_incrementally",
    "from_symbol",
    "to_symbol",
]


class clingoMIL:

    from ._forward_chained import (
        _make_fc_context,
        _ground_fc,
        _ground_pfc,
        _ground_ufc,
    )
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
        # initialize examples
        self.examples = []

        # create clingo control object
        self.control = None
        self.reset_control(0, 0, *args, **kwargs)

    def reset_control(self, size, skolems, *args, **kwargs) -> None:
        # resets the control, but with size and skolems added to arguments in
        # any case
        del self.control
        if "arguments" not in kwargs.keys():
            kwargs["arguments"] = []
        kwargs["arguments"].extend(
            ["-c size={}".format(size), "-c skolems={}".format(skolems)]
        )
        self.control = _clingo.Control(*args, **kwargs)
        self.solve = self.control.solve

    def load_examples(self, file) -> None:
        # load examples from file, convert into internal representation
        # they must be in the "base" subprogram
        ctl = _clingo.Control(arguments=["--warn=none"])
        ctl.load(file)
        ctl.add("base", [], "#show pos_ex/3. #show neg_ex/3.")
        ctl.ground([("base", [])])
        ctl.solve(
            on_model=lambda m: self.examples.extend(m.symbols(shown=True))
        )

    def ground(self, mode="fc", functional=False) -> None:
        grounders = {
            "fc": self._ground_fc,
            "pfc": self._ground_pfc,
            "ufc": self._ground_ufc,
            "sa": self._ground_sa,
        }
        if mode not in grounders.keys():
            raise ValueError(
                f"illegal mode, must be in {list(grounders.keys())}"
            )
        grounders[mode](functional)

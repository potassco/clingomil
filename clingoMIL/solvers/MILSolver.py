import clingo
from itertools import count

# TODO: rename everything that has to do with MILSolver!!


class MILSolver:
    def __init__(self):
        if type(self) == MILSolver:
            raise RuntimeError(f"please only instantiate subclasses of {MILSolver}")

        self.reset_control(0, 0)

    def ground(self, background, examples, functional):
        raise NotImplementedError(
            f"subclasses of {MILSolver} must override {MILSolver.ground}"
        )

    # TODO: make args and kwargs optional arguments instead of consuming all arguments
    def solve(self, background, examples, functional, *args, **kwargs):
        for size in count(1):
            for skolems in range(0, size):
                self.reset_control(size, skolems)
                self.ground(background, examples, functional, *args, **kwargs)
                model = []
                res = self.control.solve(
                    on_model=lambda m: model.extend(m.symbols(shown=True))
                )
                if res.satisfiable:
                    return res, model

    def reset_control(self, size, skolems, *args, **kwargs) -> None:
        # resets the control, but with size and skolems added to arguments in any case
        if hasattr(self, "control"):
            del self.control
        if "arguments" not in kwargs.keys():
            kwargs["arguments"] = []
        kwargs["arguments"].extend(
            ["-c size={}".format(size), "-c skolems={}".format(skolems)]
        )
        self.control = clingo.Control(*args, **kwargs)

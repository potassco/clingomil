import clingo
from itertools import count


class SolverAbstract:
    def __init__(self):
        if type(self) == SolverAbstract:
            raise RuntimeError(
                f"please only instantiate subclasses of {SolverAbstract}"
            )

        self.reset_control(0, 0)

    def ground(self, background, examples, functional):
        raise NotImplementedError(
            f"subclasses of {SolverAbstract} must override {SolverAbstract.ground}"
        )

    def solve(self, background, examples, functional):
        for size in count(1):
            for skolems in range(0, size):
                self.reset_control(size, skolems)
                self.ground(background, examples, functional)
                model = []
                res = self.control.solve(
                    on_model=lambda m: model.extend(m.symbols(shown=True))
                )
                if res.satisfiable:
                    return res, model

    def reset_control(self, size, skolems):
        # resets the control, but with size and skolems added to arguments in any case
        if hasattr(self, "control"):
            del self.control
        self.control = clingo.Control(
            arguments=["-c size={}".format(size), "-c skolems={}".format(skolems)]
        )

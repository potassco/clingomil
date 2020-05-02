import clingo
import inspect


class LookupExt(object):
    def __init__(self, ctl):
        ctl = ctl
        functions = inspect.getmembers(self.__class__, inspect.isfunction)
        super_functions = inspect.getmembers(LookupExt, inspect.isfunction)
        implemented = set(obj for name, obj in functions) - set(
            obj for name, obj in super_functions
        )

        class Propagator(object):
            def init(init):
                externals = [a for a in init.symbolic_atoms if a.is_external]
                for ext in externals:
                    for f in implemented:
                        ctl.assign_external(
                            clingo.Function(f.__name__, ext.symbol.arguments),
                            f(self, ext.symbol.arguments),
                        )

        self.Propagator = Propagator

    def __setattr__(self, name, value):
        if not self.__class__ != LookupExt and name == "Propagator":
            raise ValueError("Propagator attribute must not be overridden")

        super.__setattr__(self, name, value)

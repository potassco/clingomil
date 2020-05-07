import clingo
from typing import NewType, List, Callable, Iterable

UnaryBKFunction = NewType(
    "UnaryBKFunction", Callable[[object, clingo.Symbol], bool]
)
BinaryBKFunction = NewType(
    "BinaryBKFunction",
    Callable[[object, clingo.Symbol], Iterable[clingo.Symbol]],
)


def _unary_bk_functions(self) -> List[UnaryBKFunction]:
    # load binary bk functions
    ubkfs = []
    for fname in dir(self):
        f = getattr(self, fname)
        if hasattr(f, "_is_unary_bk"):
            ubkfs.append(f)
    return ubkfs


def unary_bk(f) -> UnaryBKFunction:
    if not callable(f):
        raise RuntimeError("{} is not callable".format(f))

    def unary_bk_function_wrapper(*args, **kwargs):
        b = f(*args, **kwargs)
        if not isinstance(b, bool):
            raise RuntimeError(
                "unary bk function {} did not ".format(f)
                + "return a boolean value"
            )
        return b

    unary_bk_function_wrapper.__name__ = f.__name__
    unary_bk_function_wrapper._is_unary_bk = True
    return unary_bk_function_wrapper


def _binary_bk_functions(self) -> List[BinaryBKFunction]:
    # load binary bk functions
    bbkfs = []
    for fname in dir(self):
        f = getattr(self, fname)
        if hasattr(f, "_is_binary_bk"):
            bbkfs.append(f)
    return bbkfs


def binary_bk(f) -> BinaryBKFunction:
    if not callable(f):
        raise RuntimeError("{} is not callable".format(f))

    def binary_bk_function_wrapper(*args, **kwargs):
        for s in f(*args, **kwargs):
            if not isinstance(s, clingo.Symbol):
                raise RuntimeError(
                    "binary bk function {} returned an object ".format(f)
                    + "that was not of type {}".format(clingo.Symbol)
                )
            yield s

    binary_bk_function_wrapper.__name__ = f.__name__
    binary_bk_function_wrapper._is_binary_bk = True
    return binary_bk_function_wrapper

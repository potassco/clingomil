import clingo
from itertools import count
import importlib.resources as pkg_resources

from . import _metarules as metarules_resource


def induced_program(symbols):
    metas = []
    for sym in symbols:
        if sym.match("meta", 4):
            metas.append(sym)

    string_substitutions = []
    for file in pkg_resources.contents(metarules_resource):
        if (
            not pkg_resources.is_resource(metarules_resource, file)
            or file == "__init__.py"
        ):
            continue

        ctl = clingo.Control()
        with pkg_resources.path(metarules_resource, file) as path:
            ctl.load(str(path))
        ctl.ground([("string_substitution", [])])
        ctl.solve(
            on_model=lambda m: string_substitutions.extend(
                m.symbols(shown=True)
            )
        )

    def predicate_formats():
        for i in count(1):
            yield "P{}".format(i)

    program = []
    for meta in metas:
        for subst in string_substitutions:
            [meta_name, format_string] = subst.arguments
            if meta_name == meta.arguments[0]:
                predicates = []
                for pred in meta.arguments[1:]:
                    if pred.type == clingo.SymbolType.Number:
                        predicates.append("invented{}".format(pred.number))
                    elif pred.type == clingo.SymbolType.Function:
                        predicates.append(pred.name)
                    else:
                        raise RuntimeError(
                            "could not convert symbol {} to string".format(
                                pred
                            )
                        )

                ps = dict(zip(predicate_formats(), predicates))
                program.append(format_string.string.format_map(ps))

    return program


def solve_incrementally(mil, *args, **kwargs):
    for size in count(1):
        for skolems in range(0, size):
            mil.reset_control(size, skolems)
            mil.ground(*args, **kwargs)
            model = []
            res = mil.solve(
                on_model=lambda m: model.extend(m.symbols(shown=True))
            )
            if res.satisfiable:
                return res, model


def from_symbol(symbol):
    if symbol.type == clingo.SymbolType.Number:
        return symbol.number
    if symbol.type == clingo.SymbolType.String:
        return symbol.string
    if symbol.type == clingo.SymbolType.Function:
        return symbol.name
    raise ValueError(f"could not convert {symbol}")


def to_symbol(obj):
    if isinstance(obj, int):
        return clingo.Number(obj)
    if isinstance(obj, str):
        return clingo.String(obj)
        return clingo.Number(obj)
    if isinstance(obj, str):
        return clingo.String(obj)
    raise NotImplementedError(f"conversion of {type(obj)} to {clingo.Symbol}")

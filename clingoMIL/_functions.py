import clingo
from itertools import count


def induced_program(symbols):
    def predicate_formats():
        for i in count(1):
            yield "P{}".format(i)

    string_substitutions = {
        "chain": "{P1}(X,Y) :- {P2}(X,Z), {P3}(Z,Y).",
        "postcon": "{P1}(X,Y) :- {P2}(X,Y), {P3}(Y).",
        "precon": "{P1}(X,Y) :- {P2}(X), {P3}(X,Y).",
        "tailrec": "{P1}(X,Y) :- {P2}(X,Z), {P1}(Z,Y).",
    }

    metas = []
    for sym in symbols:
        if sym.match("meta", 4):
            metas.append(sym)

    program = []
    for meta in metas:
        for meta_name, format_string in string_substitutions.items():
            if meta_name == meta.arguments[0].name:
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
                program.append(format_string.format_map(ps))

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

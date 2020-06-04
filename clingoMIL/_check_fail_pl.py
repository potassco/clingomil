import sys
from typing import Union

from . import _functions
from ._pyswip.prolog import PrologError
from ._pyswip import (
    Prolog,
    PrologMT,
    registerForeign,
    Atom,
    Variable,
)


# Creating Prolog instance. Should probably be changed to be lazy
try:
    prolog = PrologMT()
except PrologError as e:
    print(
        f"Warning: {str(e)}. "
        + "Using standard Prolog instance (no multithreading support)",
        file=sys.stderr,
    )
    prolog = Prolog()


# The following two functions are used in the foreign functions helpers.
# They yield from_symbol of their generator, which is set to the unary/binary
# function of the forward chained context of the given mil problem (within
# the check_fail_pl function)
def unary_bg(symbol):
    for y in unary_bg.generator(symbol):
        yield _functions.from_symbol(y)


def binary_bg(symbol):
    for p, y in binary_bg.generator(symbol):
        yield _functions.from_symbol(p), _functions.from_symbol(y)


# These are helper functions for the foreign functions.
# Depending on p and y being variables or atoms, one of these is called
def unary_prove(p: str, x: str) -> bool:
    for proved_p in unary_bg(_functions.to_symbol(x)):
        if proved_p == p:
            return True
    return False


def unary_unify_ps(ps: Variable, x: str) -> bool:
    proved_ps = list(unary_bg(_functions.to_symbol(x)))
    if proved_ps is not []:
        ps.unify(proved_ps)
        return True
    return False


def binary_prove(p: str, x: str, y: str) -> bool:
    for proved_p, proved_y in binary_bg(_functions.to_symbol(x)):
        if proved_p == p and proved_y == y:
            return True
    return False


def binary_unify_ys(p: str, x: str, ys: Variable) -> bool:
    bg = binary_bg(_functions.to_symbol(x))
    proved_ys = [y for p_, y in bg if p_ == p]
    if len(proved_ys) > 0:
        ys.unify(proved_ys)
        return True
    return False


def binary_unify_pys(ps: Variable, x: str, ys: Variable) -> bool:
    proved_pys = list(binary_bg(_functions.to_symbol(x)))
    if len(proved_pys) > 0:
        ps.unify([py[0] for py in proved_pys])
        ys.unify([py[1] for py in proved_pys])
        return True
    return False


# Foreign functions used by pyswip
# They check for type of p and y and call helper accordingly
def import_unary(ps: Union[Atom, Variable], x: Atom) -> bool:
    if isinstance(ps, Atom):
        return unary_prove(ps.value, x.value)
    elif isinstance(ps, Variable):
        return unary_unify_ps(ps, x.value)
    return False


def import_binary(
    ps: Union[Atom, Variable], x: Atom, ys: Union[Atom, Variable]
) -> bool:
    if isinstance(ps, Atom) and isinstance(ys, Atom):
        return binary_prove(ps.value, x.value, ys.value)
    elif isinstance(ps, Atom) and isinstance(ys, Variable):
        return binary_unify_ys(ps.value, x.value, ys)
    elif isinstance(ps, Variable) and isinstance(ys, Variable):
        return binary_unify_pys(ps, x.value, ys)
    return False


# Loading logic program and registering foreign functions
prolog.consult("clingoMIL/_encodings/check_fail_pl.pl")
registerForeign(import_unary, arity=2)
registerForeign(import_binary, arity=3)


# Actual fail check.
# Asserts examples and meta assignments, queries fail, reverts assertions
def check_fail_pl(self, examples, meta_assignments, functional):
    global unary_bg, binary_bg

    context = self._make_fc_context()
    unary_bg.generator = lambda sym: context.unary(self, sym)
    binary_bg.generator = lambda sym: context.binary(self, sym)

    for example in examples:
        # Prolog has single quotes for strings
        prolog.assertz(str(example).replace('"', "'"))
    for meta in meta_assignments:
        # meta assignments should only contain functions, not strings
        prolog.assertz(str(meta))

    result = prolog.query("fail_functional" if functional else "fail_neg")
    fail = len(list(result)) > 0

    prolog.retractall("pos_ex(_,_,_)")
    prolog.retractall("neg_ex(_,_,_)")
    prolog.retractall("meta(_,_,_,_)")

    return fail

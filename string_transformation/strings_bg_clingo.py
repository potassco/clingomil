import clingo
from clingoMIL import Background

strings_bg = Background()


@strings_bg.unary_bg
def isA(string):
    return string[1] == "a"


@strings_bg.unary_bg
def isB(string):
    return string[1] == "b"


@strings_bg.unary_bg
def isC(string):
    return string[1] == "c"


@strings_bg.binary_bg
def remove(string):
    cs = [c for c in string if c not in "[,]"]
    if len(cs) > 0:
        yield f"[{','.join(cs[1:])}]"


@strings_bg.binary_bg
def switch(string):
    cs = [c for c in string if c not in "[,]"]
    if len(cs) >= 2:
        yield f"[{','.join([cs[1], cs[0]] + cs[2:])}]"

import clingo
from clingoMIL import clingoMIL


class StringsMIL(clingoMIL):
    @clingoMIL.unary_bk
    def isA(self, string):
        return string.string[1] == "a"

    @clingoMIL.unary_bk
    def isB(self, string):
        return string.string[1] == "b"

    @clingoMIL.unary_bk
    def isC(self, string):
        return string.string[1] == "c"

    @clingoMIL.binary_bk
    def remove(self, string):
        cs = [c for c in string.string if c not in "[,]"]
        if len(cs) > 0:
            yield clingo.String(f"[{','.join(cs[1:])}]")

    @clingoMIL.binary_bk
    def switch(self, string):
        cs = [c for c in string.string if c not in "[,]"]
        if len(cs) >= 2:
            yield clingo.String(f"[{','.join([cs[1], cs[0]] + cs[2:])}]")

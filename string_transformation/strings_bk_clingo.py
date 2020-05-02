from lib import LookupExt


class StringsLookupExt(LookupExt):
    def isA(self, string):
        return string[0].string[1] == "a"

    def isB(self, string):
        return string[0].string[1] == "b"

    def isC(self, string):
        return string[0].string[1] == "c"


class StringsContext(object):
    def remove(self, string):
        cs = [c for c in string.string if c not in "[,]"]
        if len(cs) == 0:
            return []

        # print(f'{string.string} remove {"[" + ",".join(cs[1:]) + "]"}')
        return "[" + ",".join(cs[1:]) + "]"

    def switch(self, string):
        cs = [c for c in string.string if c not in "[,]"]
        if len(cs) < 2:
            return []
        # print(f'{string.string} switch {"[" + ",".join([cs[1], cs[0]] + cs[2:]) + "]"}')
        return "[" + ",".join([cs[1], cs[0]] + cs[2:]) + "]"

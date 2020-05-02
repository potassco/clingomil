import re
from lib import LookupExt


class TrainsLookupExt(LookupExt):
    def contains(self, clw):
        car_list, word = clw
        return bool(re.search(word.string, car_list.string))


class TrainsContext(object):
    def getFirst(self, car_list):
        if car_list.string != "[]":
            first = re.search("c\((.+?)\)(]|,c)", car_list.string).group(1)
            return f"[c({first})]"
        return []

    def removeFirst(self, car_list):
        if re.search("c\(.+?\)(]|,c)(.*)]", car_list.string):
            rest = re.search("c\(.+?\)(]|,c)(.*)]", car_list.string).group(2)
            return f"[c({rest})]"
        elif car_list.string != "[]":
            return "[]"
        return []

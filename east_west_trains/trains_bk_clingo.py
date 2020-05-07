import re
import clingo
from clingoMIL import clingoMIL

can_be_containted = [
    ",rectangle",
    ",u_shaped",
    ",ellipse",
    ",hexagon",
    ",bucket",
    "short",
    "long",
    "double",
    "not_double",
    "none",
    "flat",
    "jagged",
    "peaked",
    "arc",
    "flat",
    "jagged",
    "peaked",
    "arc",
    "l.circle",
    "l.diamond",
    "l.hexagon",
    "l.rectangle",
    "l.triangle",
    "l.utriangle",
    "circle,0",
    "diamond,0",
    "hexagon,0",
    "rectangle,0",
    "triangle,0",
    "utriangle,0",
    "circle,1",
    "diamond,1",
    "hexagon,1",
    "rectangle,1",
    "triangle,1",
    "utriangle,1",
    "circle,2",
    "diamond,2",
    "hexagon,2",
    "rectangle,2",
    "triangle,2",
    "utriangle,2",
    "circle,3",
    "diamond,3",
    "hexagon,3",
    "rectangle,3",
    "triangle,3",
    "utriangle,3",
    ",2,",
    ",3,",
]


class TrainsMIL(clingoMIL):
    # @clingoMIL.binary_bk
    # def getFirst(self, car_list):
    #     if car_list.string != "[]":
    #         first = re.search("c\((.+?)\)(]|,c)", car_list.string).group(1)
    #         yield clingo.String(f"[c({first})]")

    @clingoMIL.binary_bk
    def removeFirst(self, car_list):
        result = re.search("c\(.+?\)(]|,c)(.*)]", car_list.string)
        if result:
            rest = result.group(2)
            yield clingo.String(f"[c({rest}]")
        elif car_list.string != "[]":
            yield clingo.String("[]")

    def make_contains(self, thing):
        @clingoMIL.unary_bk
        def contains_thing(car_list):
            return bool(re.search(thing, car_list.string))

        fname = f"contains_{thing.replace(',', '_').replace('.','_')}"
        contains_thing.__name__ = fname
        return contains_thing

    def __init__(self):
        super().__init__()

        for thing in can_be_containted:
            contains_thing = self.make_contains(thing)
            self.__setattr__(contains_thing.__name__, contains_thing)

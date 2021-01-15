import re
import clingo

from clingoMIL import Background


trains_bg = Background()


@trains_bg.binary_bg
def removeFirst(car_list):
    result = re.search(r"c\(.+?\)(]|,c)(.*)]", car_list)
    if result:
        rest = result.group(2)
        yield f"[c({rest}]"
    elif car_list != "[]":
        yield "[]"


# fmt: off
can_be_containted = [",rectangle", ",u_shaped", ",ellipse", ",hexagon", ",bucket", "short", "long", "double", "not_double", "none", "flat", "jagged", "peaked", "arc", "flat", "jagged", "peaked", "arc", "l.circle", "l.diamond", "l.hexagon", "l.rectangle", "l.triangle", "l.utriangle", "circle,0", "diamond,0", "hexagon,0", "rectangle,0", "triangle,0", "utriangle,0", "circle,1", "diamond,1", "hexagon,1", "rectangle,1", "triangle,1", "utriangle,1", "circle,2", "diamond,2", "hexagon,2", "rectangle,2", "triangle,2", "utriangle,2", "circle,3", "diamond,3", "hexagon,3", "rectangle,3", "triangle,3", "utriangle,3", ",2,", ",3,"]
# fmt : on

def make_contains_thing(thing):
    def contains_thing(car_list):
        return bool(re.search(thing, car_list))

    fname = f"contains_{thing.replace(',', '_').replace('.','_')}"
    contains_thing.__name__ = fname
    return contains_thing


for thing in can_be_containted:
    contains_thing = make_contains_thing(thing)
    trains_bg.register(unary=contains_thing)

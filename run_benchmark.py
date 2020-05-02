import re
import os
import json
import clingo
from itertools import count
from robot_strategies.robot_bk_clingo import RobotLookupExt, RobotContext
from east_west_trains.trains_bk_clingo import TrainsLookupExt, TrainsContext
from string_transformation.strings_bk_clingo import (
    StringsLookupExt,
    StringsContext,
)


benchmarks = {
    "robot": {
        "folder": "robot_strategies",
        "clingo": "robot_clingo.lp",
        "lookup": RobotLookupExt,
        "context": RobotContext,
    },
    "trains": {
        "folder": "east_west_trains",
        "clingo": "trains_clingo.lp",
        "lookup": TrainsLookupExt,
        "context": TrainsContext,
    },
    "strings": {
        "folder": "string_transformation",
        "clingo": "strings_clingo.lp",
        "lookup": StringsLookupExt,
        "context": StringsContext,
    },
}


times = {k: {} for k in benchmarks.keys()}


def make_control(file, examples, args, lookupClass, contextClass):
    ctl = clingo.Control(arguments=args)
    lookup = lookupClass(ctl)
    # ctl.configuration.solve.models = 0
    ctl.configuration.solve.parallel_mode = "4,split"
    ctl.register_propagator(lookup.Propagator)

    ctl.load(file)
    ctl.add("examples", [], examples)
    ctl.add("examples", [], "#show. #show meta/4.")

    ctl.ground(
        [("base", []), ("examples", [])], context=contextClass(),
    )

    return ctl


# I've tried multishot solving, but ran into problems:
# The skolem atoms rely on the size of the hypothesis, the correct grounding of
# the order relies on the skolem atoms, and the order is needed to do meta-
# substitutions. So multi-shot solving is not really viable in a way that
# incrementally grounds the size/skolems. On the other hand, making each skolem
# atom up to some maximum value external would still require grounding as if
# all the skolems were facts, so this is not viable either. I might come back
# to that in the future.


def run_instance(benchmark, name, timeout):
    fname = os.path.join(benchmark["folder"], "instances", name)
    with open(fname) as lp:
        examples = "\n".join([(e) for e in lp.readlines()])

    time_remaining = timeout
    for step in count(0):
        for skolems in range(step):
            print(
                f"\r{'GROUNDING':11s} {name}: size {step}, skolems {skolems}",
                end="",
            )
            ctl = make_control(
                os.path.join(benchmark["folder"], benchmark["clingo"]),
                examples,
                [f"-c size={step}", f"-c skolems={skolems}"],
                benchmark["lookup"],
                benchmark["context"],
            )

            print(
                f"\r{'SOLVING':11s} {name}: size {step}, skolems {skolems}",
                end="",
            )

            models = []
            with ctl.solve(
                async_=True,
                on_model=lambda m: models.append(m.symbols(atoms=True)),
            ) as handle:
                finished = handle.wait(time_remaining)
                if not finished:
                    handle.cancel()
                result = handle.get()

                time_remaining -= ctl.statistics["summary"]["times"]["total"]
                if result.satisfiable or result.interrupted:
                    sat = "SATISFIABLE" if result.satisfiable else "TIMEOUT"
                    print(
                        f"\r{sat:11s} {name}: size {step}, skolems {skolems}"
                        + f", {timeout - time_remaining:.1f} seconds total"
                    )
                    return result, models, timeout - time_remaining


benchmark = "trains"
assert benchmark in benchmarks.keys()

for instance in sorted(
    os.listdir(f"{benchmarks[benchmark]['folder']}/instances")
):
    match = re.fullmatch(r"instance(\d+?)-(\d+?).lp", instance)
    size, num = match.group(1), match.group(2)

    result, models, time = run_instance(benchmarks[benchmark], instance, 600)

    if size not in times[benchmark].keys():
        times[benchmark][size] = {}
    times[benchmark][size][num] = time

    with open("times.json", "w") as f:
        json.dump(times, f, indent=4, sort_keys=True)

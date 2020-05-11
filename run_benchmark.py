#!/usr/bin/env python3

import os
import re
import json
from itertools import count
from collections import defaultdict
from time import time as current_time
from robot_strategies.robot_bk_clingo import RobotMIL
from east_west_trains.trains_bk_clingo import TrainsMIL
from string_transformation.strings_bk_clingo import StringsMIL


benchmarks = [
    ("robot", RobotMIL, "robot_strategies/instances"),
    ("trains", TrainsMIL, "east_west_trains/instances"),
    ("strings", StringsMIL, "string_transformation/instances"),
]
times = {
    "fc": {b[0]: defaultdict(dict) for b in benchmarks},
    "sa": {b[0]: defaultdict(dict) for b in benchmarks},
}


def run_instance(milclass, mode, functional, instance, timeout):
    name = milclass.__name__
    mil = milclass()
    mil.load_examples(instance)

    start = current_time()
    for size in count(1):
        for skolems in range(0, size):
            mil.reset_control(size, skolems)
            print(
                f"\r{'GROUNDING':11s} {name} with {mode} on {instance}: size "
                + f"{size}, skolems {skolems}",
                end="",
            )
            mil.ground(mode=mode, functional=functional)

            print(
                f"\r{'SOLVING':11s} {name} with {mode} on {instance}: size "
                + f"{size}, skolems {skolems}",
                end="",
            )
            model = []
            with mil.solve(
                async_=True,
                on_model=lambda m: model.extend(m.symbols(shown=True)),
            ) as handle:
                terminated = False
                while not terminated and current_time() - start < timeout:
                    terminated = handle.wait(5)
                if not terminated:
                    handle.cancel()
                result = handle.get()
                time = current_time() - start

                if result.satisfiable or result.interrupted:
                    sat = "SATISFIABLE" if result.satisfiable else "TIMEOUT"
                    print(
                        f"\r{sat:11s} {name} with {mode} on {instance}: "
                        + f"size {size}, skolems {skolems} {time:.1f} seconds"
                    )
                    return result, model, time


def main():
    for mode in ["fc", "sa"]:
        for name, milclass, instances in benchmarks:
            is_robot = issubclass(milclass, RobotMIL)
            for examples in sorted(os.listdir(instances))[:5]:
                if mode == "fc" and is_robot:
                    continue

                match = re.fullmatch(r"instance(\d+?)-(\d+?).lp", examples)
                size, num = match.group(1), match.group(2)

                result, model, time = run_instance(
                    milclass,
                    mode,
                    is_robot,
                    os.path.join(instances, examples),
                    60,
                )

                times[mode][name][size][num] = time
                with open("times.json", "w") as f:
                    json.dump(times, f, indent=2, sort_keys=True)


if __name__ == "__main__":
    main()

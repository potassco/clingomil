import os
import re
import pandas as pd
from itertools import count
from collections import defaultdict
from time import time as current_time

from robot_strategies.robot_bg_clingo import robot_bg
from east_west_trains.trains_bg_clingo import trains_bg
from string_transformation.strings_bg_clingo import strings_bg

from clingoMIL import Examples, FCSolver, UFCSolver, SASolver, PFCSolver


benchmarks = [
    ("trains", trains_bg, "east_west_trains/instances"),
    ("strings", strings_bg, "string_transformation/instances"),
    ("robot", robot_bg, "robot_strategies/instances"),
]
solvers = {
    "fc": FCSolver,
    "ufc": UFCSolver,
    "sa": SASolver,
    "pfc": PFCSolver,
}


def benchmark_solver(solver_class, solver_name, problem, instance, timeout):
    class BenchmarkSolver(solver_class):
        def solve(self, background, examples, functional):
            start = current_time()
            for size in count(1):
                for skolems in range(0, size):
                    self.reset_control(size, skolems)
                    print(
                        f"\r{'GROUNDING':11s} {problem}"
                        f" with {solver_name:3s}"
                        f" on {instance}:"
                        f" size {size}, skolems {skolems}",
                        end="",
                    )
                    self.ground(background, examples, functional)

                    print(
                        f"\r{'SOLVING':11s} {problem}"
                        f" with {solver_name:3s}"
                        f" on {instance}:"
                        f" size {size}, skolems {skolems}",
                        end="",
                    )
                    model = []
                    with self.control.solve(
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
                                f"\r{sat:11s} {problem}"
                                f" with {solver_name:3s}"
                                f" on {instance}:"
                                f" size {size}, skolems {skolems} {time:.1f} seconds"
                            )
                            return result, model, time

    return BenchmarkSolver


def main():
    data = []
    for problem, background, instances in benchmarks:
        functional = problem == "robot"

        for instance in sorted(os.listdir(instances))[:5]:
            examples = Examples().load(os.path.join(instances, instance))

            for solver_name, solver_class in solvers.items():
                if solver_name in ["fc", "ufc"] and functional:
                    continue

                match = re.fullmatch(r"instance(\d+?)-(\d+?).lp", instance)
                size, num = match.group(1), match.group(2)

                solver = benchmark_solver(
                    solver_class, solver_name, problem, instance, 60
                )
                result, _, time = solver().solve(background, examples, functional)

                data.append(
                    {
                        "solver": solver_name,
                        "problem": problem,
                        "size": int(size),
                        "num": int(num),
                        "time": time,
                        "result": str(result),
                    }
                )
                pd.DataFrame(data).to_csv("times.csv")


if __name__ == "__main__":
    main()

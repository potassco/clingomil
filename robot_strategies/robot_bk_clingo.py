import re
import clingo
from clingoMIL import clingoMIL


class RobotMIL(clingoMIL):
    @clingoMIL.unary_bk
    def wants_tea(self, state):
        cur_pos = re.search(r"robot_pos\((\d+)\)", state.string).group(1)
        end_pos = re.search(r"end_pos\((\d+)\)", state.string).group(1)

        if int(cur_pos) < int(end_pos):
            wants = re.search(
                f"place\({cur_pos},(\w+),cup", state.string
            ).group(1)
            if wants == "tea":
                return True
        return False

    @clingoMIL.unary_bk
    def wants_coffee(self, state):
        cur_pos = re.search("robot_pos\((\d+)\)", state.string).group(1)
        end_pos = re.search("end_pos\((\d+)\)", state.string).group(1)

        if int(cur_pos) < int(end_pos):
            wants = re.search(
                f"place\({cur_pos},(\w+),cup", state.string
            ).group(1)
            if wants == "coffee":
                return True
        return False

    @clingoMIL.unary_bk
    def at_end(self, state):
        # print(f"{state}, {type(state)}")
        cur_pos = re.search("robot_pos\((\d+)\)", state.string).group(1)
        end_pos = re.search("end_pos\((\d+)\)", state.string).group(1)
        return int(cur_pos) == int(end_pos)

    @clingoMIL.binary_bk
    def pour_tea(self, state):
        cur_pos = re.search("robot_pos\((\d+)\)", state.string).group(1)
        end_pos = re.search("end_pos\((\d+)\)", state.string).group(1)
        if int(cur_pos) < int(end_pos):
            cup_state = re.search(
                f"place\({cur_pos},\w+,cup\((.+?)\)", state.string
            ).group(1)
            wants = re.search(
                f"place\({cur_pos},(\w+),cup", state.string
            ).group(1)

            if cup_state == "up,empty":
                return [
                    clingo.String(
                        re.sub(
                            f"place\({cur_pos},\w+,cup\((.+?)\)",
                            f"place({cur_pos},{wants},cup(up,tea)",
                            state.string,
                        )
                    )
                ]
        return []

    @clingoMIL.binary_bk
    def pour_coffee(self, state):
        cur_pos = re.search("robot_pos\((\d+)\)", state.string).group(1)
        end_pos = re.search("end_pos\((\d+)\)", state.string).group(1)
        if int(cur_pos) < int(end_pos):
            cup_state = re.search(
                f"place\({cur_pos},\w+,cup\((.+?)\)", state.string
            ).group(1)
            wants = re.search(
                f"place\({cur_pos},(\w+),cup", state.string
            ).group(1)

            if cup_state == "up,empty":
                return [
                    clingo.String(
                        re.sub(
                            f"place\({cur_pos},\w+,cup\((.+?)\)",
                            f"place({cur_pos},{wants},cup(up,coffee)",
                            state.string,
                        )
                    )
                ]
        return []

    @clingoMIL.binary_bk
    def turn_cup_over(self, state):
        cur_pos = re.search("robot_pos\((\d+)\)", state.string).group(1)
        end_pos = re.search("end_pos\((\d+)\)", state.string).group(1)
        if int(cur_pos) < int(end_pos):
            cup_state = re.search(
                f"place\({cur_pos},\w+,cup\((.+?),", state.string
            ).group(1)
            wants = re.search(
                f"place\({cur_pos},(\w+),cup", state.string
            ).group(1)

            if cup_state == "down":
                return [
                    clingo.String(
                        re.sub(
                            f"place\({cur_pos},\w+,cup\((.+?),",
                            f"place({cur_pos},{wants},cup(up,",
                            state.string,
                        )
                    )
                ]
        return []

    @clingoMIL.binary_bk
    def move_right(self, state):
        # print(type(state))
        cur_pos = re.search("robot_pos\((\d+)\)", state.string).group(1)
        end_pos = re.search("end_pos\((\d+)\)", state.string).group(1)

        if int(cur_pos) < int(end_pos):
            return [
                clingo.String(
                    re.sub(
                        "robot_pos\((\d+)\)",
                        f"robot_pos({int(cur_pos)+1})",
                        state.string,
                    )
                )
            ]
        return []

import re
from lib import LookupExt


class RobotLookupExt(LookupExt):
    def wants_tea(self, state):
        state = state[0]
        cur_pos = re.search("robot_pos\((\d+)\)", state.string).group(1)
        end_pos = re.search("end_pos\((\d+)\)", state.string).group(1)

        if int(cur_pos) < int(end_pos):
            wants = re.search(
                f"place\({cur_pos},(\w+),cup", state.string
            ).group(1)
            if wants == "tea":
                return True
        return False

    def wants_coffee(self, state):
        state = state[0]
        cur_pos = re.search("robot_pos\((\d+)\)", state.string).group(1)
        end_pos = re.search("end_pos\((\d+)\)", state.string).group(1)

        if int(cur_pos) < int(end_pos):
            wants = re.search(
                f"place\({cur_pos},(\w+),cup", state.string
            ).group(1)
            if wants == "coffee":
                return True
        return False

    def at_end(self, state):
        state = state[0]
        cur_pos = re.search("robot_pos\((\d+)\)", state.string).group(1)
        end_pos = re.search("end_pos\((\d+)\)", state.string).group(1)
        return int(cur_pos) == int(end_pos)


class RobotContext(object):
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
                return re.sub(
                    f"place\({cur_pos},\w+,cup\((.+?)\)",
                    f"place({cur_pos},{wants},cup(up,tea)",
                    state.string,
                )
        return []

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
                return re.sub(
                    f"place\({cur_pos},\w+,cup\((.+?)\)",
                    f"place({cur_pos},{wants},cup(up,coffee)",
                    state.string,
                )
        return []

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
                return re.sub(
                    f"place\({cur_pos},\w+,cup\((.+?),",
                    f"place({cur_pos},{wants},cup(up,",
                    state.string,
                )
        return []

    def move_right(self, state):
        cur_pos = re.search("robot_pos\((\d+)\)", state.string).group(1)
        end_pos = re.search("end_pos\((\d+)\)", state.string).group(1)

        if int(cur_pos) < int(end_pos):
            return re.sub(
                "robot_pos\((\d+)\)",
                f"robot_pos({int(cur_pos)+1})",
                state.string,
            )
        return []

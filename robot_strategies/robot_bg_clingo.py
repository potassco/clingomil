import re
import clingo
from clingoMIL import Background

robot_bg = Background()


@robot_bg.unary_bg
def wants_tea(state):
    cur_pos = re.search(r"robot_pos\((\d+)\)", state).group(1)
    end_pos = re.search(r"end_pos\((\d+)\)", state).group(1)

    if int(cur_pos) < int(end_pos):
        wants = re.search(f"place\\({cur_pos},(\\w+),cup", state).group(1)
        if wants == "tea":
            return True
    return False


@robot_bg.unary_bg
def wants_coffee(state):
    cur_pos = re.search(r"robot_pos\((\d+)\)", state).group(1)
    end_pos = re.search(r"end_pos\((\d+)\)", state).group(1)

    if int(cur_pos) < int(end_pos):
        wants = re.search(f"place\\({cur_pos},(\\w+),cup", state).group(1)
        if wants == "coffee":
            return True
    return False


@robot_bg.unary_bg
def at_end(state):
    # print(f"{state}, {type(state)}")
    cur_pos = re.search(r"robot_pos\((\d+)\)", state).group(1)
    end_pos = re.search(r"end_pos\((\d+)\)", state).group(1)
    return int(cur_pos) == int(end_pos)


@robot_bg.binary_bg
def pour_tea(state):
    cur_pos = re.search(r"robot_pos\((\d+)\)", state).group(1)
    end_pos = re.search(r"end_pos\((\d+)\)", state).group(1)
    if int(cur_pos) < int(end_pos):
        cup_state = re.search(f"place\\({cur_pos},\\w+,cup\\((.+?)\\)", state).group(1)
        wants = re.search(f"place\\({cur_pos},(\\w+),cup", state).group(1)

        if cup_state == "up,empty":
            return [
                re.sub(
                    f"place\\({cur_pos},\\w+,cup\\((.+?)\\)",
                    f"place({cur_pos},{wants},cup(up,tea)",
                    state,
                )
            ]
    return []


@robot_bg.binary_bg
def pour_coffee(state):
    cur_pos = re.search(r"robot_pos\((\d+)\)", state).group(1)
    end_pos = re.search(r"end_pos\((\d+)\)", state).group(1)
    if int(cur_pos) < int(end_pos):
        cup_state = re.search(f"place\\({cur_pos},\\w+,cup\\((.+?)\\)", state).group(1)
        wants = re.search(f"place\\({cur_pos},(\\w+),cup", state).group(1)

        if cup_state == "up,empty":
            return [
                re.sub(
                    f"place\\({cur_pos},\\w+,cup\\((.+?)\\)",
                    f"place({cur_pos},{wants},cup(up,coffee)",
                    state,
                )
            ]
    return []


@robot_bg.binary_bg
def turn_cup_over(state):
    cur_pos = re.search(r"robot_pos\((\d+)\)", state).group(1)
    end_pos = re.search(r"end_pos\((\d+)\)", state).group(1)
    if int(cur_pos) < int(end_pos):
        cup_state = re.search(f"place\\({cur_pos},\\w+,cup\\((.+?),", state).group(1)
        wants = re.search(f"place\\({cur_pos},(\\w+),cup", state).group(1)

        if cup_state == "down":
            return [
                re.sub(
                    f"place\\({cur_pos},\\w+,cup\\((.+?),",
                    f"place({cur_pos},{wants},cup(up,",
                    state,
                )
            ]
    return []


@robot_bg.binary_bg
def move_right(state):
    # print(type(state))
    cur_pos = re.search(r"robot_pos\((\d+)\)", state).group(1)
    end_pos = re.search(r"end_pos\((\d+)\)", state).group(1)

    if int(cur_pos) < int(end_pos):
        return [re.sub(r"robot_pos\((\d+)\)", f"robot_pos({int(cur_pos)+1})", state,)]
    return []

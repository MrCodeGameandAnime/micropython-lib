from enum_mini import Enum


class Color(Enum):
    RED = 1
    GREEN = 2


print(Color.RED.name, Color.RED.value)
print(Color(2).name)
print(len(Color))

State = Enum("State", {"OFF": 0, "ON": 1})
print(State.ON.name, State.ON.value)

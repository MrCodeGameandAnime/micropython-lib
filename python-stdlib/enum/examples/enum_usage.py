from enum import Enum, IntEnum, StrEnum


class Color(Enum):
    RED = 1
    GREEN = 2


print(Color.RED.name, Color.RED.value)
print(Color(2).name)
print(Color()["RED"].name)
print(len(Color()))


class Priority(IntEnum):
    LOW = 1
    HIGH = 2


print(Priority.HIGH.value + 1)


class Status(StrEnum):
    PENDING = "pending"
    DONE = "done"


print(Status.PENDING.name, Status.PENDING.value)
print(isinstance(Status.PENDING, Status))

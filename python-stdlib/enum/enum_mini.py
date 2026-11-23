# enum_mini.py
# Minimalist Enum implementation without metaclasses


def _n(n):
    # str.capitalize()
    return n[0].upper() + n[1:]


def _c(cls, name, value):
    # prevent modification of enum item attributes
    def readonly(self, key, value):
        raise AttributeError("readonly")

    enum_name = cls.__name__

    # create readonly subclass inheriting the value'self type (int, str, float etc.)
    return type(
        f"{enum_name}.{name}",
        (type(value), cls),
        {
            "name": name,
            "value": value,
            "__str__": lambda self: f"{enum_name}.{name}",
            "__repr__": lambda self: f"<{enum_name}.{name}: {value!r}>",
            "__call__": lambda self: value,
            "__setattr__": readonly,
        },
    )(value)


class Enum:
    def __new__(cls, value=None, names=None):
        # Functional API: Enum('Name', {'KEY': 'val'})
        if value is not None and names is not None:
            if not isinstance(names, dict):
                raise TypeError("must be dict")

            # build and return a new Enum subclass
            names["__name__"] = value
            c = type(str(value), (cls,), names)
            c._i()
            return c()

        # lookup by value or name: Color(1) / Color("RED")
        if value is not None and cls is not Enum:
            return cls.__call__(value)

        return super().__new__(cls)

    @classmethod
    def __contains__(cls, v):
        # lookup by value or name
        return any(i.value == v or i.name == v for i in cls._i())

    @classmethod
    def __call__(cls, v=None):
        if v is None:
            return cls()

        # lookup by value or name
        for i in cls._i():
            if i.value == v or i.name == v:
                return i
        raise ValueError(f"invalid: {v!r}")

    # True if both classes are Enums and the member dicts match
    __eq__ = classmethod(lambda cls, o: getattr(o, "_i", False) and cls._i() == o._i())
    __iter__ = classmethod(lambda cls: iter(cls._i()))
    __len__ = classmethod(lambda cls: len(cls._i()))

    @classmethod
    def __setattr__(cls, k, v):
        raise AttributeError("readonly")

    @classmethod
    def __delattr__(cls, k):
        raise AttributeError("readonly")

    @classmethod
    def _i(cls):
        # build and return the dict that maps member instances to their values
        if "__members__" not in cls.__dict__:
            for b in cls.__bases__:
                if issubclass(b, Enum) and b is not Enum:  # and b._i():
                    raise TypeError(f"can't extend {b.__name__}")

            # convert raw class attributes into typed enum instances
            cls.__members__ = {}
            for k, v in list(cls.__dict__.items()):
                if not k.startswith("_") and not callable(v):
                    if v in cls.__members__:
                        raise ValueError(f"duplicate value {v!r} in {cls.__name__}")
                    e = _c(cls, k, v)
                    setattr(cls, k, e)
                    cls.__members__[e] = v
        return cls.__members__


# install class-builder hook
import builtins

_orig = builtins.__build_class__


def _bc(f, n, *b, **kw):
    # when a base is an Enum instance (returned by cls()), extract its class
    b = tuple(type(e) if isinstance(e, Enum) else e for e in b)
    cls = _orig(f, n, *b, **kw)
    if issubclass(cls, Enum):
        cls._i()
        return cls()
    return cls


builtins.__build_class__ = _bc


import inspect

class InheritDocstrings(type):
    def __init__(cls, name, bases, dct):
        def is_public_member(key):
            return (
                (key.startswith('__') and key.endswith('__')
                 and len(key) > 4) or
                not key.startswith('_'))

        for key, val in dct.items():
            if ((inspect.isfunction(val) or isinstance(val, property)) and
                is_public_member(key) and
                val.__doc__ is None):
                for base in cls.__mro__[1:]:
                    super_method = getattr(base, key, None)
                    if super_method is not None:
                        val.__doc__ = super_method.__doc__
                        break

        super().__init__(name, bases, dct)

class A:
    @classmethod
    def wiggle(cls):
        "Wiggle classmethod"
        pass

    @staticmethod
    def waggle():
        "Waggle staticmethod"
        pass

class B(A, metaclass=InheritDocstrings):
    @classmethod
    def wiggle(cls):
        pass

    @staticmethod
    def waggle():
        pass

print(f"B.wiggle.__doc__: {B.wiggle.__doc__}")
print(f"B.waggle.__doc__: {B.waggle.__doc__}")

if B.wiggle.__doc__ == A.wiggle.__doc__:
    print("SUCCESS: classmethod docstring inherited")
else:
    print("FAILURE: classmethod docstring NOT inherited")

if B.waggle.__doc__ == A.waggle.__doc__:
    print("SUCCESS: staticmethod docstring inherited")
else:
    print("FAILURE: staticmethod docstring NOT inherited")

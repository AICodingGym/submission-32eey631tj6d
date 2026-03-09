
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

class A(metaclass=InheritDocstrings):
    @property
    def wiggle(self):
        "Wiggle A"
        return 1

class B(A, metaclass=InheritDocstrings):
    @property
    def wiggle(self):
        # No docstring here, should inherit from A
        return 2

class C(B, metaclass=InheritDocstrings):
    @property
    def wiggle(self):
        # No docstring here, should inherit from A (via B)
        return 3

print(f"A.wiggle.__doc__: {A.wiggle.__doc__}")
print(f"B.wiggle.__doc__: {B.wiggle.__doc__}")
print(f"C.wiggle.__doc__: {C.wiggle.__doc__}")

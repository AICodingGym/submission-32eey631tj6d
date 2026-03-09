
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
    @property
    def wiggle(self):
        "Wiggle the thingamajig"
        return True

class B(A, metaclass=InheritDocstrings):
    @property
    def wiggle(self):
        return False

print(f"A.wiggle.__doc__: {A.wiggle.__doc__}")
print(f"B.wiggle.__doc__: {B.wiggle.__doc__}")

if B.wiggle.__doc__ == A.wiggle.__doc__:
    print("SUCCESS: Docstring inherited")
else:
    print("FAILURE: Docstring NOT inherited")

class C:
    def wiggle(self):
        "Wiggle the thingamajig method"
        pass

class D(C, metaclass=InheritDocstrings):
    def wiggle(self):
        pass

print(f"C.wiggle.__doc__: {C.wiggle.__doc__}")
print(f"D.wiggle.__doc__: {D.wiggle.__doc__}")

if D.wiggle.__doc__ == C.wiggle.__doc__:
    print("SUCCESS: Method docstring inherited")
else:
    print("FAILURE: Method docstring NOT inherited")


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
                        try:
                            val.__doc__ = super_method.__doc__
                        except AttributeError:
                            # properties might not have writable __doc__ in some cases?
                            # but in Python 3 they should if they are the property object itself.
                            pass
                        break

        super().__init__(name, bases, dct)

class A(metaclass=InheritDocstrings):
    @property
    def wiggle(self):
        "Wiggle the thingamajig"
        return True

class B(A):
    @property
    def wiggle(self):
        return False

print(f"A.wiggle.__doc__: {A.wiggle.__doc__}")
print(f"B.wiggle.__doc__: {B.wiggle.__doc__}")

if B.wiggle.__doc__ == A.wiggle.__doc__:
    print("SUCCESS: Docstring inherited")
else:
    print("FAILURE: Docstring NOT inherited")

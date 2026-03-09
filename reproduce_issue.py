
import inspect
from astropy.utils.misc import InheritDocstrings

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

class C(metaclass=InheritDocstrings):
    def wiggle(self):
        "Wiggle the thingamajig method"
        pass

class D(C):
    def wiggle(self):
        pass

print(f"C.wiggle.__doc__: {C.wiggle.__doc__}")
print(f"D.wiggle.__doc__: {D.wiggle.__doc__}")

if D.wiggle.__doc__ == C.wiggle.__doc__:
    print("SUCCESS: Method docstring inherited")
else:
    print("FAILURE: Method docstring NOT inherited")

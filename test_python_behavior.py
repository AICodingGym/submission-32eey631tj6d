
class A:
    @property
    def wiggle(self):
        "Wiggle A"
        return 1

class B(A):
    @property
    def wiggle(self):
        return 2

print(f"A.wiggle.__doc__: {A.wiggle.__doc__}")
print(f"B.wiggle.__doc__: {B.wiggle.__doc__}")

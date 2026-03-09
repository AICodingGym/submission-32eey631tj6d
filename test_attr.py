
class A:
    @property
    def wiggle(self):
        "Wiggle doc"
        return 1

print(f"A.wiggle: {A.wiggle}")
print(f"type(A.wiggle): {type(A.wiggle)}")
print(f"A.wiggle.__doc__: {A.wiggle.__doc__}")

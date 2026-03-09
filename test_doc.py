
class A:
    @property
    def wiggle(self):
        "Getter doc"
        return True

class B:
    @property
    def wiggle(self):
        return False

print(f"B.wiggle.__doc__: {B.wiggle.__doc__}")

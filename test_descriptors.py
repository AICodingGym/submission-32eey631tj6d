
import inspect

def my_func(cls):
    pass

cm = classmethod(my_func)
sm = staticmethod(my_func)

print(f"inspect.isfunction(cm): {inspect.isfunction(cm)}")
print(f"inspect.isfunction(sm): {inspect.isfunction(sm)}")

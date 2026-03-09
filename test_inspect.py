
import inspect

def my_func(self):
    return 1

p = property(my_func)
print(f"inspect.isfunction(my_func): {inspect.isfunction(my_func)}")
print(f"inspect.isfunction(p): {inspect.isfunction(p)}")
print(f"isinstance(p, property): {isinstance(p, property)}")

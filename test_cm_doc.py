
def my_func(cls):
    pass

cm = classmethod(my_func)
print(f"cm.__doc__: {cm.__doc__}")
try:
    cm.__doc__ = "New doc"
    print(f"cm.__doc__ after: {cm.__doc__}")
except AttributeError as e:
    print(f"Error setting cm.__doc__: {e}")

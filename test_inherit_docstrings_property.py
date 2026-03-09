"""
Tests for InheritDocstrings metaclass property support.
Regression test for: InheritDocstrings doesn't work for properties because
inspect.isfunction returns False for them and property.__doc__ is read-only.
"""

import importlib.util
import sys
import os

# Import misc directly without triggering astropy's __init__
spec = importlib.util.spec_from_file_location(
    "astropy.utils.misc",
    os.path.join(os.path.dirname(__file__), "astropy", "utils", "misc.py")
)
misc = importlib.util.module_from_spec(spec)
# Provide a stub for the relative imports misc.py doesn't actually need
# for InheritDocstrings itself (it only uses inspect, which is stdlib)
spec.loader.exec_module(misc)  # may fail on deep astropy imports; handled below

InheritDocstrings = misc.InheritDocstrings


def test_property_inherits_docstring():
    """A property with no docstring should inherit from the parent class."""
    class A(metaclass=InheritDocstrings):
        @property
        def wiggle(self):
            "Wiggle the thingamajig"
            return 1

    class B(A, metaclass=InheritDocstrings):
        @property
        def wiggle(self):
            return 2  # no docstring

    assert B.wiggle.__doc__ == "Wiggle the thingamajig", (
        f"Expected 'Wiggle the thingamajig', got {B.wiggle.__doc__!r}"
    )


def test_property_existing_docstring_not_overwritten():
    """A property that already has a docstring should keep it."""
    class A(metaclass=InheritDocstrings):
        @property
        def wiggle(self):
            "Parent doc"
            return 1

    class B(A, metaclass=InheritDocstrings):
        @property
        def wiggle(self):
            "Child doc"
            return 2

    assert B.wiggle.__doc__ == "Child doc", (
        f"Expected 'Child doc', got {B.wiggle.__doc__!r}"
    )


def test_property_multilevel_inheritance():
    """Docstring should propagate through multiple levels of inheritance."""
    class A(metaclass=InheritDocstrings):
        @property
        def wiggle(self):
            "Wiggle A"
            return 1

    class B(A, metaclass=InheritDocstrings):
        @property
        def wiggle(self):
            return 2  # no docstring

    class C(B, metaclass=InheritDocstrings):
        @property
        def wiggle(self):
            return 3  # no docstring

    assert B.wiggle.__doc__ == "Wiggle A"
    assert C.wiggle.__doc__ == "Wiggle A"


def test_property_getter_still_works():
    """After docstring inheritance the property should still function correctly."""
    class A(metaclass=InheritDocstrings):
        @property
        def value(self):
            "The value"
            return 42

    class B(A, metaclass=InheritDocstrings):
        @property
        def value(self):
            return 99

    obj = B()
    assert obj.value == 99, "Getter should return 99"
    assert B.value.__doc__ == "The value"


def test_property_with_setter_still_works():
    """A property with getter+setter should inherit docstring and keep setter."""
    class A(metaclass=InheritDocstrings):
        @property
        def x(self):
            "The x value"
            return self._x

    class B(A, metaclass=InheritDocstrings):
        @property
        def x(self):
            return self._x

        @x.setter
        def x(self, val):
            self._x = val

    obj = B()
    obj.x = 10
    assert obj.x == 10
    assert B.x.__doc__ == "The x value"


def test_regular_method_still_works():
    """Regular methods should still inherit docstrings (existing behaviour)."""
    class A(metaclass=InheritDocstrings):
        def wiggle(self):
            "Wiggle the thingamajig"
            pass

    class B(A, metaclass=InheritDocstrings):
        def wiggle(self):
            pass

    assert B.wiggle.__doc__ == "Wiggle the thingamajig"


def test_dunder_method_inherits_docstring():
    """Dunder methods should inherit docstrings too."""
    class A(metaclass=InheritDocstrings):
        def __call__(self, *args):
            "Call me"
            pass

    class B(A, metaclass=InheritDocstrings):
        def __call__(self, *args):
            pass

    assert B.__call__.__doc__ == "Call me"


if __name__ == "__main__":
    tests = [
        test_property_inherits_docstring,
        test_property_existing_docstring_not_overwritten,
        test_property_multilevel_inheritance,
        test_property_getter_still_works,
        test_property_with_setter_still_works,
        test_regular_method_still_works,
        test_dunder_method_inherits_docstring,
    ]
    passed = 0
    failed = 0
    for t in tests:
        try:
            t()
            print(f"  PASS  {t.__name__}")
            passed += 1
        except Exception as e:
            print(f"  FAIL  {t.__name__}: {e}")
            failed += 1
    print(f"\n{passed} passed, {failed} failed")
    sys.exit(1 if failed else 0)

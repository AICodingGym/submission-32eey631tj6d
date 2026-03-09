"""
Standalone tests for Paginator.__iter__.

Runs directly with `uv run python test_paginator_iter.py` without requiring
the full Django test infrastructure (which is broken on Python 3.14 due to
the removal of the `cgi` module).
"""
import os
import sys
import types
import unittest

# Make the local django package importable
sys.path.insert(0, os.path.dirname(__file__))

# Minimal Django settings required to import django.core.paginator
from django.conf import settings
if not settings.configured:
    settings.configure(USE_I18N=False)

from django.core.paginator import Paginator, Page


class TestPaginatorIter(unittest.TestCase):

    def test_iter_yields_page_objects(self):
        """__iter__ should yield Page instances for each page."""
        paginator = Paginator([1, 2, 3, 4, 5], 2)
        pages = list(paginator)
        self.assertEqual(len(pages), 3)
        for page in pages:
            self.assertIsInstance(page, Page)

    def test_iter_correct_page_contents(self):
        """Each yielded page should contain the right slice of objects."""
        paginator = Paginator([1, 2, 3, 4, 5], 2)
        pages = list(paginator)
        self.assertEqual(list(pages[0]), [1, 2])
        self.assertEqual(list(pages[1]), [3, 4])
        self.assertEqual(list(pages[2]), [5])

    def test_iter_page_numbers(self):
        """Page numbers yielded by __iter__ must be 1-based and sequential."""
        paginator = Paginator([1, 2, 3, 4, 5], 2)
        numbers = [p.number for p in paginator]
        self.assertEqual(numbers, [1, 2, 3])

    def test_iter_matches_page_range(self):
        """Iterating via __iter__ should yield the same pages as using page_range."""
        data = list(range(1, 12))
        paginator = Paginator(data, 3)
        via_iter = list(paginator)
        via_page_range = [paginator.page(n) for n in paginator.page_range]
        self.assertEqual(len(via_iter), len(via_page_range))
        for a, b in zip(via_iter, via_page_range):
            self.assertEqual(list(a), list(b))
            self.assertEqual(a.number, b.number)

    def test_iter_single_page(self):
        """When all items fit on one page, __iter__ yields exactly that page."""
        paginator = Paginator([1, 2, 3], 10)
        pages = list(paginator)
        self.assertEqual(len(pages), 1)
        self.assertEqual(list(pages[0]), [1, 2, 3])

    def test_iter_empty_list_allow_empty(self):
        """Empty object_list with allow_empty_first_page=True yields one empty page."""
        paginator = Paginator([], 2)
        pages = list(paginator)
        self.assertEqual(len(pages), 1)
        self.assertEqual(list(pages[0]), [])

    def test_iter_empty_list_no_empty_first_page(self):
        """Empty object_list with allow_empty_first_page=False yields no pages."""
        paginator = Paginator([], 2, allow_empty_first_page=False)
        pages = list(paginator)
        self.assertEqual(len(pages), 0)

    def test_iter_is_generator(self):
        """Paginator.__iter__ should return an iterator (not e.g. a list)."""
        paginator = Paginator([1, 2, 3], 2)
        self.assertIsInstance(iter(paginator), types.GeneratorType)


if __name__ == '__main__':
    unittest.main(verbosity=2)

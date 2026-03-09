import sys
import importlib.util

spec = importlib.util.spec_from_file_location("introspection", "astropy/utils/introspection.py")
introspection = importlib.util.module_from_spec(spec)
sys.modules["astropy.utils.introspection"] = introspection
spec.loader.exec_module(introspection)

minversion = introspection.minversion

import math

def test():
    math.__version__ = '1.14.3'
    try:
        print("1.14.3 >= 1.14dev ?", minversion(math, '1.14dev'))
    except Exception as e:
        print("TypeError 1.14.3 vs 1.14dev:", e)

    math.__version__ = '1.14'
    try:
        print("1.14 >= 1.14dev ?", minversion(math, '1.14dev'))
    except Exception as e:
        print("TypeError 1.14 vs 1.14dev:", e)
        
    math.__version__ = '1.14dev'
    try:
        print("1.14dev >= 1.14.3 ?", minversion(math, '1.14.3'))
    except Exception as e:
        print("TypeError 1.14dev vs 1.14.3:", e)

test()

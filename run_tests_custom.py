import sys, types
sys.modules['cgi'] = types.ModuleType('cgi')
sys.modules['cgi'].parse_header = lambda x: (x, {})

sys.path.insert(0, './tests')
from runtests import django_tests
django_tests(-1, False, False, (), [], ['queries'], False, 1)

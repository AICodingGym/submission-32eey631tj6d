import sys, types
sys.modules['cgi'] = types.ModuleType('cgi')
sys.modules['cgi'].parse_header = lambda x: (x, {})
import django
from django.conf import settings
from django.db import models

settings.configure(
    DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': ':memory:'}},
    INSTALLED_APPS=['__main__'],
)
django.setup()

class Dimension(models.Model):
    f1 = models.IntegerField()
    class Meta: app_label = '__main__'

qs = Dimension.objects.filter(pk=10)
qs_other = Dimension.objects.filter(pk=16)

# Before union eval
import copy
state_before = vars(qs.query).copy()

union_qs = qs.union(qs_other)
list(union_qs)

# After union eval
state_after = vars(qs.query).copy()

for k in state_before:
    if state_before[k] != state_after[k]:
        print(f"MUTATED: {k}")
        print(f"  before: {state_before[k]}")
        print(f"  after:  {state_after[k]}")


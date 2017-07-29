from django.test import TestCase

# Create your tests here.
from .models import StockWatch as ss
def filteronmany():
    conditions = dict(income__gross_profit__lte=5000)
    conditions.update(balancesheet__capital__lte=5000000)
    r =ss.objects.filter(**conditions)
    return r
    # TODO create dic for filter and implament on this fuction
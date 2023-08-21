from django.test import TestCase
from orders.models import Order, Table, OrderItem

class TestModels(TestCase):
    def setUp(self): 
        self.table1 = Table.objects.create(
            name='table 1',
            is_reserved=False,
        )
        
    def test_table_str(self):
        self.assertEquals(str(self.table1), f"{self.table1}")
        
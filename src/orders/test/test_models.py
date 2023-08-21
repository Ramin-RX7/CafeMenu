from django.test import TestCase
from orders.models import Order, Table, OrderItem

class TestModels(TestCase):
    def setUp(self): 
        self.table1 = Table.objects.create(
            name='table 1',
            is_reserved=False,
        )
        
        self.table2 = Table.objects.create(
            name='table 2',
            is_reserved=True,
        )
        
        
    def test_table_str(self):
        self.assertEquals(str(self.table1), f"{self.table1}")
        
    def test_get_available_table(self):
        available_table = Table.get_available_table()
        self.assertEqual(available_table, self.table1)
        
    def test_save_table(self):
        self.assertEqual(Table.objects.count(), 2)
        
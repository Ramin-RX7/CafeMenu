from django.test import TestCase
from orders.models import Order, Table, OrderItem
from foods.models import Food, Category

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
        
        self.category1 = Category.objects.create(
            title='Iranian Foods'
        )
        
        self.food1 = Food.objects.create(
            title='Kabab',
            price=22,
            category=self.category1
        )
        self.food2 = Food.objects.create(
            title='Ghormeh Sabzi',
            price=20,
            category=self.category1
        )
        
        
    def test_table_str(self):
        self.assertEquals(str(self.table1), f"{self.table1}")
        
    def test_get_available_table(self):
        available_table = Table.get_available_table()
        self.assertEqual(available_table, self.table1)
        
    def test_save_table(self):
        self.assertEqual(Table.objects.count(), 2)
        
from django.test import TestCase
from orders.models import Order, Table, OrderItem
from foods.models import Food, Category
from users.models import User

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
        
        self.user1 = User.objects.create(
            phone="9176877108",
            first_name = 'Ali',
            last_name= 'Afzal',
            is_active=True,
            is_staff=False,
        )
        
        self.order1 = Order(
            customer='9176877108',
            table=self.table1,
            discount=2,
            responsible_staff=self.user1,
        )
        self.order1.save(check_items=False)
        
        
        self.order_item1 = OrderItem.objects.create(order=self.order1,
                                                    food=self.food1,
                                                    unit_price=self.food1.price,
                                                    quantity=4,
                                                    discount=0.0,
                                                    )
        
        self.order_item2 = OrderItem.objects.create(order=self.order1,
                                                    food=self.food2,
                                                    unit_price=self.food2.price,
                                                    quantity=8,
                                                    discount=0.0,
                                                    )
        
    def test_table_str(self):
        self.assertEquals(str(self.table1), f"{self.table1}")
        
    def test_get_available_table(self):
        available_table = Table.get_available_table()
        self.assertEqual(available_table, self.table1)
        
    def test_save_table(self):
        self.assertEqual(Table.objects.count(), 2)
        
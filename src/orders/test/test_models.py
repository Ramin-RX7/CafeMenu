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
        
    def test_price_order(self):
        calculated_price = self.order1.price
        expected_price = self.order_item1.unit_price*self.order_item1.quantity + self.order_item2.unit_price*self.order_item2.quantity
        
        self.assertEqual(calculated_price, expected_price)
        
    def test_final_price_order(self):
        expected_price = self.order1.price / 100 * (self.order1.discount or 100)
        final_price = self.order1.final_price
        
        self.assertEquals(final_price, expected_price)
        
    def test__str__order(self):
        customer_order1 = str(self.order1.customer)
        customer__str__ = str(self.order1)
        
        self.assertEquals(customer__str__, customer_order1)
        
    def test_approve_order(self):
        self.order1.approve()
        updated_order = Order.objects.get(pk=self.order1.pk)
        
        self.assertEquals(updated_order.status, 'Approved')
        
    def test_reject_order(self):
        self.order1.reject()
        updated_order = Order.objects.get(pk=self.order1.pk)
        
        self.assertEquals(updated_order.status, 'Rejected')
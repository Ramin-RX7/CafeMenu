from django.test import TestCase
from orders.models import Order, Table, OrderItem
from foods.models import Food, Category
from users.models import User
from unittest.mock import Mock
import unittest

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
            price=10,
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
    
    # def test_save_order(self):
    #     order_item = OrderItem.objects.create(order=self.order1,
    #                                             food=self.food1,
    #                                             unit_price=self.food1.price,
    #                                             quantity=0,
    #                                             discount=0.0,
    #                                             )
    #     order_item.save()
    #     self.assertEqual(self.order1.price, 0)
    
    # def test_save_with_price(self):
    #     self.food = Food.objects.create(
    #         title='Koofteh',
    #         price=0,
    #         category=self.category1
    #     )
        
    #     self.food3 = Food.objects.create(
    #         title='omlet',
    #         price=0,
    #         category=self.category1
    #     )
        
    #     order = Order(
    #         customer='9176877108',
    #         table=self.table1,
    #         discount=2,
    #         responsible_staff=self.user1,
    #     )
    #     order.save(check_items=True)
        
    #     order_item = OrderItem.objects.create(order=self.order,
    #                                             food=self.food,
    #                                             unit_price=self.food.price,
    #                                             quantity=0,
    #                                             discount=0.0,
    #                                             )
        
    #     order_item.save()
        
    #     self.assertTrue(order_item.save(), "Order should be marked as saved")
    
    
    # def test_save_without_price(self):
    #     order_item = OrderItem.objects.create(order=self.order1,
    #                                             food=self.food1,
    #                                             unit_price=self.food1.price,
    #                                             quantity=3,
    #                                             discount=0.0,
    #                                             )
    #     with self.assertRaises(SystemError):
    #         order_item.save()

        
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
        
        self.assertEquals(self.order1.status, 'Approved')
        
    def test_reject_order(self):
        self.order1.reject()
        
        self.assertEquals(self.order1.status, 'Rejected')
        
    def test_deliver_order(self):
        self.order1.deliver()
        
        self.assertEquals(self.order1.status, 'Delivered')
        
    def test_pay_order(self):
        self.order1.pay()
        
        self.assertEquals(self.order1.status, 'Paid')
        
    def test_take_responsibility_order(self):
        self.order1.take_responsibility(self.user1)
        updated_order1 = Order.objects.get(pk=self.order1.pk)
        
        self.assertEqual(updated_order1.responsible_staff, self.user1)
        
    def test__str__orderitem(self):
        order_item_quantity = str(self.order_item1.quantity)
        quantity__str__ = str(self.order_item1)
        
        self.assertEquals(quantity__str__, order_item_quantity)
        
    def test__save__orderitem(self):
        order2 = Order(
            customer='9173523613',
            table=self.table2,
            discount=2,
            responsible_staff=self.user1, 
        )
        order2.save(check_items=False) 
        
        related_order_item_1 = OrderItem.objects.create(order=order2, unit_price=self.food1.price, food=self.food1, quantity=2, discount=0.0)
        related_order_item_2 = OrderItem.objects.create(order=order2, food=self.food1, unit_price=self.food1.price, quantity=3, discount=0.0)
        
        self.assertEquals(related_order_item_2.quantity, 5) 
        
        
    
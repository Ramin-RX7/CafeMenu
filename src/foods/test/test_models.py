from django.test import TestCase
from foods.models import Category,Food



class ModelFoodTest(TestCase):
    
    def setUp(self):
        self.category = Category.objects.create(
            title = "category test",
            description ="Category descriptoin test"
        )
        
        self.food = Food.objects.create(
            title = "test food",
            description ="food descriptoin test",
            price = 10,
            category = self.category,
            is_active =False
        )
        
    def test_category_model(self):
        self.assertEqual(f"{self.category.title}","category test")
        self.assertEqual(f"{self.category.description}","Category descriptoin test")
    
    def test_str_category(self):
        self.assertEqual(str(self.category),"category test")
        
    def test_food_model(self):
        self.assertEqual(f"{self.food.title}","test food")
        self.assertEqual(f"{self.food.description}","food descriptoin test")
        self.assertEqual(f"{self.food.price}",'10')
        self.assertEqual(f"{self.food.category}","category test")
        self.assertEqual(f"{self.food.is_active}",'False')
        
    def test_str_food(self):
        self.assertEqual(str(self.food),"test food")
        
            
    
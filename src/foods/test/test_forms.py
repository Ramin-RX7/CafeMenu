from django.test import TestCase
from foods.forms import CategoryForm,FoodForm
from foods.models import Category


class FoodFormsTest(TestCase):
           
    def test_is_valid_form_category(self):
        form_data={
            'title':'test juice',
            'description':'test category description'}
        form = CategoryForm(data=form_data)
        
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['title'], 'test juice')
        
        odj_saved = form.save()
        self.assertEqual(odj_saved.title, 'test juice')
        self.assertEqual(odj_saved.description, 'test category description')
        
    
    def test_in_valid_form_category(self):
        form_data = {
            'description':'test category description',
        }
        
        form =CategoryForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)
        
    
    def test_is_valid_form_food(self):
        
        category = Category.objects.create(title='test juice',description='test category description')
        
        form_data ={
            'title':"test food",
            'description':"food descriptoin test",
            'price':10,
            'discount':0.0,
            'category': category.id,
            'is_active':False
        }
        
        
        form =FoodForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['title'], "test food")
        odj_saved = form.save()
        self.assertEqual(odj_saved.title, "test food")
        self.assertEqual(odj_saved.description , "food descriptoin test")
        self.assertEqual(odj_saved.price,10)
        self.assertEqual(odj_saved.category, category)
        self.assertEqual(bool(odj_saved.is_active), False)
    
    
    def test_in_valid_form_food(self):
        
        # category = Category.objects.create(title='test juice',description='test category description')
        
        form_data ={
            'title':"test food",
            'description':"food descriptoin test",
            'price':10,
            'discount':0.0,
            # 'category': category.id,
            'is_active':False
        }
        
        form =FoodForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('category', form.errors)

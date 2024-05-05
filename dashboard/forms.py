from django import forms
from .models import Product, Order, Category, OrderCustomer

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['product', 'order_qty']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    subject = forms.CharField(max_length=200)
    message = forms.CharField(widget=forms.Textarea)
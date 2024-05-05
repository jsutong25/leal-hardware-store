from django.db import models
from django.contrib.auth.models import User
import uuid

class Category(models.Model):
    class Meta:
        verbose_name_plural = 'Category'

    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to= 'category_images', null=True)

    def __str__(self):
        return f"{self.name}"

class Product(models.Model):
    name = models.CharField(max_length=100, null=False)
    category = models.ForeignKey(Category, null=True, on_delete=models.CASCADE)
    image = models.ImageField(upload_to= 'images', null=True)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def __str__(self):
        return f"{self.name}"
    
class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=False)
    staff = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    order_qty = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"'{self.product}' ordered by '{self.staff}'"
    
class OrderHistory(models.Model):
    class Meta:
        verbose_name_plural = 'Order History'

    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=False)
    staff = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    order_qty = models.PositiveIntegerField()
    date_requested = models.DateTimeField(null=True)
    date_accepted = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"'{self.product}' ordered by '{self.staff}'"
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    unique_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)

    def __str__(self):
        return f"Cart for {self.user} with ID: {self.unique_id}"

class CartItems(models.Model):
    class Meta:
        verbose_name_plural = 'Cart Items'
        
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.cart}: - cart items"
    
class OrderCustomer(models.Model):
    ordercustomer_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user}: #{self.ordercustomer_id} - {self.date}"

class OrderCustomerItem(models.Model):
    order = models.ForeignKey(OrderCustomer, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.order} Items"
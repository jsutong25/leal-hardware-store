from django.contrib import admin
from .models import *

admin.site.site_header = 'Liel Hardware'

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    list_filter = ('category',)

class OrderAdmin(admin.ModelAdmin):
    list_display = ('product','staff', 'order_qty','date')
    list_filter = ('product', 'staff', 'date')
    
class OrderHistoryAdmin(admin.ModelAdmin):
    list_display = ('product','staff', 'order_qty','date_requested','date_accepted')
    list_filter = ('product', 'staff', 'date_requested', 'date_accepted')

# Register your models here.
admin.site.register(Category)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderHistory, OrderHistoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Cart)
admin.site.register(CartItems)
admin.site.register(OrderCustomer)
admin.site.register(OrderCustomerItem)
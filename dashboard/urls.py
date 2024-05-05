from django.urls import path
from . import views
from .views import add_to_cart, cart_view

urlpatterns = [
    path('', views.index, name='db-index'),
    path('about/', views.about, name='db-about'),
    path('user/', views.users, name='db-user'),
    path('user/details/<int:id>', views.user_detail, name='db-user_details'),
    path('products/', views.customer_products, name='db-customer_products'),
    path('search/', views.search_products, name='search_products'),
    path('search_categoryproduct/', views.search_product_category, name='search_products_category'),

    path('add/<int:product_id>', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart'),
    path('remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update-cart-item/<int:item_id>/', views.update_cart_item, name='update_cart_item'),

    path('checkout/<uuid:cart_id>', views.checkout_page, name='checkout_page'),
    path('payment-success/<uuid:cart_id>', views.payment_successful, name='payment-success'),
    path('payment-failed/<uuid:cart_id>', views.payment_failed, name='payment-failed'),
    

    path('product/', views.product, name='db-product'),
    path('product/details/<int:id>', views.product_detail, name='db-product_details'),
    path('product/edit/<int:id>', views.product_edit, name='db-product_edit'),
    path('order/', views.order, name='db-order'),
    path('order/order_history/', views.order_history, name='db-order_history'),
    path('db-category/', views.category, name='db-category'),

    path('category/<int:id>', views.category_detail, name='category_detail'),
    path('category/product/<int:id>', views.category_product_detail, name='category_product_detail'),
    
    path('sales/', views.sales, name='db-sales'),
    path('sales/details/<int:id>', views.sales_details, name='db-sales_details'),
]
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
import json
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import F, Sum, Q
from urllib.parse import unquote
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
import uuid
from django.urls import reverse
from django.db.models.functions import TruncDay
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Count
from django.template.loader import render_to_string
from django.core.mail import send_mail

# Create your views here.
def index(request):
    product = Product.objects.all()
    product_count = product.count()
    users = User.objects.all()
    users_count = users.count()
    orders = Order.objects.all()
    order_count = orders.count()
    category = Category.objects.all()
    sales = OrderCustomer.objects.all()

    product_form = ProductForm()
    order_form = OrderForm() 

    daily_order_count = (
        OrderCustomer.objects.annotate(day=TruncDay('date')).values('day').annotate(order_count=Count('id')).order_by('day')
    )
    daily_order_count_json = json.dumps(list(daily_order_count), cls=DjangoJSONEncoder)

    # 
    daily_sales = (
        OrderCustomer.objects.annotate(day=TruncDay('date')).values('day').annotate(total_sales=Sum('total')).order_by('day')
    )

    daily_sales_json = json.dumps(list(daily_sales), cls=DjangoJSONEncoder)

    staff_count = User.objects.filter(Q(is_staff=True) | Q(is_superuser=True)).count()
    non_staff_count = User.objects.filter(is_staff=False, is_superuser=False).count()

    user_count_data = [
        {'user_type': 'Staff and Admin', 'count': staff_count},
        {'user_type': 'Customer', 'count': non_staff_count},
    ]

    # Serialize the data to JSON
    user_count_json = json.dumps(user_count_data)

    active_carts_count = (
        Cart.objects.annotate(item_count=Count('unique_id')).filter(item_count__gt=0).values('user').distinct().count()
    )

    cart_data = [
        {'status': 'Active Carts', 'count': active_carts_count},
        {'status': 'Inactive Carts', 'count': User.objects.count() - active_carts_count},
    ]

    cart_data_json = json.dumps(cart_data)

    if request.method == 'POST':
        if 'product_submit' in request.POST:
            product_form = ProductForm(request.POST, request.FILES)
            if product_form.is_valid():
                product_form.save()
                messages.success(request, 'Product added successfully!')
                product_form = ProductForm()  
            else:
                messages.error(request, 'Product addition failed. Please try again.')
        elif 'order_submit' in request.POST:
            order_form = OrderForm(request.POST)
            if order_form.is_valid():
                obj = order_form.save(commit=False)
                obj.staff = request.user
                order_form.save()
                messages.success(request, 'Order requested successfully!')
                order_form = OrderForm() 
            else:
                messages.error(request, 'Order request failed. Please try again.')

    context = {
        'product': product,
        'orders': orders,
        'users': users,
        'product_count': product_count,
        'order_count': order_count,
        'users_count': users_count,
        'product_form': product_form,
        'order_form': order_form,
        'category': category,
        'daily_order_count_json': daily_order_count_json,
        'daily_sales_json': daily_sales_json,
        'user_count_json': user_count_json,
        'cart_data_json': cart_data_json
    }
    return render(request, 'dashboard/index.html', context)

def about(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            email_subject = f"Liel Hardware Store Form Submission: {subject}"
            email_message = f"Name: {name}\nEmail: {email}\n\n{message}"
            recipient_list = ['jtongshs@gmail.com']

            send_mail(email_subject, email_message, email, recipient_list)
            messages.success(request, 'Your message was sent, thank you!')
            return redirect('/about?submitted=True')
        else:
            messages.error(request, 'Failed to send message, please try again.')
            
    else:
        form = ContactForm()

    context = {
        'form': form
    }

    return render(request, 'dashboard/about.html', context)

def customer_products(request):
    query = request.GET.get('q', '')
    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) | Q(category__name__icontains=query)
        )
    else:
        products = Product.objects.all()

    context = {
        'products': products,
        'query': query,
    }
    return render(request, 'dashboard/customer_products.html', context)

def search_products(request):
    query = request.GET.get('q', '')  # Retrieve the search query from the request
    
    if query:
        products = Product.objects.filter(Q(name__icontains=query) | Q(category__name__icontains=query))
    else:
        products = Product.objects.all()

    context = {
        'products': products,
        'query': query,
    }
    product_list_html = render_to_string('dashboard/product_list_partial.html', context)

    return JsonResponse({'product_list_html': product_list_html})

def search_product_category(request, id):
    query = request.GET.get('q', '')

    category = get_object_or_404(Category, id=id)

    if query:
        products = Product.objects.filter(categry=category & Q(name__icontains=query) | Q(category__name__icontains=query))
    else:
        products = Product.objects.filter(category=category)

    context = {
        'category': category,
        'products': products,
        'query': query,
    }

    product_list_html = render_to_string('dashboard/product_list_partial.html', context)

    return JsonResponse({'product_list_html': product_list_html})

def category_detail(request, id):
    category = get_object_or_404(Category, id=id)
    products = Product.objects.filter(category=category)
    
    context = {
        'category': category,
        'products': products,
    }
    return render(request, 'dashboard/category_detail.html', context)

def category_product_detail(request, id):
    product = get_object_or_404(Product, id=id)

    context = {
        'p': product,
    }
    return render(request, 'dashboard/category_product_detail.html', context)

def add_to_cart(request, product_id):
    if not request.user.is_authenticated:
        messages.error(request, 'You must be logged in.')
        return HttpResponseRedirect('/login')
    
    product = Product.objects.get(id=product_id)
    user_cart, created = Cart.objects.get_or_create(user=request.user)

    cart_item, created = CartItems.objects.get_or_create(cart=user_cart, product=product)

    cart_item.quantity += 1
    cart_item.save()

    messages.success(request, 'Product added to cart.')

    return_url = request.GET.get('return_url', '/')
    return HttpResponseRedirect(unquote(return_url))

def cart_view(request):

    if not request.user.is_authenticated:
        messages.error(request, 'You must be logged in.')
        return HttpResponseRedirect('/login')
    
    cart, created = Cart.objects.get_or_create(user=request.user)

    cart_items = CartItems.objects.filter(cart=cart)
    cart_items_with_subtotals = []

    product_count = cart_items.count()

    total = 0
    for item in cart_items:
        item_subtotal = item.product.price * item.quantity  # Calculate the subtotal for this item
        cart_items_with_subtotals.append({
            'item': item,
            'subtotal': item_subtotal,
        })
        total += item_subtotal


    context = {
        'cart_items': cart_items_with_subtotals,
        'total': total,
        'product_count': product_count,
        'cart_id': cart.unique_id,
    }
    return render(request, 'dashboard/cart.html', context)

def remove_from_cart(request, item_id):
    cart_item = CartItems.objects.get(id=item_id)
    cart_item.delete()
    messages.error(request, 'Product removed from cart.')
    return redirect('cart')

def update_cart_item(request, item_id):

    if request.method == 'POST':
        data = json.loads(request.body)
        new_quantity = int(data.get('quantity', 0))

        cart_item = CartItems.objects.get(id=item_id)
        cart_item.quantity = new_quantity
        cart_item.save()

        subtotal = cart_item.product.price * cart_item.quantity

        user_cart = Cart.objects.get(user=request.user)

        total = sum(
            item.product.price * item.quantity
            for item in CartItems.objects.filter(cart=user_cart)
        )

        return JsonResponse({
            'success': True,
            'subtotal': subtotal,
            'total': total,
        })

    return JsonResponse({'success': False}, status=400)

@login_required
def checkout_page(request, cart_id):

    host = request.get_host()

    cart = get_object_or_404(Cart, unique_id=cart_id)

    cart_items = CartItems.objects.filter(cart=cart)
    cart_items_with_subtotals = []

    product_count = cart_items.count()

    total = 0
    product_names = []
    for index, item in enumerate(cart_items, start=1):
        item_subtotal = item.product.price * item.quantity  # Calculate the subtotal for this item
        cart_items_with_subtotals.append({
            'index': index,
            'item': item,
            'subtotal': item_subtotal,
        })
        total += item_subtotal
        product_names.append(item.product.name)

    cart_id = uuid.UUID(str(cart_id))

    item_name = ','.join(product_names)
    
    paypal_checkout = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': total,
        'item_name': item_name,
        'invoice': uuid.uuid4(),
        'currency_code': 'USD',
        'notify_url': f"http://{host}{reverse('paypal-ipn')}",
        'return_url': f"http://{host}{reverse('payment-success', kwargs= {'cart_id': cart_id})}",
        'cancel_url': f"http://{host}{reverse('payment-failed', kwargs= {'cart_id': cart_id})}"
    }

    paypal_payment = PayPalPaymentsForm(initial=paypal_checkout)

    context = {
        'cart_items': cart_items_with_subtotals,
        'total': total,
        'product_count': product_count,
        'paypal': paypal_payment,
    }

    return render(request, 'dashboard/checkout.html', context)

def payment_successful(request, cart_id):
    cart_id = get_object_or_404(Cart, unique_id=cart_id)

    total = sum(item.product.price * item.quantity for item in CartItems.objects.filter(cart=cart_id))
    order = OrderCustomer.objects.create(user=cart_id.user, total=total)
    order.save()

    cart_items = CartItems.objects.filter(cart=cart_id)
    for item in cart_items:
        OrderCustomerItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price,
        )

    cart_items.delete()

    return render(request, 'dashboard/payment_success.html')

def payment_failed(request, cart_id):
    cart_id = get_object_or_404(Cart, cart_id=cart_id)
    return render(request, 'dashboard/payment_failed.html')


# admin views
def users(request):
    users = User.objects.all().values()
    context = {
        'users': users
    }
    return render(request, 'dashboard/users.html', context)

def user_detail(request, id):
    user = get_object_or_404(User, id=id)
    context = {
        'user': user
    }
    return render(request, 'dashboard/users_details.html', context)

def product(request):
    products = Product.objects.all().select_related('category')
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product added succesfully')
            return redirect('/product')
        else:
            messages.error(request, 'Product addition failed. Please try again.')
    else:
        form = ProductForm()
    context = {
        'form': form,
        'products': products,
    }
    return render(request, 'dashboard/product.html', context)

def product_detail(request, id):
    products = Product.objects.all().select_related('category').get(id=id)
    context = {
        'products': products
    }
    return render(request, 'dashboard/product_details.html', context)

def product_edit(request, id):
    product = Product.objects.get(id=id)
    if request.method == 'POST':
        # Instance fills the form out with the current info
        product_form = ProductForm(request.POST, request.FILES, instance=product)
        if 'update' in request.POST:
            if product_form.is_valid():
                product_form.save()
                messages.success(request, 'Product updated successfully.')
                return redirect('/product')
        elif 'delete' in request.POST:
            product.delete()
            messages.success(request, 'Product deleted successfully.')
            return redirect('/product')
    else:
        product_form = ProductForm(instance=product)

    context = { 
        'form': product_form,
        'product': product,
    }
    return render(request, 'dashboard/edit_product.html', context)

def product_delete(request, id):
    product = Product.objects.get(id=id)
    if request.method == 'POST':
        if 'delete' in request.POST:
            product.delete()
            messages.success(request, 'Product deleted successfully.')

    return render(request, 'dashboard/product.html')

def order(request):
    orders = Order.objects.all().select_related('product','staff')
    form = OrderForm()
    if request.method == 'POST':
        if 'order_submit' in request.POST:
            form = OrderForm(request.POST)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.staff = request.user
                obj.save()
                messages.success(request, 'Order requested succesfully')
                return redirect('/order')
            else:
                messages.error(request, 'Order request failed. Please try again.')
        elif 'accept_order' in request.POST:
            order_id = request.POST.get('order_id')
            try:
                order = Order.objects.get(pk=order_id)
                order.product.quantity = F('quantity') + order.order_qty
                order.product.save(update_fields=['quantity'])

                order_history = OrderHistory.objects.create(product=order.product, staff=order.staff, order_qty=order.order_qty, date_requested=order.date)
                order.delete()
                messages.success(request, 'Order accepted.')
                return redirect('/order')


            except Order.DoesNotExist:
                messages.error(request, 'Order not found.')
            except Exception as e:
                messages.error(request, f'Error accepting order: {e}')
        elif 'reject_order' in request.POST:
            order_id = request.POST.get('order_id')
            try:
                order = Order.objects.get(pk=order_id)
                order.delete()
                messages.success(request, 'Order rejected.')
                return redirect('/order')
            except Order.DoesNotExist:
                messages.error(request, 'Order not found.')
            except Exception as e:
                messages.error(request, f'Error rejecting order: {e}')
    else:
        form = OrderForm()

    context = {
        'form': form,
        'orders': orders,
    }
    return render(request, 'dashboard/order.html', context)

def order_history(request):
    order_history = OrderHistory.objects.all()

    context = {
        'order_history': order_history,
    }
    return render(request, 'dashboard/order_history.html', context)

def category(request):
    category = Category.objects.all()
    form = CategoryForm()
    if request.method == 'POST':
        if 'category-submit' in request.POST:
            form = CategoryForm(request.POST, request.FILES)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.save()
                messages.success(request, 'Category added successfully.')
                return redirect('/db-category')
            else:
                messages.error(request, 'Failed to add category. Please try again.')
        elif 'delete-category' in request.POST:
            category_id = request.POST.get('category_id')
            try:
                category = Category.objects.get(pk=category_id)
                category.delete()
                messages.success(request, 'Category deleted.')
                return redirect('/db-category')
            except Category.DoesNotExist:
                messages.error(request, 'Category not found.')
            except Exception as e:
                messages.error(request, f'Error deleting category: {e}')
    else:
        form = CategoryForm()
    context = {
        'form': form,
        'category': category,
    }
    return render(request, 'dashboard/db-category.html', context)

def sales(request):
    sales = OrderCustomer.objects.all()

    context = {
        'sales': sales
    }
    return render(request, 'dashboard/sales.html', context)

def sales_details(request, id):
    sales = get_object_or_404(OrderCustomer, id=id)
    sales_details = OrderCustomerItem.objects.filter(order=sales)

    context = {
        'sales': sales,
        'details': sales_details
    }
    return render(request, 'dashboard/sales_details.html', context)

import django
from django.contrib.auth.models import User
from store.models import Address, Cart, Category, Order, Product
from django.shortcuts import redirect, render, get_object_or_404
from .forms import RegistrationForm, AddressForm
from django.contrib import messages
from django.views import View
import decimal
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator 
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import EmotionData
import json
import logging
from django.core.paginator import Paginator

logger = logging.getLogger(__name__)

# @login_required
# def check_login_status(request):
#     return JsonResponse({'logged_in': True})

# def not_logged_in(request):
#     return JsonResponse({'logged_in': False})

@csrf_exempt
@login_required
def save_emotion_data(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        logger.debug(f'Received data: {data}')
        joy = data.get('joy', 0.0)
        sadness = data.get('sadness', 0.0)
        surprise = data.get('surprise', 0.0)
        anger = data.get('anger', 0.0)
        fear = data.get('fear', 0.0)
        disgust = data.get('disgust', 0.0)

        emotion_data = EmotionData.objects.create(
            user=request.user,
            joy=joy,
            sadness=sadness,
            surprise=surprise,
            anger=anger,
            fear=fear,
            disgust=disgust
        )
        logger.debug(f'Emotion data saved: {emotion_data}')
        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'fail'})

# Create your views here.

def home(request):
    categories = Category.objects.filter(is_active=True, is_featured=True)[:3]
    products = Product.objects.filter(is_active=True, is_featured=True)[:8]
    context = {
        'categories': categories,
        'products': products,
    }
    return render(request, 'store/index.html', context)


def detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    related_products = Product.objects.exclude(id=product.id).filter(is_active=True, category=product.category)
    context = {
        'product': product,
        'related_products': related_products,

    }
    return render(request, 'store/detail.html', context)


def all_categories(request):
    categories = Category.objects.filter(is_active=True)
    return render(request, 'store/categories.html', {'categories':categories})


def category_products(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category)

    # Lọc sản phẩm theo từ khóa tìm kiếm nếu có
    query = request.GET.get('q')
    if query:
        products = products.filter(title__icontains=query)
    
    # Lọc sản phẩm theo các tiêu chí filter
    price_from = request.GET.get('price_from')
    price_to = request.GET.get('price_to')
    if price_from and price_to:
        products = products.filter(price__gte=price_from, price__lte=price_to)

    # Sắp xếp sản phẩm
    sort_by = request.GET.get('sort_by', 'default')
    if sort_by == 'popularity':
        products = products.order_by('-popularity')
    elif sort_by == 'low-high':
        products = products.order_by('price')
    elif sort_by == 'high-low':
        products = products.order_by('-price')
    else:
        products = products.order_by('id')  # Mặc định sắp xếp theo id

    # Phân trang sản phẩm
    paginator = Paginator(products, 12)  # 12 sản phẩm mỗi trang
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.all()
    context = {
        'category': category,
        'products': page_obj,  # Chỉ truyền đối tượng trang
        'categories': categories,
        'price_from': price_from,
        'price_to': price_to,
        'query': query,
        'sort_by': sort_by,
        'paginator': paginator,
    }
    return render(request, 'store/category_products.html', context)

# Authentication Starts Here

class RegistrationView(View):
    def get(self, request):
        form = RegistrationForm()
        return render(request, 'account/register.html', {'form': form})
    
    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request, "Congratulations! Registration Successful!")
            form.save()
        return render(request, 'account/register.html', {'form': form})
        

@login_required
def profile(request):
    addresses = Address.objects.filter(user=request.user)
    orders = Order.objects.filter(user=request.user)
    return render(request, 'account/profile.html', {'addresses':addresses, 'orders':orders})


@method_decorator(login_required, name='dispatch')
class AddressView(View):
    def get(self, request):
        form = AddressForm()
        return render(request, 'account/add_address.html', {'form': form})

    def post(self, request):
        form = AddressForm(request.POST)
        if form.is_valid():
            user=request.user
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            reg = Address(user=user, locality=locality, city=city, state=state)
            reg.save()
            messages.success(request, "New Address Added Successfully.")
        return redirect('store:profile')


@login_required
def remove_address(request, id):
    a = get_object_or_404(Address, user=request.user, id=id)
    a.delete()
    messages.success(request, "Address removed.")
    return redirect('store:profile')

@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = get_object_or_404(Product, id=product_id)

    # Check whether the Product is alread in Cart or Not
    item_already_in_cart = Cart.objects.filter(product=product_id, user=user)
    if item_already_in_cart:
        cp = get_object_or_404(Cart, product=product_id, user=user)
        cp.quantity += 1
        cp.save()
    else:
        Cart(user=user, product=product).save()
    
    return redirect('store:cart')


@login_required
def cart(request):
    user = request.user
    cart_products = Cart.objects.filter(user=user)

    # Display Total on Cart Page
    amount = decimal.Decimal(0)
    shipping_amount = decimal.Decimal(10)
    # using list comprehension to calculate total amount based on quantity and shipping
    cp = [p for p in Cart.objects.all() if p.user==user]
    if cp:
        for p in cp:
            temp_amount = (p.quantity * p.product.price)
            amount += temp_amount

    # Customer Addresses
    addresses = Address.objects.filter(user=user)

    context = {
        'cart_products': cart_products,
        'amount': amount,
        'shipping_amount': shipping_amount,
        'total_amount': amount + shipping_amount,
        'addresses': addresses,
    }
    return render(request, 'store/cart.html', context)


@login_required
def remove_cart(request, cart_id):
    if request.method == 'GET':
        c = get_object_or_404(Cart, id=cart_id)
        c.delete()
        messages.success(request, "Product removed from Cart.")
    return redirect('store:cart')


@login_required
def plus_cart(request, cart_id):
    if request.method == 'GET':
        cp = get_object_or_404(Cart, id=cart_id)
        cp.quantity += 1
        cp.save()
    return redirect('store:cart')


@login_required
def minus_cart(request, cart_id):
    if request.method == 'GET':
        cp = get_object_or_404(Cart, id=cart_id)
        # Remove the Product if the quantity is already 1
        if cp.quantity == 1:
            cp.delete()
        else:
            cp.quantity -= 1
            cp.save()
    return redirect('store:cart')

from django.http import HttpResponseBadRequest

@login_required
def checkout(request):
    user = request.user
    address_id = request.GET.get('address')
    
    address = get_object_or_404(Address, id=address_id, user=user)
    # Get all the products of User in Cart
    cart = Cart.objects.filter(user=user)
    
    for c in cart:
        # Saving all the products from Cart to Order
        Order(user=user, address=address, product=c.product, quantity=c.quantity).save()
        # And Deleting from Cart
        c.delete()
    
    # Redirect to Checkout HTML page
    return render(request, 'store/checkout.html', {'address': address, 'cart': cart})



@login_required
def orders(request):
    all_orders = Order.objects.filter(user=request.user).order_by('-ordered_date')
    return render(request, 'store/orders.html', {'orders': all_orders})





def shop(request):
    return render(request, 'store/shop.html')





def test(request):
    return render(request, 'store/test.html')

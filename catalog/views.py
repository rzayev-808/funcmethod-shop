from django.shortcuts import render
from .models import *
from .forms import *
from django.views.generic.edit import FormView 
from django.forms import ModelForm
from django.shortcuts import render
from decimal import Decimal
from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib.auth import login, authenticate
from django.views.generic import View
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.core.mail import send_mail, BadHeaderError
from django.shortcuts import get_object_or_404 
from django.shortcuts import redirect

# Create your views here.
from django.db.models import Q

def index(request):
    try:
        num_visits = request.session.get('num_visits', 0)
        request.session['num_visits'] = num_visits + 1
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)
    
    categories = Category.objects.all()
    products = Product.objects.all()
    brands = Brand.objects.all()
    fovarites = Fovarite.objects.all()
    
    context = {
        'categories': categories,
        'products': products,
        'brands': brands,
        'cart': cart,
        "home_page": "active",
        'fovarites': fovarites
        
    }
    return render(request, 'base/index.html', context)    


def product_view(request, product_slug):
    try:
        x = request.GET.get('id')
        product_list = request.session.get('product_list', {})
        product_list[product_slug] = x
        request.session['product_list'] = product_list
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)
    his = {}
    keys = []
    
    for key,values in product_list.items():
        keys.append(key)
    history = list(keys)
    for n in history:
        history_products = Product.objects.filter(Q(slug__icontains=n[0])|  Q(slug__icontains=n[5])| Q(slug__icontains=n[3]) | Q(slug__icontains=n[2])| Q(slug__icontains=n[1]))
    #history = list(keys)
    
    #his['slug'] = keys
    
    product = Product.objects.get(slug=product_slug)
    categories = Category.objects.all()
    context = {
        'product': product,
        'categories': categories,
        'cart': cart,
        'product_page': "active",
        'product_list': product_list,
        'history_products': history_products,
        
    }
    return render(request, 'base/product.html', context)

def product_history(request):
    try:
        x = request.GET.get('id')
        product_list = request.session.get('product_list', {})
        product_list[product_slug] = x
        request.session['product_list'] = product_list
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)
    his = {}
    keys = []
    
    for key,values in product_list.items():
        keys.append(key)
    history = list(keys)
    for n in history:
       pass

def category_view(request, category_slug):

    
    category = Category.objects.get(slug=category_slug)
    price_filter_type = request.GET.get('price_filter_type')
    print (price_filter_type)
    products_of_category = Product.objects.filter(category=category)
    context = {
        'category': category,
        'products_of_category': products_of_category,
        #'cart': cart,
        'category_page': "active"
    }
    return render(request, 'base/brand.html', context)




def brand_view(request, brand_slug):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)
   
    brand = Brand.objects.get(slug=brand_slug)
    price_filter_type = request.GET.get('price_filter_type')
    print(price_filter_type)
    products_of_brand = Product.objects.filter(brand=brand)
    categories_of_brand = Category.objects.filter(brand=brand)
    context = {
        'brand': brand,
        'products_of_brand': products_of_brand,
        'categories_of_brand': categories_of_brand,
        'cart': cart,
        'brand_page': "active"
    }
    return render(request, 'base/brand.html', context)

def cart_view(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)
    categories = Category.objects.all()
    context = {
        
        'categories': categories,
        'cart': cart,
    }
    return render(request, 'project/cart.html', context)


def add_to_cart_view(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)
    product_slug = request.GET.get('product_slug')
    product = Product.objects.get(slug=product_slug)
    cart.add_to_cart(product.slug)
    new_cart_total = 0.00
    for item in cart.items.all():
        new_cart_total += float(item.item_total)
    cart.cart_total = new_cart_total
    cart.save()
    return JsonResponse({'cart_total': cart.items.count(), 'cart_total_price': cart.cart_total})

def remove_from_cart_view(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)
    product_slug = request.GET.get('product_slug')
    product = Product.objects.get(slug=product_slug)
    cart.remove_from_cart(product.slug)
    new_cart_total = 0.00
    for item in cart.items.all():
        new_cart_total += float(item.item_total)
    cart.cart_total = new_cart_total
    cart.save()
    return JsonResponse({'cart_total': cart.items.count(), 'cart_total_price': cart.cart_total})


def change_item_qty(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)
    qty = request.GET.get('qty')
    item_id = request.GET.get('item_id')
    cart.change_qty(qty, item_id)
    cart_item = CartItem.objects.get(id=int(item_id))
    return JsonResponse(
        {'cart_total': cart.items.count(), 
        'item_total': cart_item.item_total,
        'cart_total_price': cart.cart_total})


def checkout_view(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)
    categories = Category.objects.all()
    context = {
        
        'categories': categories,
        'cart': cart,
    }
    return render(request, 'project/checkout.html', context)


def order_create_view(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)
    form = OrderForm(request.POST or None)
    categories = Category.objects.all()
    context = {
        'form': form,
        
        'categories': categories
    }
    return render(request, 'project/order.html', context)


def make_order_view(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)
    form = OrderForm(request.POST or None)
    categories = Category.objects.all()
    if form.is_valid():
        name = form.cleaned_data['name']
        last_name = form.cleaned_data['last_name']
        phone = form.cleaned_data['phone']
        buying_type = form.cleaned_data['buying_type']
        address = form.cleaned_data['address']
        comments = form.cleaned_data['comments']
        new_order = Order.objects.create(
            user=request.user,
            items=cart,
            total=cart.cart_total,
            first_name=name,
            last_name=last_name,
            phone=phone,
            address=address,
            buying_type=buying_type,
            comments=comments
            )
        del request.session['cart_id']
        del request.session['total']
        return HttpResponseRedirect(reverse('thank_you'))
    return render(request, 'order.html', {'categories': categories})

def account_view(request):
    order = Order.objects.filter(user=request.user).order_by('-id')
    categories = Category.objects.all()
    for item in order:
        for new_item in item.items.items.all():
            print(new_item.item_total)
    context = {
        'order': order,
        'categories': categories
    }
    return render(request, 'project/account.html', context)

def registration_view(request):
    form = RegistrationForm(request.POST or None)
    categories = Category.objects.all()
    if form.is_valid():
        new_user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        email = form.cleaned_data['email']
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        new_user.username = username
        new_user.set_password(password)
        new_user.first_name = first_name
        new_user.last_name = last_name
        new_user.email = email
        new_user.save()
        login_user = authenticate(username=username, password=password)
        if login_user:
            login(request, login_user)
            return HttpResponseRedirect(reverse('index'))
    context = {
        'form': form,
        'categories': categories
    }
    return render(request, 'project/registration.html', context)


def login_view(request):
    form = LoginForm(request.POST or None)
    categories = Category.objects.all()
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        login_user = authenticate(username=username, password=password)
        if login_user:
            login(request, login_user)
            return HttpResponseRedirect(reverse('index'))
    context = {
        'form': form,
        'categories': categories
    }
    return render(request, 'project/login.html', context)

def fovarite_update(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    fovarite = Fovarite()
    fovarite.user = request.user
    fovarite.save()
    fovarite.fovarit.add(product)
    #fovarite.fovarit.(product)
    
    
    
    return redirect('index')
    

def filters(request):
    return render(request, 'sufre.html')


def login(request):
    return render(request, 'login.html')

def details(request):
    return render(request, 'product-detail.html')
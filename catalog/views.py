from django.shortcuts import render
from .models import *
from .forms import *
from django.views.generic.edit import FormView 
from django.forms import ModelForm
from django.shortcuts import render
from decimal import Decimal
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib.auth import login, authenticate
from django.views.generic import View
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.core.mail import send_mail, BadHeaderError
from django.shortcuts import get_object_or_404 
from django.shortcuts import redirect
from .filter import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from star_ratings.models import AbstractBaseRating
from django.shortcuts import render, redirect
from django.views.generic import CreateView, FormView, DetailView, UpdateView, View,ListView,TemplateView
from django.views.generic.edit import FormMixin
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.utils.http import is_safe_url
from django.utils.safestring import mark_safe
from django.urls import reverse_lazy
# Create your views here.
from django.db.models import Q
from django.views.generic.list import ListView
from django_filters.views import FilterView
import django_filters
from pyexcel_xlsx import get_data
import json
import hashlib
import xml.etree.ElementTree as ET
import requests
from django.db.models import F


import pyexcel as pe
def data(request):
    xlsxfile = "2f.xlsx"
    with open(xlsxfile, "rb") as f:
        content = f.read()
        r = pe.get_book(file_type="xlsx", file_content=content)
        # for x in r[3]:
        #     create = Product.objects.update_or_create(
        #         barcode=x[0],
        #         #brand_id=1,
        #         category_name=x[1],
        #         #code=x[1],
        #         image = 'bg.jpg',
        #         name=x[2],
        #         price=x[3],
        #         sale=x[4],
        #         title=x[5],
        #     )
        for x in r[3]:
            create = Product.objects.update_or_create(
                #barcode=x[0],
                #brand_id=1,
                #category_name=x[2],
                #code=x[1],
                #image = 'bg.jpg',
                #name=x[3],
                #price=x[4],
                #sale=x[5],
                #title=x[6],
                #barcode=x[0],
                #brand_id=1,
                #category_name=x[1],
                #code=x[1],
                #image = 'bg.jpg',
                #name=x[2],
                #price=x[3],
                #sale=x[5],
                #title=x[5],
                barcode=x[0],
                #brand_id=1,
                category_name=x[1],
                #code=x[1],
                image = 'bg.jpg',
                name=x[2],
                price=x[3],
                sale=x[4],
                title=x[5],
            )
    
    
    return render(request, 'import.html')





class NumberInFilter(django_filters.BaseInFilter, django_filters.NumberFilter):
    pass

class Filters(django_filters.FilterSet):
    brand_id_in = NumberInFilter(field_name='brand', lookup_expr='in')
    class Meta:
        model = Product
        fields = ['price', 'category', 'brand_id_in',]

class PostsView(ListView):
    model = Brand 
    paginate_by = 10
    context_object_name = 'posts'
    template_name = 'sufre.html'
    ordering = ['?']
    #filter_class = ProductsFilter
    def get_queryset(self):
        if self.request.method == 'GET':
            try:
                brand = self.request.GET.get('brand')
                
                    
                return Product.objects.filter(brand__in= self.request.GET.get('brand'))
            except:
                ValueError
                return Product.objects.all()
       

        
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
    
    categories = SubCategory.objects.all()

    products = Product.objects.all().order_by('?')[:6]
    brands = Brand.objects.all()
    w = Product.objects.all().order_by('?')[:9]
    r = Product.objects.all().order_by('?')[:6]
    a = request.session.get('fovarites')
    phone = Phone.objects.get(id=1)
    main = MainCategory.objects.all().order_by('-id')
    cat = Category.objects.all()
    banner = Banner.objects.all()
    
    #x = len(request.session.get('fovarites'))
    #fovarites = Fovarite.objects.all()
    b = []
    try:
        for i in request.session['fovarites']:
            b.append(i['id'])
    except KeyError:
        b = None

    f = ProductFilter(request.GET, queryset=Product.objects.all())
    context = {
        'categories': categories,
        'products': products,
        'brands': brands,
        'cart': cart,
        "home_page": "active",
        #'fovarites': fovarites,
        'filter': f,
        'fovarites_list': request.session.get('fovarites'),
        'w': w,
        'r': r,
        'a': a,
        'b': b,
        'phone':phone,
        'main': main,
        'cat': cat,
        'banner':banner,
        #'one':Banner.objects.get
        
    }
    return render(request, 'base/index.html', context)    

def id_data(request):
    d = Product.objects.all()
    return render(request, 'id.html', {"d":d})


def product_list(request):
    
    f = ProductFilter(request.GET, queryset=Product.objects.all())
    return render(request, 'product_list.html', {'filter': f})

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
    #print(product_list)
    for key,values in product_list.items():
        keys.append(key)
    history = list(keys)
    for n in history:
        history_products = Product.objects.filter(slug__icontains=n[1]).order_by('?')[:3]

    #history = list(keys)
    
    #his['slug'] = keys
    #print(history_products)
    b = []
    try:
        for i in request.session['fovarites']:
            b.append(i['id'])
    except KeyError:
        b = None
    product = Product.objects.get(slug=product_slug)
    categories = Category.objects.all()
    if request.method == 'POST':
        form = ProductComment(request.POST or None)
        if form.is_valid():

            # Create Comment object but don't save to database yet
            form = form.save(commit=False)
            # Assign the current post to the comment
            form.post = product
            # Save the comment to the database
            form.save()
    else:
        form = ProductComment()
    context = {
        'product': product,
        'categories': categories,
        'cart': cart,
        'product_page': "active",
        'product_list': product_list,
        'history_products': history_products,
        'form':form,
        'b':b,
        
    }
    return render(request, 'product-detail.html', context)


def category_view(request, category_slug):

    
    category = Category.objects.get(slug=category_slug)
    price_filter_type = request.GET.get('price_filter_type')
    print (price_filter_type)
    main = MainCategory.objects.all().order_by('-id')
    cat = Category.objects.all()
    subcategory_of_category = SubCategory.objects.filter(category=category)
    #products_of_category 
    context = {
        'category': category,
        #'products_of_category': products_of_category,
        #'cart': cart,
        'subcategory_of_category':subcategory_of_category,
        'category_page': "active",
        'main':main,
        'cat':cat
    }
    return render(request, 'base/brand.html', context)



def subcategory_view(request, subcategory_slug):

    
    subcategory = SubCategory.objects.get(slug=subcategory_slug)
    main = MainCategory.objects.all().order_by('-id')
    cat = Category.objects.all()
    products_of_subcategory = Product.objects.filter(category=subcategory)
    context = {
        'subcategory': subcategory,
        'products_of_subcategory': products_of_subcategory,
        #'cart': cart,
        'category_page': "active",

        'main':main,
        'cat':cat
    }
    return render(request, 'category.html', context)


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
    color = request.GET.get('color')
    product = Product.objects.get(slug=product_slug)
    cart.add_to_cart(product.slug, color)
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
    promo = CompanyPromoCode.objects.all()
    context = {
        
        'categories': categories,
        'cart': cart,
        'promo':promo
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
        promocode = request.POST.get('promocode')
        com = CompanyPromoCode.objects.filter(code=promocode)
        sale = 0
        main = int(cart.cart_total)
        print("com :",len(com))
        amount = int(cart.cart_total) * 100
        f = 0
        money = 0
        limit = 0
        for t in com:
            f = t.faiz
            count = t.count
            money=t.money
            limit = t.limit

        #rint(sale)
        
        if int(f) > 1 and int(count) < int(limit):
            dis = main = (int(cart.cart_total) * int(f)) / 100
            amount = (int(cart.cart_total) - int(dis)) * 100
            count = CompanyPromoCode.objects.update(count=F('count')+1)

        elif int(money) > 1 and int(count) < int(limit):
            amount = (int(cart.cart_total) - int(money)) * 100
            count = CompanyPromoCode.objects.update(count=F('count')+1)
        merchantName = "schafer_az"
        authKey = "97994b5611e443fc9ed4f3c2262e463a"
        cardType = "v"
        
        #print(promocode)
        description = str(cart)
        a = ("97994b5611e443fc9ed4f3c2262e463a{}{}{}{}").format(merchantName,cardType,amount,description)
        h = hashlib.md5(a.encode("utf-8")).hexdigest()
        g = {

            "merchantName": merchantName,

            "cardType": cardType,

            "hashCode": h,

            "lang": "lv",

            "amount":amount,

            "description":description

        }
        print(g)
        url = "https://rest.goldenpay.az/web/service/merchant/getPaymentKey"
        l = requests.post(url, json=g)
        
        root = ET.fromstring(l.content)
        print(root)
        del request.session['cart_id']
        del request.session['total']
        for x in root.iter('paymentKey'):
            
            return redirect("https://rest.goldenpay.az/web/pay/" + x.text)
    return render(request, 'order.html', {'categories': categories})

def account_view(request):
    order = Order.objects.filter(user=request.user).order_by('-id')
    categories = Category.objects.all()
    history = HistoryProducts.objects.filter(user=request.user).order_by('-id')
    mesaj = Message.objects.filter(user=request.user)
    fovarites = request.session.get('fovarites')
    pk = []
    if not fovarites:
        pass
    else:
        for x in fovarites:
            pk.append(x['id'])
    k = Product.objects.filter(id__in=pk)
    for item in order:
        for new_item in item.items.items.all():
            print(new_item.item_total)
    context = {
        'order': order,
        'categories': categories,
        'history':history,
        'mesaj':mesaj,
        'k':k
    }
    return render(request, 'account.html', context)

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
        
        
        new_user.set_password(password)
        new_user.first_name = first_name
        new_user.username = username
        new_user.last_name = last_name
        new_user.email = email
        
        new_user.save()
        login_user = authenticate(email=email, password=password)
        if login_user:
            login(request, login_user)
            return HttpResponseRedirect(reverse('cart'))
        
        #return HttpResponseRedirect(reverse('account'))
    context = {
        'form': form,
        'categories': categories
    }
    return render(request, 'register.html', context)


def login_view(request):
    forms = LoginForm(request.POST or None)
    form = RegistrationForm(request.POST or None)
    categories = Category.objects.all()
    if forms.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        login_user = authenticate(username=username, password=password)
        if login_user:
            login(request, login_user)
            return HttpResponseRedirect(reverse('index'))
    context = {
        'forms': forms,
        'form':form,
        'categories': categories
    }
    return render(request, 'login.html', context)

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



def details(request):
    filter = Filters(request.GET, queryset=Product.objects.all().order_by('-id'))
    brand = Brand.objects.all()

    context = {
         'filter': filter,
         'brand': brand,
     }
    return render(request, 'detail.html', context)

def accounts(request):
    return render(request, 'account.html')

def buy(request, product_slug):
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
    product_slug = product_slug
    color = request.GET.get('color')
    print(color)
    product = Product.objects.get(slug=product_slug)
    cart.add_to_cart(product.slug , color)
    print(cart)
    new_cart_total = 0.00
    for item in cart.items.all():
        new_cart_total += float(item.item_total)
    cart.cart_total = new_cart_total
    cart.save()
    #return JsonResponse({'cart_total': cart.items.count(), 'cart_total_price': cart.cart_total})
    return HttpResponseRedirect(reverse('cart'))

from django.views import generic
from django.urls import reverse_lazy


class ClickCreateView(generic.CreateView):
    model = ClickForms
    form_class = ClickForms
    # context_object_name = 'people'
    template_name = 'elan/form.html'
    success_url = reverse_lazy('thank_you')

    

    def form_valid(self, form):
        obj = form.save(commit=False)
        #obj.product = self.request.GET.get('id')
        return super(ClickCreateView, self).form_valid(form)


from .mixins import *

class RegisterView(CreateView):
  form_class = RegisterForm
  template_name = 'register.html'
  success_url = reverse_lazy('login')


class LoginView(NextUrlMixin, RequestFormAttachMixin, FormView):
  form_class = LoginsForm
  template_name = 'login.html'
  success_url = reverse_lazy('accounts')
  default_next = reverse_lazy('accounts')

  def form_valid(self, form):
    next_path = self.get_next_url()
    return redirect(next_path)


class SearchProductView(ListView):
  template_name = "search/view.html"
  paginate_by = 12
  def get_context_data(self, *args, **kwargs):
    context = super(SearchProductView, self).get_context_data(*args, **kwargs)
    context['query'] = self.request.GET.get('q')
    context['main'] = MainCategory.objects.all().order_by('-id')
    return context

  def get_queryset(self, *args, **kwargs):
    request = self.request
    query = request.GET.get('q', None)
    main = MainCategory.objects.all().order_by('-id')
    cat = Category.objects.all()
    if query is not None:
      return Product.objects.search(query)
    return Product.objects.featured()

def add_to_fovarite(request, id):
    if request.method == "POST":
        if not request.session.get('fovarites'):
            request.session['fovarites'] = list()
        else:
            request.session['fovarites'] = list(request.session['fovarites'])
        if not request.session.get('visits'):
            request.session['visits'] = list()
        else:
            request.session['visits'] = list(request.session['visits'])
        item_exist = next((item for item in request.session['fovarites'] if  item['id'] == id), False)
    #visit = 0
    
    
    #count = visits + request.POST.get('visits')
    add_data = {
        #'type': request.POST.get('type'),
        'id': id,
        #'visit': visit,
    }
    
    if not item_exist:
        request.session['fovarites'].append(add_data)
        request.session.modified = True
        #visit += 1
        #visits = int(request.session.get('visits', '1')) + 1
    return JsonResponse({'add_data': add_data})

def products_history(request):

    if request.method == "POST":
        form = HistoryForms(request.POST or None)
        if form.is_valid():
            new = form.save(commit=False)
            new.product = request.POST.get('product_id')
            new.user = request.POST.get('user_id')
            #new.product = request.GET.get('id')

            #if  HistoryProducts.objects.filter(user=new.user).filter(product=request.POST.get('product_id')):
              #  pass
           #else:
            new.save()
    a = HistoryProducts.objects.update_or_create(
                user_id = request.POST.get('user_id'),
                product_id=request.POST.get('product_id')
            )
    context = {
        'a':a
    }
    return render(request, 'a.html', context)
     

def fovarite_list(request):
    fovarites = request.session.get('fovarites')
    pk = []
    if not fovarites:
        pass
    else:
        for x in fovarites:
            pk.append(x['id'])
        k = Product.objects.filter(id__in=pk)
       
        context = {
            'f' : k
        }
  
        return render(request, 'fovarites.html', context )
    return render(request, 'fovarites.html')

from django.core.paginator import Paginator


def filter_list(request):
    brand = Brand.objects.all()
    category = SubCategory.objects.all()
    posts = Product.objects.all()
    filter = Filters(request.GET, queryset=Product.objects.all().order_by('?'))
    paginator = Paginator(filter.qs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    #page_obj = paginator.get_page(page_number)
    context = {
        'brand': brand,
        'category': category,
        'posts': posts,
        'filter': filter,
        'page_obj':page_obj
    }
    return render(request, 'sufre.html', context)

def color_view(request, id):
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
    #print(product_list)
    for key,values in product_list.items():
        keys.append(key)
    history = list(keys)
    for n in history:
        history_products = Product.objects.filter(slug__icontains=n[1]).order_by('-id')
    #history = list(keys)
    
    #his['slug'] = keys
    #print(history_products)
    color = Color.objects.get(id=id)
    categories = Category.objects.all()
    if request.method == 'POST':
        form = ProductComment(request.POST or None)
        if form.is_valid():

            # Create Comment object but don't save to database yet
            form = form.save(commit=False)
            # Assign the current post to the comment
            form.post = product
            # Save the comment to the database
            form.save()
    else:
        form = ProductComment()
    context = {
        'color': color,
        'categories': categories,
        'cart': cart,
        'product_page': "active",
        'product_list': product_list,
        'history_products': history_products,
        'form':form,
        
    }
    return render(request, 'color-detail.html', context)



def delete_fovarites(request):
    if request.session.get('fovarites'):
        del request.session['fovarites']
    
    return redirect(request.POST.get('url_from'))


def remove_fovarites(request, id):
    if request.method == 'POST':
        for i in request.session['fovarites']:
            
            if i['id'] == id:

                
                i.clear()
                
                
                

        while {} in request.session['fovarites']:
            request.session['fovarites'].remove({})

        if not request.session['fovarites']:
            del request.session['fovarites']
        
        request.session.modified = True
        return redirect(request.POST.get('url_from'))


def banner(request, link):
    banner = Banner.objects.all()
    context = {
        'banner':banner,
    }
    return render(request, 'banner.html', context)
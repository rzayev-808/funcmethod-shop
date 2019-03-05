from django.db import models
from django.utils.text import slugify
from time import time
from django.urls import reverse
from decimal import Decimal
from django.conf import settings
from django.db import models
from django.db.models import Q
from django.db.models.signals import pre_save, post_save
from django.contrib.auth.models import User
from PIL import Image
import os
import glob

# Create your models here.

class Brand(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('brand_detail', kwargs={'brand_slug': self.slug})

    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name+str(self.name))
        super(Brand, self).save(*args, **kwargs)
    


class Category(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, verbose_name='Brand')
    name = models.CharField(max_length=100)
    slug = models.SlugField()
    img = models.ImageField()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name+str(self.name))
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'category_slug': self.slug})


def gen_slug(s):
    new_slug = slugify(s, allow_unicode=True)
    return new_slug + '_' + str(int(time()))

class Product(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE, verbose_name='Kategoriya')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, verbose_name='Brand')
    name = models.CharField(max_length=100)
    image = models.ImageField()
    price = models.DecimalField(max_digits=9, decimal_places=2, default=0.00, verbose_name='Qiymeti')
    title = models.TextField()
    phone = models.CharField(max_length=100, verbose_name="Elaqe normesi")
    addres = models.CharField(max_length=200, verbose_name="Address")
    data = models.DateField(auto_now_add=True)
    link = models.URLField(blank=True)
    slug = models.SlugField(max_length=75, blank=True)

    def save (self, *args, **kwargs):
        if not self.id:
            self.slug = gen_slug(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name}' + ' , "' + f'{self.data}" '

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'product_slug': self.slug})


    
class CartItem(models.Model):

    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(default=1)
    item_total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)

    def  __str__(self):
        return "Cart item for product {0}".format(self.product.title)


class Cart(models.Model):

    items = models.ManyToManyField(CartItem, blank=True)
    cart_total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)

    def  __str__(self):
        return str(self.id)

    def add_to_cart(self, product_slug):
        cart = self
        product = Product.objects.get(slug=product_slug)
        new_item, _ = CartItem.objects.get_or_create(product=product, item_total=product.price)
        cart_items = [item.product for item in cart.items.all()]
        if new_item.product not in cart_items:
            cart.items.add(new_item)
            cart.save()

    def remove_from_cart(self, product_slug):
        cart = self
        product = Product.objects.get(slug=product_slug)
        for cart_item in cart.items.all():
            if cart_item.product == product:
                cart.items.remove(cart_item)
                cart.save()

    def change_qty(self, qty, item_id):
        cart = self
        cart_item = CartItem.objects.get(id=int(item_id))
        cart_item.qty = int(qty)
        cart_item.item_total = int(qty) * Decimal(cart_item.product.price)
        cart_item.save()
        new_cart_total = 0.00
        for item in cart.items.all():
            new_cart_total += float(item.item_total)
        cart.cart_total = new_cart_total
        cart.save()

ORDER_STATUS_CHOICES = (
	('Qeyde alindi', 'Qeyde alindi'),
	('Icra olunur', 'Icra olunur'),
	('Odenilib', 'Odenilib')
)

class Order(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ForeignKey('Cart', on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    buying_type = models.CharField(max_length=40, choices=(('Magazada', 'Magazada'), 
        ('Catdirilma', 'Catdirilma')), default='Magazada')
    date = models.DateTimeField(auto_now_add=True)
    comments = models.TextField()
    status = models.CharField(max_length=100, choices=ORDER_STATUS_CHOICES, default=ORDER_STATUS_CHOICES[0][0])

    def  __str__(self):
        return "Muraciyet №{0}".format(str(self.id))

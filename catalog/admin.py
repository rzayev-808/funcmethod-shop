from django.contrib import admin
from .models import Category, Brand, Product, CartItem, Cart, Order


def make_payed(modeladmin, request, queryset):
    queryset.update(status='Odenilib')
make_payed.short_description = "Odenilmis kimi qeyd et"

class OrderAdmin(admin.ModelAdmin):
	list_filter = ['status']
	actions = [make_payed]


class ProductAdmin(admin.ModelAdmin):

	list_display = ("category", "brand", "title",)
	model = Product




admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Product, ProductAdmin)
admin.site.register(CartItem)
admin.site.register(Cart)
admin.site.register(Order, OrderAdmin)
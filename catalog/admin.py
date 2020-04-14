from django.contrib import admin
from .models import *
#from simple_history.admin import SimpleHistoryAdmin


class ProductMultiImage(admin.TabularInline):
    model = MultiImage
    fields = ['image',]

def make_payed(modeladmin, request, queryset):
    queryset.update(status='Odenilib')
make_payed.short_description = "Odenilmis kimi qeyd et"

class OrderAdmin(admin.ModelAdmin):
	list_filter = ['status']
	actions = [make_payed]


class ProductAdmin(admin.ModelAdmin):
	inlines = [ProductMultiImage,]
	list_display = ("category", "name", "active", "stock", "price", "sale", "dicount",)
	model = Product


admin.site.register(MultiImage)
admin.site.register(Fovarite)
admin.site.register(Color)

admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(SubCategory)

admin.site.register(Product, ProductAdmin)
admin.site.register(CartItem)
admin.site.register(Cart)
admin.site.register(Order, OrderAdmin)
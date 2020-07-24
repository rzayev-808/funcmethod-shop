from django.contrib import admin
from .models import *
#from simple_history.admin import SimpleHistoryAdmin



class ProductColor(admin.StackedInline):
	
    model = Color
    fields = ['color_name','color','code', 'image',]
	
	

class ProductMultiImage(admin.TabularInline):
    model = MultiImage
    fields = ['image',]

class ProductMultiSize(admin.TabularInline):
    model = Size
    fields = ['name',]

class ProductMultiPromoCode(admin.TabularInline):
    model = PromoCode
    fields = ['name', 'code', ]
	
class ColorssAdmin(admin.TabularInline):
    #extra = 1
	
	model = Color
	fields = ['code', 'color','color_name', 'image']
	#show_change_link = True
	extra = 0
	#readonly_fields = ['odenis',]
	

def make_payed(modeladmin, request, queryset):
    queryset.update(status='Odenilib')
make_payed.short_description = "Odenilmis kimi qeyd et"


def category_payed(modeladmin, request, queryset):
    queryset.update()
category_payed.short_description = "Yenile"


def deactive_payed(modeladmin, request, queryset):
    queryset.update(active='False')
deactive_payed.short_description = "Secilmis mehsullari deaktiv et"


def active_payed(modeladmin, request, queryset):
    queryset.update(active='True')
active_payed.short_description = "Secilmis mehsullari aktiv et"

class OrderAdmin(admin.ModelAdmin):
	list_filter = ['status']
	actions = [make_payed]


class SubCategoryAdmin(admin.ModelAdmin):
	actions = [category_payed,]
	list_display = ('name',)
	model = SubCategory
	
class ColorAdmin(admin.ModelAdmin):
	list_display = ('code',)
	actions = [category_payed,]
	model = Color
	search_fields = ('code',)

class ProductAdmin(admin.ModelAdmin):
	inlines = [ProductMultiImage, ProductMultiPromoCode,ProductMultiSize, ColorssAdmin]
	extra = 1
	list_display = ("category", "slug" ,"name", "active", "stock", "price", "sale", "dicount","prome_code_in",)
	model = Product
	actions = [deactive_payed, active_payed]
	#extra = 2
	list_filter = ('active','codes__name','brand',)
	#readonly_fields = ['slug','reting',]
	#fields = ['kredit',]
	search_fields = ('name', 'code',)
	

class CartAdmin(admin.ModelAdmin):
    	#inlines = [ProductMultiImage, ProductMultiPromoCode,ProductMultiSize, ColorssAdmin]
	#
	#list_display = ("category", "slug" ,"name", "active", "stock", "price", "sale", "dicount","prome_code_in",)
	model = Cart
	actions = [deactive_payed, active_payed]
	#extra = 2
	#list_filter = ('active','codes__name','brand',)
	#readonly_fields = ['slug','reting',]
	#fields = ['kredit',]
	search_fields = ('id',)
admin.site.register(MultiImage)
#Sadmin.site.register(Fovarite)
#n.site.register(Color)
admin.site.register(PromoCode)
admin.site.register(CompanyPromoCode)
admin.site.register(Click)
admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(User)
admin.site.register(Color)
admin.site.register(Phone)
admin.site.register(Message)

admin.site.register(HistoryProducts)
admin.site.register(Comment)
admin.site.register(Product, ProductAdmin)
admin.site.register(CartItem)
admin.site.register(Cart, CartAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(MainCategory)

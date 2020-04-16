from django.contrib import admin
from .models import *
#from simple_history.admin import SimpleHistoryAdmin


class ProductMultiImage(admin.TabularInline):
    model = MultiImage
    fields = ['image',]

class ProductMultiSize(admin.TabularInline):
    model = Size
    fields = ['name',]

class ProductMultiPromoCode(admin.TabularInline):
    model = PromoCode
    fields = ['name', 'code', ]
	
class Kredit_18Admin(admin.StackedInline):
    #extra = 1
	
	model = Kredit_18_ay
	fields = ['faiz', 'odenis',]
	show_change_link = True
	extra = 1
	readonly_fields = ['odenis',]
	def get_max_num(self, request, obj=None, **kwargs):
		max_num = 1
		if obj and obj.kredit:
			return max_num 
		return max_num

def make_payed(modeladmin, request, queryset):
    queryset.update(status='Odenilib')
make_payed.short_description = "Odenilmis kimi qeyd et"

class OrderAdmin(admin.ModelAdmin):
	list_filter = ['status']
	actions = [make_payed]

class ProductAdmin(admin.ModelAdmin):
	inlines = [ProductMultiImage, ProductMultiPromoCode,Kredit_18Admin,ProductMultiSize]
	extra = 1
	list_display = ("category", "name", "active", "stock", "price", "sale", "dicount","prome_code_in","kredit_18",)
	model = Product
	#extra = 2
	list_filter = ('active','codes__name','company__name',)
	readonly_fields = ['slug','month_6', 'month_12',]
	#fields = ['kredit',]
	


admin.site.register(MultiImage)
admin.site.register(Fovarite)
admin.site.register(Color)
admin.site.register(PromoCode)

admin.site.register(CompanyPromoCode)

admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(SubCategory)
admin.site.register(Kredit_18_ay)


admin.site.register(Product, ProductAdmin)
admin.site.register(CartItem)
admin.site.register(Cart)
admin.site.register(Order, OrderAdmin)

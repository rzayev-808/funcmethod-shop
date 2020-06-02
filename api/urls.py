from django.urls import path, include
from rest_framework import routers
from .views import *
router = routers.DefaultRouter()
router.register(r'product', ProductsApiViews)
router.register(r'category', SubCategoryApiViews)
router.register(r'brand', BrandApiViews)


urlpatterns = [
    
    path('api/v1/', include(router.urls)),
]
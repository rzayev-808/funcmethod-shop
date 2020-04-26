from django.urls import path, include
from rest_framework import routers
from .views import *
router = routers.DefaultRouter()
router.register(r'product', ProductsApiViews)

urlpatterns = [
    
    path('api/v1/', include(router.urls)),
]
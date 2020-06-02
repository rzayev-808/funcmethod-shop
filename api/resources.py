from import_export import resources
from .models import *

class ProductResource(resources.ModelResource):
    class Meta:
        model = Product
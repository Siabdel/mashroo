backoffice/admin.py

from django.contrib import admin
from models import *

admin.site.register(Product)
admin.site.register(ProductItem)
admin.site.register(ProductAttribute)
admin.site.register(ProductAttributeValue)

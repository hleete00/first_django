from django.contrib import admin
from .models import Product

# Register a model here to allow the admin to add products in the admin view
admin.site.register(Product)
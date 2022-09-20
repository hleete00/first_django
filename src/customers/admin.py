from django.contrib import admin
from .models import Customer


# Adding this line allows the admin to add customers to the database from the admin site
admin.site.register(Customer)

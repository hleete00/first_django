from math import prod
from ssl import create_default_context
from tkinter import CASCADE
from turtle import ondrag
from django.db import models
from products.models import Product
from customers.models import Customer
from profiles.models import Profile
from django.utils import timezone
from django.shortcuts import reverse
from .utils import generate_code


# Create model to hold sale positions
class Position(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.FloatField(blank=True)
    created = models.DateTimeField(blank=True)

    # Create a string that can be displayed when this model is called.
    def __str__(self):
        return f"id: {self.id}, product: {self.product.name}, quantity: {self.quantity}"

    # On save, generate the total price of the position
    def save(self, *args, **kwargs):
        self.price = self.product.price * self.quantity
        return super().save(*args, **kwargs)

    # Get object of Sales that pertains to current position. Return the Id of the Sale.
    def get_sales_id(self):
        sale_obj = self.sale_set.first()
        return sale_obj.id
    
    def get_sales_customer(self):
        sale_obj = self.sale_set.first()
        return sale_obj.customer.name


# Create model to hold sale information
class Sale(models.Model):
    transaction_id = models.CharField(max_length=12, blank=True)
    position = models.ManyToManyField(Position)
    total_price = models.FloatField(blank=True, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    salesman = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created = models.DateTimeField(blank=True)
    updated = models.DateTimeField(auto_now=True)

    # Generate string that will be displayed when this model is called
    def __str__(self):
        return f"Sales for the amount of ${self.total_price}"

    # If no transaction Id, generate one.
    def save(self, *args, **kwargs):
        if self.transaction_id == "":
            self.transaction_id = generate_code()
        if self.created is None:
            self.created = timezone.now()
        return super().save(*args, **kwargs)

    # Get positions related to sale records
    def get_positions(self):
        return self.position.all()

    # Get the URL for specific sales when clicked on
    def get_absolute_url(self):
        return reverse('sales:detail', kwargs={'pk': self.pk})


class CSV(models.Model):
    file_name = models.CharField(max_length=120, null=True)
    csv_file = models.FileField(upload_to='csvs', null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.file_name)
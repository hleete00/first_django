from distutils.command.upload import upload
from email.policy import default
from django.db import models


# Create a model to hold the customer information in the database.
class Customer(models.Model):
    name = models.CharField(max_length=120)
    logo = models.ImageField(upload_to='customers', default='no_picture.png')

    def __str__(self):
        return str(self.name)
from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=120)
    price = models.DecimalField(decimal_places=2, max_digits=100000)
    description = models.TextField(blank=True)
    image = models.URLField()
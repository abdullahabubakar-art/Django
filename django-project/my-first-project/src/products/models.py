from django.db import models
from django.urls import reverse

# Create your models here.
# product class inheret main Model class


class Product(models.Model):

    title = models.CharField(max_length=120)  # max_length is required
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(decimal_places=2, max_digits=10000)
    # blank = False means field are required, null = False means database cann't contain null value
    summary = models.TextField(blank=False, null=False)
    featured = models.BooleanField(default=False)  # null= True, default= True

    # convention to grab the urls inside Django, so it's use in other place
    # if we ever change the url it will change everywhere
    # def get_absolute_url(self):
    #     return f"/products/{self.id}/"

    # Reverse the urls
    def get_absolute_url(self):
        return reverse("products:product-details", kwargs={"id": self.id})

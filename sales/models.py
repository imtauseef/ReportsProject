from django.db import models
from products.models import Product

# Create your models here.
class Position(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.FloatField(blank=True)
    created = models.DateTimeField(blank=True)

    def __str__(self):
        return f"id: {self.id}, product: {self.product.name}, quantity: {self.quantity}"


class Sale(models.Model):
    pass


class CSV(models.Model):
    pass

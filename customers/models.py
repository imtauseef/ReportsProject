from django.db import models

# Create your models here.
class Customer(models.Model):
    name = models.CharField(max_length=150)
    pic = models.ImageField(upload_to='customer', default='zama_aks.jpg')

    def __str__(self):
        return str(self.name)


from django.contrib.auth.models import User
from django.db import models

# profile model


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=12, blank=True, null=True)

    def __str__(self):
        return self.name

# product model


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-price']

# Cart model


class ProductCart(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    ordered = models.BooleanField(default=False)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.product.name} - {self.quantity}'


# create order model
class Order(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    phone = models.CharField(max_length=11)
    address = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    quantity = models.IntegerField()
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.product.name} - {self.quantity}'

from django.db import models

# Category
class Category(models.Model):
    category_name = models.CharField(max_length=100)

    def __str__(self):
        return self.category_name


# Unit
class Unit(models.Model):
    unit_name = models.CharField(max_length=100)
    abbreviation = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return f"{self.unit_name} ({self.abbreviation})"


# Product
class Product(models.Model):
    product_name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    unit = models.ForeignKey(Unit, on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return self.product_name


# Inventory
class Inventory(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.product.product_name} - {self.quantity}"


# Stock Transaction
class StockTransaction(models.Model):
    TRANSACTION_TYPE = (
        ('IN', 'Stock In'),
        ('OUT', 'Stock Out'),
    )

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=3, choices=TRANSACTION_TYPE)
    quantity = models.IntegerField()
    transaction_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.product_name} - {self.transaction_type}"

from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=StockTransaction)
def update_inventory(sender, instance, created, **kwargs):
    if created:
        inventory, _ = Inventory.objects.get_or_create(product=instance.product)

        if instance.transaction_type == 'IN':
            inventory.quantity += instance.quantity
        else:
            inventory.quantity -= instance.quantity

        inventory.save()
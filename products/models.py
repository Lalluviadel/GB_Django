from django.db import models


class ProductCategory(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField(blank=True)
    discount = models.PositiveIntegerField(default=0)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=256)
    image = models.ImageField(upload_to='product_images', blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    available = models.BooleanField(default=True, db_index=True)

    # available = models.BooleanField(default=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f'{self.name} | {self.category}'

from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=20, unique=True)
    def __str__(self):
        return self.name

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Category'
        verbose_name_plural = 'Category'
class Company(models.Model):
    name = models.CharField(max_length=20, unique=True)
    def __str__(self):
        return self.name

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'company'
        verbose_name_plural = 'company'
class Color(models.Model):
    name = models.CharField(max_length=30, unique=True)
    def __str__(self):
        return self.name

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Color'
        verbose_name_plural = 'Color'
class Product(models.Model):
    name = models.CharField(max_length=80, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    image_url = models.ImageField(null=True , blank=True , upload_to="images")
    def __str__(self):
        return self.name

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Product'
        verbose_name_plural = 'Product'

class ProductColor(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    def __str__(self):
        return f"product {self.product} color {self.color}"

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'product-c'
        verbose_name_plural = 'product-c'

class ProductStock(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    color = models.ForeignKey(ProductColor, on_delete=models.CASCADE)
    size = models.IntegerField()
    quantity = models.IntegerField()
    def __str__(self):
        return f"prduct {self.product} - color {self.color} - size {self.size} - quantity {self.quantity}"

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'PStock'
        verbose_name_plural = 'Pstock'

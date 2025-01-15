from django.db import models
from user.models import User as MyUser

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)
    image = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    rate = models.FloatField()
    comment_count = models.IntegerField()
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    price = models.IntegerField()
    final_price = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    is_banner = models.BooleanField(default=False)
    date = models.DateField(auto_now=True)
    date_modified = models.DateField(auto_now=True)

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    banner = models.CharField(max_length=200, null=True)
    image = models.CharField(max_length=200, null=True)
    image2 = models.CharField(max_length=200, null=True)
    image3 = models.CharField(max_length=200, null=True)
    image4 = models.CharField(max_length=200, null=True)
    image5 = models.CharField(max_length=200, null=True)
    image6 = models.CharField(max_length=200, null=True)
    image7 = models.CharField(max_length=200, null=True)
    video = models.CharField(max_length=200, null=True)

class ProductComment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    comment = models.TextField()
    date = models.DateField(auto_now=True)
    rate = models.PositiveIntegerField(default=5)









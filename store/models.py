from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    creator = models.CharField(max_length=50)
    price = models.PositiveIntegerField()
    image = models.ImageField(upload_to='products/')
    likes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name
    
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'product')  # 같은 유저가 같은 상품 여러번 찜 못하게

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"
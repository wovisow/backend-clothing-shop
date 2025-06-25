from django.db import models
from django.contrib.auth.models import AbstractUser

class UserCustom(AbstractUser):
    fio = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['fio', 'username']


class Category(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='category_images/', blank=True, null=True)

    def __str__(self):
        return self.name


class Color(models.Model):
    name = models.CharField(max_length=30)
    hex_code = models.CharField(max_length=7, blank=True, null=True)  # Пример: "#FFFFFF"

    def __str__(self):
        return self.name


class Size(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    price = models.IntegerField(default=0)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    is_new_collection = models.BooleanField(default=False, verbose_name='Новая коллекция')
    color = models.ForeignKey(Color, on_delete=models.SET_NULL, null=True, blank=True)
    size = models.ForeignKey(Size, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

class Cart(models.Model):
    products = models.ManyToManyField(Product)
    user = models.ForeignKey(UserCustom, on_delete=models.CASCADE)


class Order(models.Model):
    products = models.ManyToManyField(Product)
    user = models.ForeignKey(UserCustom, on_delete=models.CASCADE)
    order_price = models.IntegerField(default=0)
    DELIVERY_METHOD_CHOICES = [
        ('courier', 'Курьерская доставка'),
        ('pickup', 'Самовывоз'),
    ]
    delivery_method = models.CharField(
        max_length=20,
        choices=DELIVERY_METHOD_CHOICES,
        default='courier'
    )
    delivery_address = models.CharField(max_length=255, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"Заказ #{self.id} от {self.user.email}"

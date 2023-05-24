from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


CATEGORY_CHOICES = (
    ('P', 'Phones'),
    ('T', 'Tablets'),
    ('C', 'Computers'),
    ('M', 'Monitors')
)

class Item(models.Model):
    title = models.CharField(max_length=255)
    price = models.FloatField()
    category = models.CharField(max_length=2, choices=CATEGORY_CHOICES)
    image = models.URLField(blank='True', null=True)
    description = models.CharField(max_length=255)
    slug = models.SlugField(blank=True, unique=True)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.item.title}"

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    shipping_date = models.DateTimeField(blank=True, null=True)
    ordered = models.BooleanField(default=False)
    address = models.ForeignKey("Address", related_name='shipping_address', on_delete=models.SET_NULL, null=True, blank=True)
    payment = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}'s Order"

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    country = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.user.username}'s Address"

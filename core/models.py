from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return self.user.username

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  # Linked to Category
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='products/')
    color_image1 = models.ImageField(upload_to='products/', blank=True)
    color_image2 = models.ImageField(upload_to='products/', blank=True)
    
    # Stock for different combinations of RAM and Storage
    stock_4gb_128gb = models.PositiveIntegerField(default=0)
    stock_4gb_256gb = models.PositiveIntegerField(default=0)
    stock_4gb_512gb = models.PositiveIntegerField(default=0)
    stock_4gb_1tb = models.PositiveIntegerField(default=0)
    stock_8gb_128gb = models.PositiveIntegerField(default=0)
    stock_8gb_256gb = models.PositiveIntegerField(default=0)
    stock_8gb_512gb = models.PositiveIntegerField(default=0)
    stock_8gb_1tb = models.PositiveIntegerField(default=0)

    is_featured = models.BooleanField(default=False)  # Optional field for featured products

    # Adding RAM and Storage options
    ram = models.CharField(max_length=20, choices=[('4GB', '4GB'), ('8GB', '8GB')], default='4GB')
    storage = models.CharField(max_length=20, choices=[('128GB', '128GB'), 
                                                      ('256GB', '256GB'), 
                                                      ('512GB', '512GB'), 
                                                      ('1TB', '1TB')], 
                               default='128GB')

    def __str__(self):
        return self.name

    def get_stock(self):
        if self.ram == '4GB' and self.storage == '128GB':
            return self.stock_4gb_128gb
        elif self.ram == '4GB' and self.storage == '256GB':
            return self.stock_4gb_256gb
        elif self.ram == '4GB' and self.storage == '512GB':
            return self.stock_4gb_512gb
        elif self.ram == '4GB' and self.storage == '1TB':
            return self.stock_4gb_1tb
        elif self.ram == '8GB' and self.storage == '128GB':
            return self.stock_8gb_128gb
        elif self.ram == '8GB' and self.storage == '256GB':
            return self.stock_8gb_256gb
        elif self.ram == '8GB' and self.storage == '512GB':
            return self.stock_8gb_512gb
        elif self.ram == '8GB' and self.storage == '1TB':
            return self.stock_8gb_1tb
        else:
            return 0  # Default to 0 if no match

class Order(models.Model):
    PAYMENT_CHOICES = [
        ('COD', 'Cash on Delivery'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_mode = models.CharField(max_length=10, choices=PAYMENT_CHOICES, default='COD')  # Cash on Delivery

    @property
    def get_total(self):
        total = sum(item.quantity * item.price for item in self.items.all())
        return total

    def __str__(self):
        return f"Order #{self.id} - {self.payment_mode}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    ram = models.CharField(max_length=10, default='4GB')  # Default value set to '4GB'
    storage = models.CharField(max_length=10, default='128GB')  # Default value set to '128GB'

    def __str__(self):
        return f"{self.product.name} ({self.ram}, {self.storage})"



class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=20)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.user.username

def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    instance.userprofile.save()

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def total_price(self):
        total = sum(item.total_price for item in self.items.all())
        return total

    @property
    def total_items(self):
        return sum(item.quantity for item in self.items.all())

class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ram = models.CharField(max_length=10, default='4GB')
    storage = models.CharField(max_length=10, default='128GB')
    color = models.URLField(default='/static/assets/default_color_image.jpg')  # Default color image URL
    cart = models.ForeignKey(Cart, related_name="items", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.product.name} ({self.ram}, {self.storage}, {self.color})"

    @property
    def total_price(self):
        return self.product.price * self.quantity

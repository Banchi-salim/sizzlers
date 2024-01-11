from django.db import models
from django.contrib.auth.models import User

class MenuItem(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='menu_images/')

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    contact_number = models.CharField(max_length=15)
    address = models.TextField()

    def __str__(self):
        return self.user.username

class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Preparing', 'Preparing'),
        ('Delivering', 'Delivering'),
        ('Completed', 'Completed'),
    ]

    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    items = models.ManyToManyField(MenuItem, through='OrderItem')
    order_date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    delivery_address = models.TextField()

    def __str__(self):
        return f"Order #{self.id} by {self.user.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} x {self.menu_item.name}"

class Payment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment for Order #{self.order.id}"

class Notification(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.user.username} - {self.message}"

class CustomerFeedback(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    feedback_text = models.TextField()
    rating = models.PositiveIntegerField()

    def __str__(self):
        return f"Feedback from {self.user.user.username}"
from django.db import models

# Create your models here.

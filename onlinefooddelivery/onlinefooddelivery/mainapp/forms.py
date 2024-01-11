# forms.py

from django import forms
from django.contrib.auth.forms import AuthenticationForm

from .models import UserProfile, MenuItem, Order, Payment, Notification, CustomerFeedback, OrderItem

class LoginForm(AuthenticationForm):
    pass
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['contact_number', 'address']

class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ['name', 'description', 'price', 'image']

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['user', 'items', 'total_price', 'status', 'delivery_address']

class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['order', 'menu_item', 'quantity']

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['order', 'amount_paid']

class NotificationForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ['user', 'message']

class CustomerFeedbackForm(forms.ModelForm):
    class Meta:
        model = CustomerFeedback
        fields = ['user', 'feedback_text', 'rating']

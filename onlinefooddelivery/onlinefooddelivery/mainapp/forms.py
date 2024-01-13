# forms.py

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import UserProfile, MenuItem, Order, Payment, Notification, CustomerFeedback, OrderItem, Staff, \
    FoodItemAvailability


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

class FoodItemAvailabilityForm(forms.ModelForm):
    menu_item = forms.ModelChoiceField(queryset=MenuItem.objects.all(),
                                       widget=forms.Select(attrs={'class': 'custom-class-for-menu-item-field'}))

    class Meta:
        model = FoodItemAvailability
        fields = ['menu_item', 'availability']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # You can customize the choices or add additional attributes if needed
        self.fields['availability'].widget.attrs['class'] = 'custom-class-for-availability-field'

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


class StaffProfileForm(UserCreationForm):
    date_added = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))

    class Meta:
        model = Staff
        fields = ['username', 'password1', 'password2', 'date_added', 'position']

    def __init__(self, *args, **kwargs):
        super(StaffProfileForm, self).__init__(*args, **kwargs)
        # Customize labels, widgets, or add more fields if neededz
# forms.py

from django import forms
from .models import MenuItem

class OrderForm(forms.Form):
    food = forms.ModelChoiceField(queryset=MenuItem.objects.all(), empty_label="Select food")
    drink = forms.ModelChoiceField(queryset=MenuItem.objects.all(), empty_label="Select drink")
    quantity = forms.IntegerField(min_value=1, widget=forms.NumberInput(attrs={'required': True}))
    location = forms.CharField(widget=forms.TextInput(attrs={'required': True}))
    chicken = forms.BooleanField(required=False)
    Extra_Meat = forms.BooleanField(required=False)
    Egg = forms.BooleanField(required=False)
    coslow = forms.BooleanField(required=False)
    plantain = forms.BooleanField(required=False)
    Sauce = forms.BooleanField(required=False)
    contact = forms.CharField(widget=forms.TextInput(attrs={'required': True}))

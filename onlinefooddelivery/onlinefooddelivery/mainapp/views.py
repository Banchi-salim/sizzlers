# views.py
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import UserProfile, MenuItem, Order, Payment, Notification, CustomerFeedback, Staff
from .forms import UserProfileForm, MenuItemForm, OrderForm, PaymentForm, NotificationForm, CustomerFeedbackForm, \
    LoginForm, StaffProfileForm, FoodItemAvailabilityForm
import requests


# Decorator to ensure the user is logged in to access certain views
@login_required
def login_required_view(view_func):
    return login_required(view_func)


@method_decorator(login_required, name='dispatch')
class UserProfileView(View):
    def get(self, request):
        user_profile = UserProfile.objects.get(user=request.user)
        form = UserProfileForm(instance=user_profile)
        return render(request, 'user_profile.html', {'form': form})

    def post(self, request):
        user_profile = UserProfile.objects.get(user=request.user)
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
        return render(request, 'user_profile.html', {'form': form})


@method_decorator(login_required, name='dispatch')
class AdminView(View):
    def get(self, request):
        staff_list = Staff.objects.all()
        form = StaffProfileForm()
        return render(request, 'mainapp/adminhome.html', context={'form': form, "staff_list":staff_list})

    def post(self, request):
        form = StaffProfileForm()
        if form.is_valid():
            form.save()
            return redirect('menu')
        staff_list = Staff.objects.all()
        return render(request, 'mainapp/adminhome.html', context={'form': form, "staff_list":staff_list})


@method_decorator(login_required, name='dispatch')
class ManageMenuView(View):

    def get(self, request, form1=None):
        menu_items = MenuItem.objects.all()
        form1 = MenuItemForm()
        form2 = FoodItemAvailabilityForm()
        return render(request, 'mainapp/managemenu.html', {'form1': form1, 'form2':form2 })

    def post(self, request):
        form1 = MenuItemForm()
        form2 = FoodItemAvailabilityForm()
        if form1.is_valid():
            form1.save()
            return redirect('menu')

        if form2.is_valid():
            form2.save()
            return redirect('menu')

        # menu_items = MenuItem.objects.all()
        return render(request, 'mainapp/managemenu.html', {'form1': form1, 'form2':form2})


class MenuView(View):
    def get(self, request):
        menu_items = MenuItem.objects.all()
        return render(request, 'menu.html', {'menu_items': menu_items})


@method_decorator(login_required, name='dispatch')
class OrderView(View):

    def get(self, request):
        menu_items = MenuItem.objects.all()
        form = OrderForm()
        return render(request, 'order.html', {'menu_items': menu_items, 'form': form})

    def post(self, request):
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = UserProfile.objects.get(user=request.user)
            order.save()
            form.save_m2m()
            messages.success(request, 'Order placed successfully.')
            return redirect('order_confirmation', order_id=order.id)
        return render(request, 'order.html', {'form': form})


@method_decorator(login_required, name='dispatch')
class OrderConfirmationView(View):

    def get(self, request, order_id):
        order = Order.objects.get(id=order_id)
        return render(request, 'order_confirmation.html', {'order': order})


@method_decorator(login_required, name='dispatch')
class PaymentView(View):

    def get(self, request, order_id):
        order = Order.objects.get(id=order_id)
        form = PaymentForm()
        return render(request, 'payment.html', {'order': order, 'form': form})

    def post(self, request, order_id):
        order = Order.objects.get(id=order_id)
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.order = order
            payment.save()

            # Process payment with Monify API (replace 'YOUR_MONIFY_API_KEY' with your actual Monify API key)
            monify_api_key = 'MK_TEST_QKQ4WUYXQ8'
            monify_payment_url = 'https://api.monify.io/v1/transactions'
            headers = {'Authorization': f'Bearer {monify_api_key}'}
            data = {
                'amount': str(order.total_price),
                'currency': 'NGN',
                'description': f'Payment for Order #{order.id}',
                'payment_type': 'card',
            }

            response = requests.post(monify_payment_url, json=data, headers=headers)

            if response.status_code == 200:
                messages.success(request, 'Payment successful.')
                order.status = 'Completed'
                order.save()
            else:
                messages.error(request, 'Payment failed. Please try again.')

            return redirect('order_confirmation', order_id=order.id)
        return render(request, 'payment.html', {'order': order, 'form': form})


@method_decorator(login_required, name='dispatch')
class NotificationView(View):

    def get(self, request):
        notifications = Notification.objects.filter(user=request.user.userprofile)
        return render(request, 'notifications.html', {'notifications': notifications})


@method_decorator(login_required, name='dispatch')
class FeedbackView(View):

    def get(self, request):
        form = CustomerFeedbackForm()
        return render(request, 'feedback.html', {'form': form})

    def post(self, request):
        form = CustomerFeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = UserProfile.objects.get(user=request.user)
            feedback.save()
            messages.success(request, 'Feedback submitted. Thank you!')
        return render(request, 'feedback.html', {'form': form})


class SignUpView(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, 'signup.html', {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully. You are now logged in.')
            return redirect('homepage')
        return render(request, 'signup.html', {'form': form})


class LoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'mainapp/login.html', {'form': form})

    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'Login successful.')
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password.')
        return render(request, 'mainapp/login.html', {'form': form})


class HomePageView(View):
    def get(self, request):
        form = OrderForm()
        return render(request, 'mainapp/homepage.html', {'form': form})

    def post(self, request):
        form = OrderForm(request.post)
        if request.method == 'POST' and form.is_valid():
            order = form.save(commit=False)
            order.user = UserProfile.objects.get(user=request.user)
            order.save()
            form.save_m2m()
            messages.success(request, 'Order placed successfully.')
            return redirect('order_confirmation', order_id=order.id)
            # return redirect('success_page')
        return render(request, 'mainapp/homepage.html', {'form': form})

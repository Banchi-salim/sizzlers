# urls.py

from django.urls import path
from .views import UserProfileView, MenuView, OrderView, OrderConfirmationView, PaymentView, NotificationView, \
    FeedbackView, LoginView, HomePageView

urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('homepage/', HomePageView.as_view(), name='home'),
    path('profile/', UserProfileView.as_view(), name='user_profile'),
    path('menu/', MenuView.as_view(), name='menu'),
    path('order/', OrderView.as_view(), name='order'),
    path('order/<int:order_id>/confirmation/', OrderConfirmationView.as_view(), name='order_confirmation'),
    path('order/<int:order_id>/payment/', PaymentView.as_view(), name='payment'),
    path('notifications/', NotificationView.as_view(), name='notifications'),
    path('feedback/', FeedbackView.as_view(), name='feedback'),
    # Add other URL patterns as needed
]

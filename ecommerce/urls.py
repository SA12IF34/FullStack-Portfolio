from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('cart/', CartsAPI.as_view()),
    path('cart/<str:name>/', CartAPI.as_view()),
    path('checkout/', CheckoutAPI.as_view()), 
    path('boughts/', BoughtsAPI.as_view()),
    path('boughts/<str:name>/', BoughtAPI.as_view()),
    path('register/', UserAPI.as_view()),
    path('token/', MyTokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view())
] 
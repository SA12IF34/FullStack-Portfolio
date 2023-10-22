from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('token/', MyTokenObtainPairView.as_view()), # login api
    path('token/refresh/', TokenRefreshView.as_view()), # token refresh api
    path('signup/', SignUpAPI.as_view()),
    path('perfume/', PerfumeAPI.as_view()),
    path('search/', SearchAPI.as_view()),
    path('cart/', CartAPI.as_view()),
    path('cart/<str:name>/delete/', CartAPI.as_view()),
    path('boughts/', BoughtsAPI.as_view()),
    path('checkout/', CheckoutAPI.as_view())
]
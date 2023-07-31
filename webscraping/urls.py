from django.urls import path
from .views import *

urlpatterns = [
    path('', home), # Page Route
    path('books/trending/', trending), # API Route
    path('subjects/', subjects), # API Route
    path('subjects/<str:subject>/', subject_page), # Page Route
    path('subject-<str:pk>/', subject), # API Route
]
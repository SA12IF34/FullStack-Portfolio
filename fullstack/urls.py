from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from .views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home),
    path('projects/web-scraping/', include('webscraping.urls')),
    path('projects/ecommerce/', include('ecommerce.urls')),
    path('projects/social_media/', include('social_media.urls'))
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 

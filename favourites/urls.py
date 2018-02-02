from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('zoo/', include('favourites.zoo.urls')),
    path('admin/', admin.site.urls),
]

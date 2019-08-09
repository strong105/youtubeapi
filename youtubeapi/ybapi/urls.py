from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('ybsearch.urls')),
    path('searchresult/', include('ybsearch.urls')),
]
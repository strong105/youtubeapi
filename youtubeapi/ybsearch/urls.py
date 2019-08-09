from django.urls import path
from . import views

urlpatterns = [
    path('', views.search_view),
    path('login/', views.authenticate_view),
    path('logout/', views.logout_view),
]

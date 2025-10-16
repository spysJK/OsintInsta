from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),   # login será a página inicial
    path('home/', views.home, name='home'),
         # home será acessada depois do login
]

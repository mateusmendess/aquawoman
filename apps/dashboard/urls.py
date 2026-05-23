from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('painel/', views.dashboard_home, name='home'),
]
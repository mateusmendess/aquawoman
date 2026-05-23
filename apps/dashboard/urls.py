from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('painel/', views.dashboard_home, name='home'),
    path('painel/pedido/<int:pedido_id>/status/', views.atualizar_status, name='atualizar_status'),
]
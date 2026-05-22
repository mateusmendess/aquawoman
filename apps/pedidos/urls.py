from django.urls import path
from . import views

app_name = 'pedidos'

urlpatterns = [
    path('carrinho/', views.carrinho_detalhe, name='carrinho'),
    path('carrinho/adicionar/<int:produto_id>/', views.carrinho_adicionar, name='carrinho_adicionar'),
    path('carrinho/remover/<int:produto_id>/', views.carrinho_remover, name='carrinho_remover'),
    path('carrinho/atualizar/<int:produto_id>/', views.carrinho_atualizar, name='carrinho_atualizar'),
]
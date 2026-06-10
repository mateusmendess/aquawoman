from django.urls import path
from . import views

app_name = 'pedidos'

urlpatterns = [
    path('carrinho/', views.carrinho_detalhe, name='carrinho'),
    path('carrinho/adicionar/<int:produto_id>/', views.carrinho_adicionar, name='carrinho_adicionar'),
    path('carrinho/remover/<int:produto_id>/', views.carrinho_remover, name='carrinho_remover'),
    path('carrinho/atualizar/<int:produto_id>/', views.carrinho_atualizar, name='carrinho_atualizar'),
    path('checkout/', views.checkout, name='checkout'),
    path('confirmacao/<int:pedido_id>/', views.confirmacao, name='confirmacao'),
    path('meus-pedidos/', views.meus_pedidos, name='meus_pedidos'),
    path('status/<int:pedido_id>/', views.pedido_status, name='pedido_status'),
    path('geocodificar/', views.geocodificar, name='geocodificar'),
]
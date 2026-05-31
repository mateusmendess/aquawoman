from django.urls import path
from . import views

app_name = 'pagamentos'

urlpatterns = [
    path('pagamento/criar/<int:pedido_id>/', views.criar_preferencia, name='criar'),
    path('pagamento/sucesso/<int:pedido_id>/', views.pagamento_sucesso, name='sucesso'),
    path('pagamento/falha/<int:pedido_id>/', views.pagamento_falha, name='falha'),
    path('pagamento/pendente/<int:pedido_id>/', views.pagamento_pendente, name='pendente'),
    path('pagamento/webhook/', views.webhook, name='webhook'),
]
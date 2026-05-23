from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from apps.pedidos.models import Pedido
from apps.produtos.models import Produto
from django.utils import timezone
from django.db.models import Sum

@staff_member_required
def dashboard_home(request):
    hoje = timezone.now().date()

    pedidos_hoje = Pedido.objects.filter(criado_em__date=hoje)
    pedidos_recentes = Pedido.objects.all()[:10]
    total_hoje = pedidos_hoje.aggregate(total=Sum('total'))['total'] or 0
    estoque_baixo = Produto.objects.filter(estoque__lte=10, ativo=True)
    total_pedidos = Pedido.objects.count()

    context = {
        'pedidos_hoje': pedidos_hoje,
        'pedidos_recentes': pedidos_recentes,
        'total_hoje': total_hoje,
        'estoque_baixo': estoque_baixo,
        'total_pedidos': total_pedidos,
        'quantidade_hoje': pedidos_hoje.count(),
    }
    return render(request, 'dashboard/home.html', context)
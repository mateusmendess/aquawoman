from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from apps.pedidos.models import Pedido
from apps.produtos.models import Produto
from django.utils import timezone
from django.db.models import Sum

@staff_member_required
def dashboard_home(request):
    hoje = timezone.now().date()

    pedidos_hoje = Pedido.objects.filter(criado_em__date=hoje, status='entregue')
    quantidade_hoje = Pedido.objects.filter(criado_em__date=hoje).count()
    pedidos_recentes = Pedido.objects.all().order_by('-criado_em')[:10]
    total_hoje = pedidos_hoje.aggregate(total=Sum('total'))['total'] or 0
    estoque_baixo = Produto.objects.filter(estoque__lte=10, ativo=True)

    context = {
        'pedidos_hoje': pedidos_hoje,
        'pedidos_recentes': pedidos_recentes,
        'total_hoje': total_hoje,
        'estoque_baixo': estoque_baixo,
        'total_pedidos': Pedido.objects.count(),
        'quantidade_hoje': quantidade_hoje,
    }
    return render(request, 'dashboard/home.html', context)

@staff_member_required
def atualizar_status(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    novo_status = request.POST.get('status')
    if novo_status in dict(Pedido.STATUS_CHOICES):
        status_anterior = pedido.status
        pedido.status = novo_status
        pedido.save()

        if novo_status == 'entregue' and status_anterior != 'entregue':
            for item in pedido.itens.all():
                produto = item.produto
                produto.estoque = max(0, produto.estoque - item.quantidade)
                produto.save()

    return redirect('dashboard:home')
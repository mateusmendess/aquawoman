from django.shortcuts import render, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from apps.pedidos.models import Pedido
from apps.produtos.models import Produto
from django.utils import timezone
from django.db.models import Sum

@staff_member_required
def dashboard_home(request):
    hoje = timezone.now().date()

    pedidos_hoje = Pedido.objects.filter(criado_em__date=hoje, status='entregue')
    quantidade_hoje = Pedido.objects.filter(criado_em__date=hoje).count()
    pedidos_recentes = Pedido.objects.all()[:10]
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
        pedido.status = novo_status
        pedido.save()

    cores = {
        'pendente': 'bg-yellow-50 text-yellow-700',
        'confirmado': 'bg-blue-50 text-blue-700',
        'em_entrega': 'bg-purple-50 text-purple-700',
        'entregue': 'bg-green-50 text-green-700',
        'cancelado': 'bg-red-50 text-red-700',
    }
    cor = cores.get(pedido.status, '')

    opcoes = ''
    for valor, label in Pedido.STATUS_CHOICES:
        selected = 'selected' if pedido.status == valor else ''
        opcoes += f'<option value="{valor}" {selected}>{label}</option>'

    csrf = request.META.get('CSRF_COOKIE', '')

    return HttpResponse(f'''
        <select
          hx-post="/painel/pedido/{pedido.id}/status/"
          hx-target="this"
          hx-swap="outerHTML"
          hx-headers='{{"X-CSRFToken": "{csrf}"}}'
          name="status"
          class="text-xs border border-gray-200 rounded-lg px-2 py-1 cursor-pointer {cor}">
          {opcoes}
        </select>
    ''')
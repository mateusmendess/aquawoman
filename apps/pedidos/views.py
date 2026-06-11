from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib import messages
from apps.produtos.models import Produto
from .carrinho import Carrinho
from .models import Pedido, ItemPedido
from django.conf import settings
from apps.clientes.models import Cliente
from django.http import JsonResponse
import urllib.request
import urllib.parse
import json
import threading
import resend

def login_cliente_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.session.get('cliente_id'):
            request.session['next'] = request.path
            return redirect('clientes:login')
        return view_func(request, *args, **kwargs)
    return wrapper

@login_cliente_required
def carrinho_detalhe(request):
    carrinho = Carrinho(request)
    context = {
        'carrinho': carrinho,
        'total': carrinho.total(),
        'quantidade_total': len(carrinho),
    }
    return render(request, 'pedidos/carrinho.html', context)

def carrinho_adicionar(request, produto_id):
    carrinho = Carrinho(request)
    produto = get_object_or_404(Produto, id=produto_id)
    carrinho.adicionar(produto)
    return HttpResponse(f'''
        <span id="carrinho-contador"
              class="absolute -top-2 -right-2 bg-white text-[#1A3FAA] text-xs font-bold w-5 h-5 rounded-full flex items-center justify-center">
            {len(carrinho)}
        </span>
    ''')

def carrinho_remover(request, produto_id):
    carrinho = Carrinho(request)
    produto = get_object_or_404(Produto, id=produto_id)
    carrinho.remover(produto)
    return render(request, 'pedidos/partials/itens_carrinho.html', {
        'carrinho': carrinho,
        'total': carrinho.total(),
    })

def carrinho_atualizar(request, produto_id):
    carrinho = Carrinho(request)
    produto = get_object_or_404(Produto, id=produto_id)
    quantidade = int(request.POST.get('quantidade', 1))
    if quantidade > 0:
        carrinho.carrinho[str(produto_id)]['quantidade'] = quantidade
        carrinho.salvar()
    else:
        carrinho.remover(produto)
    return render(request, 'pedidos/partials/itens_carrinho.html', {
        'carrinho': carrinho,
        'total': carrinho.total(),
    })

def enviar_email_pedido(pedido):
    itens_texto = ''
    for item in pedido.itens.all():
        itens_texto += f'<li>{item.produto.nome} x{item.quantidade} — R$ {item.subtotal():.2f}</li>'

    recebimento = pedido.get_forma_recebimento_display()
    pagamento = pedido.get_forma_pagamento_display()

    html = f'''
    <h2>🛒 Novo pedido #{pedido.id} — Aquawoman</h2>
    <p><strong>Cliente:</strong> {pedido.nome}</p>
    <p><strong>Telefone:</strong> {pedido.telefone}</p>
    <p><strong>Recebimento:</strong> {recebimento}</p>
    <p><strong>Endereço:</strong> {pedido.endereco}</p>
    <p><strong>Pagamento:</strong> {pagamento}</p>
    <h3>Produtos:</h3>
    <ul>{itens_texto}</ul>
    <p><strong>Total: R$ {pedido.total:.2f}</strong></p>
    <br>
    <a href="https://aquawoman.up.railway.app/painel/">Acessar o painel</a>
    '''

    def enviar():
        try:
            resend.api_key = settings.RESEND_API_KEY
            resend.Emails.send({
                "from": "Aquawoman <onboarding@resend.dev>",
                "to": [settings.EMAIL_DESTINATARIO],
                "subject": f"🛒 Novo pedido #{pedido.id} — Aquawoman",
                "html": html,
            })
        except Exception as e:
            print(f"Erro ao enviar email: {e}")

    thread = threading.Thread(target=enviar)
    thread.daemon = True
    thread.start()

@login_cliente_required
def checkout(request):
    carrinho = Carrinho(request)

    if len(carrinho) == 0:
        messages.error(request, 'Seu carrinho está vazio!')
        return redirect('produtos:lista')
    
    cliente = Cliente.objects.get(id=request.session['cliente_id'])

    if request.method == 'POST':
        nome = request.POST.get('nome')
        telefone = request.POST.get('telefone')
        endereco = request.POST.get('endereco', 'Retirada na loja')
        pagamento = request.POST.get('pagamento')
        tipo_entrega = request.POST.get('tipo_entrega', 'entrega')

        forma_recebimento = tipo_entrega  # 'entrega' ou 'retirada'

        if pagamento == 'online':
            # Identifica se é pix ou cartão online
            forma_pagamento_selecionada = request.POST.get('forma_pagamento_tipo', 'pix')
            if forma_pagamento_selecionada == 'cartao':
                forma_pagamento = 'cartao_online'
            else:
                forma_pagamento = 'pix_online'
        else:
            forma_pagamento = request.POST.get('forma_pagamento_tipo', 'dinheiro')

        pedido = Pedido.objects.create(
            nome=nome,
            telefone=telefone,
            endereco=endereco,
            forma_recebimento=forma_recebimento,
            forma_pagamento=forma_pagamento,
            total=carrinho.total(),
            cliente_id=request.session.get('cliente_id'),
            latitude=cliente.latitude,
            longitude=cliente.longitude,
        )

        for item in carrinho:
            ItemPedido.objects.create(
                pedido=pedido,
                produto=item['produto'],
                quantidade=item['quantidade'],
                preco_unitario=item['preco'],
            )

        carrinho.limpar()

        if pagamento == 'online':
            return redirect(f'/pagamento/criar/{pedido.id}/')

        # Só envia email para pagamento na entrega/retirada
        enviar_email_pedido(pedido)
        messages.success(request, f'Pedido #{pedido.id} realizado com sucesso!')
        return redirect('pedidos:confirmacao', pedido_id=pedido.id)
    
    context = {
        'carrinho': carrinho,
        'total': carrinho.total(),
        'cliente': cliente,
        'cliente_lat': str(cliente.latitude).replace(',', '.') if cliente.latitude else '-6.066532',
        'cliente_lng': str(cliente.longitude).replace(',', '.') if cliente.longitude else '-49.866094',
    }

    return render(request, 'pedidos/checkout.html', context)

def confirmacao(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    return render(request, 'pedidos/confirmacao.html', {'pedido': pedido})

def get_progress_steps(status):
    ordem = ['pendente', 'confirmado', 'em_entrega', 'entregue']
    icones = {
        'pendente': 'clock',
        'confirmado': 'check',
        'em_entrega': 'truck',
        'entregue': 'home',
    }
    labels = {
        'pendente': 'Pendente',
        'confirmado': 'Confirmado',
        'em_entrega': 'Em entrega',
        'entregue': 'Entregue',
    }
    try:
        idx_atual = ordem.index(status)
    except ValueError:
        idx_atual = -1

    steps = []
    for i, step in enumerate(ordem):
        steps.append({
            'label': labels[step],
            'icon': icones[step],
            'done': i < idx_atual,
            'active': i == idx_atual,
        })
    return steps


@login_cliente_required
def meus_pedidos(request):
    cliente_id = request.session.get('cliente_id')
    pedidos = Pedido.objects.filter(cliente_id=cliente_id).order_by('-criado_em')
    pedidos_com_steps = [
        {'pedido': p, 'progress_steps': get_progress_steps(p.status)}
        for p in pedidos
    ]
    return render(request, 'pedidos/meus_pedidos.html', {
        'pedidos_com_steps': pedidos_com_steps,
    })


def pedido_status(request, pedido_id):
    cliente_id = request.session.get('cliente_id')
    pedido = get_object_or_404(Pedido, id=pedido_id, cliente_id=cliente_id)
    return render(request, 'pedidos/partials/pedido_card.html', {
        'pedido': pedido,
        'progress_steps': get_progress_steps(pedido.status),
    })

def geocodificar(request):
    q = request.GET.get('q', '')
    url = 'https://nominatim.openstreetmap.org/search?format=json&q=' + urllib.parse.quote(q) + '&limit=1'
    req = urllib.request.Request(url, headers={'User-Agent': 'Aquawoman/1.0'})
    with urllib.request.urlopen(req) as r:
        data = json.loads(r.read())
    return JsonResponse(data, safe=False)
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib import messages
from apps.produtos.models import Produto
from .carrinho import Carrinho
from .models import Pedido, ItemPedido
from django.core.mail import send_mail
from django.conf import settings

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
    import threading
    import resend

    itens_texto = ''
    for item in pedido.itens.all():
        itens_texto += f'<li>{item.produto.nome} x{item.quantidade} — R$ {item.subtotal()}</li>'

    html = f'''
    <h2>🛒 Novo pedido #{pedido.id} — Aquawoman</h2>
    <p><strong>Cliente:</strong> {pedido.nome}</p>
    <p><strong>Telefone:</strong> {pedido.telefone}</p>
    <p><strong>Endereço:</strong> {pedido.endereco}</p>
    <p><strong>Pagamento:</strong> {pedido.get_forma_pagamento_display()}</p>
    <h3>Produtos:</h3>
    <ul>{itens_texto}</ul>
    <p><strong>Total: R$ {pedido.total}</strong></p>
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

def checkout(request):
    carrinho = Carrinho(request)

    if len(carrinho) == 0:
        messages.error(request, 'Seu carrinho está vazio!')
        return redirect('produtos:lista')

    if request.method == 'POST':
        nome = request.POST.get('nome')
        telefone = request.POST.get('telefone')
        endereco = request.POST.get('endereco', 'Retirada na loja')
        pagamento = request.POST.get('pagamento')
        tipo_entrega = request.POST.get('tipo_entrega', 'entrega')

        if tipo_entrega == 'retirada':
            forma_pagamento = 'retirada'
        elif pagamento == 'online':
            forma_pagamento = 'pix'
        else:
            forma_pagamento = 'entrega'

        pedido = Pedido.objects.create(
            nome=nome,
            telefone=telefone,
            endereco=endereco,
            forma_pagamento=forma_pagamento,
            total=carrinho.total(),
        )

        for item in carrinho:
            ItemPedido.objects.create(
                pedido=pedido,
                produto=item['produto'],
                quantidade=item['quantidade'],
                preco_unitario=item['preco'],
            )

        carrinho.limpar()
        enviar_email_pedido(pedido)

        if pagamento == 'online':
            return redirect(f'/pagamento/criar/{pedido.id}/')

        messages.success(request, f'Pedido #{pedido.id} realizado com sucesso!')
        return redirect('pedidos:confirmacao', pedido_id=pedido.id)

    context = {
        'carrinho': carrinho,
        'total': carrinho.total(),
    }
    return render(request, 'pedidos/checkout.html', context)

def confirmacao(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    return render(request, 'pedidos/confirmacao.html', {'pedido': pedido})

def meus_pedidos(request):
    pedidos = []
    telefone = ''

    if request.method == 'POST':
        telefone = request.POST.get('telefone', '').strip()
        if telefone:
            pedidos = Pedido.objects.filter(telefone=telefone).order_by('-criado_em')

    return render(request, 'pedidos/meus_pedidos.html', {
        'pedidos': pedidos,
        'telefone': telefone,
    })
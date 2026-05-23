from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib import messages
from apps.produtos.models import Produto
from .carrinho import Carrinho
from .models import Pedido, ItemPedido

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

def checkout(request):
    carrinho = Carrinho(request)

    if len(carrinho) == 0:
        messages.error(request, 'Seu carrinho está vazio!')
        return redirect('produtos:lista')

    if request.method == 'POST':
        nome = request.POST.get('nome')
        telefone = request.POST.get('telefone')
        endereco = request.POST.get('endereco')
        forma_pagamento = request.POST.get('forma_pagamento')

        # Cria o pedido
        pedido = Pedido.objects.create(
            nome=nome,
            telefone=telefone,
            endereco=endereco,
            forma_pagamento=forma_pagamento,
            total=carrinho.total(),
        )

        # Cria os itens do pedido
        for item in carrinho:
            ItemPedido.objects.create(
                pedido=pedido,
                produto=item['produto'],
                quantidade=item['quantidade'],
                preco_unitario=item['preco'],
            )

        # Limpa o carrinho
        carrinho.limpar()

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
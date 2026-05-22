from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from apps.produtos.models import Produto
from .carrinho import Carrinho

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
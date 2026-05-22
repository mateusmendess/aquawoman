from django.shortcuts import render
from .models import Produto, Categoria
from apps.pedidos.carrinho import Carrinho

def lista_produtos(request):
    categorias = Categoria.objects.filter(ativo=True)
    produtos = Produto.objects.filter(ativo=True)
    categoria_slug = request.GET.get('categoria')
    if categoria_slug:
        produtos = produtos.filter(categoria__slug=categoria_slug)

    carrinho = Carrinho(request)
    context = {
        'produtos': produtos,
        'categorias': categorias,
        'categoria_slug': categoria_slug,
        'quantidade_carrinho': len(carrinho),
    }

    if request.headers.get('HX-Request'):
        return render(request, 'produtos/partials/lista_produtos.html', context)

    return render(request, 'produtos/lista.html', context)
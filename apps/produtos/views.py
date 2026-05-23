from django.shortcuts import render
from .models import Produto, Categoria
from apps.pedidos.carrinho import Carrinho

def lista_produtos(request):
    categorias = Categoria.objects.filter(ativo=True)
    produtos = Produto.objects.filter(ativo=True)

    categoria_slug = request.GET.get('categoria')
    busca = request.GET.get('busca', '').strip()

    if categoria_slug:
        produtos = produtos.filter(categoria__slug=categoria_slug)

    if busca:
        produtos = produtos.filter(nome__icontains=busca)

    context = {
        'produtos': produtos,
        'categorias': categorias,
        'categoria_slug': categoria_slug,
        'busca': busca,
    }

    if request.headers.get('HX-Request'):
        return render(request, 'produtos/partials/lista_produtos.html', context)

    return render(request, 'produtos/lista.html', context)
from django.shortcuts import render
from .models import Produto, Categoria
from apps.pedidos.carrinho import Carrinho

def lista_produtos(request):
    categorias = Categoria.objects.filter(ativo=True)
    categorias_slugs = request.GET.getlist('categoria')
    busca = request.GET.get('busca', '').strip()

    if categorias_slugs:
        produtos = None
        categorias_com_produtos = []
        cats_filtradas = categorias.filter(slug__in=categorias_slugs)
        for categoria in cats_filtradas:
            prods = Produto.objects.filter(ativo=True, categoria=categoria).order_by('-destaque', 'nome')
            if prods.exists():
                categorias_com_produtos.append({
                    'categoria': categoria,
                    'produtos': prods,
                })
    elif busca:
        produtos = Produto.objects.filter(ativo=True, nome__icontains=busca).order_by('-destaque', 'nome')
        categorias_com_produtos = None
    else:
        produtos = None
        categorias_com_produtos = []
        for categoria in categorias:
            prods = Produto.objects.filter(ativo=True, categoria=categoria).order_by('-destaque', 'nome')
            if prods.exists():
                categorias_com_produtos.append({
                    'categoria': categoria,
                    'produtos': prods,
                })

    context = {
        'produtos': produtos,
        'categorias': categorias,
        'categoria_slug': categorias_slugs,
        'busca': busca,
        'categorias_com_produtos': categorias_com_produtos,
    }

    if request.headers.get('HX-Request'):
        return render(request, 'produtos/partials/lista_produtos.html', context)

    return render(request, 'produtos/lista.html', context)

def home(request):
    return render(request, 'home.html')
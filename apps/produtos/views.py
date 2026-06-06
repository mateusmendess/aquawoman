from django.shortcuts import render
from .models import Produto, Categoria
from apps.pedidos.carrinho import Carrinho

def lista_produtos(request):
    categorias = Categoria.objects.filter(ativo=True)
    categoria_slug = request.GET.get('categoria')
    busca = request.GET.get('busca', '').strip()

    if categoria_slug:
        produtos = Produto.objects.filter(ativo=True, categoria__slug=categoria_slug).order_by('-destaque', 'nome')
        categorias_com_produtos = None
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
        'categoria_slug': categoria_slug,
        'busca': busca,
        'categorias_com_produtos': categorias_com_produtos,
    }

    if request.headers.get('HX-Request'):
        return render(request, 'produtos/partials/lista_produtos.html', context)

    return render(request, 'produtos/lista.html', context)

def home(request):
    return render(request, 'home.html')
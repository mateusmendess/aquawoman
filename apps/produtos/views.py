from django.shortcuts import render
from .models import Produto, Categoria

def lista_produtos(request):
    categorias = Categoria.objects.filter(ativo=True)
    destaques = Produto.objects.filter(ativo=True, destaque=True)

    categoria_slug = request.GET.get('categoria')
    if categoria_slug:
        produtos = Produto.objects.filter(ativo=True, categoria__slug=categoria_slug)
    else:
        produtos = Produto.objects.filter(ativo=True)

    context = {
        'produtos': produtos,
        'categorias': categorias,
        'destaques': destaques,
        'categoria_slug': categoria_slug,
    }

    # Se a requisição veio do HTMX, retorna só o partial
    if request.headers.get('HX-Request'):
        return render(request, 'produtos/partials/lista_produtos.html', context)

    return render(request, 'produtos/lista.html', context)
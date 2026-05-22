from django.shortcuts import render
from .models import Produto, Categoria

def lista_produtos(request):
    produtos = Produto.objects.filter(ativo=True)
    categorias = Categoria.objects.filter(ativo=True)
    destaques = Produto.objects.filter(ativo=True, destaque=True)
    
    context = {
        'produtos': produtos,
        'categorias': categorias,
        'destaques': destaques,
    }
    return render(request, 'produtos/lista.html', context)
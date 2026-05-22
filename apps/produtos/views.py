from django.shortcuts import render

def lista_produtos(request):
    return render(request, 'produtos/lista.html')
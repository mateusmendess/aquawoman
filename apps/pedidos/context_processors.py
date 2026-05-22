from .carrinho import Carrinho

def carrinho_quantidade(request):
    carrinho = Carrinho(request)
    return {'quantidade_carrinho': len(carrinho)}
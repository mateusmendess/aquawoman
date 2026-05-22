from apps.produtos.models import Produto

CARRINHO_SESSION_KEY = 'carrinho'

class Carrinho:
    def __init__(self, request):
        self.session = request.session
        carrinho = self.session.get(CARRINHO_SESSION_KEY)
        if not carrinho:
            carrinho = self.session[CARRINHO_SESSION_KEY] = {}
        self.carrinho = carrinho

    def adicionar(self, produto, quantidade=1):
        produto_id = str(produto.id)
        if produto_id not in self.carrinho:
            self.carrinho[produto_id] = {
                'quantidade': 0,
                'preco': str(produto.preco),
                'nome': produto.nome,
            }
        self.carrinho[produto_id]['quantidade'] += quantidade
        self.salvar()

    def remover(self, produto):
        produto_id = str(produto.id)
        if produto_id in self.carrinho:
            del self.carrinho[produto_id]
            self.salvar()

    def salvar(self):
        # Garante que só dados serializáveis ficam na sessão
        sessao_limpa = {}
        for k, v in self.carrinho.items():
            sessao_limpa[k] = {
                'quantidade': v['quantidade'],
                'preco': v['preco'],
                'nome': v['nome'],
            }
        self.session[CARRINHO_SESSION_KEY] = sessao_limpa
        self.session.modified = True
        self.carrinho = self.session[CARRINHO_SESSION_KEY]

    def __iter__(self):
        produto_ids = self.carrinho.keys()
        produtos = Produto.objects.filter(id__in=produto_ids)
        produto_map = {str(p.id): p for p in produtos}
        for produto_id, item in self.carrinho.items():
            yield {
                'produto': produto_map.get(produto_id),
                'quantidade': item['quantidade'],
                'preco': float(item['preco']),
                'subtotal': float(item['preco']) * item['quantidade'],
            }

    def __len__(self):
        return sum(item['quantidade'] for item in self.carrinho.values())

    def total(self):
        return sum(float(item['preco']) * item['quantidade'] for item in self.carrinho.values())

    def limpar(self):
        del self.session[CARRINHO_SESSION_KEY]
        self.session.modified = True
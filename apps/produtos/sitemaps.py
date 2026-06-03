from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Produto

class ProdutoSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        return Produto.objects.filter(ativo=True)

    def location(self, item):
        return '/'

class StaticSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.5

    def items(self):
        return ['produtos:lista', 'pedidos:meus_pedidos']

    def location(self, item):
        return reverse(item)
from django.contrib import admin
from django.urls import path, include
from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from apps.produtos.sitemaps import ProdutoSitemap, StaticSitemap

sitemaps = {
    'produtos': ProdutoSitemap,
    'static': StaticSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.produtos.urls')),
    path('', include('apps.pedidos.urls')),
    path('', include('apps.dashboard.urls')),
    path('', include('apps.pagamentos.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
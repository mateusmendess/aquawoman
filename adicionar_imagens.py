# -*- coding: utf-8 -*-
import os
import requests
import tempfile
import cloudinary
import cloudinary.uploader
from django.conf import settings
from apps.produtos.models import Produto

print("Iniciando busca de imagens...")

UNSPLASH_KEY = settings.UNSPLASH_ACCESS_KEY
LIMITE_POR_EXECUCAO = 50

def buscar_imagem_unsplash(query):
    try:
        url = "https://api.unsplash.com/search/photos"
        params = {
            "query": query,
            "per_page": 1,
            "orientation": "squarish",
            "client_id": UNSPLASH_KEY,
        }
        r = requests.get(url, params=params, timeout=10)
        data = r.json()
        if data.get("results"):
            return data["results"][0]["urls"]["regular"]
    except Exception as e:
        print("Erro ao buscar: " + str(e))
    return None

def baixar_e_subir_cloudinary(url_imagem, slug):
    try:
        r = requests.get(url_imagem, timeout=15)
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as f:
            f.write(r.content)
            tmp_path = f.name
        resultado = cloudinary.uploader.upload(
            tmp_path,
            folder="produtos",
            public_id=slug[:50],
            overwrite=True,
        )
        os.unlink(tmp_path)
        return resultado.get("public_id")
    except Exception as e:
        print("Erro ao subir: " + str(e))
        return None

produtos = Produto.objects.filter(foto="").order_by("id")[:LIMITE_POR_EXECUCAO]
total = produtos.count()
print("Processando " + str(total) + " produtos...")

sucesso = 0
erros = 0

for i, produto in enumerate(produtos):
    print("[" + str(i+1) + "/" + str(total) + "] " + produto.nome)

    # Busca pelo nome do produto em inglês seria melhor mas vamos tentar em português
    termo = produto.nome
    url_img = buscar_imagem_unsplash(termo)

    # Se não achar, tenta pela categoria
    if not url_img:
        termo = produto.categoria.nome + " cleaning product"
        url_img = buscar_imagem_unsplash(termo)

    if not url_img:
        print("  Sem imagem encontrada")
        erros += 1
        continue

    public_id = baixar_e_subir_cloudinary(url_img, produto.slug)
    if not public_id:
        print("  Erro ao subir para Cloudinary")
        erros += 1
        continue

    produto.foto = public_id
    produto.save()
    print("  OK")
    sucesso += 1

restantes = Produto.objects.filter(foto="").count()
print("\n" + str(sucesso) + " imagens adicionadas!")
if erros:
    print(str(erros) + " erros")
print(str(restantes) + " produtos ainda sem imagem")
if restantes > 0:
    print("Rode o script novamente apos 1 hora para continuar!")
print("Feito!")
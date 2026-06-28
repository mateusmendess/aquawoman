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

# Termos de busca em ingles por slug do produto
TERMOS = {
    "agua-sanitaria-economica-1l": "bleach cleaning bottle",
    "agua-sanitaria-economica-2l": "bleach cleaning bottle",
    "agua-sanitaria-economica-5l": "bleach cleaning gallon",
    "agua-sanitaria-fc-verde-1l": "bleach bottle green",
    "agua-sanitaria-fc-verde-2l": "bleach bottle green",
    "agua-sanitaria-fc-verde-5l": "bleach gallon green",
    "desinfetante-floral-1l": "disinfectant spray floral",
    "desinfetante-floral-2l": "disinfectant spray floral",
    "desinfetante-floral-5l": "disinfectant gallon",
    "desinfetante-jasmim-1l": "disinfectant jasmine bottle",
    "desinfetante-jasmim-2l": "disinfectant jasmine bottle",
    "desinfetante-lavanda-1l": "lavender disinfectant bottle",
    "desinfetante-lavanda-2l": "lavender disinfectant bottle",
    "desinfetante-lavanda-5l": "lavender disinfectant gallon",
    "desinfetante-pinho-sol-38l": "pine disinfectant bottle",
    "desinfetante-azulim-500ml": "disinfectant spray bottle blue",
    "desinfetante-azulim-lavanda-1l": "lavender disinfectant bottle",
    "desinfetante-azulim-wave-1l": "disinfectant spray bottle",
    "lava-louca-economico-limao-500ml": "dish soap lemon bottle",
    "lava-louca-economico-maca-500ml": "dish soap apple bottle",
    "lava-louca-economico-neutro-500ml": "dish soap neutral bottle",
    "lava-louca-fc-limao-pet-50ml": "dish soap lemon small bottle",
    "lava-louca-fc-maca-pet-500ml": "dish soap apple bottle",
    "lava-louca-fc-neutro-pet-5000ml": "dish soap large gallon",
    "lava-louca-oi-limao-500ml": "dish soap lemon bottle",
    "lava-louca-oi-maca-500ml": "dish soap apple bottle",
    "lava-louca-oi-neutro-500ml": "dish soap bottle",
    "lava-louca-oi-neutro-5l": "dish soap large bottle",
    "lava-louca-economico-5l": "dish soap gallon",
    "lava-louca-azulim-500ml": "dish soap blue bottle",
    "papel-higienico-30m-mili-16x4-neutro": "toilet paper roll white",
    "papel-hig-elegans-duo-8-rolos-50m": "toilet paper pack rolls",
    "papel-hig-elegans-soft-simples-8-rolos-300m": "toilet paper soft rolls",
    "papel-hig-mili-neutro-bianco-30m": "toilet paper white roll",
    "papel-hig-atualle-20m-8x12": "toilet paper rolls pack",
    "papel-hig-mili-neutro-cmpc-4x16": "toilet paper rolls",
    "papel-hig-cai-cai-fl-duplo-elegans": "toilet paper double layer",
    "papel-hig-equilibrio-300m": "toilet paper roll large",
    "papel-toalha-interfolhas-unique-1000fl-194-20cm": "paper towel interleaved",
    "papel-toalha-interfolhas-unique-1000fl-23-20cm": "paper towel interleaved pack",
    "papel-toalha-bobina-3-rolos-360-folhas": "paper towel rolls",
    "papel-toalha-bobina-tenaz-200m-6-rolos": "paper towel bobbin rolls",
    "papel-toalha-bobina-100-celulose-fit-alveflor-200m": "paper towel roll cellulose",
    "papel-toalha-bobina-100-celulose-200m": "paper towel roll white",
    "papel-toalha-bobina-equilibrio-200m": "paper towel bobbin",
    "papel-toalha-interfolha-equilibrio-1000fl": "paper towel interleaved",
    "papel-toalha-snob-3-unidades": "paper towel rolls pack",
    "papel-aluminio-30x75mt": "aluminum foil roll kitchen",
    "pano-microfibra-polylar-35cmx50cm": "microfiber cleaning cloth",
    "pano-multiuso-polylar-branco-28cmx50cm": "white cleaning cloth",
    "pano-multiuso-rolo-azul-25m": "blue cleaning cloth roll",
    "pano-de-microfibra-100x100": "microfiber cloth large",
    "pano-multiuso-rolo-azul-240m": "cleaning cloth roll blue",
    "pano-alvejado-copalimpa-70x45cm": "white bleached cleaning cloth",
    "pano-alvejado-ra-novo-mundo-40x64cm": "white cleaning cloth",
    "pano-xadrez-polylar-60x80cm": "checkered kitchen cloth",
    "pano-cru-novo-mundo-58x80cm": "raw cotton cleaning cloth",
    "saco-de-lixo-azul-15l-rolo-60-unidades": "blue trash bag",
    "saco-de-lixo-azulim-30l-rolo-30-unidades": "blue garbage bag roll",
    "saco-de-lixo-azulim-50l-rolo-30-unidades": "blue garbage bag large",
    "saco-de-lixo-vorel-100l-15-unidades": "black trash bag large",
    "saco-lixo-azulim-pct-20-unidades": "garbage bag pack",
    "saco-lixo-preto-sacolmax-30lt-pct-10-unidades": "black trash bag small",
    "saco-lixo-preto-sacolmax-50lt-pct-10-unidades": "black trash bag medium",
    "saco-lixo-preto-sacolmax-100lt-pct-10-unidades": "black trash bag large",
    "saco-de-lixo-30l-rolo-50-unidades": "garbage bag roll",
    "saco-de-lixo-50l-rolo-40-unidades": "garbage bag medium roll",
    "saco-de-lixo-100l-rolo-20-unidades": "garbage bag large roll",
    "saco-de-lixo-leve-100l-pct-100-unidades": "light trash bag pack",
    "saco-de-lixo-medio-100l-pct-100-unidades": "trash bag medium pack",
    "saco-de-lixo-reforcado-100l-pct-100-unidades": "heavy duty trash bag",
    "saco-de-lixo-medio-200l-pct-100-unidades": "large trash bag pack",
    "saco-de-lixo-reforcado-200l-pct-100-unidades": "heavy duty large trash bag",
    "lava-roupa-em-barra-pct-5-unidades": "laundry soap bar",
    "lava-roupa-liquido-oi-5l": "liquid laundry detergent gallon",
    "lava-roupa-liquido-ala-lavanda-18l": "lavender liquid laundry detergent",
    "lava-roupa-liquido-ala-3l": "liquid laundry detergent bottle",
    "lava-roupa-em-po-ala-lavanda-400g": "lavender laundry powder",
    "lava-roupa-em-po-brilhante-400g": "laundry powder box",
    "lava-roupa-em-po-classico-tradicional-4kg": "laundry detergent powder large",
    "lava-roupa-em-po-guarany-4kg": "laundry powder large box",
    "lava-roupa-po-tixan-ype-800g": "laundry detergent powder",
    "lava-roupa-po-tixan-ype-13kg": "laundry powder box large",
    "lava-roupa-po-tixan-ype-4kg": "laundry detergent powder bag",
    "lava-roupa-tixan-ipe-8kg": "laundry detergent large bag",
    "lava-roupa-tixan-ipe-400g": "laundry detergent powder small",
    "lava-roupa-liquido-tuff-15l": "liquid laundry detergent bottle",
    "lava-roupa-liquido-economico-3l": "liquid laundry detergent",
    "copo-descartavel-cristcopo-180ml-cx-25-pacotes": "disposable plastic cups",
    "copo-descartavel-cristcopo-200ml-cx-25-pacotes": "disposable plastic cups pack",
    "copo-descartavel-cristcopo-50ml-cx-50-pacotes": "small disposable cups",
    "copo-br-150ml-cx-25-pacotes": "disposable cups small",
    "copo-br-180ml-cx-25-pacotes": "disposable plastic cups",
    "copo-br-200ml-cx-25-pacotes": "plastic disposable cups pack",
    "copo-br-300ml-cx-20-pacotes": "large disposable cups",
    "luva-vabene-multiuso-flex-mg-par": "rubber cleaning gloves",
    "luva-latex-nobre-caixa": "latex gloves box",
    "luva-nitrilica-preta-caixa": "black nitrile gloves box",
    "luva-mucambo-amarela-par": "yellow rubber gloves",
    "luva-ranhurada-m-par": "textured rubber gloves",
    "luva-de-borracha-g-par": "rubber gloves cleaning",
    "vassoura-versalli-com-cabo-faxina": "broom with handle",
    "vassoura-norcia-com-cabo-faxina": "floor broom",
    "rodo-com-cabo-de-madeira-40cm": "floor squeegee mop",
    "rodo-aluminio-start-40cm": "aluminum squeegee floor",
    "rodo-aluminio-start-60cm": "aluminum floor squeegee large",
    "rodo-aluminio-start-80cm": "aluminum mop squeegee",
    "limpa-aluminio-economico-500ml": "aluminum cleaner spray",
    "limpa-aluminio-azulim-500ml": "metal cleaner spray bottle",
    "limpa-forno-500ml": "oven cleaner spray",
    "limpa-aluminio-politriz-500ml": "metal polish cleaner",
    "limpador-perfumado-azulim-1l": "scented multipurpose cleaner",
    "multiuso-azulim-500ml": "multipurpose cleaner spray",
    "multi-uso-cremoso-300ml": "cream multipurpose cleaner",
    "multi-uso-cha-branco-500ml": "multipurpose cleaner bottle",
    "multi-uso-economico-500ml": "multipurpose spray cleaner",
    "multi-uso-veja-uso-original-500ml": "multipurpose cleaning spray",
    "bom-ar-alegria-360ml": "air freshener spray",
    "bom-ar-jasmim-360ml": "jasmine air freshener",
    "bom-ar-limao-360ml": "lemon air freshener spray",
    "bom-ar-romance-360ml": "floral air freshener spray",
    "bom-ar-talco-360ml": "talcum powder air freshener",
    "esponja-pertuto-multiuso": "kitchen sponge scrubber",
    "la-de-aco-6-unidades": "steel wool scrubber pad",
    "alcool-gel-antisseptico-70-1l": "hand sanitizer gel bottle",
    "alcool-70-azulim-1l": "alcohol sanitizer bottle",
    "alcool-hidratado-liquido-46-inpm-1l": "liquid alcohol bottle",
    "alcool-hidratado-70-inpm-1l": "isopropyl alcohol bottle",
    "alcool-liquido-70-start-1l": "alcohol cleaning bottle",
    "alcool-46-bactericida-top-5l": "alcohol disinfectant gallon",
    "alcool-70-asseotgel-5l": "alcohol gel large bottle",
    "alcool-gel-para-maos-420g": "hand sanitizer gel pump",
    "inseticida-spb": "insecticide spray can",
    "inseticida-baygom": "cockroach insecticide spray",
    "lustra-moveis-azulim-200g": "furniture polish spray",
    "sabonete-liquido-erva-doce-5l": "liquid soap anise gallon",
    "sabonete-bouquet-verde-5l": "green liquid soap gallon",
    "sabonete-erva-doce-com-hortela-500ml": "liquid hand soap bottle",
    "sabonete-only-verde-perolado-5l": "pearlized liquid soap",
    "pulverizador-spray-1l": "spray bottle trigger pump",
    "pulverizador-manual-vazio-500ml": "empty spray bottle",
    "coador-flanela-aro-metal-n08": "coffee filter flannel",
    "pastilhas-sanitaria-cx-3-unidades": "toilet bowl cleaner tablet",
    "pedra-sanitaria": "toilet cleaner block",
    "flanela-copa-lima-laranja-branca-30x50": "orange white flannel cloth",
    "amaciante-tuff-cha-branco-15l": "fabric softener bottle",
    "amaciante-soft-blue-5l": "fabric softener gallon blue",
    "argus-detergente-5l": "industrial detergent gallon",
    "hipoclorito-de-sodio-5l": "sodium hypochlorite gallon",
    "magico-removedor-de-ceras-5l": "floor wax remover gallon",
    "naftalina-nobre-50g": "mothballs naphthalene",
    "naftalina-azulim-30g": "mothballs small pack",
    "pedrex-5l": "floor cleaner gallon",
    "percabonato-1kg": "percarbonate powder cleaning",
    "peroxi-lavanda-5l": "peroxide lavender cleaner",
    "pretita-5l": "black floor cleaner gallon",
    "alvejante-economico-1l": "bleach whitener bottle",
    "alvejante-economico-2l": "bleach whitener large bottle",
    "cabo-de-aluminio-15m": "aluminum mop handle",
    "escova-para-lavar-roupa": "laundry brush scrub",
    "tira-ferrugem-azulim-50ml": "rust remover spray",
    "toca-rede-nylon-100-unidades": "hair net nylon pack",
    "toca-descartavel": "disposable hair cap",
    "guardanapo": "paper napkin pack",
}

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
            folder="media/produtos",
            public_id=slug[:50],
            overwrite=True,
        )
        os.unlink(tmp_path)
        return slug[:50]
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

    termo = TERMOS.get(produto.slug, None)
    if not termo:
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

    produto.foto = "produtos/" + public_id
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
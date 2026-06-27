# -*- coding: utf-8 -*-
from apps.pedidos.models import ItemPedido, Pedido
from apps.produtos.models import Categoria, Produto
from django.utils.text import slugify

print("Removendo itens de pedidos...")
ItemPedido.objects.all().delete()
print("Removendo pedidos...")
Pedido.objects.all().delete()
print("Removendo produtos...")
Produto.objects.all().delete()
print("Removendo categorias...")
Categoria.objects.all().delete()
print("Removido!")

print("Criando categorias...")
categorias_data = [
    (u"\u00c1gua Sanit\u00e1ria",            "agua-sanitaria"),
    ("Desinfetante",                           "desinfetante"),
    ("Detergente",                             "detergente"),
    (u"Papel Higi\u00eanico",                 "papel-higienico"),
    ("Papel Toalha",                           "papel-toalha"),
    ("Pano",                                   "pano"),
    ("Saco para Lixo",                         "saco-para-lixo"),
    (u"Sab\u00e3o",                            "sabao"),
    (u"Copos Descart\u00e1veis",              "copos-descartaveis"),
    ("Luvas",                                  "luvas"),
    ("Vassoura & Rodo",                        "vassoura-rodo"),
    (u"Limpa Alum\u00ednio e Multiuso",       "limpa-aluminio-multiuso"),
    ("Desodorizador Bom Ar",                   "desodorizador-bom-ar"),
    ("Esponja",                                "esponja"),
    (u"\u00c1lcool",                           "alcool"),
    ("Inseticida",                             "inseticida"),
    ("Diversos",                               "diversos"),
]

categorias = {}
for nome, slug in categorias_data:
    c = Categoria.objects.create(nome=nome, slug=slug, icone="", ativo=True)
    categorias[nome] = c
    print("  OK: " + nome)

print("\nCadastrando produtos...")
produtos_data = [
    (u"\u00c1gua Sanit\u00e1ria Econ\u00f4mica 1L", u"\u00c1gua Sanit\u00e1ria", 2.81, "Embalagem 1L"),
    (u"\u00c1gua Sanit\u00e1ria Econ\u00f4mica 2L", u"\u00c1gua Sanit\u00e1ria", 5.33, "Embalagem 2L"),
    (u"\u00c1gua Sanit\u00e1ria Econ\u00f4mica 5L", u"\u00c1gua Sanit\u00e1ria", 14.51, "Embalagem 5L"),
    (u"\u00c1gua Sanit\u00e1ria FC Verde 1L", u"\u00c1gua Sanit\u00e1ria", 2.16, "Embalagem 1L"),
    (u"\u00c1gua Sanit\u00e1ria FC Verde 2L", u"\u00c1gua Sanit\u00e1ria", 3.65, "Embalagem 2L"),
    (u"\u00c1gua Sanit\u00e1ria FC Verde 5L", u"\u00c1gua Sanit\u00e1ria", 10.47, "Embalagem 5L"),
    ("Desinfetante Floral 1L", "Desinfetante", 4.28, "Embalagem 1L"),
    ("Desinfetante Floral 2L", "Desinfetante", 8.24, "Embalagem 2L"),
    ("Desinfetante Floral 5L", "Desinfetante", 20.87, "Embalagem 5L"),
    ("Desinfetante Jasmim 1L", "Desinfetante", 4.28, "Embalagem 1L"),
    ("Desinfetante Jasmim 2L", "Desinfetante", 8.24, "Embalagem 2L"),
    ("Desinfetante Lavanda 1L", "Desinfetante", 4.28, "Embalagem 1L"),
    ("Desinfetante Lavanda 2L", "Desinfetante", 8.24, "Embalagem 2L"),
    ("Desinfetante Lavanda 5L", "Desinfetante", 20.87, "Embalagem 5L"),
    ("Desinfetante Pinho Sol 3,8L", "Desinfetante", 54.55, "Embalagem 3,8L"),
    ("Desinfetante Azulim 500ML", "Desinfetante", 3.93, "Embalagem 500ML"),
    ("Desinfetante Azulim Lavanda 1L", "Desinfetante", 0.00, "Embalagem 1L"),
    ("Desinfetante Azulim Wave 1L", "Desinfetante", 0.00, "Embalagem 1L"),
    (u"Lava Lou\u00e7a Econ\u00f4mico Lim\u00e3o 500ML", "Detergente", 2.58, "Embalagem 500ML"),
    (u"Lava Lou\u00e7a Econ\u00f4mico Ma\u00e7\u00e3 500ML", "Detergente", 2.58, "Embalagem 500ML"),
    (u"Lava Lou\u00e7a Econ\u00f4mico Neutro 500ML", "Detergente", 2.58, "Embalagem 500ML"),
    (u"Lava Lou\u00e7a FC Lim\u00e3o Pet 50ML", "Detergente", 1.98, "Embalagem 50ML"),
    (u"Lava Lou\u00e7a FC Ma\u00e7\u00e3 Pet 500ML", "Detergente", 1.98, "Embalagem 500ML"),
    (u"Lava Lou\u00e7a FC Neutro Pet 5000ML", "Detergente", 1.98, "Embalagem 5000ML"),
    (u"Lava Lou\u00e7a OI Lim\u00e3o 500ML", "Detergente", 1.73, "Embalagem 500ML"),
    (u"Lava Lou\u00e7a OI Ma\u00e7\u00e3 500ML", "Detergente", 1.73, "Embalagem 500ML"),
    (u"Lava Lou\u00e7a OI Neutro 500ML", "Detergente", 1.73, "Embalagem 500ML"),
    (u"Lava Lou\u00e7a OI Neutro 5L", "Detergente", 19.13, "Embalagem 5L"),
    (u"Lava Lou\u00e7a Econ\u00f4mico 5L", "Detergente", 24.75, "Embalagem 5L"),
    (u"Lava Lou\u00e7a Azulim 500ML", "Detergente", 0.00, "Embalagem 500ML"),
    (u"Papel Higi\u00eanico 30M Mili 16X4 Neutro", u"Papel Higi\u00eanico", 18.70, "PCT C/16"),
    (u"Papel Hig. Elegans Duo 8 Rolos 50M", u"Papel Higi\u00eanico", 136.58, "8 Rolos/50M"),
    (u"Papel Hig. Elegans Soft Simples 8 Rolos 300M", u"Papel Higi\u00eanico", 69.76, "8 Rolos/300M"),
    (u"Papel Hig. Mili Neutro Bianco 30M", u"Papel Higi\u00eanico", 4.68, u"Unit\u00e1rio"),
    (u"Papel Hig. Atualle 20M 8X12", u"Papel Higi\u00eanico", 19.39, "16x4"),
    (u"Papel Hig. Mili Neutro CMPC 4X16", u"Papel Higi\u00eanico", 12.84, "4x30M"),
    (u"Papel Hig. Cai Cai FL Duplo Elegans", u"Papel Higi\u00eanico", 129.20, "16/500FLS"),
    (u"Papel Hig. Equil\u00edbrio 300M", u"Papel Higi\u00eanico", 78.68, "300M"),
    ("Papel Toalha Interfolhas Unique 1000FL 19,4/20CM", "Papel Toalha", 19.72, "1000FL 19,4/20CM"),
    ("Papel Toalha Interfolhas Unique 1000FL 23/20CM", "Papel Toalha", 23.52, "1000FL 23/20CM"),
    ("Papel Toalha Bobina 3 Rolos 360 Folhas", "Papel Toalha", 19.61, "3 Rolos 360 Folhas"),
    ("Papel Toalha Bobina Tenaz 200M 6 Rolos", "Papel Toalha", 109.71, "200M/6 Rolos"),
    ("Papel Toalha Bobina 100% Celulose Fit Alveflor 200M", "Papel Toalha", 124.99, "200M/6 Rolos"),
    ("Papel Toalha Bobina 100% Celulose 200M", "Papel Toalha", 77.99, "200M/6 Rolos"),
    (u"Papel Toalha Bobina Equil\u00edbrio 200M", "Papel Toalha", 80.41, "200M/6 Rolos"),
    (u"Papel Toalha Interfolha Equil\u00edbrio 1000FL", "Papel Toalha", 17.13, "1000FL/19,4/20CM"),
    ("Papel Toalha Snob 3 Unidades", "Papel Toalha", 19.61, "3 Unidades"),
    (u"Papel Alum\u00ednio 30X7,5MT", "Papel Toalha", 5.85, "30X7,5MT"),
    ("Pano Microfibra Polylar 35CMX50CM", "Pano", 6.75, u"Unit\u00e1rio"),
    ("Pano Multiuso Polylar Branco 28CMX50CM", "Pano", 138.99, "300M"),
    ("Pano Multiuso Rolo Azul 25M", "Pano", 21.87, "25M/50 Panos"),
    ("Pano de Microfibra 100X100", "Pano", 22.47, "100/100"),
    ("Pano Multiuso Rolo Azul 240M", "Pano", 93.80, "240M/600 Panos"),
    ("Pano Alvejado Copalimpa 70X45CM", "Pano", 10.50, "70X45CM"),
    ("Pano Alvejado RA Novo Mundo 40X64CM", "Pano", 5.07, "40X64CM"),
    ("Pano Xadrez Polylar 60X80CM", "Pano", 12.50, "60X80CM"),
    ("Pano Cru Novo Mundo 58X80CM", "Pano", 5.85, "50X80CM"),
    ("Saco de Lixo Azul 15L Rolo 60 Unidades", "Saco para Lixo", 19.30, "Rolo 60 Uni"),
    ("Saco de Lixo Azulim 30L Rolo 30 Unidades", "Saco para Lixo", 0.00, "Rolo 30 Uni"),
    ("Saco de Lixo Azulim 50L Rolo 30 Unidades", "Saco para Lixo", 0.00, "Rolo 30 Uni"),
    ("Saco de Lixo Vorel 100L 15 Unidades", "Saco para Lixo", 0.00, "PCT 15 Uni"),
    ("Saco Lixo Azulim PCT 20 Unidades", "Saco para Lixo", 5.75, "PCT 20 Uni"),
    ("Saco Lixo Preto Sacolmax 30LT PCT 10 Unidades", "Saco para Lixo", 3.99, "PCT 10 Uni"),
    ("Saco Lixo Preto Sacolmax 50LT PCT 10 Unidades", "Saco para Lixo", 4.80, "PCT 10 Uni"),
    ("Saco Lixo Preto Sacolmax 100LT PCT 10 Unidades", "Saco para Lixo", 5.20, "PCT 10 Uni"),
    ("Saco de Lixo 30L Rolo 50 Unidades", "Saco para Lixo", 17.20, "Rolo 50 Uni"),
    ("Saco de Lixo 50L Rolo 40 Unidades", "Saco para Lixo", 17.20, "Rolo 40 Uni"),
    ("Saco de Lixo 100L Rolo 20 Unidades", "Saco para Lixo", 17.20, "Rolo 20 Uni"),
    ("Saco de Lixo Leve 100L PCT 100 Unidades", "Saco para Lixo", 49.50, "PCT 100 Uni"),
    (u"Saco de Lixo M\u00e9dio 100L PCT 100 Unidades", "Saco para Lixo", 61.80, "PCT 100 Uni"),
    (u"Saco de Lixo Refor\u00e7ado 100L PCT 100 Unidades", "Saco para Lixo", 81.80, "PCT 100 Uni"),
    (u"Saco de Lixo M\u00e9dio 200L PCT 100 Unidades", "Saco para Lixo", 95.80, "PCT 100 Uni"),
    (u"Saco de Lixo Refor\u00e7ado 200L PCT 100 Unidades", "Saco para Lixo", 126.00, "PCT 100 Uni"),
    ("Lava Roupa em Barra PCT 5 Unidades", u"Sab\u00e3o", 9.50, "PCT 5 Uni"),
    ("Lava Roupa Líquido OI 5L", u"Sab\u00e3o", 29.35, "Embalagem 5L"),
    ("Lava Roupa Líquido ALA Lavanda 1,8L", u"Sab\u00e3o", 16.50, "Embalagem 1,8L"),
    ("Lava Roupa Líquido ALA 3L", u"Sab\u00e3o", 25.60, "Embalagem 3L"),
    (u"Lava Roupa em P\u00f3 ALA Lavanda 400G", u"Sab\u00e3o", 4.07, "Embalagem 400G"),
    (u"Lava Roupa em P\u00f3 Brilhante 400G", u"Sab\u00e3o", 6.36, "Embalagem 400G"),
    (u"Lava Roupa em P\u00f3 Cl\u00e1ssico Tradicional 4KG", u"Sab\u00e3o", 28.79, "Embalagem 4KG"),
    (u"Lava Roupa em P\u00f3 Guarany 4KG", u"Sab\u00e3o", 21.40, "Embalagem 4KG"),
    (u"Lava Roupa P\u00f3 Tixan Yp\u00ea 800G", u"Sab\u00e3o", 10.54, "Embalagem 800G"),
    (u"Lava Roupa P\u00f3 Tixan Yp\u00ea 1,3KG", u"Sab\u00e3o", 17.04, "Embalagem 1,3KG"),
    (u"Lava Roupa P\u00f3 Tixan Yp\u00ea 4KG", u"Sab\u00e3o", 48.99, "Embalagem 4KG"),
    (u"Lava Roupa Tixan Ip\u00ea 8KG", u"Sab\u00e3o", 97.66, "Embalagem 8KG"),
    (u"Lava Roupa Tixan Ip\u00ea 400G", u"Sab\u00e3o", 5.66, "Embalagem 400G"),
    (u"Lava Roupa L\u00edquido Tuff 1,5L", u"Sab\u00e3o", 18.71, "Embalagem 1,5L"),
    (u"Lava Roupa L\u00edquido Econ\u00f4mico 3L", u"Sab\u00e3o", 16.83, "Embalagem 3L"),
    (u"Copo Descart\u00e1vel Cristcopo 180ML CX 25 Pacotes", u"Copos Descart\u00e1veis", 5.42, "CX 25 Pacotes 100 Uni"),
    (u"Copo Descart\u00e1vel Cristcopo 200ML CX 25 Pacotes", u"Copos Descart\u00e1veis", 6.42, "CX 25 Pacotes 100 Uni"),
    (u"Copo Descart\u00e1vel Cristcopo 50ML CX 50 Pacotes", u"Copos Descart\u00e1veis", 3.22, "CX 50 Pacotes 100 Uni"),
    (u"Copo BR 150ML CX 25 Pacotes", u"Copos Descart\u00e1veis", 4.39, "CX 25 Pacotes 100 Uni"),
    (u"Copo BR 180ML CX 25 Pacotes", u"Copos Descart\u00e1veis", 4.79, "CX 25 Pacotes 100 Uni"),
    (u"Copo BR 200ML CX 25 Pacotes", u"Copos Descart\u00e1veis", 5.59, "CX 25 Pacotes 100 Uni"),
    (u"Copo BR 300ML CX 20 Pacotes", u"Copos Descart\u00e1veis", 9.24, "CX 20 Pacotes 100 Uni"),
    ("Luva Vabene Multiuso Flex M/G Par", "Luvas", 5.72, "Par"),
    ("Luva Latex Nobre Caixa", "Luvas", 32.50, "Caixa"),
    ("Luva Nitrilica Preta Caixa", "Luvas", 35.70, "Caixa"),
    ("Luva Mucambo Amarela Par", "Luvas", 9.28, "Par"),
    ("Luva Ranhurada M Par", "Luvas", 18.62, "Par"),
    ("Luva de Borracha G Par", "Luvas", 7.50, "Par"),
    ("Vassoura Versalli com Cabo Faxina", "Vassoura & Rodo", 14.09, u"Unit\u00e1rio"),
    ("Vassoura Norcia com Cabo Faxina", "Vassoura & Rodo", 15.16, u"Unit\u00e1rio"),
    ("Rodo com Cabo de Madeira 40CM", "Vassoura & Rodo", 14.69, "40CM"),
    (u"Rodo Alum\u00ednio Start 40CM", "Vassoura & Rodo", 41.24, "40CM"),
    (u"Rodo Alum\u00ednio Start 60CM", "Vassoura & Rodo", 49.38, "60CM"),
    (u"Rodo Alum\u00ednio Start 80CM", "Vassoura & Rodo", 57.40, "80CM"),
    (u"Limpa Alum\u00ednio Econ\u00f4mico 500ML", u"Limpa Alum\u00ednio e Multiuso", 1.95, "Embalagem 500ML"),
    (u"Limpa Alum\u00ednio Azulim 500ML", u"Limpa Alum\u00ednio e Multiuso", 0.00, "Embalagem 500ML"),
    ("Limpa Forno 500ML", u"Limpa Alum\u00ednio e Multiuso", 18.75, "Embalagem 500ML"),
    (u"Limpa Alum\u00ednio Politriz 500ML", u"Limpa Alum\u00ednio e Multiuso", 4.26, "Embalagem 500ML"),
    ("Limpador Perfumado Azulim 1L", u"Limpa Alum\u00ednio e Multiuso", 8.11, "Embalagem 1L"),
    ("Multiuso Azulim 500ML", u"Limpa Alum\u00ednio e Multiuso", 0.00, "Embalagem 500ML"),
    ("Multi-Uso Cremoso 300ML", u"Limpa Alum\u00ednio e Multiuso", 10.20, "Embalagem 300ML"),
    (u"Multi-Uso Ch\u00e1 Branco 500ML", u"Limpa Alum\u00ednio e Multiuso", 5.12, "Embalagem 500ML"),
    (u"Multi-Uso Econ\u00f4mico 500ML", u"Limpa Alum\u00ednio e Multiuso", 4.60, "Embalagem 500ML"),
    ("Multi-Uso Veja Uso Original 500ML", u"Limpa Alum\u00ednio e Multiuso", 5.33, "Embalagem 500ML"),
    ("Bom Ar Alegria 360ML", "Desodorizador Bom Ar", 13.98, "Embalagem 360ML"),
    ("Bom Ar Jasmim 360ML", "Desodorizador Bom Ar", 13.98, "Embalagem 360ML"),
    (u"Bom Ar Lim\u00e3o 360ML", "Desodorizador Bom Ar", 13.98, "Embalagem 360ML"),
    ("Bom Ar Romance 360ML", "Desodorizador Bom Ar", 13.98, "Embalagem 360ML"),
    ("Bom Ar Talco 360ML", "Desodorizador Bom Ar", 13.98, "Embalagem 360ML"),
    ("Esponja Pertuto Multiuso", "Esponja", 1.90, u"Unit\u00e1rio"),
    (u"L\u00e3 de A\u00e7o 6 Unidades", "Esponja", 2.30, "6 Uni"),
    (u"\u00c1lcool Gel Antiss\u00e9ptico 70% 1L", u"\u00c1lcool", 9.38, "Embalagem 1L"),
    (u"\u00c1lcool 70% Azulim 1L", u"\u00c1lcool", 11.50, "Embalagem 1L"),
    (u"\u00c1lcool Hidratado L\u00edquido 46 INPM 1L", u"\u00c1lcool", 10.30, "Embalagem 1L"),
    (u"\u00c1lcool Hidratado 70 INPM 1L", u"\u00c1lcool", 12.75, "Embalagem 1L"),
    (u"\u00c1lcool L\u00edquido 70% Start 1L", u"\u00c1lcool", 11.50, "Embalagem 1L"),
    (u"\u00c1lcool 46 Bactericida Top 5L", u"\u00c1lcool", 54.90, "Embalagem 5L"),
    (u"\u00c1lcool 70% Asseotgel 5L", u"\u00c1lcool", 55.95, "Embalagem 5L"),
    (u"\u00c1lcool Gel para M\u00e3os 420G", u"\u00c1lcool", 12.99, "Embalagem 420G"),
    ("Inseticida SPB", "Inseticida", 16.93, u"Unit\u00e1rio"),
    ("Inseticida Baygom", "Inseticida", 16.00, u"Unit\u00e1rio"),
    ("Lustra Móveis Azulim 200G", "Diversos", 7.20, "Embalagem 200G"),
    (u"Sabonete L\u00edquido Erva Doce 5L", "Diversos", 52.24, "Embalagem 5L"),
    ("Sabonete Bouquet Verde 5L", "Diversos", 60.96, "Embalagem 5L"),
    (u"Sabonete Erva Doce com Hortel\u00e3 500ML", "Diversos", 13.58, "Embalagem 500ML"),
    ("Sabonete Only Verde Perolado 5L", "Diversos", 52.65, "Embalagem 5L"),
    ("Pulverizador Spray 1L", "Diversos", 16.58, "Embalagem 1L"),
    ("Pulverizador Manual Vazio 500ML", "Diversos", 5.47, "Frasco 500ML"),
    ("Coador Flanela Aro Metal N08", "Diversos", 4.62, u"Unit\u00e1rio"),
    ("Pastilhas Sanitária CX 3 Unidades", "Diversos", 7.87, "CX 3 Uni"),
    ("Pedra Sanitária", "Diversos", 2.20, u"Unit\u00e1rio"),
    ("Flanela Copa Lima Laranja/Branca 30X50", "Diversos", 4.70, "30X50CM"),
    (u"Amaciante Tuff Ch\u00e1 Branco 1,5L", "Diversos", 22.26, "Embalagem 1,5L"),
    ("Amaciante Soft Blue 5L", "Diversos", 23.50, "Embalagem 5L"),
    ("Argus Detergente 5L", "Diversos", 64.68, "Embalagem 5L"),
    (u"Hipoclorito de S\u00f3dio 5L", "Diversos", 51.20, "Embalagem 5L"),
    (u"M\u00e1gico Removedor de Ceras 5L", "Diversos", 62.50, "Embalagem 5L"),
    ("Naftalina Nobre 50G", "Diversos", 3.60, "Embalagem 50G"),
    ("Naftalina Azulim 30G", "Diversos", 3.29, "Embalagem 30G"),
    ("Pedrex 5L", "Diversos", 53.59, "Embalagem 5L"),
    ("Percabonato 1KG", "Diversos", 35.00, "Embalagem 1KG"),
    ("Peroxi Lavanda 5L", "Diversos", 155.00, "Embalagem 5L"),
    ("Pretita 5L", "Diversos", 107.95, "Embalagem 5L"),
    (u"Alvejante Econ\u00f4mico 1L", "Diversos", 6.71, "Embalagem 1L"),
    (u"Alvejante Econ\u00f4mico 2L", "Diversos", 12.26, "Embalagem 2L"),
    (u"Cabo de Alum\u00ednio 1,5M", "Diversos", 34.25, u"Unit\u00e1rio"),
    ("Escova para Lavar Roupa", "Diversos", 3.33, u"Unit\u00e1rio"),
    ("Tira Ferrugem Azulim 50ML", "Diversos", 0.00, "Embalagem 50ML"),
    ("Toca Rede Nylon 100 Unidades", "Diversos", 32.63, "PCT 100 Uni"),
    (u"Toca Descart\u00e1vel", "Diversos", 10.34, u"Unit\u00e1rio"),
    ("Guardanapo", "Diversos", 2.50, u"Unit\u00e1rio"),
]

slugs_usados = set()
criados = 0
erros = 0

for nome, cat_nome, preco, descricao in produtos_data:
    try:
        categoria = categorias[cat_nome]
        slug_base = slugify(nome)
        slug = slug_base
        contador = 1
        while slug in slugs_usados:
            slug = slug_base + "-" + str(contador)
            contador += 1
        slugs_usados.add(slug)
        Produto.objects.create(
            nome=nome,
            slug=slug,
            descricao=descricao,
            preco=preco,
            estoque=100,
            categoria=categoria,
            ativo=True,
            destaque=False,
        )
        criados += 1
    except Exception as e:
        print("ERRO em " + nome + ": " + str(e))
        erros += 1

print("\n" + str(criados) + " produtos cadastrados com sucesso!")
print("Feito!")
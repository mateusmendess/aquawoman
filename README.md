# 🛒 Aquawoman

> E-commerce completo de produtos de limpeza e descartáveis com entrega em Parauapebas/PA. Sistema com loja, carrinho, checkout com mapa, painel administrativo e integração com Mercado Pago.

[![Deploy](https://img.shields.io/badge/deploy-railway-6366f1?style=for-the-badge&logo=railway)](https://aquawoman.up.railway.app)
[![Python](https://img.shields.io/badge/Python-3.x-3776ab?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Django](https://img.shields.io/badge/Django-6.0-092e20?style=for-the-badge&logo=django&logoColor=white)](https://djangoproject.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169e1?style=for-the-badge&logo=postgresql&logoColor=white)](https://postgresql.org)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-38bdf8?style=for-the-badge&logo=tailwindcss&logoColor=white)](https://tailwindcss.com)
[![HTMX](https://img.shields.io/badge/HTMX-36c?style=for-the-badge)](https://htmx.org)
[![Railway](https://img.shields.io/badge/Railway-6366f1?style=for-the-badge&logo=railway&logoColor=white)](https://railway.app)

---

## 🌐 Demo

**Acesse o projeto online:** [aquawoman.up.railway.app](https://aquawoman.up.railway.app)

---

## 📸 Screenshots & GIFs

> *Em breve: screenshots e GIFs do fluxo completo*

---

## 🚀 Funcionalidades

### Loja
- Listagem de produtos por categoria com filtros dinâmicos via HTMX (sem reload)
- Busca em tempo real por nome de produto
- Grid responsivo — 2 colunas no mobile, 6 no desktop
- Badge de destaque nos produtos em promoção
- Produto marcado como "Indisponível" quando estoque zero

### Carrinho
- Adicionar, remover e atualizar quantidades em tempo real via HTMX
- Contador do carrinho atualizado instantaneamente no navbar (desktop e mobile)
- Acessível sem login — bloqueio apenas no checkout

### Checkout
- Formulário com dados do cliente preenchidos automaticamente
- Opção de entrega em casa ou retirada na loja
- Mapa interativo (Leaflet + OpenStreetMap) colapsável para marcar o local de entrega
- Marcador da loja visível no mapa para referência
- Geocodificação reversa — clicou no mapa, endereço preenche automaticamente
- Reset de pin e coordenadas ao entrar no checkout para evitar inconsistências
- Opções de pagamento: Dinheiro, Pix ou Cartão (online via Mercado Pago ou na entrega)

### Autenticação de clientes
- Cadastro, login e logout
- Modelo `Cliente` customizado separado do `User` do Django
- Proteção de rotas com decorator personalizado

### Meus Pedidos
- Histórico completo de pedidos do cliente
- Barra de progresso visual com status em tempo real (Pendente → Confirmado → Em entrega → Entregue)

### Painel administrativo
- Dashboard com métricas: pedidos hoje, faturamento, total de pedidos, estoque baixo
- Tabela de pedidos com itens inline em pílulas
- Atualização de status via dropdown com submit automático
- Cards responsivos no mobile (sem tabela horizontal)
- Mapa de rota por pedido com distância e tempo estimado (OSRM)
- Paginação de pedidos
- Alerta de estoque baixo (≤ 10 unidades)
- Decremento automático de estoque ao marcar pedido como entregue

### Integrações
- **Mercado Pago Checkout Pro** — pagamento online via Pix e Cartão
- **Resend** — emails transacionais (Railway bloqueia SMTP)
- **Cloudinary** — armazenamento de imagens dos produtos
- **Nominatim / OpenStreetMap** — geocodificação e mapas
- **OSRM** — cálculo de rota e tempo de entrega

---

## 🛠️ Tecnologias

| Camada | Tecnologia |
|---|---|
| Backend | Python, Django 6.0 |
| Banco de dados | SQLite (local) / PostgreSQL (produção) |
| Frontend | Tailwind CSS, HTMX, JavaScript |
| Mapas | Leaflet.js, OpenStreetMap, Nominatim, OSRM |
| Pagamentos | Mercado Pago Checkout Pro |
| Email | Resend |
| Imagens | Cloudinary |
| Deploy | Railway |

---

## 📁 Estrutura do projeto

```
aquawoman/
├── apps/
│   ├── clientes/               # Autenticação e perfil do cliente
│   │   ├── migrations/
│   │   ├── admin.py
│   │   ├── models.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── dashboard/              # Painel administrativo
│   │   ├── migrations/
│   │   ├── admin.py
│   │   ├── models.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── pagamentos/             # Integração Mercado Pago
│   │   ├── models.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── pedidos/                # Carrinho, checkout e pedidos
│   │   ├── management/
│   │   │   └── commands/
│   │   │       └── wait_for_db.py
│   │   ├── migrations/
│   │   ├── admin.py
│   │   ├── carrinho.py
│   │   ├── context_processors.py
│   │   ├── models.py
│   │   ├── urls.py
│   │   └── views.py
│   └── produtos/               # Catálogo e categorias
│       ├── migrations/
│       ├── admin.py
│       ├── models.py
│       ├── sitemaps.py
│       ├── urls.py
│       └── views.py
├── core/                       # Settings, URLs e configurações
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── static/
│   ├── css/
│   ├── img/
│   │   └── logo.png
│   └── js/
│       └── main.js
├── staticfiles/                # Arquivos estáticos coletados (produção)
├── templates/
│   ├── clientes/
│   │   ├── cadastro.html
│   │   ├── editar_conta.html
│   │   ├── login.html
│   │   └── minha_conta.html
│   ├── dashboard/
│   │   └── home.html
│   ├── partials/
│   ├── pedidos/
│   │   ├── partials/
│   │   │   ├── itens_carrinho.html
│   │   │   └── pedido_card.html
│   │   ├── carrinho.html
│   │   ├── checkout.html
│   │   ├── confirmacao.html
│   │   └── meus_pedidos.html
│   ├── produtos/
│   │   ├── partials/
│   │   │   └── lista_produtos.html
│   │   └── lista.html
│   ├── base.html
│   └── home.html
├── .env                        # Variáveis de ambiente (não versionado)
├── .gitignore
├── db.sqlite3
├── manage.py
├── mise.toml
├── Procfile
├── README.md
├── requirements.txt
├── robots.txt
└── runtime.txt
```

---

## ⚙️ Como rodar localmente

### Pré-requisitos

- Python 3.10+
- pip
- Git

### Passo a passo

**1. Clone o repositório**
```bash
git clone https://github.com/mateusmendess/aquawoman.git
cd aquawoman
```

**2. Crie e ative o ambiente virtual**
```bash
python -m venv venv

# Windows (Git Bash)
source venv/Scripts/activate

# Linux/Mac
source venv/bin/activate
```

**3. Instale as dependências**
```bash
pip install -r requirements.txt
```

**4. Configure as variáveis de ambiente**

Crie um arquivo `.env` na raiz do projeto:
```env
SECRET_KEY=sua-chave-secreta
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
CLOUDINARY_URL=cloudinary://...
MERCADOPAGO_ACCESS_TOKEN=seu-token
RESEND_API_KEY=sua-chave
EMAIL_DESTINATARIO=seu@email.com
```

**5. Rode as migrations**
```bash
python manage.py migrate
```

**6. Crie um superusuário**
```bash
python manage.py createsuperuser
```

**7. Rode o projeto**
```bash
python manage.py runserver
```

**8. Acesse no navegador**
```
http://localhost:8000
```

---

## 🔮 Próximas melhorias

- Avaliações e comentários nos produtos
- Cupons de desconto
- Notificações push de status do pedido
- Relatórios de vendas com gráficos
- App mobile (PWA)

---

## 👨‍💻 Autor

Feito por **Mateus Mendes**

[![GitHub](https://img.shields.io/badge/GitHub-mateusmendess-181717?style=for-the-badge&logo=github)](https://github.com/mateusmendess)
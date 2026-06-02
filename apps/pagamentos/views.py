import mercadopago
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import json
from apps.pedidos.views import enviar_email_pedido
from apps.pedidos.models import Pedido

sdk = mercadopago.SDK(settings.MP_ACCESS_TOKEN)

def criar_preferencia(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)

    items = []
    for item in pedido.itens.all():
        items.append({
            "title": item.produto.nome,
            "quantity": item.quantidade,
            "unit_price": float(item.preco_unitario),
        })

    preference_data = {
        "items": items,
        "payer": {
            "name": pedido.nome,
            "phone": {
                "number": pedido.telefone,
            }
        },
        "back_urls": {
            "success": f"{settings.SITE_URL}/pagamento/sucesso/{pedido.id}/",
            "failure": f"{settings.SITE_URL}/pagamento/falha/{pedido.id}/",
            "pending": f"{settings.SITE_URL}/pagamento/pendente/{pedido.id}/",
        },
        "external_reference": str(pedido.id),
    }

    if not settings.DEBUG:
        preference_data["auto_return"] = "approved"
        preference_data["notification_url"] = f"{settings.SITE_URL}/pagamento/webhook/" 

    preference_response = sdk.preference().create(preference_data)
    preference = preference_response["response"]

    if "init_point" not in preference:
        return JsonResponse(preference, status=400)

    return redirect(preference["init_point"])


def pagamento_sucesso(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    pedido.status = 'confirmado'
    pedido.save()
    enviar_email_pedido(pedido)
    return redirect(f'/confirmacao/{pedido.id}/')


def pagamento_falha(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    return redirect('/carrinho/')


def pagamento_pendente(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    return redirect(f'/confirmacao/{pedido.id}/')


@csrf_exempt
def webhook(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        if data.get('type') == 'payment':
            payment_id = data['data']['id']
            payment_info = sdk.payment().get(payment_id)
            payment = payment_info['response']
            pedido_id = payment.get('external_reference')
            status = payment.get('status')
            if pedido_id and status == 'approved':
                try:
                    pedido = Pedido.objects.get(id=pedido_id)
                    pedido.status = 'confirmado'
                    pedido.save()
                except Pedido.DoesNotExist:
                    pass
    return HttpResponse(status=200)
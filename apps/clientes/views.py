from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from .models import Cliente
import json as json_lib

def cadastro(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        telefone = request.POST.get('telefone')
        senha = request.POST.get('senha')

        if Cliente.objects.filter(email=email).exists():
            messages.error(request, 'Este email já está cadastrado.')
            return render(request, 'clientes/cadastro.html')

        cliente: Cliente = Cliente.objects.create(
            nome=nome,
            email=email,
            telefone=telefone,
            senha_hash=make_password(senha),
        )

        request.session['cliente_id'] = cliente.id
        request.session['cliente_nome'] = cliente.nome.split()[0]
        messages.success(request, f'Bem-vindo, {cliente.nome}!')
        return redirect('/')
        
    return render(request, 'clientes/cadastro.html')


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        try:
            cliente = Cliente.objects.get(email=email)
            if check_password(senha, cliente.senha_hash):
                request.session['cliente_id'] = cliente.id
                request.session['cliente_nome'] = cliente.nome.split()[0]
                messages.success(request, f'Bem-vindo, {cliente.nome}!')
                next_url = request.session.pop('next', '/')
                return redirect(next_url)
            else:
                messages.error(request, 'Senha incorreta.')
        except Cliente.DoesNotExist:
            messages.error(request, 'Email não encontrado.')

    return render(request, 'clientes/login.html')


def logout_view(request):
    request.session.flush()
    return redirect('/')


def minha_conta(request):
    cliente_id = request.session.get('cliente_id')
    if not cliente_id:
        return redirect('clientes:login')

    cliente = Cliente.objects.get(id=cliente_id)
    return render(request, 'clientes/minha_conta.html', {'cliente': cliente})

def logout_view(request):
    request.session.flush()
    messages.success(request, 'Você saiu da conta.')
    return redirect('/')

def editar_conta(request):
    cliente_id = request.session.get('cliente_id')
    if not cliente_id:
        return redirect('clientes:login')

    cliente: Cliente = Cliente.objects.get(id=cliente_id)

    if request.method == 'POST':
        nome = request.POST.get('nome', '').strip()
        telefone = request.POST.get('telefone', '').strip()
        senha_atual = request.POST.get('senha_atual', '')
        senha_nova = request.POST.get('senha_nova', '')

        if nome:
            cliente.nome = nome
            request.session['cliente_nome'] = nome.split()[0]

        if telefone:
            cliente.telefone = telefone

        endereco = request.POST.get('endereco', '').strip()
        cliente.endereco = endereco

        if senha_nova:
            if not check_password(senha_atual, cliente.senha_hash):
                messages.error(request, 'Senha atual incorreta.')
                return render(request, 'clientes/editar_conta.html', {'cliente': cliente})
            cliente.senha_hash = make_password(senha_nova)

        cliente.save()
        messages.success(request, 'Dados atualizados com sucesso!')
        return redirect('clientes:minha_conta')

    return render(request, 'clientes/editar_conta.html', {'cliente': cliente})

def salvar_localizacao(request):
    if request.method == 'POST':
        cliente_id = request.session.get('cliente_id')
        if cliente_id:
            data = json_lib.loads(request.body)
            Cliente.objects.filter(id=cliente_id).update(
                latitude=data.get('lat'),
                longitude=data.get('lng'),
            )
    from django.http import JsonResponse
    return JsonResponse({'ok': True})
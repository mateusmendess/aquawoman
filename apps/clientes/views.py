from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from .models import Cliente

def cadastro(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        telefone = request.POST.get('telefone')
        senha = request.POST.get('senha')

        if Cliente.objects.filter(email=email).exists():
            messages.error(request, 'Este email já está cadastrado.')
            return render(request, 'clientes/cadastro.html')

        Cliente.objects.create(
            nome=nome,
            email=email,
            telefone=telefone,
            senha_hash=make_password(senha),
        )

        request.session['cliente_id'] = cliente.id
        request.session['cliente_nome'] = cliente.nome
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
                request.session['cliente_nome'] = cliente.nome
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
    return redirect('/')
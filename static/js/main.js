// ── Toast de confirmação ao adicionar ao carrinho ──
document.body.addEventListener('htmx:afterRequest', function(e) {
  const path = e.detail.requestConfig && e.detail.requestConfig.path;
  if (path && path.includes('adicionar')) {
    const toast = document.getElementById('toast');
    toast.classList.remove('hidden');
    toast.classList.add('flex');
    setTimeout(() => {
      toast.classList.add('hidden');
      toast.classList.remove('flex');
    }, 2000);
  }
});

// ── Filtro de categorias — botão ativo ──
function setAtivo(btn) {
  document.querySelectorAll('.cat-btn').forEach(b => {
    b.classList.remove('bg-[#29AADF]', 'text-white');
    b.classList.add('border', 'border-[#29AADF]', 'text-[#1A3FAA]');
  });
  btn.classList.add('bg-[#29AADF]', 'text-white');
  btn.classList.remove('border', 'border-[#29AADF]', 'text-[#1A3FAA]');
}

// ── Checkout — recebimento, pagamento e botão dinâmico ──
document.addEventListener('DOMContentLoaded', function() {
  if (!document.getElementById('form-checkout')) return;

  let tipoRecebimento = 'entrega';
  let tipoPagamento = 'dinheiro';
  let tipoQuando = 'depois';

  window.selecionarRecebimento = function(el, tipo) {
    document.querySelectorAll('.ck-opt').forEach(o => o.classList.remove('active'));
    el.classList.add('active');
    tipoRecebimento = tipo;
    document.getElementById('campo-endereco').classList.toggle('hidden', tipo === 'retirada');
    document.getElementById('box-retirada').classList.toggle('hidden', tipo === 'entrega');
    document.getElementById('input-tipo-entrega').value = tipo;
    document.getElementById('quando-lbl').textContent = tipo === 'entrega' ? 'Na entrega' : 'Na retirada';
    document.getElementById('input-endereco').required = tipo === 'entrega';
    atualizarBotao();
  }

  window.selecionarPagamento = function(el, tipo) {
    document.querySelectorAll('.ck-pay').forEach(p => p.classList.remove('active'));
    el.classList.add('active');
    tipoPagamento = tipo;
    const quando = document.getElementById('quando-pagar');
    if (tipo === 'pix' || tipo === 'cartao') {
      quando.classList.remove('hidden');
      document.querySelectorAll('.ck-when')[0].classList.add('active');
      document.querySelectorAll('.ck-when')[1].classList.remove('active');
      tipoQuando = 'agora';
    } else {
      quando.classList.add('hidden');
      tipoQuando = 'depois';
    }
    atualizarBotao();
  }

  window.selecionarQuando = function(el, tipo) {
    document.querySelectorAll('.ck-when').forEach(w => w.classList.remove('active'));
    el.classList.add('active');
    tipoQuando = tipo;
    atualizarBotao();
  }

  function atualizarBotao() {
    const btn = document.getElementById('btn-confirmar');
    const info = document.getElementById('info-btn');
    const local = tipoRecebimento === 'entrega' ? 'na entrega' : 'na retirada';
    const acao = tipoRecebimento === 'entrega' ? 'Confirmar pedido →' : 'Confirmar retirada →';

    if (tipoPagamento === 'dinheiro') {
      btn.textContent = acao;
      btn.className = 'w-full bg-[#29AADF] text-white py-3 rounded-xl font-medium hover:bg-[#1A3FAA] transition';
      info.textContent = `Você paga em dinheiro ${local}`;
      document.getElementById('input-pagamento').value = 'entrega';
    } else if (tipoPagamento === 'pix') {
      if (tipoQuando === 'agora') {
        btn.textContent = 'Pagar agora via Pix →';
        btn.className = 'w-full bg-[#009EE3] text-white py-3 rounded-xl font-medium hover:bg-[#007EB5] transition';
        info.textContent = 'Você será redirecionado para pagar via Pix agora';
        document.getElementById('input-pagamento').value = 'online';
      } else {
        btn.textContent = acao;
        btn.className = 'w-full bg-[#29AADF] text-white py-3 rounded-xl font-medium hover:bg-[#1A3FAA] transition';
        info.textContent = `Você paga via Pix ${local}`;
        document.getElementById('input-pagamento').value = 'entrega';
      }
    } else if (tipoPagamento === 'cartao') {
      if (tipoQuando === 'agora') {
        btn.textContent = 'Pagar agora com Cartão →';
        btn.className = 'w-full bg-[#009EE3] text-white py-3 rounded-xl font-medium hover:bg-[#007EB5] transition';
        info.textContent = 'Você será redirecionado para pagar com cartão agora';
        document.getElementById('input-pagamento').value = 'online';
      } else {
        btn.textContent = acao;
        btn.className = 'w-full bg-[#29AADF] text-white py-3 rounded-xl font-medium hover:bg-[#1A3FAA] transition';
        info.textContent = `Você paga no cartão ${local}`;
        document.getElementById('input-pagamento').value = 'entrega';
      }
    }
  }

  window.confirmarPedido = function() {
    document.getElementById('form-checkout').submit();
  }
});
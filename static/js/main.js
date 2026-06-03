// ── Popup de confirmação ao adicionar ao carrinho ──
document.body.addEventListener('htmx:afterRequest', function(e) {
  if (e.detail.requestConfig && e.detail.requestConfig.path && e.detail.requestConfig.path.includes('adicionar')) {
    const toast = document.getElementById('toast');
    if (toast) {
      toast.style.display = 'block';
      setTimeout(function() {
        toast.style.display = 'none';
      }, 1500);
    }
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
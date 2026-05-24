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
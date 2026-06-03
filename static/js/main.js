// ── Filtro de categorias — botão ativo ──
function setAtivo(btn) {
  document.querySelectorAll('.cat-btn').forEach(b => {
    b.classList.remove('bg-[#29AADF]', 'text-white');
    b.classList.add('border', 'border-[#29AADF]', 'text-[#1A3FAA]');
  });
  btn.classList.add('bg-[#29AADF]', 'text-white');
  btn.classList.remove('border', 'border-[#29AADF]', 'text-[#1A3FAA]');
}
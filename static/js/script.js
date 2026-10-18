function toggleMenu(){
  const menu = document.getElementById('mobile-menu');
  const button = document.querySelector('.hamburger');
  const isOpen = menu.classList.toggle('open');
  button.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
}

document.addEventListener('keydown', function (e) {
  const menu = document.getElementById('mobile-menu');
  if (e.key === 'Escape' && menu && menu.classList.contains('open')) {
    toggleMenu();
    document.querySelector('.hamburger').focus();
  }
});

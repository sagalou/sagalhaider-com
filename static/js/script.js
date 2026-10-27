/**
 * Toggle the mobile navigation menu.
 * Opens or closes the menu and updates aria-expanded on the hamburger
 * button so screen readers know the menu state.
 */
function toggleMenu() {
  const menu = document.getElementById('mobile-menu');
  const button = document.querySelector('.hamburger');
  const isOpen = menu.classList.toggle('open');
  button.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
}

/**
 * Close the mobile menu with the Escape key (keyboard accessibility).
 * Focus goes back to the hamburger button so keyboard users
 * don't lose their place on the page.
 */
document.addEventListener('keydown', function (e) {
  const menu = document.getElementById('mobile-menu');
  if (e.key === 'Escape' && menu && menu.classList.contains('open')) {
    toggleMenu();
    document.querySelector('.hamburger').focus();
  }
});

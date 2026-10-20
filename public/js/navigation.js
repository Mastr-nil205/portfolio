export function initNavigation() {
  const button = document.querySelector('.menu-toggle');
  const nav = document.querySelector('#primary-nav');
  if (!button || !nav) return;
  button.hidden = false;
  const close = () => {
    button.setAttribute('aria-expanded', 'false');
    nav.classList.remove('is-open');
  };
  button.addEventListener('click', () => {
    const open = button.getAttribute('aria-expanded') !== 'true';
    button.setAttribute('aria-expanded', String(open));
    nav.classList.toggle('is-open', open);
  });
  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && button.getAttribute('aria-expanded') === 'true') {
      close();
      button.focus();
    }
  });
  nav.addEventListener('click', (event) => {
    if (event.target instanceof Element && event.target.closest('a')) close();
  });
  window.matchMedia('(min-width: 761px)').addEventListener('change', close);
}

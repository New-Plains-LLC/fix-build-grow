(function () {
  const nav = document.querySelector('.nav-links');
  const toggle = document.getElementById('nav-toggle');
  if (!nav || !toggle) return;

  const BODY_CLASS = 'nav-open';
  const FOCUSABLE = 'a, button, [tabindex]:not([tabindex="-1"])';

  function isOpen() {
    return document.body.classList.contains(BODY_CLASS);
  }

  function open() {
    document.body.classList.add(BODY_CLASS);
    toggle.setAttribute('aria-expanded', 'true');
    toggle.querySelector('.hamburger-label').textContent = 'Close menu';
    // Focus first nav link
    const first = nav.querySelector('a');
    if (first) first.focus();
  }

  function close() {
    document.body.classList.remove(BODY_CLASS);
    toggle.setAttribute('aria-expanded', 'false');
    toggle.querySelector('.hamburger-label').textContent = 'Open menu';
    toggle.focus();
  }

  toggle.addEventListener('click', function () {
    isOpen() ? close() : open();
  });

  // Close on ESC
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && isOpen()) {
      close();
    }
  });

  // Close when clicking outside the nav
  document.addEventListener('click', function (e) {
    if (!isOpen()) return;
    if (!nav.contains(e.target) && e.target !== toggle && !toggle.contains(e.target)) {
      close();
    }
  });

  // Close after clicking a nav link
  nav.addEventListener('click', function (e) {
    if (e.target.tagName === 'A') {
      close();
    }
  });

  // Trap focus inside open nav
  nav.addEventListener('keydown', function (e) {
    if (e.key !== 'Tab' || !isOpen()) return;
    const focusable = nav.querySelectorAll(FOCUSABLE);
    if (!focusable.length) return;
    const first = focusable[0];
    const last = focusable[focusable.length - 1];
    if (e.shiftKey && document.activeElement === first) {
      e.preventDefault();
      last.focus();
    } else if (!e.shiftKey && document.activeElement === last) {
      e.preventDefault();
      first.focus();
    }
  });
})();

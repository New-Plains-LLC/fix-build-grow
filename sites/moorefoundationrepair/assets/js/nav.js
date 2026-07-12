document.addEventListener('DOMContentLoaded', () => {
  const toggle = document.getElementById('nav-toggle');
  if (!toggle) return;
  toggle.addEventListener('click', () => {
    document.body.classList.toggle('nav-open');
    const expanded = document.body.classList.contains('nav-open');
    toggle.setAttribute('aria-expanded', expanded);
  });
  // Close on nav link click (mobile)
  document.querySelectorAll('.nav-links a').forEach(link => {
    link.addEventListener('click', () => {
      document.body.classList.remove('nav-open');
      toggle.setAttribute('aria-expanded', 'false');
    });
  });
});
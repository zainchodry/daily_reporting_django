// ==========================================
// Daily Reporting System — Main JS
// ==========================================

document.addEventListener('DOMContentLoaded', function () {

  // --- Toast Auto-dismiss ---
  const toasts = document.querySelectorAll('.toast');
  toasts.forEach((toast, index) => {
    // Stagger entrance
    toast.style.animationDelay = `${index * 0.15}s`;

    // Auto-dismiss after 4.5s
    setTimeout(() => {
      dismissToast(toast);
    }, 4500 + index * 150);
  });

  // Close button on toasts
  document.querySelectorAll('.toast-close').forEach(btn => {
    btn.addEventListener('click', function () {
      dismissToast(this.closest('.toast'));
    });
  });

  function dismissToast(toast) {
    if (!toast || toast.classList.contains('toast-exit')) return;
    toast.classList.add('toast-exit');
    setTimeout(() => toast.remove(), 300);
  }

  // --- Sidebar Toggle (Mobile) ---
  const sidebarToggle = document.querySelector('.sidebar-toggle');
  const sidebar = document.querySelector('.sidebar');
  const overlay = document.querySelector('.sidebar-overlay');

  if (sidebarToggle && sidebar) {
    sidebarToggle.addEventListener('click', () => {
      sidebar.classList.toggle('open');
      if (overlay) overlay.classList.toggle('active');
    });
  }

  if (overlay) {
    overlay.addEventListener('click', () => {
      sidebar.classList.remove('open');
      overlay.classList.remove('active');
    });
  }

  // --- Confirm Delete ---
  document.querySelectorAll('[data-confirm]').forEach(el => {
    el.addEventListener('click', function (e) {
      if (!confirm(this.dataset.confirm)) {
        e.preventDefault();
      }
    });
  });

  // --- Active Nav Link Highlight ---
  const currentPath = window.location.pathname;
  document.querySelectorAll('.sidebar .nav-link').forEach(link => {
    const href = link.getAttribute('href');
    if (href === currentPath || (href !== '/' && currentPath.startsWith(href))) {
      link.classList.add('active');
    }
  });

});

document.addEventListener('DOMContentLoaded', () => {
  // Toggle search box
  const toggleBtn = document.getElementById('toggleSearch');
  const searchForm = document.getElementById('searchForm');
  toggleBtn?.addEventListener('click', e => {
    e.preventDefault();
    searchForm?.classList.toggle('show');
  });
});


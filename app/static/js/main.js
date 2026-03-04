/* Les Rougon-Macquart — main.js */

/* ── Language toggle ─────────────────────────────────────────────────────── */
const LANG_KEY = 'rm_lang';

function setLang(lang) {
  document.documentElement.setAttribute('data-lang', lang);
  localStorage.setItem(LANG_KEY, lang);

  // Toggle button states
  document.querySelectorAll('[data-lang-btn]').forEach(btn => {
    btn.classList.toggle('active', btn.dataset.langBtn === lang);
  });

  // Swap text content for data-en / data-fr elements
  document.querySelectorAll('[data-en]').forEach(el => {
    el.textContent = lang === 'fr' ? (el.dataset.fr || el.dataset.en) : el.dataset.en;
  });

  // Swap placeholder
  document.querySelectorAll('[data-en-placeholder]').forEach(el => {
    el.placeholder = lang === 'fr'
      ? (el.dataset.frPlaceholder || el.dataset.enPlaceholder)
      : el.dataset.enPlaceholder;
  });

  // Notify tree if it exists
  if (window.treeSetLang) window.treeSetLang(lang);
}

// Restore on load
(function initLang() {
  const saved = localStorage.getItem(LANG_KEY) || 'en';
  setLang(saved);
})();


/* ── Live search ─────────────────────────────────────────────────────────── */
const searchInput = document.getElementById('globalSearch');
const searchDropdown = document.getElementById('searchDropdown');

let searchTimer = null;

if (searchInput) {
  searchInput.addEventListener('input', () => {
    clearTimeout(searchTimer);
    const q = searchInput.value.trim();
    if (q.length < 2) { closeDropdown(); return; }
    searchTimer = setTimeout(() => fetchSearch(q), 220);
  });

  searchInput.addEventListener('keydown', e => {
    if (e.key === 'Escape') { closeDropdown(); searchInput.blur(); }
    if (e.key === 'Enter') {
      window.location.href = `/search?q=${encodeURIComponent(searchInput.value.trim())}`;
    }
  });

  document.addEventListener('click', e => {
    if (!searchInput.contains(e.target) && !searchDropdown.contains(e.target)) {
      closeDropdown();
    }
  });
}

async function fetchSearch(q) {
  try {
    const res = await fetch(`/search/api?q=${encodeURIComponent(q)}`);
    const data = await res.json();
    renderDropdown(data.results, q);
  } catch (_) { /* silently fail */ }
}

function renderDropdown(results, q) {
  if (!results.length) { closeDropdown(); return; }
  const lang = document.documentElement.getAttribute('data-lang') || 'en';

  searchDropdown.innerHTML = results.map(r => `
    <a class="search-result-item" href="${r.url}">
      <span class="search-result-type">${r.type}</span>
      <span>
        <div class="search-result-name">${r.name}</div>
        ${r.subtitle ? `<div class="search-result-sub">${r.subtitle}</div>` : ''}
      </span>
    </a>
  `).join('') + `
    <a class="search-result-item" href="/search?q=${encodeURIComponent(q)}" style="justify-content:center;font-style:italic;opacity:0.7;font-size:0.8rem;">
      See all results →
    </a>
  `;
  searchDropdown.hidden = false;
}

function closeDropdown() {
  searchDropdown.hidden = true;
  searchDropdown.innerHTML = '';
}


/* ── Hamburger nav toggle ─────────────────────────────────────────────────── */
const navToggle = document.getElementById('navToggle');
const siteNav   = document.getElementById('siteNav');

if (navToggle && siteNav) {
  navToggle.addEventListener('click', () => {
    const open = siteNav.classList.toggle('open');
    navToggle.setAttribute('aria-expanded', open);
  });

  // Close nav when a link is tapped (mobile UX)
  siteNav.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', () => {
      siteNav.classList.remove('open');
      navToggle.setAttribute('aria-expanded', 'false');
    });
  });

  // Close nav when clicking outside header
  document.addEventListener('click', e => {
    if (!navToggle.contains(e.target) && !siteNav.contains(e.target)) {
      siteNav.classList.remove('open');
      navToggle.setAttribute('aria-expanded', 'false');
    }
  });
}

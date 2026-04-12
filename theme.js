// ══════════════════════════════════════════════════════════════════════════════
// SHARED THEME SYSTEM
// Include this file in all pages for consistent theme toggle functionality
// ══════════════════════════════════════════════════════════════════════════════

(function() {
  'use strict';

  // Load saved theme preference
  const savedTheme = localStorage.getItem('dutchapp-theme') || 'dark';

  // Apply theme immediately to prevent flash
  if (savedTheme === 'light') {
    document.documentElement.classList.add('light-mode');
    document.body.classList.add('light-mode');
  }

  // Wait for DOM to be ready
  function initThemeToggle() {
    const themeToggle = document.getElementById('themeToggle');
    const themeIcon = document.getElementById('themeIcon');
    const themeText = document.getElementById('themeText');

    if (!themeToggle) {
      console.warn('Theme toggle button not found');
      return;
    }

    // Update button state based on current theme
    function updateThemeButton(isLight) {
      if (themeIcon) themeIcon.textContent = isLight ? '🌙' : '☀️';
      if (themeText) themeText.textContent = isLight ? 'Dark' : 'Light';
    }

    // Initialize button state
    updateThemeButton(savedTheme === 'light');

    // Toggle theme
    themeToggle.addEventListener('click', () => {
      const isLight = document.body.classList.toggle('light-mode');
      document.documentElement.classList.toggle('light-mode', isLight);

      updateThemeButton(isLight);
      localStorage.setItem('dutchapp-theme', isLight ? 'light' : 'dark');
    });
  }

  // Initialize when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initThemeToggle);
  } else {
    initThemeToggle();
  }
})();

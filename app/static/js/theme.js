/**
 * theme.js — Dark/Light mode toggle for AI Meeting Intelligence System.
 * Persists choice to localStorage; falls back to prefers-color-scheme.
 * Loaded on every page via the shared <head> or nav section.
 */

(function () {
  const STORAGE_KEY = "theme";

  /**
   * Determine the initial theme: saved preference → OS preference → light.
   */
  function getInitialTheme() {
    const saved = localStorage.getItem(STORAGE_KEY);
    if (saved === "dark" || saved === "light") return saved;
    if (window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches) {
      return "dark";
    }
    return "light";
  }

  /**
   * Apply the given theme to the document.
   */
  function applyTheme(theme) {
    if (theme === "dark") {
      document.documentElement.setAttribute("data-theme", "dark");
    } else {
      document.documentElement.removeAttribute("data-theme");
    }
    updateToggleIcon(theme);
  }

  /**
   * Update the toggle button icon (sun/moon) to reflect the current theme.
   */
  function updateToggleIcon(theme) {
    const btn = document.getElementById("themeToggleBtn");
    if (!btn) return;
    const icon = btn.querySelector("i");
    if (!icon) return;
    if (theme === "dark") {
      icon.className = "bi bi-sun-fill";
      btn.setAttribute("aria-label", "Switch to light mode");
      btn.title = "Switch to light mode";
    } else {
      icon.className = "bi bi-moon-fill";
      btn.setAttribute("aria-label", "Switch to dark mode");
      btn.title = "Switch to dark mode";
    }
  }

  /**
   * Toggle between dark and light themes. Saves to localStorage.
   */
  window.toggleTheme = function () {
    const current = document.documentElement.getAttribute("data-theme") === "dark" ? "dark" : "light";
    const next = current === "dark" ? "light" : "dark";
    localStorage.setItem(STORAGE_KEY, next);
    applyTheme(next);
  };

  // Apply theme immediately on script load (before DOMContentLoaded)
  // to prevent flash of wrong theme.
  applyTheme(getInitialTheme());

  // Once DOM is ready, update the icon (button may not exist yet during initial apply).
  document.addEventListener("DOMContentLoaded", function () {
    const theme = document.documentElement.getAttribute("data-theme") === "dark" ? "dark" : "light";
    updateToggleIcon(theme);
  });
})();

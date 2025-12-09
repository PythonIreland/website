(function () {
    var storageKey = 'pythonie-theme';
    var className = 'dark';
    var root = document.documentElement;
    var toggleButton;

    function getStoredTheme() {
        try {
            return window.localStorage ? localStorage.getItem(storageKey) : null;
        } catch (e) {
            return null;
        }
    }

    function setStoredTheme(theme) {
        try {
            if (window.localStorage) {
                localStorage.setItem(storageKey, theme);
            }
        } catch (e) {
            /* ignore storage errors */
        }
    }

    function prefersDark() {
        return window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
    }

    function getActiveTheme() {
        return getStoredTheme() || (prefersDark() ? 'dark' : 'light');
    }

    function applyTheme(theme) {
        if (theme === 'dark') {
            root.classList.add(className);
        } else {
            root.classList.remove(className);
            theme = 'light';
        }
        root.dataset.theme = theme;
        updateToggle(theme);
    }

    function updateToggle(theme) {
        if (!toggleButton) return;
        var isDark = theme === 'dark';
        toggleButton.setAttribute('aria-pressed', isDark);
        toggleButton.classList.toggle('is-dark', isDark);
        var label = toggleButton.querySelector('[data-theme-label]');
        if (label) label.textContent = isDark ? 'Light' : 'Dark';
    }

    function handleToggle() {
        var isDark = root.classList.contains(className);
        var nextTheme = isDark ? 'light' : 'dark';
        applyTheme(nextTheme);
        setStoredTheme(nextTheme);
    }

    function initThemeToggle() {
        toggleButton = document.querySelector('[data-theme-toggle]');
        if (!toggleButton) {
            return;
        }
        toggleButton.addEventListener('click', handleToggle);
        applyTheme(getActiveTheme());
    }

    document.addEventListener('DOMContentLoaded', initThemeToggle);
})();

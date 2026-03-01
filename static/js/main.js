/* static/js/main.js - v51.0 Triple Theme + Ramadan */
// ===== إدارة الأوضاع الثلاثة والواجهة =====

document.addEventListener('DOMContentLoaded', function () {
    // 1. تطبيق السمة المحفوظة
    const savedTheme = localStorage.getItem('theme') || 'gold';
    applyTheme(savedTheme);

    // 2. إعداد زر تبديل الأوضاع
    setupThemeToggle();

    // 3. تفعيل القائمة الجانبية للجوال
    setupMobileSidebar();

    // 4. تفعيل العناصر النشطة في القائمة
    setupActiveNav();

    // 5. تهيئة وضع رمضان
    initRamadan();
});

// ===== وضع رمضان (دائم) =====
function initRamadan() {
    document.documentElement.setAttribute('data-ramadan', 'enabled');
    generateOrnaments();
    localStorage.setItem('ramadanMode', 'enabled');
}

window.toggleRamadan = function () {
    console.log('وضع رمضان مفعل تلقائياً! 🌙✨');
};

function generateOrnaments() {
    removeOrnaments();

    const container = document.createElement('div');
    container.className = 'ramadan-ornaments';
    document.body.prepend(container);

    // Stars
    for (let i = 0; i < 60; i++) {
        const star = document.createElement('div');
        star.className = 'star';
        const size = Math.random() * 2 + 1;
        star.style.width = `${size}px`;
        star.style.height = `${size}px`;
        star.style.left = `${Math.random() * 100}%`;
        star.style.top = `${Math.random() * 100}%`;
        star.style.setProperty('--duration', `${Math.random() * 3 + 2}s`);
        star.style.animationDelay = `${Math.random() * 5}s`;
        container.appendChild(star);
    }

    // Hanging Lanterns
    const lanternPositions = [15, 30, 70, 85];
    lanternPositions.forEach(pos => {
        const lantern = document.createElement('div');
        lantern.className = 'lantern-css';
        lantern.style.left = `${pos}%`;
        lantern.style.top = `0`;
        lantern.style.animationDelay = `${Math.random() * 2}s`;
        container.appendChild(lantern);
    });

    // Crescent Moon
    const crescent = document.createElement('div');
    crescent.className = 'crescent-festive';
    container.appendChild(crescent);
}

function removeOrnaments() {
    const container = document.querySelector('.ramadan-ornaments');
    if (container) container.remove();
}

// ===== إدارة السمات الثلاثة =====
function applyTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    document.body.classList.remove('dark-mode');

    if (theme === 'dark') {
        document.body.classList.add('dark-mode');
    }

    // حفظ السمة
    localStorage.setItem('theme', theme);
    // تنظيف المفتاح القديم
    localStorage.removeItem('darkMode');

    updateThemeIcon(theme);

    // تحديث الخلفية حسب الوضع
    updateBackground(theme);
}

// تحديث الخلفية حسب السمة
function updateBackground(theme) {
    const meshBg = document.querySelector('.mesh-background');
    const ornaments = document.querySelector('.ramadan-ornaments');

    if (theme === 'gold') {
        // الوضع الذهبي: خلفية رمضان + زينة مرئية
        document.documentElement.style.backgroundImage = "url('/static/ramadan_bg.png')";
        document.documentElement.style.backgroundSize = 'cover';
        document.documentElement.style.backgroundPosition = 'center';
        document.documentElement.style.backgroundAttachment = 'fixed';
        document.documentElement.style.backgroundRepeat = 'no-repeat';
        if (meshBg) {
            meshBg.style.background = 'radial-gradient(circle at center, #0B2B40 0%, #051622 100%)';
            meshBg.style.opacity = '0.4';
        }
        if (ornaments) ornaments.style.display = 'block';
    } else if (theme === 'dark') {
        // الوضع المظلم: فضاء عميق بدون خلفية صورة
        document.documentElement.style.backgroundImage = 'none';
        document.documentElement.style.backgroundColor = '#010814';
        if (meshBg) {
            meshBg.style.background = 'radial-gradient(circle at 30% 50%, #001d3d 0%, #010814 50%, #000 100%)';
            meshBg.style.opacity = '1';
        }
        if (ornaments) ornaments.style.display = 'block';
    } else {
        // الوضع الفاتح: تدرج سماوي نظيف
        document.documentElement.style.backgroundImage = 'none';
        document.documentElement.style.backgroundColor = '#f8fbff';
        if (meshBg) {
            meshBg.style.background = 'radial-gradient(circle at 30% 20%, #e0f7fa 0%, #f8fbff 50%, #e1f5fe 100%)';
            meshBg.style.opacity = '0.8';
        }
        // إخفاء الزينة في الوضع الفاتح
        if (ornaments) ornaments.style.display = 'none';
    }
}

// إعداد زر تبديل السمات: فاتح → مظلم → ذهبي → فاتح
function setupThemeToggle() {
    const toggle = document.querySelector('.dark-mode-toggle');
    if (!toggle) return;

    toggle.addEventListener('click', function () {
        const currentTheme = document.documentElement.getAttribute('data-theme') || 'gold';
        let nextTheme;

        if (currentTheme === 'light') {
            nextTheme = 'dark';
        } else if (currentTheme === 'dark') {
            nextTheme = 'gold';
        } else {
            // gold → light
            nextTheme = 'light';
        }

        applyTheme(nextTheme);

        // Show theme name toast
        showThemeToast(nextTheme);
    });
}

function showThemeToast(theme) {
    // Remove old toast
    const old = document.querySelector('.theme-toast');
    if (old) old.remove();

    const names = { light: '☀️ الوضع الفاتح', dark: '🌙 الوضع المظلم', gold: '👑 الوضع الذهبي' };
    const toast = document.createElement('div');
    toast.className = 'theme-toast';
    toast.textContent = names[theme] || theme;
    toast.style.cssText = `
        position: fixed; bottom: 100px; left: 50%; transform: translateX(-50%);
        background: var(--glass-bg); backdrop-filter: blur(20px);
        color: var(--text-primary); padding: 12px 30px; border-radius: 20px;
        font-weight: 800; font-size: 1.1rem; z-index: 9999;
        border: 1px solid var(--glass-border);
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        animation: toastIn 0.4s ease-out;
    `;
    document.body.appendChild(toast);
    setTimeout(() => toast.remove(), 2000);
}

// دالة تحديث الأيقونة
function updateThemeIcon(theme) {
    const icon = document.querySelector('.dark-mode-toggle i');
    if (icon) {
        if (theme === 'light') icon.className = 'fas fa-sun';
        else if (theme === 'dark') icon.className = 'fas fa-moon';
        else if (theme === 'gold') icon.className = 'fas fa-crown';
    }
}

// إعداد القائمة الجانبية
function setupMobileSidebar() {
    const sidebar = document.getElementById('sidebar');
    const menuBtn = document.querySelector('.menu-toggle-btn');

    if (menuBtn && sidebar) {
        menuBtn.addEventListener('click', function (e) {
            e.stopPropagation();
            sidebar.classList.toggle('open');
        });

        document.addEventListener('click', function (e) {
            if (sidebar.classList.contains('open') && !sidebar.contains(e.target) && !menuBtn.contains(e.target)) {
                sidebar.classList.remove('open');
            }
        });
    }
}

// دالة تفعيل الكلاس النشط
function setupActiveNav() {
    document.querySelectorAll('.nav-item').forEach(item => {
        item.addEventListener('click', function () {
            document.querySelectorAll('.nav-item').forEach(nav => nav.classList.remove('active'));
            this.classList.add('active');
            if (window.innerWidth <= 992) {
                const sidebar = document.getElementById('sidebar');
                if (sidebar) sidebar.classList.remove('open');
            }
        });
    });
}

window.toggleSidebar = function () {
    const sidebar = document.getElementById('sidebar');
    if (sidebar) sidebar.classList.toggle('open');
};

// Service Worker
if ('serviceWorker' in navigator) {
    window.addEventListener('load', function () {
        navigator.serviceWorker.register('/sw.js').then(function (registration) {
            console.log('ServiceWorker registration successful with scope: ', registration.scope);
        }, function (err) {
            console.log('ServiceWorker registration failed: ', err);
        });
    });
}

// Like Toggle
window.toggleLike = function (postId) {
    fetch(`/like_post/${postId}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
    })
        .then(response => response.json())
        .then(data => {
            if (data.error) { alert(data.error); return; }

            const btn = document.querySelector(`.like-btn[onclick="toggleLike(${postId})"]`);
            if (!btn) return;

            const countSpan = btn.querySelector('.like-count');
            if (countSpan) countSpan.textContent = data.count;

            if (data.status === 'liked') {
                btn.classList.add('active');
                btn.style.color = '#ef4444';
                btn.style.borderColor = '#ef4444';
            } else {
                btn.classList.remove('active');
                btn.style.color = 'var(--text-secondary)';
                btn.style.borderColor = 'var(--border-color)';
            }
        })
        .catch(err => console.error('Error toggling like:', err));
};

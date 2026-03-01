/* ============================================
   El-Dahih Mobile App - Application Logic
   ============================================ */

// === Configuration ===
const API_BASE = window.location.origin;
const APP_VERSION = '2.0.0';

// === State ===
let currentUser = null;
let authToken = null;
let currentLang = localStorage.getItem('app_lang') || 'ar';
let currentTheme = localStorage.getItem('app_theme') || 'light';
let selectedGender = 'male';

// === Translations ===
const LANG = {
    ar: {
        login_title: 'تسجيل الدخول',
        login_subtitle: 'أدخل بياناتك للوصول للمنصة',
        student_code: 'الكود الجامعي',
        password: 'كلمة المرور',
        login_btn: 'الدخول الآن',
        register_title: 'تسجيل حساب جديد',
        register_btn: 'تسجيل الحساب',
        no_account: 'ليس لديك حساب؟ سجل الآن',
        have_account: 'لديك حساب؟ سجل دخول',
        home_title: '<i class="fas fa-home"></i> الصفحة الرئيسية',
        courses_title: '<i class="fas fa-book"></i> المواد الدراسية',
        profile_title: 'الملف الشخصي',
        nav_home: 'الرئيسية',
        nav_courses: 'المواد',
        nav_profile: 'حسابي',
        logout: 'خروج',
        loading: 'جاري التحميل...',
        secured: 'محمي',
        male: 'ذكر',
        female: 'أنثى',
        no_posts: 'لا توجد منشورات حالياً',
        no_courses: 'لا توجد مواد مسجلة',
        no_lessons: 'لا توجد دروس في هذه المادة',
        likes: 'إعجاب',
        comments: 'تعليق',
        views: 'مشاهدة',
        view_pdf: 'عرض الملف',
        personal_info: 'المعلومات الشخصية',
        academic_info: 'المعلومات الأكاديمية',
        name: 'الاسم',
        code: 'الكود',
        phone: 'الهاتف',
        email: 'البريد',
        department: 'القسم',
        year: 'الفرقة',
        points: 'النقاط',
        courses_count: 'المواد',
        security_level: 'مستوى الأمان',
        welcome: 'مرحباً',
        point: 'نقطة',
        lesson: 'درس',
        lessons_count: 'عدد الدروس',
        login_success: 'تم تسجيل الدخول بنجاح!',
        login_error: 'فشل تسجيل الدخول',
        reg_success: 'تم التسجيل! انتظر موافقة الإدارة',
        fill_required: 'يرجى إدخال البيانات المطلوبة',
        connection_error: 'خطأ في الاتصال بالسيرفر',
        screenshot_warning: '⚠️ محاولة تصوير الشاشة!',
        security_notice: 'هذا المحتوى محمي بحقوق الملكية',
        ago_now: 'الآن',
        ago_min: 'د',
        ago_hour: 'س',
        ago_day: 'ي',
        enrolled_courses: 'المواد المسجلة'
    },
    en: {
        login_title: 'Student Login',
        login_subtitle: 'Enter your credentials to access',
        student_code: 'Student Code',
        password: 'Password',
        login_btn: 'Login Now',
        register_title: 'Create Account',
        register_btn: 'Register',
        no_account: "Don't have an account? Register",
        have_account: 'Have an account? Login',
        home_title: '<i class="fas fa-home"></i> Home',
        courses_title: '<i class="fas fa-book"></i> Courses',
        profile_title: 'My Profile',
        nav_home: 'Home',
        nav_courses: 'Courses',
        nav_profile: 'Profile',
        logout: 'Logout',
        loading: 'Loading...',
        secured: 'Secured',
        male: 'Male',
        female: 'Female',
        no_posts: 'No posts yet',
        no_courses: 'No courses enrolled',
        no_lessons: 'No lessons in this course',
        likes: 'Like',
        comments: 'Comment',
        views: 'View',
        view_pdf: 'View File',
        personal_info: 'Personal Information',
        academic_info: 'Academic Information',
        name: 'Name',
        code: 'Code',
        phone: 'Phone',
        email: 'Email',
        department: 'Department',
        year: 'Year',
        points: 'Points',
        courses_count: 'Courses',
        security_level: 'Security Level',
        welcome: 'Welcome',
        point: 'pts',
        lesson: 'lesson',
        lessons_count: 'Lessons',
        login_success: 'Login successful!',
        login_error: 'Login failed',
        reg_success: 'Registered! Waiting for admin approval',
        fill_required: 'Please fill all required fields',
        connection_error: 'Connection error',
        screenshot_warning: '⚠️ Screenshot attempt detected!',
        security_notice: 'This content is protected',
        ago_now: 'now',
        ago_min: 'm',
        ago_hour: 'h',
        ago_day: 'd',
        enrolled_courses: 'Enrolled Courses'
    }
};

// === Helper: Get translation ===
function t(key) {
    return LANG[currentLang]?.[key] || LANG['ar'][key] || key;
}

// === Initialization ===
document.addEventListener('DOMContentLoaded', () => {
    // Apply saved theme
    applyTheme(currentTheme);
    applyLang(currentLang);

    // Check saved session
    const savedUser = localStorage.getItem('user_data');
    const savedToken = localStorage.getItem('auth_token');

    // Splash screen animation
    setTimeout(() => {
        document.getElementById('splash-screen').classList.add('hide');
        document.getElementById('app').style.display = 'block';

        if (savedUser && savedToken) {
            try {
                currentUser = JSON.parse(savedUser);
                authToken = savedToken;
                enterApp();
            } catch (e) {
                showScreen('screen-login');
            }
        } else {
            showScreen('screen-login');
        }
    }, 2200);

    // Security: Detect screenshot attempts
    setupSecurityListeners();
});

// === Screen Management ===
function showScreen(screenId) {
    document.querySelectorAll('.screen').forEach(s => s.classList.remove('active'));
    const screen = document.getElementById(screenId);
    if (screen) {
        screen.classList.add('active');
    }
}

// === Tab switching inside main screen ===
function switchTab(tabId, btnEl) {
    // Hide all tabs
    document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));

    // Show selected
    const tab = document.getElementById(tabId);
    if (tab) tab.classList.add('active');
    if (btnEl) btnEl.classList.add('active');

    // Load data for tab
    if (tabId === 'tab-home') loadPosts();
    if (tabId === 'tab-courses') loadCourses();
    if (tabId === 'tab-profile') loadProfile();
}

function showTab(tabId) {
    document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
    const tab = document.getElementById(tabId);
    if (tab) tab.classList.add('active');
}

// === Authentication ===
async function doLogin() {
    const code = document.getElementById('login-code').value.trim();
    const password = document.getElementById('login-password').value;

    if (!code || !password) {
        showToast(t('fill_required'), 'warning');
        return;
    }

    const btn = document.getElementById('login-btn');
    btn.classList.add('loading');
    btn.innerHTML = '<span>' + t('loading') + '</span> <i class="fas fa-spinner fa-spin"></i>';

    try {
        const res = await fetch(`${API_BASE}/api/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            credentials: 'include',
            body: JSON.stringify({ code, password, device_id: getDeviceId() })
        });

        const data = await res.json();

        if (res.ok && data.status === 'success') {
            currentUser = data.user;
            authToken = data.token;

            // Save session
            localStorage.setItem('user_data', JSON.stringify(currentUser));
            localStorage.setItem('auth_token', authToken);

            showToast(t('login_success'), 'success');
            enterApp();
        } else {
            showToast(data.error || t('login_error'), 'error');
        }
    } catch (err) {
        showToast(t('connection_error'), 'error');
        console.error('Login error:', err);
    }

    btn.classList.remove('loading');
    btn.innerHTML = '<span>' + t('login_btn') + '</span> <i class="fas fa-arrow-left"></i>';
}

async function doRegister() {
    const code = document.getElementById('reg-code').value.trim();
    const name = document.getElementById('reg-name').value.trim();
    const password = document.getElementById('reg-password').value;
    const phone = document.getElementById('reg-phone').value.trim();
    const department = document.getElementById('reg-department').value;
    const year = document.getElementById('reg-year').value;

    if (!code || !name || !password) {
        showToast(t('fill_required'), 'warning');
        return;
    }

    showLoading(true);

    try {
        const res = await fetch(`${API_BASE}/api/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ code, full_name: name, password, phone, department, year, gender: selectedGender })
        });

        const data = await res.json();

        if (res.ok && data.status === 'success') {
            showToast(t('reg_success'), 'success');
            setTimeout(() => showScreen('screen-login'), 1500);
        } else {
            showToast(data.error || 'Error', 'error');
        }
    } catch (err) {
        showToast(t('connection_error'), 'error');
    }

    showLoading(false);
}

function doLogout() {
    localStorage.removeItem('user_data');
    localStorage.removeItem('auth_token');
    currentUser = null;
    authToken = null;
    showScreen('screen-login');
    showToast(currentLang === 'ar' ? 'تم تسجيل الخروج' : 'Logged out', 'info');
}

// === Enter App (after login) ===
function enterApp() {
    showScreen('screen-main');

    // Update header
    const greeting = currentLang === 'ar'
        ? `مرحباً ${currentUser?.full_name || ''}`
        : `Welcome ${currentUser?.full_name || ''}`;
    document.getElementById('header-name').textContent = greeting;
    document.getElementById('header-points').innerHTML = `<i class="fas fa-star"></i> <span>${currentUser?.points || 0}</span> ${t('point')}`;

    // Load home tab
    loadPosts();
}

// === Load Posts ===
async function loadPosts() {
    const container = document.getElementById('posts-container');

    try {
        const res = await fetch(`${API_BASE}/api/posts`, {
            credentials: 'include'
        });
        const posts = await res.json();

        if (!posts || posts.length === 0) {
            container.innerHTML = `
                <div class="empty-state">
                    <i class="fas fa-newspaper"></i>
                    <p>${t('no_posts')}</p>
                </div>`;
            return;
        }

        container.innerHTML = posts.map((post, i) => `
            <div class="post-card" style="animation-delay: ${i * 0.08}s">
                <div class="post-header">
                    <h3>${escapeHtml(post.title)}</h3>
                    <span class="post-time">
                        <i class="fas fa-clock"></i> ${timeAgo(post.timestamp)}
                    </span>
                </div>
                <div class="post-body">${escapeHtml(post.content)}</div>
                ${post.image_url ? `<img class="post-image" src="${API_BASE}${post.image_url}" alt="" loading="lazy">` : ''}
                ${post.pdf_url ? `
                    <div class="post-pdf-badge" onclick="openPdf('${API_BASE}${post.pdf_url}', '${escapeHtml(post.title)}')">
                        <i class="fas fa-file-pdf"></i> ${t('view_pdf')}
                    </div>` : ''}
                <div class="post-actions">
                    <button class="post-action" onclick="likePost(${post.id}, this)">
                        <i class="far fa-heart"></i> <span>${post.likes_count}</span> ${t('likes')}
                    </button>
                    <span class="post-action">
                        <i class="far fa-comment"></i> ${post.comments_count} ${t('comments')}
                    </span>
                    <span class="post-action">
                        <i class="far fa-eye"></i> ${post.views_count} ${t('views')}
                    </span>
                </div>
            </div>
        `).join('');

    } catch (err) {
        container.innerHTML = `
            <div class="empty-state">
                <i class="fas fa-wifi-slash"></i>
                <p>${t('connection_error')}</p>
            </div>`;
    }
}

// === Load Courses ===
async function loadCourses() {
    const container = document.getElementById('courses-container');

    try {
        const res = await fetch(`${API_BASE}/api/courses`, {
            credentials: 'include',
            headers: authToken ? { 'X-Auth-Token': authToken } : {}
        });

        if (res.status === 401) {
            container.innerHTML = `
                <div class="empty-state">
                    <i class="fas fa-lock"></i>
                    <p>${t('no_courses')}</p>
                </div>`;
            return;
        }

        const courses = await res.json();

        if (!courses || courses.length === 0) {
            container.innerHTML = `
                <div class="empty-state">
                    <i class="fas fa-book"></i>
                    <p>${t('no_courses')}</p>
                </div>`;
            return;
        }

        container.innerHTML = courses.map((course, i) => `
            <div class="course-card" onclick="showLessons(${course.id}, '${escapeHtml(course.name)}')" style="animation-delay: ${i * 0.08}s">
                <div class="course-icon c${i % 6}">
                    <i class="fas fa-book-open"></i>
                </div>
                <div class="course-info">
                    <h3>${escapeHtml(course.name)}</h3>
                    <span><i class="fas fa-layer-group"></i> ${course.lessons_count || 0} ${t('lesson')}</span>
                </div>
                <i class="fas fa-chevron-left course-arrow"></i>
            </div>
        `).join('');
    } catch (err) {
        container.innerHTML = `
            <div class="empty-state">
                <i class="fas fa-exclamation-triangle"></i>
                <p>${t('connection_error')}</p>
            </div>`;
    }
}

// === Show Lessons ===
async function showLessons(courseId, courseName) {
    showTab('tab-lessons');
    document.getElementById('lessons-title').textContent = courseName;
    const container = document.getElementById('lessons-container');
    container.innerHTML = '<div class="skeleton-loader"><div class="skeleton-card"></div><div class="skeleton-card"></div></div>';

    try {
        const res = await fetch(`${API_BASE}/api/lessons/${courseId}`, {
            credentials: 'include',
            headers: authToken ? { 'X-Auth-Token': authToken } : {}
        });
        const lessons = await res.json();

        if (!lessons || lessons.length === 0) {
            container.innerHTML = `
                <div class="empty-state">
                    <i class="fas fa-file-alt"></i>
                    <p>${t('no_lessons')}</p>
                </div>`;
            return;
        }

        container.innerHTML = lessons.map((lesson, i) => `
            <div class="lesson-item" onclick="openLesson(${lesson.id}, '${escapeHtml(lesson.title)}')" style="animation-delay: ${i * 0.06}s">
                <div class="lesson-icon">
                    <i class="fas ${lesson.content_type === 'pdf' ? 'fa-file-pdf' : 'fa-play-circle'}"></i>
                </div>
                <div class="lesson-info">
                    <h4>${escapeHtml(lesson.title)}</h4>
                    <span>${lesson.content_type === 'pdf' ? 'PDF' : t('lesson')}</span>
                </div>
                <i class="fas fa-chevron-left" style="color: var(--text-secondary); font-size: 12px;"></i>
            </div>
        `).join('');
    } catch (err) {
        container.innerHTML = `
            <div class="empty-state">
                <i class="fas fa-exclamation-triangle"></i>
                <p>${t('connection_error')}</p>
            </div>`;
    }
}

// === Open Lesson ===
function openLesson(lessonId, title) {
    const url = `${API_BASE}/api/secure_content/lesson/${lessonId}`;
    // For now, open the lesson's PDF in the secure viewer
    openPdf(`${API_BASE}/api/secure_content/lesson/${lessonId}`, title);
}

// === Load Profile ===
async function loadProfile() {
    const container = document.getElementById('profile-container');

    if (!currentUser) {
        container.innerHTML = '<div class="empty-state"><p>Not logged in</p></div>';
        return;
    }

    // Try to fetch latest profile data
    try {
        const res = await fetch(`${API_BASE}/api/profile`, {
            credentials: 'include',
            headers: authToken ? { 'X-Auth-Token': authToken } : {}
        });
        if (res.ok) {
            const data = await res.json();
            currentUser = { ...currentUser, ...data };
            localStorage.setItem('user_data', JSON.stringify(currentUser));
        }
    } catch (e) { }

    const u = currentUser;
    container.innerHTML = `
        <div class="profile-hero">
            <div class="profile-avatar">
                <i class="fas fa-user-graduate"></i>
            </div>
            <h2>${escapeHtml(u.full_name || '')}</h2>
            <p>${escapeHtml(u.code || '')} | ${escapeHtml(u.department || '')} - ${escapeHtml(u.year || '')}</p>
            <div class="profile-stats">
                <div class="stat-item">
                    <div class="stat-value">${u.points || 0}</div>
                    <div class="stat-label">${t('points')}</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">${u.courses_count || 0}</div>
                    <div class="stat-label">${t('courses_count')}</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">${u.pan_level || 0}</div>
                    <div class="stat-label">${t('security_level')}</div>
                </div>
            </div>
        </div>
        
        <div class="profile-section">
            <h3><i class="fas fa-user"></i> ${t('personal_info')}</h3>
            <div class="profile-info-row">
                <span class="info-label"><i class="fas fa-id-card"></i> ${t('code')}</span>
                <span class="info-value">${escapeHtml(u.code || '-')}</span>
            </div>
            <div class="profile-info-row">
                <span class="info-label"><i class="fas fa-phone"></i> ${t('phone')}</span>
                <span class="info-value">${escapeHtml(u.phone || '-')}</span>
            </div>
            <div class="profile-info-row">
                <span class="info-label"><i class="fas fa-envelope"></i> ${t('email')}</span>
                <span class="info-value">${escapeHtml(u.email || '-')}</span>
            </div>
        </div>
        
        <div class="profile-section">
            <h3><i class="fas fa-graduation-cap"></i> ${t('academic_info')}</h3>
            <div class="profile-info-row">
                <span class="info-label"><i class="fas fa-building"></i> ${t('department')}</span>
                <span class="info-value">${escapeHtml(u.department || '-')}</span>
            </div>
            <div class="profile-info-row">
                <span class="info-label"><i class="fas fa-layer-group"></i> ${t('year')}</span>
                <span class="info-value">${escapeHtml(u.year || '-')}</span>
            </div>
        </div>
        
        ${u.courses && u.courses.length > 0 ? `
        <div class="profile-section">
            <h3><i class="fas fa-book"></i> ${t('enrolled_courses')}</h3>
            ${u.courses.map(c => `
                <div class="profile-info-row">
                    <span class="info-label"><i class="fas fa-circle" style="font-size:6px"></i> ${escapeHtml(c.name)}</span>
                    <span class="info-value" style="font-size:12px;color:var(--text-secondary)">${escapeHtml(c.code)}</span>
                </div>
            `).join('')}
        </div>` : ''}
    `;
}

// === Crypto Utilities for Secure PDF ===
async function decryptAESCBC(encryptedBuffer, keyHex) {
    // Convert hex key to Uint8Array
    function hexToBytes(hex) {
        let bytes = new Uint8Array(hex.length / 2);
        for (let i = 0; i < hex.length; i += 2)
            bytes[i / 2] = parseInt(hex.substring(i, i + 2), 16);
        return bytes;
    }

    // The first 16 bytes are the IV
    const encryptedArray = new Uint8Array(encryptedBuffer);
    const iv = encryptedArray.slice(0, 16);
    const ciphertext = encryptedArray.slice(16);

    // Import the key
    const rawKey = hexToBytes(keyHex);
    const cryptoKey = await window.crypto.subtle.importKey(
        "raw", rawKey, { name: "AES-CBC" }, false, ["decrypt"]
    );

    // Decrypt (Web Crypto handles PKCS7 automatically)
    const decrypted = await window.crypto.subtle.decrypt(
        { name: "AES-CBC", iv: iv }, cryptoKey, ciphertext
    );

    return decrypted;
}

// === Secure PDF Viewer ===
async function openPdf(url, title) {
    showScreen('screen-pdf');
    document.getElementById('pdf-title').textContent = title || t('view_pdf');
    const container = document.getElementById('pdf-render-container');
    container.innerHTML = '<div style="color:white;text-align:center;padding:50px;"><i class="fas fa-spinner fa-spin fa-3x"></i><p style="margin-top:15px;font-family:Cairo;">جار الفتح وفك التشفير بصيغة آمنة...</p></div>';

    setupWatermark();

    try {
        // Fetch encrypted PDF
        const response = await fetch(url, {
            headers: { 'X-Auth-Token': authToken }
        });

        if (!response.ok) throw new Error('فشل تحميل الملف');

        const encryptedBytes = await response.arrayBuffer();

        // Decrypt using authToken (which is the AES key)
        const decryptedBytes = await decryptAESCBC(encryptedBytes, authToken);

        // Render with PDF.js
        const loadingTask = pdfjsLib.getDocument({ data: new Uint8Array(decryptedBytes) });
        const pdf = await loadingTask.promise;

        container.innerHTML = ''; // clear loading

        // Render all pages
        for (let pageNum = 1; pageNum <= pdf.numPages; pageNum++) {
            const page = await pdf.getPage(pageNum);

            // Set scale to match device width for clarity
            const viewport = page.getViewport({ scale: 1.5 });
            const screenWidth = window.innerWidth;
            const scale = (screenWidth * 0.95) / viewport.width;
            const scaledViewport = page.getViewport({ scale: scale > 1 ? scale : 1.5 });

            const canvas = document.createElement('canvas');
            canvas.style.display = 'block';
            canvas.style.margin = '0 auto 15px auto';
            canvas.style.width = '100%';
            canvas.style.maxWidth = '800px';
            canvas.style.borderRadius = '8px';

            const context = canvas.getContext('2d');
            canvas.height = scaledViewport.height;
            canvas.width = scaledViewport.width;

            container.appendChild(canvas);

            await page.render({
                canvasContext: context,
                viewport: scaledViewport
            }).promise;
        }

    } catch (err) {
        console.error('PDF Decryption/Render Error:', err);
        container.innerHTML = `<div style="color:#ff6b6b;text-align:center;padding:50px;font-family:Cairo;"><i class="fas fa-exclamation-triangle fa-3x"></i><p style="margin-top:15px;">حدث خطأ أثناء فتح الملف: ${err.message}</p></div>`;
    }
}

function closePdfViewer() {
    const container = document.getElementById('pdf-render-container');
    container.innerHTML = '';
    showScreen('screen-main');
}

function setupWatermark() {
    const overlay = document.getElementById('watermark-overlay');
    if (!currentUser) return;

    const name = currentUser.full_name || '';
    const code = currentUser.code || '';
    const text = `${name} | ${code}`;

    let html = '';
    for (let row = 0; row < 15; row++) {
        for (let col = 0; col < 5; col++) {
            const top = row * 100 + (col % 2 ? 50 : 0);
            const left = col * 250 - 50;
            html += `<div class="watermark-text" style="top:${top}px;left:${left}px">${escapeHtml(text)}</div>`;
        }
    }
    overlay.innerHTML = html;
}

// === Like Post ===
async function likePost(postId, btn) {
    if (!currentUser) return;

    try {
        const res = await fetch(`${API_BASE}/api/like/${postId}`, {
            method: 'POST',
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json',
                ...(authToken ? { 'X-Auth-Token': authToken } : {})
            }
        });

        if (res.ok) {
            const data = await res.json();
            const icon = btn.querySelector('i');
            const countSpan = btn.querySelector('span');

            if (data.status === 'liked') {
                btn.classList.add('liked');
                icon.className = 'fas fa-heart';
            } else {
                btn.classList.remove('liked');
                icon.className = 'far fa-heart';
            }
            countSpan.textContent = data.count;
        }
    } catch (e) { }
}

// === Theme ===
function toggleTheme() {
    currentTheme = currentTheme === 'light' ? 'dark' : 'light';
    applyTheme(currentTheme);
    localStorage.setItem('app_theme', currentTheme);
}

function applyTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    const icon = document.getElementById('theme-icon');
    if (icon) {
        icon.className = theme === 'dark' ? 'fas fa-sun' : 'fas fa-moon';
    }
    // Update meta theme color
    const meta = document.querySelector('meta[name="theme-color"]');
    if (meta) {
        meta.content = theme === 'dark' ? '#0a0e27' : '#f0f4f8';
    }
}

// === Language ===
function toggleLang() {
    currentLang = currentLang === 'ar' ? 'en' : 'ar';
    applyLang(currentLang);
    localStorage.setItem('app_lang', currentLang);

    // Update dynamic content
    if (currentUser) enterApp();
}

function applyLang(lang) {
    const dir = lang === 'ar' ? 'rtl' : 'ltr';
    document.documentElement.lang = lang;
    document.documentElement.dir = dir;

    // Update all data-i18n elements
    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.getAttribute('data-i18n');
        const val = t(key);
        if (val) el.innerHTML = val;
    });

    // Update placeholders
    document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
        const key = el.getAttribute('data-i18n-placeholder');
        const val = t(key);
        if (val) el.placeholder = val;
    });
}

// === Gender Selection ===
function selectGender(gender, el) {
    selectedGender = gender;
    document.querySelectorAll('.gender-option').forEach(g => g.classList.remove('active'));
    el.classList.add('active');
}

// === Password Toggle ===
function togglePassword(inputId, btn) {
    const input = document.getElementById(inputId);
    const icon = btn.querySelector('i');
    if (input.type === 'password') {
        input.type = 'text';
        icon.className = 'fas fa-eye-slash';
    } else {
        input.type = 'password';
        icon.className = 'fas fa-eye';
    }
}

// === Security Features ===
function setupSecurityListeners() {
    // Prevent context menu
    document.addEventListener('contextmenu', e => e.preventDefault());

    // Prevent keyboard shortcuts for saving/printing
    document.addEventListener('keydown', (e) => {
        if ((e.ctrlKey || e.metaKey) && (e.key === 's' || e.key === 'p' || e.key === 'u')) {
            e.preventDefault();
        }
        // Detect PrintScreen
        if (e.key === 'PrintScreen') {
            e.preventDefault();
            reportViolation('PrintScreen key pressed');
        }
    });

    // Visibility change detection (screenshot apps often trigger this)
    document.addEventListener('visibilitychange', () => {
        if (document.hidden && document.querySelector('#screen-pdf.active')) {
            // User switched away while viewing PDF - potential screenshot
            reportViolation('App backgrounded during PDF view');
        }
    });

    // Prevent drag
    document.addEventListener('dragstart', e => e.preventDefault());
}

async function reportViolation(reason) {
    showToast(t('screenshot_warning'), 'error');

    try {
        await fetch(`${API_BASE}/api/report_violation`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            credentials: 'include',
            body: JSON.stringify({ reason, details: `Device: ${navigator.userAgent}` })
        });
    } catch (e) { }
}

// === Utility Functions ===
function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function timeAgo(timestamp) {
    if (!timestamp) return '';
    const now = new Date();
    const date = new Date(timestamp);
    const diff = Math.floor((now - date) / 1000);

    if (diff < 60) return t('ago_now');
    if (diff < 3600) return Math.floor(diff / 60) + t('ago_min');
    if (diff < 86400) return Math.floor(diff / 3600) + t('ago_hour');
    return Math.floor(diff / 86400) + t('ago_day');
}

function getDeviceId() {
    let id = localStorage.getItem('device_id');
    if (!id) {
        id = 'web_' + Math.random().toString(36).substr(2, 16) + '_' + Date.now();
        localStorage.setItem('device_id', id);
    }
    return id;
}

function showToast(message, type = 'info') {
    const toast = document.getElementById('toast');
    const icons = {
        success: '<i class="fas fa-check-circle" style="color:#2ecc71"></i>',
        error: '<i class="fas fa-times-circle" style="color:#e74c3c"></i>',
        warning: '<i class="fas fa-exclamation-triangle" style="color:#f39c12"></i>',
        info: '<i class="fas fa-info-circle" style="color:#00a8e8"></i>'
    };

    toast.className = `toast ${type}`;
    toast.innerHTML = `${icons[type] || ''} ${message}`;

    // Show
    setTimeout(() => toast.classList.add('show'), 10);

    // Hide after 3s
    setTimeout(() => toast.classList.remove('show'), 3200);
}

function showLoading(show) {
    document.getElementById('loading-overlay').style.display = show ? 'flex' : 'none';
}

// === PWA Registration ===
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/sw.js').catch(() => { });
    });
}

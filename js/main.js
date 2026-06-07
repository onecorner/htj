// Smooth scroll for nav links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    });
});

// Navbar blur effect on scroll
window.addEventListener('scroll', () => {
    const navbar = document.querySelector('.navbar');
    navbar.style.background = window.pageYOffset > 50
        ? 'rgba(15, 23, 42, 0.95)'
        : 'rgba(15, 23, 42, 0.9)';
});

// Form submission via AJAX (no page redirect)
document.getElementById('orderForm')?.addEventListener('submit', async function(e) {
    e.preventDefault();
    const btn = this.querySelector('button');
    const originalText = btn.textContent;
    btn.disabled = true;
    btn.textContent = '发送中...';

    try {
        const formData = new FormData(this);
        formData.append('_next', window.location.origin + '/htj/?sent=ok');
        formData.append('_captcha', 'true');

        const resp = await fetch(this.action, { method: 'POST', body: formData });
        if (resp.ok) {
            btn.textContent = '✅ 已发送！我会尽快联系你';
            btn.style.background = '#22c55e';
            this.querySelectorAll('input, textarea').forEach(el => el.value = '');
        } else {
            throw new Error('Send failed');
        }
    } catch (e) {
        btn.textContent = '❌ 发送失败，请加微信 jzone120';
        btn.style.background = '#ef4444';
    }

    btn.disabled = false;
    setTimeout(() => {
        btn.textContent = originalText;
        btn.style.background = '';
    }, 4000);
});

// Show success toast if redirected back with ?sent=ok
if (window.location.search.includes('sent=ok')) {
    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.textContent = '✅ 消息已发送！我会在10分钟内联系你';
    document.body.appendChild(toast);
    setTimeout(() => toast.remove(), 5000);
    window.history.replaceState({}, '', window.location.pathname);
}

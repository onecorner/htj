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

// Form submission
document.getElementById('orderForm')?.addEventListener('submit', function(e) {
    e.preventDefault();
    const btn = this.querySelector('button');
    const originalText = btn.textContent;
    btn.textContent = '✅ 已收到！我会尽快联系你';
    btn.style.background = '#22c55e';
    this.querySelectorAll('input, textarea').forEach(el => el.value = '');

    setTimeout(() => {
        btn.textContent = originalText;
        btn.style.background = '';
    }, 3000);
});

// Navbar blur effect on scroll
let lastScroll = 0;
window.addEventListener('scroll', () => {
    const navbar = document.querySelector('.navbar');
    const currentScroll = window.pageYOffset;
    navbar.style.background = currentScroll > 50
        ? 'rgba(15, 23, 42, 0.95)'
        : 'rgba(15, 23, 42, 0.9)';
    lastScroll = currentScroll;
});

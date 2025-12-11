// Main JavaScript for Heart Attack Risk Analysis

// Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Hide loading spinner when image loads
document.addEventListener('DOMContentLoaded', function() {
    const plotImages = document.querySelectorAll('.plot-image');
    
    plotImages.forEach(img => {
        img.addEventListener('load', function() {
            const loadingDiv = this.parentElement.querySelector('.plot-loading');
            if (loadingDiv) {
                loadingDiv.style.display = 'none';
            }
            this.style.opacity = '1';
        });
        
        // If image is already loaded (cached)
        if (img.complete) {
            const loadingDiv = img.parentElement.querySelector('.plot-loading');
            if (loadingDiv) {
                loadingDiv.style.display = 'none';
            }
            img.style.opacity = '1';
        }
    });
});

// Add active state to navigation links
const currentPath = window.location.pathname;
document.querySelectorAll('.nav-link').forEach(link => {
    if (link.getAttribute('href') === currentPath) {
        link.style.color = 'var(--accent-color)';
        link.style.background = 'var(--glass-bg)';
    }
});

// Intersection Observer for fade-in animations
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver(function(entries) {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// Observe elements with animation
document.querySelectorAll('.card, .stat-box, .section').forEach(el => {
    observer.observe(el);
});

// Add tooltip functionality for stats
document.querySelectorAll('.stat-box').forEach(box => {
    box.addEventListener('mouseenter', function() {
        this.style.transform = 'translateY(-5px) scale(1.02)';
    });
    
    box.addEventListener('mouseleave', function() {
        this.style.transform = 'translateY(0) scale(1)';
    });
});

// Console log for debugging
console.log('%c Heart Attack Risk Analysis ', 'background: #BF124D; color: white; font-size: 20px; padding: 10px;');
console.log('Application loaded successfully!');

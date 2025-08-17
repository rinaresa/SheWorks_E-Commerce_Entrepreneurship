// Basic example script to demonstrate dynamic behavior
document.addEventListener('DOMContentLoaded', function() {
    console.log('SheWorks platform loaded');

    // Example: highlight active nav link
    const links = document.querySelectorAll('.nav-links a');
    links.forEach(link => {
        if (link.href === window.location.href) {
            link.style.color = '#ff6600';
            link.style.fontWeight = 'bold';
        }
    });
});

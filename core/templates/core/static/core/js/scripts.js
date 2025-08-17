document.addEventListener('DOMContentLoaded', function() {
    console.log('SheWorks Platform loaded successfully');

    // Example: alert message when user clicks Marketplace
    const marketplaceLink = document.querySelector('a[href*="products"]');
    if (marketplaceLink) {
        marketplaceLink.addEventListener('click', function() {
            console.log('Navigating to Marketplace...');
        });
    }
});

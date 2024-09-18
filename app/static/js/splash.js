document.addEventListener('DOMContentLoaded', () => {
    const splashScreen = document.getElementById('splash-screen');
    const splashText = document.querySelector('.splash-text');
    const splashSubtext = document.querySelector('.splash-subtext');
    // Returns list of all animated elements
    const animatedTexts = document.querySelectorAll('.animated-text');

    const initialDelay = window.globalAnimationDelay;
    const delayBetweenElements = 200; // 200ms delay between each element

    // Attach event listener to the 'Home' button in the navbar
    const homeLink = document.getElementById('home-link');
    if (homeLink) {
        homeLink.addEventListener('click', (e) => {
            sessionStorage.setItem('navbarClicked', 'true');
        });
    }

    // Get the current page URL and check session storage
    const currentPage = window.location.pathname;
    const navbarClicked = sessionStorage.getItem('navbarClicked');

    // Show splash screen only on direct entry or refresh of home page, not via navbar
    if (currentPage === '/' && !navbarClicked) {
        showSplashScreen();
    } else {
        splashScreen.style.display = 'none';
        setTimeout(() => animateTexts(), initialDelay);
    }

    // Clear navbar flag after processing
    // Needed to make sure splash shows when page is reloaded
    sessionStorage.removeItem('navbarClicked');

    function showSplashScreen() {
        splashScreen.style.display = 'flex';

        setTimeout(() => {
            splashText.classList.add('fade-in');
        }, 500);

        setTimeout(() => {
            splashSubtext.classList.add('fade-in');
        }, 1500);

        setTimeout(() => {
            splashScreen.classList.add('fade-out');
            // Start animating texts after splash screen fades out
            setTimeout(() => animateTexts(), initialDelay);
        }, 4000);
    }

    function animateTexts() {
        animatedTexts.forEach((text, index) => {
            setTimeout(() => {
                text.style.animation = `fadeInUp 1s ease forwards`;
            }, index * delayBetweenElements);
        });
    }
});
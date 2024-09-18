document.addEventListener('DOMContentLoaded', function () {
    // Typewriter effect for welcome message
    const words = ['websites', 'applications', 'solutions'];
    let wordIndex = 0;
    let charIndex = 0;
    let isDeleting = false;
    const changingText = document.getElementById('changing-text');

    function typeWriter() {
        const currentWord = words[wordIndex];
        
        if (isDeleting) {
            changingText.textContent = currentWord.substring(0, charIndex - 1);
            charIndex--;
        } else {
            changingText.textContent = currentWord.substring(0, charIndex + 1);
            charIndex++;
        }

        if (!isDeleting && charIndex === currentWord.length) {
            isDeleting = true;
            setTimeout(typeWriter, 1500); // Wait before starting to delete
        } else if (isDeleting && charIndex === 0) {
            isDeleting = false;
            wordIndex = (wordIndex + 1) % words.length;
            setTimeout(typeWriter, 500); // Wait before typing next word
        } else {
            setTimeout(typeWriter, isDeleting ? 50 : 100); // Deleting is faster than typing
        }
    }
    
    // Start the typewriter effect after the global delay
    setTimeout(() => typeWriter(), window.globalAnimationDelay);

    // PDF viewer responsiveness
    function handlePDFViewer() {
        const pdfViewer = document.getElementById('pdf-viewer');
        const pdfLink = document.getElementById('pdf-link');
        
        if (window.innerWidth <= 480) {
            pdfViewer.style.display = 'none';
            pdfLink.style.display = 'block';
        } else {
            pdfViewer.style.display = 'block';
            pdfLink.style.display = 'none';
        }
    }

    // Initial PDF viewer handling
    handlePDFViewer();

    // Update PDF viewer on window resize
    window.addEventListener('resize', handlePDFViewer);
});

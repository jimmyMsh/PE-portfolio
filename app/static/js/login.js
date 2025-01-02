document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('admin-login-form');
    const logoutBtn = document.getElementById('admin-logout');
    const errorDiv = document.getElementById('login-error');

    if (loginForm) {
        loginForm.addEventListener('submit', async function(event) {
            event.preventDefault();
            
            const passwordInput = document.getElementById('admin-password');
            const password = passwordInput.value;

            try {
                const response = await fetch(window.APP_URLS.login, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                    },
                    body: `password=${encodeURIComponent(password)}`
                });

                if (response.ok) {
                    // Redirect to home page on successful login
                    window.location.href = window.APP_URLS.home;
                } else {
                    const data = await response.json();
                    // Show error message
                    errorDiv.textContent = data.error || 'Login failed';
                    errorDiv.style.display = 'block';
                    // Clear password field
                    passwordInput.value = '';
                }
            } catch (error) {
                console.error('Login error:', error);
                errorDiv.textContent = 'Login failed. Please try again.';
                errorDiv.style.display = 'block';
            }
        });
    }

    if (logoutBtn) {
        logoutBtn.addEventListener('click', async function() {
            try {
                const response = await fetch(window.APP_URLS.logout, {
                    method: 'POST'
                });

                if (response.ok) {
                    window.location.reload();
                } else {
                    alert('Logout failed. Please try again.');
                }
            } catch (error) {
                console.error('Logout error:', error);
                alert('Logout failed. Please try again.');
            }
        });
    }
});
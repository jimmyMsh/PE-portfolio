/**
 * Handles all navbar functionality including:
 * - Burger menu toggle
 * - Outside click detection
 * - Admin logout
 * - Mobile responsive behavior
 */
document.addEventListener('DOMContentLoaded', () => {
  // Initialize burger menu functionality
  const initializeBurgerMenu = () => {
      const $navbarBurgers = Array.prototype.slice.call(document.querySelectorAll('.navbar-burger'), 0);
      
      $navbarBurgers.forEach(el => {
          el.addEventListener('click', () => {
              const target = el.dataset.target;
              const $target = document.getElementById(target);
              const $adminSection = document.querySelector('.navbar-end');
              
              // Ensure admin section stays visible
              if ($adminSection) {
                  $adminSection.style.display = 'flex';
              }
              
              el.classList.toggle('is-active');
              $target.classList.toggle('is-active');
          });
      });
  };

  // Handle clicks outside the navbar
  const handleOutsideClicks = () => {
      document.addEventListener('click', (event) => {
          const navbar = document.querySelector('.navbar-menu');
          const burger = document.querySelector('.navbar-burger');
          const adminSection = document.querySelector('.navbar-end');
          
          if (navbar.classList.contains('is-active')) {
              if (!navbar.contains(event.target) && 
                  !burger.contains(event.target) && 
                  !adminSection?.contains(event.target)) {
                  navbar.classList.remove('is-active');
                  burger.classList.remove('is-active');
              }
          }
      });
  };

  // Handle admin logout functionality
  const initializeAdminLogout = () => {
      const logoutBtn = document.getElementById('admin-logout');
      
      if (logoutBtn) {
          logoutBtn.addEventListener('click', async function() {
              try {
                  const response = await fetch('/api/admin/logout', {
                      method: 'POST'
                  });

                  if (response.ok) {
                      window.location.reload();
                  } else {
                      const data = await response.json();
                      alert(data.error || 'Logout failed. Please try again.');
                  }
              } catch (error) {
                  console.error('Logout error:', error);
                  alert('Logout failed. Please try again.');
              }
          });
      }
  };

  // Initialize all navbar functionality
  initializeBurgerMenu();
  handleOutsideClicks();
  initializeAdminLogout();
});
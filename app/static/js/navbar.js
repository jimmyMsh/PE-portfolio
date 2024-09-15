document.addEventListener('DOMContentLoaded', () => {
    const $navbarBurgers = Array.prototype.slice.call(document.querySelectorAll('.navbar-burger'), 0);
    $navbarBurgers.forEach(el => {
      el.addEventListener('click', () => {
        const target = el.dataset.target;
        const $target = document.getElementById(target);
        el.classList.toggle('is-active');
        $target.classList.toggle('is-active');
      });
    });
  
    document.addEventListener('click', (event) => {
      const navbar = document.querySelector('.navbar-menu');
      const burger = document.querySelector('.navbar-burger');
      
      if (navbar.classList.contains('is-active')) {
        if (!navbar.contains(event.target) && !burger.contains(event.target)) {
          navbar.classList.remove('is-active');
          burger.classList.remove('is-active');
        }
      }
    });
  });
const hamburger = document.querySelector('.hamburger');
const slider = document.querySelector('.slider');

hamburger.addEventListener('click', () => {
    slider.classList.toggle('active');
});


// слайдер наши партнеры
const projectsSlider = document.querySelector('.partners-swiper-container');
const myProgectsGallery = new Swiper(projectsSlider, {
    slidesPerView: 3,
    slidesPerColumnFill: 'row',
    slidesPerColumn: 1,
    slidesPerGroup: 3,
    spaceBetween: 50,
    direction: 'horizontal',



    navigation: {
        nextEl: '.swiper-button-next',
        prevEl: '.swiper-button-prev',
    },

    breakpoints: {
        300: {
            slidesPerView: 1,
            slidesPerColumn: 1,
            slidesPerGroup: 1,
        },

        577: {
            slidesPerView: 2,
            slidesPerColumn: 1,
            spaceBetween: 36,
            slidesPerGroup: 2,
        },

        769: {
            slidesPerView: 3,
            slidesPerColumn: 1,
            spaceBetween: 34,
            slidesPerGroup: 2,
        },

        1025: {
            slidesPerView: 5,
            slidesPerColumn: 1,
            spaceBetween: 34,
            slidesPerGroup: 3,
        },

        1411: {
            slidesPerView: 5,
            slidesPerColumn: 1,
            spaceBetween: 50,
            slidesPerGroup: 3,
        },
    }
});

// Маска телефона
const phoneInput = document.querySelector('input[type="tel"]');
const im = new Inputmask("+7 (999) 999-99-99");
im.mask(phoneInput);
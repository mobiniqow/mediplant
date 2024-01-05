
$(document).ready(function () {
    "use strict";
  
    /*--------------------- Hero section Owl Slider -------------------------------- */
    $('.ms-hero-slider').owlCarousel({
      margin: 0,
      loop: true,
      dots: true,
      nav: false,
      animateOut: 'fadeOut',
      smartSpeed: 1000,
      autoplay: true,
      items: 3,
      responsiveClass: true,
      responsive: {
        0: {
          items: 1,
          nav: false
        },
        992: {
          items: 2,
          margin: 30,
          nav: false
        },
        1200: {
          items: 1,
          nav: false
        },
        1367: {
          items: 1,
          nav: false
        }
      }
    });
  
    /*----------------------------- Navigation section by section --------------------*/
    $('.navs-link').on("click", function () {
      var section = $(this).attr('data-section');
      if (section == "ms-home") {
        $("#ms-main-menu-desk").removeClass("menubar-shadow");
      } else {
        $("#ms-main-menu-desk").addClass("menubar-shadow");
      }
  
      setTimeout(
        function () {
          $("." + section).siblings(".ms-slide").fadeOut().css({
            'z-index': '11',
            'transform': 'translateY(100%)'
          });
          $("#overlay_shine").fadeIn(50).css({
            'transform': 'rotate(-30deg) translateY(-150%)',
            'display': 'none',
            'z-index': '0'
          });
        }, 1000);
  
  
      $("." + section).siblings(".ms-slide").fadeOut().css({
        'z-index': '11',
        'transform': 'translateY(-100%)'
      });
      $("#overlay_shine").fadeIn(50).css({
        'transform': 'rotate(-30deg) translateY(150%)',
        'z-index': '0'
      });
  
      setTimeout(
        function () {
          // $("."+section).css("display", "block");
          $("." + section).fadeIn().css({
            'transform': 'translateY(0)',
            'display': 'block !important',
            'z-index': '12'
          });
          $("#overlay_shine").fadeIn(50).css({
            'transform': 'rotate(-30deg) translateY(150%)',
            'z-index': '2'
          });
  
        }, 500);
  
    });
  
    /*--------------------- Search Popup JS -------------------------------- */
    $('.ms-search-toggle').on("click", function () {
      $('.ms-search-popup').fadeIn();
    });
    $('.ms-search-close').on("click", function () {
      $('.ms-search-popup').fadeOut();
    });
  
    /*--------------------- Mobile menu sidebar JS -------------------------------- */
    $('.ms-site-menu-icon').on("click", function () {
      $('.ms-mobile-menu-overlay').fadeIn();
      $('.ms-mobile-menu').addClass("ms-menu-open");
    });
  
    $('.ms-mobile-menu-overlay, .ms-close-menu').on("click", function () {
      $('.ms-mobile-menu-overlay').fadeOut();
      $('.ms-mobile-menu').removeClass("ms-menu-open");
    });
  
    /*--------------------- Listing section -------------------------------- */
    $('.ms-list-item').on("mousemove", function (event) {
      var right = event.pageX - $(this).offset().right + 30;
      var top = event.pageY - $(this).offset().top + 0;
      $(this).find('.ms-list-img').css({ top: top, right: right, opacity: 1 }).show();
      // console.log (right, top);
    });
    $('#utilities').mouseout(function () {
      $('.ms-list-img').hide();
    });
  
    /*--------------------- Day of the deal Slider (offer section) -------------------------------- */
    $('.deal-owl-carousel').owlCarousel({
      loop: true,
      dots: false,
      nav: false,
      smartSpeed: 1000,
      autoplay: true,
      items: 3,
      responsiveClass: true,
      responsive: {
        0: {
          items: 1
        },
        576: {
          items: 2
        },
        768: {
          items: 2
        },
        992: {
          items: 3
        },
        1200: {
          items: 4
        },
        1367: {
          items: 5
        }
      }
    });
  
    /*--------------------- Vendor slider (Home Page) -------------------------------- */
    $('.ms-top-vendor').owlCarousel({
      margin: 30,
      loop: true,
      dots: false,
      nav: false,
      smartSpeed: 1500,
      autoplay: true,
      items: 3,
      responsiveClass: true,
      responsive: {
        0: {
          items: 1
        },
        576: {
          items: 1
        },
        768: {
          items: 2
        },
        992: {
          items: 2
        },
        1200: {
          items: 3
        },
        1400: {
          items: 4
        }
      }
    });
  
    /*--------------------- Blog slider (Home Page) -------------------------------- */
    $('.ms-blog-carousel').owlCarousel({
      margin: 30,
      loop: true,
      dots: false,
      nav: false,
      smartSpeed: 1000,
      autoplay: true,
      items: 3,
      responsiveClass: true,
      responsive: {
        0: {
          items: 1
        },
        576: {
          items: 1
        },
        768: {
          items: 2
        },
        992: {
          items: 2
        },
        1200: {
          items: 3
        },
        1400: {
          items: 3
        }
      }
    });
  
    /*----------------------------- Testimonial Slider -------------------------------- */
    $('#ms-testimonial-slider').owlCarousel({
      margin: 0,
      loop: true,
      dots: true,
      nav: false,
      animateOut: 'fadeOut',
      smartSpeed: 1000,
      autoplay: true,
      responsiveClass: true,
      responsive: {
        0: {
          items: 1
        },
        1367: {
          items: 1
        }
      }
    });
  
    /*----------------------------- Quick view modal images select js -------------------------------- */
    $(document).ready(function () {
      var firstimg = $('.quick-nav-thumb').find("img").attr("src");
      $('.quickview-main-img').html('<img class="img-responsive quick-thumb" src="' + firstimg + '" alt="product">');
    });
    $('.quick-thumb').on("click", function () {
      var thumbimg = $(this).attr("src");
      $(".quick-thumb").removeClass("ms-active");
      $(this).addClass("ms-active");
      $('.quickview-main-img').html('<img class="img-responsive quick-thumb" src="' + thumbimg + '" alt="product">');
    });
  
    $('.quick-nav-thumb').owlCarousel({
      margin: 15,
      loop: true,
      dots: false,
      nav: true,
      animateOut: 'fadeOut',
      smartSpeed: 1000,
      autoplay: true,
      responsiveClass: true,
      responsive: {
        0: {
          items: 3,
        },
        1367: {
          items: 3,
        }
      }
    });
  
    /*--------------------- Custom Cursor JS -------------------------------- */
    var ms_cursor = document.querySelector('.ms-cursor');
    var ms_cursorinner = document.querySelector('.ms-cursor-2');
    var a = document.querySelectorAll('a');
  
    document.addEventListener('mousemove', function (e) {
      var x = e.clientX;
      var y = e.clientY;
      ms_cursor.style.transform = `translate3d(calc(${e.clientX}px - 50%), calc(${e.clientY}px - 50%), 0)`
    });
  
    document.addEventListener('mousemove', function (e) {
      var x = e.clientX;
      var y = e.clientY;
      ms_cursorinner.style.left = x + 'px';
      ms_cursorinner.style.top = y + 'px';
    });
  
    document.addEventListener('mousedown', function () {
      ms_cursor.classList.add('click');
      ms_cursorinner.classList.add('ms-cursorinnerhover')
    });
  
    document.addEventListener('mouseup', function () {
      ms_cursor.classList.remove('click')
      ms_cursorinner.classList.remove('ms-cursorinnerhover')
    });
  
    a.forEach(item => {
      item.addEventListener('mouseover', () => {
        ms_cursor.classList.add('ms-hover-cursor');
      });
      item.addEventListener('mouseleave', () => {
        ms_cursor.classList.remove('ms-hover-cursor');
      });
    })
  });
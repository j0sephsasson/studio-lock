(function () {
  "use strict";

  /**
   * Easy selector helper function
   */
  const select = (el, all = false) => {
    el = el.trim()
    if (all) {
      return [...document.querySelectorAll(el)]
    } else {
      return document.querySelector(el)
    }
  }

  /**
   * Easy event listener function
   */
  const on = (type, el, listener, all = false) => {
    let selectEl = select(el, all)
    if (selectEl) {
      if (all) {
        selectEl.forEach(e => e.addEventListener(type, listener))
      } else {
        selectEl.addEventListener(type, listener)
      }
    }
  }

  /**
   * Easy on scroll event listener 
   */
  const onscroll = (el, listener) => {
    el.addEventListener('scroll', listener)
  }

  /**
   * Scrolls to an element with header offset
   */
  const scrollto = (el) => {
    let header = select('#header')
    let offset = header.offsetHeight

    if (!header.classList.contains('header-scrolled')) {
      offset -= 16
    }

    let elementPos = select(el).offsetTop
    window.scrollTo({
      top: elementPos - offset,
      behavior: 'smooth'
    })
  }

  /**
   * Header fixed top on scroll
   */
  let selectHeader = select('#header')
  if (selectHeader) {
    let headerOffset = selectHeader.offsetTop
    let nextElement = selectHeader.nextElementSibling
    const headerFixed = () => {
      if ((headerOffset - window.scrollY) <= 0) {
        selectHeader.classList.add('fixed-top')
        nextElement.classList.add('scrolled-offset')
      } else {
        selectHeader.classList.remove('fixed-top')
        nextElement.classList.remove('scrolled-offset')
      }
    }
    window.addEventListener('load', headerFixed)
    onscroll(document, headerFixed)
  }

  /**
   * Back to top button
   */
  let backtotop = select('.back-to-top')
  if (backtotop) {
    const toggleBacktotop = () => {
      if (window.scrollY > 100) {
        backtotop.classList.add('active')
      } else {
        backtotop.classList.remove('active')
      }
    }
    window.addEventListener('load', toggleBacktotop)
    onscroll(document, toggleBacktotop)
  }

  /**
   * Mobile nav toggle
   */
  on('click', '.mobile-nav-toggle', function (e) {
    select('#navbar').classList.toggle('navbar-mobile')
    this.classList.toggle('bi-list')
    this.classList.toggle('bi-x')
  })

  /**
   * Mobile nav dropdowns activate
   */
  on('click', '.navbar .dropdown > a', function (e) {
    if (select('#navbar').classList.contains('navbar-mobile')) {
      e.preventDefault()
      this.nextElementSibling.classList.toggle('dropdown-active')
    }
  }, true)

  /**
   * Scrool with ofset on links with a class name .scrollto
   */
  on('click', '.scrollto', function (e) {
    if (select(this.hash)) {
      e.preventDefault()

      let navbar = select('#navbar')
      if (navbar.classList.contains('navbar-mobile')) {
        navbar.classList.remove('navbar-mobile')
        let navbarToggle = select('.mobile-nav-toggle')
        navbarToggle.classList.toggle('bi-list')
        navbarToggle.classList.toggle('bi-x')
      }
      scrollto(this.hash)
    }
  }, true)

  /**
   * Scroll with ofset on page load with hash links in the url
   */
  window.addEventListener('load', () => {
    if (window.location.hash) {
      if (select(window.location.hash)) {
        scrollto(window.location.hash)
      }
    }
  });

  /**
   * Hero carousel indicators
   */
  let heroCarouselIndicators = select("#hero-carousel-indicators")
  let heroCarouselItems = select('#heroCarousel .carousel-item', true)

  heroCarouselItems.forEach((item, index) => {
    (index === 0) ?
    heroCarouselIndicators.innerHTML += "<li data-bs-target='#heroCarousel' data-bs-slide-to='" + index + "' class='active'></li>":
      heroCarouselIndicators.innerHTML += "<li data-bs-target='#heroCarousel' data-bs-slide-to='" + index + "'></li>"
  });

  /**
   * Skills animation
   */
  let skilsContent = select('.skills-content');
  if (skilsContent) {
    new Waypoint({
      element: skilsContent,
      offset: '80%',
      handler: function (direction) {
        let progress = select('.progress .progress-bar', true);
        progress.forEach((el) => {
          el.style.width = el.getAttribute('aria-valuenow') + '%'
        });
      }
    })
  }

  /**
   * Porfolio isotope and filter
   */
  window.addEventListener('load', () => {
    let portfolioContainer = select('.portfolio-container');
    if (portfolioContainer) {
      let portfolioIsotope = new Isotope(portfolioContainer, {
        itemSelector: '.portfolio-item',
        layoutMode: 'fitRows'
      });

      let portfolioFilters = select('#portfolio-flters li', true);

      on('click', '#portfolio-flters li', function (e) {
        e.preventDefault();
        portfolioFilters.forEach(function (el) {
          el.classList.remove('filter-active');
        });
        this.classList.add('filter-active');

        portfolioIsotope.arrange({
          filter: this.getAttribute('data-filter')
        });
        portfolioIsotope.on('arrangeComplete', function () {
          AOS.refresh()
        });
      }, true);
    }

  });

  /**
   * Initiate portfolio lightbox 
   */
  const portfolioLightbox = GLightbox({
    selector: '.portfolio-lightbox'
  });

  /**
   * Portfolio details slider
   */
  new Swiper('.portfolio-details-slider', {
    speed: 400,
    loop: true,
    autoplay: {
      delay: 5000,
      disableOnInteraction: false
    },
    pagination: {
      el: '.swiper-pagination',
      type: 'bullets',
      clickable: true
    }
  });

  /**
   * Animation on scroll
   */
  window.addEventListener('load', () => {
    AOS.init({
      duration: 1000,
      easing: 'ease-in-out',
      once: true,
      mirror: false
    })
  });

})()

function sendMail() {
  var name = document.getElementById('contact-form-name').value;
  var email = document.getElementById('contact-form-email').value;
  var subject = document.getElementById('contact-form-subject').value;
  var message = document.getElementById('contact-form-message').value;

  if (name == null || name == "", email == null || email == "", subject == null || subject == "", message == null || message == "") {
    alert("Please Fill All Required Fields");
    window.location.href = '/#contact'
  } else {
    document.getElementById('sendmailLoadBTN').style.display = 'initial';
    document.getElementById('submit-button').style.display = 'none';

    var fd = new FormData();
    fd.append('name', name);
    fd.append('email', email);
    fd.append('subject', subject);
    fd.append('message', message);

    $j.ajax({
      type: "POST",
      url: '/contact',
      data: fd,
      processData: false,
      contentType: false
    }).done(function (err, req, resp) {
      document.getElementById('sendmailLoadBTN').style.display = 'none';
      document.getElementById('contact-form-response').innerHTML = resp.responseJSON.resp;
      document.getElementById('contact-form-respdiv').style.display = 'initial';
      setTimeout(function () {
        $j('#contact-form-respdiv').fadeOut('slow');
      }, 7000);
      document.getElementById('submit-button').style.display = 'initial';
      document.getElementById('contact-form-name').value = null;
      document.getElementById('contact-form-email').value = null;
      document.getElementById('contact-form-subject').value = null;
      document.getElementById('contact-form-message').value = null;
    });
  };
};

// subscribe to newsletter
function subscribe(event) {
  event.preventDefault();

  var email = document.getElementById('subscriber-email').value;

  if (email === null || email === '') {
    alert("Please Fill All Required Fields");
    window.location.href = '/#footer'
  } else {
    document.getElementById('subBTN').style.display = 'none';
    document.getElementById('subscribe-load').style.display = 'initial';

    var fd = new FormData();
    fd.append('email', email);

    $j.ajax({
      type: "POST",
      url: '/subscribe',
      data: fd,
      processData: false,
      contentType: false
    }).done(function (err, req, resp) {
      document.getElementById('response').innerHTML = resp.responseJSON.resp;
      document.getElementById('response').style.display = 'initial';

      document.getElementById('subBTN').style.display = 'initial';
      document.getElementById('subscribe-load').style.display = 'none';

      document.getElementById('subscriber-email').value = null;
      setTimeout(function () {
        $j('#response').fadeOut('slow');
      }, 7000);
    });
  }
};

// request signup
function requestSignup(event) {
  event.preventDefault();

  var email = document.getElementById('studioEmail').value;
  var location = document.getElementById('studioLocation').value;
  var name = document.getElementById('studioName').value;

  if (email === '' || location === '' || name === '') {
    alert("Please Fill All Required Fields");
    window.location.href = '/#cta'
  } else {
    document.getElementById('request-signup-btn').style.display = 'none';
    document.getElementById('request-signup-closeModal').style.display = 'none';
    document.getElementById('request-signup-load').style.display = 'initial';

    var fd = new FormData();
    fd.append('email', email);
    fd.append('location', location);
    fd.append('name', name);

    $j.ajax({
      type: "POST",
      url: '/request_signup',
      data: fd,
      processData: false,
      contentType: false
    }).done(function (err, req, resp) {
      document.getElementById('request-signup-response').innerHTML = resp.responseJSON.resp;
      document.getElementById('request-signup-response').style.display = 'initial';

      document.getElementById('request-signup-load').style.display = 'none';
      document.getElementById('request-signup-closeModal').style.display = 'initial';
      document.getElementById('request-signup-btn').style.display = 'initial';

      document.getElementById('studioName').value = null;
      document.getElementById('studioLocation').value = null;
      document.getElementById('studioEmail').value = null;
      setTimeout(function () {
        $j('#request-signup-response').fadeOut('slow');
      }, 7000);
    });
  }
};
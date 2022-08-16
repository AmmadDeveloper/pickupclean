"use strict";

/* global $ */
window.IronWeb = window.IronWeb || {};

window.IronWeb.HomePage = function () {
  'use strict'; // Intro container positioning

  var win = $(window);
  var winHeight = win.height();
  var body = $(document.body);
  var intro = $('#order-intro');
  var logo = intro.find('.order-intro-logo');
  var title = intro.find('.order-intro-title');
  var description = intro.find('.order-intro-description');
  var replaceSlideDescription = window.IronWeb.replaceSlideDescription || '';
  var THEME_CLASSES = 'dark light';
  var HIDDEN_CLASS = 'hidden';
  intro.removeClass('full'); // Home page slides

  function formatSlideDescription(text) {
    return text.replace(/\[\[(.*)\]\]/, replaceSlideDescription);
  }

  body.vegas({
    delay: 10000,
    timer: false,
    slides: window.IronWeb.orderSlides,
    walk: function walk(index, slide) {
      body.removeClass(THEME_CLASSES).addClass(slide.theme); // title.html(slide.title);
      // description.text(formatSlideDescription(slide.description));
      // Set icon if one was assigned to the slide, hide otherwise
      // !slide.logo || !slide.logo.src
      //   ? logo.hide()
      //   : logo.show().attr({
      //       src: slide.logo.src,
      //       alt: slide.logo.alt ? slide.logo.alt : 'Icon for ' + slide.title,
      //     });
    }
  }); // Responsive time slots

  var inLargePosition = true;
  var timeSlots = $('.time-slots');
  var timeSlotRows = timeSlots.children();
  var largeTarget = timeSlots.prev();
  var smallTarget = $('#toggle-time-slots').closest('.col-md-2');

  function positionTimeSlots() {
    if (hasLargeWidth()) {
      if (!inLargePosition) {
        timeSlotRows.addClass('row');
        timeSlots.insertAfter(largeTarget);
        inLargePosition = true;
      }
    } else if (inLargePosition) {
      timeSlots.insertAfter(smallTarget);
      timeSlotRows.removeClass('row');
      inLargePosition = false;
    }
  } // Hide Vegas Slides on scroll


  function toggleVegasSlides() {
    win.on('scroll', function () {
      var slide = $('.vegas-slide');

      if ($(this).scrollTop() > winHeight * 2) {
        slide.addClass(HIDDEN_CLASS);
      } else {
        slide.removeClass(HIDDEN_CLASS);
      }
    }); // TODO: review if this needs to run on resize
    // .on('resize', function () {
    //   winHeight = $(this).height()
    // })
  } // Site links


  $('.site-links').find('.site-links__title').click(openLinkSection);

  function openLinkSection() {
    if (hasMediumWidth()) {
      return;
    }

    var title = $(this);
    title.next().slideToggle(300);
    var section = title.parent();
    section.toggleClass('open');
    var openSection = section.siblings('.open').removeClass('open');
    openSection.children('.site-links__list').slideUp(300);
  } // Utility functions


  function hasMediumWidth() {
    return Math.max(document.documentElement.clientWidth, window.innerWidth || 0) >= 768;
  }

  function hasLargeWidth() {
    return Math.max(document.documentElement.clientWidth, window.innerWidth || 0) > 992;
  } // eslint-disable-next-line no-unused-vars, TODO: See init


  function debounce(func, wait, immediate) {
    var timeout;
    return function () {
      var context = this;
      var args = arguments;

      var later = function later() {
        timeout = null;
        if (!immediate) func.apply(context, args);
      };

      var callNow = immediate && !timeout;
      clearTimeout(timeout);
      timeout = setTimeout(later, wait);
      if (callNow) func.apply(context, args);
    };
  }

  function init() {
    // TODO: review if this needs to run on resize
    // win.resize(debounce(positionTimeSlots, 150))
    positionTimeSlots();
    toggleVegasSlides();
  }

  return {
    init: init
  };
}();

$(document).ready(function () {
  'use strict';

  window.IronWeb.HomePage.init();
});
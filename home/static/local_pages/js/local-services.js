"use strict";

(function ($) {
  'use strict';

  var TABS = 'ul.service-tabs li',
      TAB_LINK = '.service-tab-link',
      TAB_CONTENT = '.service-tab-details',
      TAB_CONTENT_ID_FRAG = '#service-',
      CURRENT = 'current';

  function init() {
    $(TABS).click(function () {
      var tabId = $(this).attr('data-tab');
      $(TAB_LINK).removeClass(CURRENT);
      $(TAB_CONTENT).removeClass(CURRENT);
      $(this).addClass(CURRENT);
      $(TAB_CONTENT_ID_FRAG + tabId).addClass(CURRENT);
    });
  }

  $(document).ready(function () {
    init();
  });
})(jQuery);
"use strict";

(function ($) {
  'use strict';

  var FAQ_QUESTION = '.faq-item-question',
      FAQ_ID_ATTR = 'data-faq-id',
      FAQ_QUESTION_CLASS_PARTIAL = '.faq-question-',
      FAQ_ANSWER_CLASS_PARTIAL = '.faq-answer-',
      COLLAPSED = 'collapsed';

  function initClickHandler(id) {
    $(FAQ_QUESTION_CLASS_PARTIAL + id).click(function () {
      $(FAQ_ANSWER_CLASS_PARTIAL + id).toggle('slow');
    });
  }

  function init() {
    $(FAQ_QUESTION).each(function () {
      var id = $(this).attr(FAQ_ID_ATTR);

      if (id) {
        initClickHandler(id);
      }
    });
  }

  $(document).ready(function () {
    init();
  });
})(jQuery);
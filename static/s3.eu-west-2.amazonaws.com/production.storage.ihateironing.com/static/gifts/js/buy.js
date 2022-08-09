"use strict";

(function () {
  'use strict';

  var $giftChoices = $('.gifts-list');
  var $amountInput = $('#id_amount');
  var $chargeAmount = $('.js-charge-amount');
  var selectedClass = 'is-selected';

  function getSelectedChoice() {
    return $giftChoices.find('.' + selectedClass);
  }

  function updateChargeAmount(choice) {
    $chargeAmount.text($.trim(choice.text()));
  }

  $giftChoices.find('.gifts-list-item').click(function () {
    getSelectedChoice().removeClass(selectedClass);
    var $choice = $(this);
    $choice.addClass(selectedClass);
    $amountInput.val($choice.attr('data-value'));
    updateChargeAmount($choice);
  }); // Update the charge amount on load

  updateChargeAmount(getSelectedChoice());
})();

(function () {
  'use strict';
  /* global $: false, Stripe: false */

  var form = $('.stripe-card-form');
  var submitButton = form.find('button[type=submit]');
  var cardNumberInput = $('.card-number');

  if (!cardNumberInput.length) {
    form.submit(function () {
      submitButton.prop('disabled', true).text('Please wait...');
    });
    return;
  }

  var formErrors = form.find('.js-form-errors');
  var cardControls = {
    number: cardNumberInput,
    expiry: $('.card-expiry'),
    cvc: $('.card-cvc'),
    getValues: function getValues() {
      var expiryVals = $.payment.cardExpiryVal(this.expiry.val());
      return {
        number: this.number.val(),
        exp_month: expiryVals.month,
        exp_year: expiryVals.year,
        cvc: this.cvc.val()
      };
    }
  }; // Main

  Stripe.setPublishableKey(form.attr('data-stripe-publishable-key'));
  initForm();
  form.submit(function (event) {
    event.preventDefault();
    submitButton.prop('disabled', true);
    var originalButtonText = submitButton.text();
    submitButton.text('Please wait...');
    setError('');
    var card = cardControls.getValues();

    if (validateForm(card)) {
      Stripe.card.createToken(card, stripeResponseHandler);
    } else {
      submitButton.prop('disabled', false).text(originalButtonText);
    }
  }); // Functions

  function stripeResponseHandler(status, response) {
    if (response.error) {
      submitButton.prop('disabled', false);
      setError(response.error.message);
    } else {
      var token = response.id;
      form.append('<input type="hidden" name="stripe_token" value="' + token + '">');
      form[0].submit();
    }
  }

  function initForm() {
    cardControls.number.payment('formatCardNumber');
    cardControls.expiry.payment('formatCardExpiry');
    var last4 = form.data('cardLast4');

    if (last4) {
      cardControls.number.prop('placeholder', '•••• •••• •••• ' + last4);
    }

    if ($.fn.placeholder !== undefined) {
      $('input').placeholder();
    }
  }

  function toggleInputError(control, hasError, errorMessage) {
    var formGroup = control.parents('.mdn-form-group');
    formGroup.toggleClass('is-invalid', hasError);
    var helpBlock = formGroup.find('.mdn-form-group__help');

    if (!helpBlock.length) {
      helpBlock = $('<div class="mdn-form-group__help"></div>');
      formGroup.append(helpBlock);
    }

    if (hasError) {
      helpBlock.text(errorMessage);
    } else {
      helpBlock.text('');
    }

    return hasError;
  }

  function validateForm(card) {
    var invalidCardNumber = !$.payment.validateCardNumber(card.number);
    toggleInputError(cardControls.number, invalidCardNumber, 'Invalid card number');
    var invalidCardExpiry = !$.payment.validateCardExpiry(card.exp_month, card.exp_year);
    toggleInputError(cardControls.expiry, invalidCardExpiry, 'Invalid expiry date');
    var cardType = $.payment.cardType(card.number);
    var invalidCardCVC = !$.payment.validateCardCVC(card.cvc, cardType);
    toggleInputError(cardControls.cvc, invalidCardCVC, 'Invalid CVC');
    return form.find('.is-invalid').length === 0;
  }

  function setError(message) {
    form.find('.gifts-error').not(formErrors).empty();
    formErrors.text(message);
  }
})();
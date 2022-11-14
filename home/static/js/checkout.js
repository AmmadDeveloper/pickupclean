(function () {
  'use strict';

  var form = $('.js-form');
  var submitButton = form.find('button[type=submit]');
  var submitButtonText = submitButton.text();
  var inputs = {
    coupon: $('#id_coupon'),
    address_details: $('#id_address_details'),
    name: $('#id_name'),
    email: $('#id_email'),
    mobile_number: $('#id_mobile_number'),
    password: $('#id_password'),
    card: $('#stripe-card-element')
  };
  var fieldsToValidate = ['name', 'email', 'mobile_number', 'password', 'address_details'];
  var stripePublishableKey = 'pk_test_51LfjniBkHrOrPPqzFob0uyBP1AllpBmvNioBGMkP8dS9QcY6cKUx3umlbYq1SVB2kSi9dXxh8iDskrpSiuLSD3SN00ybrM7SIW';
  var stripe = Stripe(stripePublishableKey);
  var stripeElements = stripe.elements({

    fonts: [{
      cssSrc: 'https://fonts.googleapis.com/css?family=Montserrat:400'
    }]
  });
  var card = stripeElements.create('card', {
    hidePostalCode: true,
    style: {
      base: {
        color: '#000',
        fontSize: '13px',
        fontFamily: 'Montserrat, "Helvetica Neue", Helvetica, Arial, sans-serif',
        fontSmoothing: 'antialiased',
        fontWeight: 400,
        '::placeholder': {
          color: '#000'
        }
      },
      invalid: {
        color: '#f1645d'
      }
    }
  }); // Main

  initForm();
  form.submit(function (event) {
    event.preventDefault();
    toggleSubmitButton(false);
    validateForm().then(function (isValid) {
      if (isValid) {
        stripe.createToken(card).then(function (result) {
          if (result.error) {
            toggleSubmitButton(true);
            toggleInputError(inputs.card, false, result.error.message);
          } else {
            form.append('<input type="hidden" name="stripe_token" value="' + result.token.id + '">');
            form[0].submit();
          }
        });
      } else {
        toggleSubmitButton(true);
      }
    }, function () {
      toggleSubmitButton(true);
      toggleInputError(inputs.card, false, 'An unexpected error occurred. Please try again or contact support');
    });
  }); // Functions

  function initForm() {
    makeFieldToggle('.js-address-details-field');
    makeFieldToggle('.js-coupon-field', function (field) {
      field.displaySavings = function (savings) {
        if (savings) {
          getHelpBlock(field.formGroup).text('You are saving ' + savings + ' on this order.');
          field.formGroup.removeClass('has-error').addClass('has-success');
        } else {
          field.formGroup.removeClass('has-error has-success');
          getHelpBlock(field.formGroup).text('');
        }
      };

      field.element.on('toggle', function (event) {
        if (!event.isActive) {
          field.displaySavings('');
        }
      });
      field.input.blur(function () {
        validateCouponCode(field);
      }); // If there is an initial value, open the coupon section

      if (field.input.val()) {
        // Display any initial savings
        var couponSavings = field.element.attr('data-savings');

        if (couponSavings) {
          // Display initial coupon savings
          field.displaySavings(couponSavings);
        }
      }
    });
    card.mount(inputs.card[0]);
    card.addEventListener('change', handleCardChange);

    if ($.fn.placeholder !== undefined) {
      $('input').placeholder();
    }
  }

  function toggleSubmitButton(isEnabled) {
    submitButton.prop('disabled', !isEnabled);
    submitButton.text(isEnabled ? submitButtonText : 'Please wait...');
  } // Executed when the coupon code input's blur event fires


  function validateCouponCode(field) {
    var code = field.input.val();

    if (!code) {
      field.displaySavings('');
      return;
    }

    validateData({
      coupon: code
    }).then(function (data) {
      if (data.coupon_savings) {
        field.displaySavings(data.coupon_savings);
        return;
      }

      if (data.errors && data.errors.coupon) {
        field.formGroup.removeClass('has-success');
        toggleInputError(field.input, false, 'Unfortunately the code you entered is not valid, please try again.');
      }
    }, function () {
      toggleInputError(field.input, false, 'An error occurred. Please try again.');
    });
  }

  function handleCardChange(event) {
    if (event.error) {
      toggleInputError(inputs.card, false, event.error.message);
    } else {
      toggleInputError(inputs.card, true);
    }
  }

  function validateForm() {
    var data = {};
    fieldsToValidate.forEach(function (fieldName) {
      data[fieldName] = inputs[fieldName].val();
    });
    var coupon = inputs.coupon.val();

    if (coupon) {
      data.coupon = coupon;
    }

    return validateData(data).then(function (data) {
      var errors = data.errors || {};
      var results = fieldsToValidate.map(function (fieldName) {
        return validateField(inputs[fieldName], errors[fieldName]);
      });
      return results.indexOf(false) === -1;
    });
  }

  function validateData(data) {
    return $.post(form.attr('data-validation-url'), data);
  }

  function validateField(input, errors) {
    if (errors) {
      return toggleInputError(input, false, errors.join(', '));
    }

    return toggleInputError(input, true);
  }

  function toggleInputError(input, isValid, errorMessage) {
    var formGroup = input.closest('.form-group');
    var helpBlock = getHelpBlock(formGroup);

    if (isValid) {
      formGroup.removeClass('has-error');
      helpBlock.text('');
    } else {
      formGroup.addClass('has-error');
      helpBlock.text(errorMessage);
    }

    return isValid;
  }

  function getHelpBlock(formGroup) {
    var helpBlock = formGroup.find('.help-block');

    if (!helpBlock.length) {
      helpBlock = $('<span class="help-block"></span>');
      formGroup.append(helpBlock);
    }

    return helpBlock;
  }

  function makeFieldToggle(selector, configure) {
    var activeClass = 'is-active';
    var parent = $(selector);
    var formGroup = parent.find('.form-group');
    var field = {
      element: parent,
      button: parent.find('.js-field-toggle'),
      formGroup: formGroup,
      input: formGroup.children('input'),
      isActive: function () {
        return parent.hasClass(activeClass);
      }
    };
    field.button.click(function (event) {
      event.preventDefault();
      var isActive = field.isActive();

      if (isActive) {
        parent.removeClass(activeClass);
        field.input.val('');
      } else {
        parent.addClass(activeClass);
        field.input.focus();
      }

      parent.trigger({
        type: 'toggle',
        isActive: !isActive
      });
    });

    if (field.input.val()) {
      parent.addClass(activeClass);
    } // Allow the caller to further configure the field


    if (configure) {
      configure(field);
    }
  }
})();

(function () {
  'use strict';
  /**
   * Login modal module
   */

  var modal = $('.login.modal');

  if (!modal.length) {
    return;
  }

  var modalOptions = {
    backdrop: 'static',
    keyboard: false
  };
  var form = modal.find('form');
  var orderEmailInput = $('#id_email');
  var usernameInput = $('#auth-form-username');
  var emailRegExp = /^[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$/i;
  var emailCheckUrl = form.data('emailCheckUrl'); // Main

  usernameInput.parent().hide();
  orderEmailInput.blur(function () {
    if (emailRegExp.test(this.value)) {
      var email = this.value;
      checkEmail(email).done(function (response) {
        if (response.template) {
          modal.html(response.template);
          modal.modal(modalOptions);
        } else if (response.result) {
          usernameInput.val(email);
          modal.modal(modalOptions);
        }
      });
    }
  });

  function checkEmail(email) {
    return $.post(emailCheckUrl, {
      email: email
    });
  }
})();

(function () {
  'use strict';
  /**
   * Prices modal module
   */

  var modal = $('.prices-modal');

  if (!modal.length) {
    return;
  }

  var priceLinks = $('a[href="/prices/"]');
  var modalBody = modal.find('.modal-body');
  var contentUrl = modal.data('contentUrl');
  priceLinks.click(function (event) {
    event.preventDefault();
    modal.modal('show');
    $.get(contentUrl).done(function (content) {
      modalBody.html(content);
    }).fail(function () {
      modalBody.text('Error loading content. Please contact support.');
    });

    if ($('.navbar-toggle').is(':visible')) {
      $('.navbar-collapse').collapse('hide');
    }
  });
})();
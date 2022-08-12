"use strict";

window.IronWeb = window.IronWeb || {};

(function () {
  'use strict';
  /**
   * Postcode Anywhere integration module
   */

  var PCA_JS_URL = '//services.postcodeanywhere.co.uk/js/address-3.70.min.js';
  var PCA_CSS_URL = '//services.postcodeanywhere.co.uk/css/address-3.70.min.css';
  var scriptElement = document.currentScript || document.querySelector('[data-pca-key]');
  $.getScript(PCA_JS_URL).done(function () {
    /* global pca */
    var control = new pca.Address([{
      element: 'id_search',
      field: ''
    }, {
      element: '_line1',
      field: 'Line1'
    }, {
      element: '_line2',
      field: 'Line2',
      mode: window.pca.fieldMode.POPULATE
    }, {
      element: '_line3',
      field: 'Line3',
      mode: pca.fieldMode.POPULATE
    }, {
      element: '_line4',
      field: 'Line4',
      mode: pca.fieldMode.POPULATE
    }, {
      element: 'id_city',
      field: 'City',
      mode: pca.fieldMode.POPULATE
    }, {
      element: 'id_postcode',
      field: 'PostalCode',
      mode: pca.fieldMode.POPULATE
    }, {
      element: 'id_country',
      field: 'CountryIso2',
      mode: pca.fieldMode.POPULATE
    }], {
      key: scriptElement.getAttribute('data-pca-key'),
      search: {
        countries: scriptElement.getAttribute('data-pca-country')
      },
      bar: {
        visible: false
      },
      suppressAutocomplete: false
    });
    control.listen('results', function (results) {
      if (results.length === 1 && results[0].Type !== 'Address') {
        control.select(results[0]);
      }
    });
    control.listen('populate', function (address, variations) {
      $.Topic('pca.address').publish(address, variations);
    });
    control.listen('search', function () {
      $.Topic('pca.search').publish();
    });
  }); // Download the CSS

  var link = document.createElement('link');
  link.rel = 'stylesheet';
  link.href = PCA_CSS_URL;
  document.getElementsByTagName('head')[0].appendChild(link);
})();

window.IronWeb.initCreateAddressModal = function (createdCallback) {
  /**
   * User address module
   */
  var modal = $('.address.modal');
  var newAddressForm = modal.find('form');
  var createAddressUrl = newAddressForm.prop('action');
  var submitButton = newAddressForm.find('button[type=submit]');
  var addressDisplay = newAddressForm.find('.found-address');
  newAddressForm.submit(function (event) {
    event.preventDefault();
    $.post(createAddressUrl, newAddressForm.serialize()).done(function (data) {
      if (data.errors) {
        showFormError();
      }

      if (typeof createdCallback === 'function') {
        createdCallback(data);
      }

      modal.modal('hide');
    }).fail(function () {
      showFormError();
    });
  });
  modal.on('hide.bs.modal', function () {
    newAddressForm[0].reset();
    clearAddressForm();
  });
  $.Topic('pca.address').subscribe(function (address) {
    submitButton.prop('disabled', false);
    var fields = ['FormattedLine1', 'FormattedLine2', 'FormattedLine3', 'FormattedLine4', 'City', 'PostalCode'];
    var parts = [];
    fields.forEach(function (field) {
      if (address[field]) {
        parts.push(address[field]);
      }
    });
    addressDisplay.text(parts.join(', '));
  });
  $.Topic('pca.search').subscribe(clearAddressForm);

  function clearAddressForm() {
    submitButton.prop('disabled', true);
    addressDisplay.text('');
  }

  function showFormError() {
    window.alert('Error adding address. Please try again or contact support.');
  }

  return modal;
};
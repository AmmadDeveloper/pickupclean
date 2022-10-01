"use strict";

function _slicedToArray(arr, i) { return _arrayWithHoles(arr) || _iterableToArrayLimit(arr, i) || _nonIterableRest(); }

function _nonIterableRest() { throw new TypeError("Invalid attempt to destructure non-iterable instance"); }

function _iterableToArrayLimit(arr, i) { if (!(Symbol.iterator in Object(arr) || Object.prototype.toString.call(arr) === "[object Arguments]")) { return; } var _arr = []; var _n = true; var _d = false; var _e = undefined; try { for (var _i = arr[Symbol.iterator](), _s; !(_n = (_s = _i.next()).done); _n = true) { _arr.push(_s.value); if (i && _arr.length === i) break; } } catch (err) { _d = true; _e = err; } finally { try { if (!_n && _i["return"] != null) _i["return"](); } finally { if (_d) throw _e; } } return _arr; }

function _arrayWithHoles(arr) { if (Array.isArray(arr)) return arr; }

function ownKeys(object, enumerableOnly) { var keys = Object.keys(object); if (Object.getOwnPropertySymbols) { var symbols = Object.getOwnPropertySymbols(object); if (enumerableOnly) symbols = symbols.filter(function (sym) { return Object.getOwnPropertyDescriptor(object, sym).enumerable; }); keys.push.apply(keys, symbols); } return keys; }

function _objectSpread(target) { for (var i = 1; i < arguments.length; i++) { var source = arguments[i] != null ? arguments[i] : {}; if (i % 2) { ownKeys(Object(source), true).forEach(function (key) { _defineProperty(target, key, source[key]); }); } else if (Object.getOwnPropertyDescriptors) { Object.defineProperties(target, Object.getOwnPropertyDescriptors(source)); } else { ownKeys(Object(source)).forEach(function (key) { Object.defineProperty(target, key, Object.getOwnPropertyDescriptor(source, key)); }); } } return target; }

function _defineProperty(obj, key, value) { if (key in obj) { Object.defineProperty(obj, key, { value: value, enumerable: true, configurable: true, writable: true }); } else { obj[key] = value; } return obj; }

window.IronWeb = window.IronWeb || {}; // TODO: Remove this setTimeout wrap hack later. This is a workaround to fix a race condition on script loading in Firefox. This won't be needed once improve our JS build process. https://3.basecamp.com/3419512/buckets/11014121/todos/4158743454

setTimeout(function () {
  'use strict';

  var Segment = {
    PICKUP: 'pickup',
    DROPOFF: 'dropoff'
  };
  var timeSlotsButton = makeTimeSlotsButton('#toggle-time-slots');
  var timeSlotsContainer = document.querySelector('.time-slots');
  var form = timeSlotsContainer.closest('form');
  var config = JSON.parse(form.dataset.config);
  var submitButton = form.querySelector('button[type=submit]');
  var inputs = form.elements;
  var timeSlots = makeTimeSlotsManager(config);
  var timeSlotPicker = window.IronWeb.TimeSlotPicker(timeSlotsContainer, _objectSpread({}, timeSlots.getPickerConfig(), {
    onSelect: function onSelect(_ref) {
      var segment = _ref.segment,
          timeSlot = _ref.timeSlot,
          selectionMode = _ref.selectionMode;
      timeSlots.select(segment, timeSlot);

      if (preselectTimeSlots && segment === Segment.DROPOFF) {
        confirmTimeSlots(); // Don't confirm on selection after the slots have been pre-selected

        preselectTimeSlots = false;
      } else if (selectionMode === 'auto') {
        if (timeSlots.areDisplayed()) {
          timeSlots.confirm(segment);
        } else if (segment === Segment.DROPOFF) {
          timeSlots.confirm();
          timeSlots.display();
        }
      }
    },
    onSubmit: function onSubmit(_ref2) {
      var segment = _ref2.segment,
          timeSlot = _ref2.timeSlot,
          selectionMode = _ref2.selectionMode;
      timeSlots.select(segment, timeSlot);

      if (segment === Segment.DROPOFF) {
        var shouldSubmitForm = selectionMode === 'auto';
        confirmTimeSlots(shouldSubmitForm);
      }
    },
    onClose: function onClose() {
      hidePicker();
      timeSlotsButton.enable();
    },
    onError: function onError(_ref3) {
      var error = _ref3.error;

      if (error.code === 'address_not_served') {
        handleUnservedAddress();
      }
    }
  }));
  var preselectTimeSlots = !!config.preselect;
  var interactionScrollTarget;
  var queryManager;

  if (localStorage.getItem('address') && document.getElementById('id_address_line1')) {
    // Only fill from localStorage if address form exists as it's different for users who have already ordered
    var storedAddress = JSON.parse(localStorage.getItem('address'));
    document.getElementById('id_address_line1').value = storedAddress.Line1;
    document.getElementById('id_address_line2').value = storedAddress.Line2;
    document.getElementById('id_address_line3').value = storedAddress.Line3;
    document.getElementById('id_address_line4').value = storedAddress.Line4;
    document.getElementById('id_city').value = storedAddress.City;
    document.getElementById('id_country').value = storedAddress.CountryIso2;
    document.getElementById('id_postcode').value = storedAddress.PostalCode;
    timeSlotsButton.enable();
  } // Main
  // Initialise the the query params manager based on the context of the form.
  // The query manager is used to provide the query parameters the time slot
  // picker will use when making API requests. The main parameters are related
  // to a user's address, which is selected in different ways depending on
  // whether the user is a new customer, an existing customer, or rescheduling
  // an existing order.


  if (config.query_params) {
    // When rescheduling, forced query params are included in the template's
    // JSON configuration.
    queryManager = makeQueryManager(function () {
      return {
        getParams: function getParams() {
          return config.query_params;
        }
      };
    });
  } else if (inputs.address) {
    // Returning customers choose addresses using a select widget
    queryManager = makeQueryManager(initAddressSelect);
  } else {
    // New customers use the third party Loqate widget to search for addresses
    queryManager = makeQueryManager(initAddressSearch);
  }

  timeSlotsButton.addEventListener('click', function () {
    if (timeSlotsButton.isDisabled()) {
      if (!queryManager.hasAddress()) {
        // TODO: Fix this message depending on the current address mode
        window.alert('Enter a postcode first.');
      }

      return;
    }

    showPicker(Segment.PICKUP);

    if (timeSlots.areSelected()) {
      timeSlots.display();
    }
  }); // Add click handlers for selected time slot displays

  timeSlots.addLabelClickHandler(showPicker);
  preventAutofill();
  form.addEventListener('submit', function () {
    submitButton.disabled = true;
    addGAClientIdInput(form);
  }); // Query manager initialisers. These functions are called by the query manager
  // and must return a configuration for it to use. They also perform side
  // effects by setting up widgets. These are ultimately the sources of the
  // address-related query params.

  function initAddressSearch() {
    var getParams = function getParams() {
      var postcode = inputs.postcode.value;
      var country = inputs.country.value;

      if (postcode && country) {
        return {
          postcode: postcode,
          country: country
        };
      }
    };

    if (!inputs.postcode.value) {
      // An address has not yet been selected via search so disabled the button;
      timeSlotsButton.disable();
    } // The address preview manager shows and hides a widget displaying the
    // selceted address after a search.


    var addressPreview = function () {
      var search = form.querySelector('.js-address-search');

      if (!search) {
        // If the search element isn't find, return  a no-op implementation
        var noop = function noop() {};

        return {
          show: noop,
          reset: noop
        };
      }

      var preview = search.querySelector('.js-address-preview');
      var input = search.querySelector('.js-address-preview-input');
      var readyClass = 'is-ready';
      var activeClass = 'is-active';

      if (input.value) {
        preview.textContent = input.value;
      }

      return {
        show: function show(value) {
          search.classList.add(readyClass);
          input.value = value;
          preview.textContent = value;
          preview.classList.add(activeClass);
          window.setTimeout(function () {
            preview.classList.remove(activeClass);
          }, 1500);
        },
        reset: function reset() {
          input.value = '';
          search.classList.remove(readyClass);
          preview.classList.remove(activeClass);
        }
      };
    }(); // Handle events from the address search widget


    $.Topic('pca.address').subscribe(function (address) {
      // An address was selected using the third party search widget
      timeSlotsButton.enable();
      addressPreview.show(address.Label);
      localStorage.setItem('address', JSON.stringify(address));
    });
    $.Topic('pca.search').subscribe(function () {
      // A new search has started using the third party widget
      if (!timeSlotsContainer.classList.contains('no-hide') && timeSlotPicker.isVisible()) {
        hidePicker();
      }

      timeSlots.hide();
      timeSlotsButton.disable();
      addressPreview.reset();
    });
    return {
      getParams: getParams
    };
  }

  function initAddressSelect() {
    var getParams = function getParams() {
      var addressId = inputs.address.value;

      if (addressId) {
        return {
          address: addressId
        };
      }
    };

    var selectForAddress = function selectForAddress() {
      var params = getParams();

      if (params) {
        timeSlotPicker.select(params);
      }
    }; // When the address select element's value changes, search for availability
    // to validate the current selections.


    inputs.address.addEventListener('change', function () {
      if (inputs.address.value) {
        if (timeSlotPicker.isVisible()) {
          // Update the address
          showPicker(Segment.PICKUP);
        } else if (timeSlots.areSelected()) {
          selectForAddress();
        }
      }
    }); // If the preselect configuration option is set, select availability before
    // showing the user interacts with the form.

    if (preselectTimeSlots) {
      selectForAddress();
    }

    return {
      getParams: getParams
    };
  } // Functions


  function makeQueryManager(configure) {
    // A `configure` function is used to allow context-dependent set up of
    // different widgets that provide the address-related query params.
    var _configure = configure(),
        getParams = _configure.getParams;

    var hasAddress = function hasAddress() {
      var params = getParams();
      return !!(params && (params.postcode && params.country || params.id));
    };

    return {
      getParams: getParams,
      hasAddress: hasAddress
    };
  }

  function makeTimeSlotsManager(config) {
    var _timeSlots;

    var selectedClass = 'time-slots-selected';
    var timeSlots = (_timeSlots = {}, _defineProperty(_timeSlots, Segment.PICKUP, {
      dateInput: inputs.pickup_date,
      timeSlotInput: inputs.pickup_time_slot,
      labelElement: form.querySelector('.js-selected-pickup'),
      selection: config.pickup || null
    }), _defineProperty(_timeSlots, Segment.DROPOFF, {
      dateInput: inputs.dropoff_date,
      timeSlotInput: inputs.dropoff_time_slot,
      labelElement: form.querySelector('.js-selected-dropoff'),
      selection: config.dropoff || null
    }), _timeSlots);
    var pickerConfig = {
      apiUrl: config.search_url,
      initialValues: {
        pickup: config.pickup && config.pickup.value,
        dropoff: config.dropoff && config.dropoff.value
      },
      rightButtonText: submitButton.textContent
    };

    if (config.picker_display_mode) {
      pickerConfig.displayMode = config.picker_display_mode;
    }

    var addLabelClickHandler = function addLabelClickHandler(handler) {
      Object.entries(timeSlots).forEach(function (_ref4) {
        var _ref5 = _slicedToArray(_ref4, 2),
            segment = _ref5[0],
            labelElement = _ref5[1].labelElement;

        labelElement.addEventListener('click', function () {
          return handler(segment);
        });
      });
    };

    var select = function select(segment, selectedValue) {
      timeSlots[segment].selection = selectedValue;
    };

    var isSelected = function isSelected(segment) {
      return !!timeSlots[segment].selection;
    };

    var confirmSegment = function confirmSegment(segment) {
      var _timeSlots$segment = timeSlots[segment],
          dateInput = _timeSlots$segment.dateInput,
          timeSlotInput = _timeSlots$segment.timeSlotInput,
          labelElement = _timeSlots$segment.labelElement,
          selection = _timeSlots$segment.selection;
      dateInput.value = selection.date;
      timeSlotInput.value = selection.id;
      labelElement.querySelector('.js-selected-label').textContent = selection.full_label;
    };

    var confirm = function confirm(segment) {
      if (segment) {
        confirmSegment(segment);
      } else {
        confirmSegment(Segment.PICKUP);
        confirmSegment(Segment.DROPOFF);
      }
    };

    var init = function init() {
      if (config.pickup) {
        confirmSegment(Segment.PICKUP);

        if (config.dropoff) {
          confirmSegment(Segment.DROPOFF);
        }
      }
    };

    init();
    return {
      getPickerConfig: function getPickerConfig() {
        return pickerConfig;
      },
      select: select,
      areSelected: function areSelected() {
        return Object.values(Segment).every(isSelected);
      },
      confirm: confirm,
      addLabelClickHandler: addLabelClickHandler,
      display: function display() {
        return form.classList.add(selectedClass);
      },
      hide: function hide() {
        return form.classList.remove(selectedClass);
      },
      areDisplayed: function areDisplayed() {
        return form.classList.contains(selectedClass);
      }
    };
  }

  function makeTimeSlotsButton(selector) {
    var button = document.querySelector(selector);
    var _isDisabled = false;
    return {
      disable: function disable() {
        _isDisabled = true;
      },
      enable: function enable() {
        _isDisabled = false;
      },
      isDisabled: function isDisabled() {
        return _isDisabled;
      },
      addEventListener: function addEventListener() {
        if (button) {
          button.addEventListener.apply(button, arguments);
        }
      }
    };
  }

  function scrollToInteractionTarget() {
    if (interactionScrollTarget === undefined) {
      interactionScrollTarget = document.querySelector('[data-order-form-scroll-target]');
    }

    if (interactionScrollTarget) {
      var offset = parseInt(interactionScrollTarget.dataset.orderFormScrollTarget) || 0;
      var top = interactionScrollTarget.getBoundingClientRect().top + window.pageYOffset - document.body.clientTop + offset;
      window.requestAnimationFrame(function () {
        return window.scroll({
          top: top,
          behavior: 'smooth'
        });
      });
    }
  }

  function showPicker(segment) {
    timeSlotsButton.disable();
    submitButton.disabled = true;
    var params = queryManager.getParams();
    timeSlotPicker.show(params, segment);
    timeSlotsContainer.classList.add('is-active');
    scrollToInteractionTarget();
  }

  function hidePicker() {
    timeSlotPicker.hide();
    timeSlotsContainer.classList.remove('is-active');
    submitButton.disabled = false;
    timeSlotsButton.disable();
  }

  function confirmTimeSlots(shouldSubmitForm) {
    timeSlots.confirm();

    if (shouldSubmitForm) {
      submitForm();
    } else {
      hidePicker();
      timeSlots.display();
    }
  }

  function submitForm() {
    // TODO: use requestSubmit() when it's better supported
    var isDisabled = submitButton.disabled;
    submitButton.disabled = false;
    submitButton.click();
    submitButton.disabled = isDisabled;
  }

  function handleUnservedAddress() {
    if (!inputs.postcode) {
      hidePicker();
      timeSlots.hide();
    }

    $('.unserved-area').modal();

    if (document.querySelector('#unserved-area-form-postcode') && inputs.postcode) {
      document.querySelector('#unserved-area-form-postcode').value = inputs.postcode.value;
    }

    if (document.querySelector('#unserved-area-form-country') && inputs.country) {
      document.querySelector('#unserved-area-form-country').value = inputs.country.value;
    }

    document.querySelector('#unserved-area-form').addEventListener('submit', function (e) {
      e.preventDefault();
      var formData = new FormData(e.target);
      return fetch(e.target.action, {
        method: 'POST',
        body: formData
      }).then(function (response) {
        return response.json();
      }).then(function (data) {
        var el = document.querySelector('.modal-body');

        if (data.status == 'ERROR') {
          el.innerHTML = '<h2>Error</h2><p>' + data.errors.join('<br />') + '</p>';
        } else {
          el.innerHTML = '<h2>Thank you</h2><p>We’ll be in touch when we reach your area.</p>';
        }
      });
    }, false);

    if (inputs.postcode) {
      inputs.postcode.value = '';
      inputs.country.value = '';
      inputs.address_line1.value = ''; // Simulate a new search so the search address mode fully resets

      $.Topic('pca.search').publish();
    }
  }

  function getGAClientId() {
    try {
      if ('ga' in window) {
        var trackers = window.ga.getAll();

        if (trackers.length) {
          return trackers[0].get('clientId');
        }
      }
    } catch (error) {// ignore
    }

    return null;
  }

  function addGAClientIdInput(form) {
    var clientId = getGAClientId();

    if (!clientId) {
      return;
    }

    var input = document.createElement('input');
    input.type = 'hidden';
    input.name = 'ga_client_id';
    input.value = clientId;
    form.appendChild(input);
  }

  function preventAutofill() {
    if (!window.chrome || !form || form.getAttribute('action')) {
      return;
    }

    var targetAction = '/order/search/';
    form.action = targetAction;
    form.addEventListener('submit', function () {
      if (form.action.indexOf(targetAction) !== -1) {
        form.removeAttribute('action');
      }
    });
  }
}, 2000); // TODO: Remove this setTimeout wrap hack later. This is a workaround to fix a race condition on script loading in Firefox. This won't be needed once improve our JS build process. https://3.basecamp.com/3419512/buckets/11014121/todos/4158743454

setTimeout(function () {
  /**
   * User address module
   */
  if (!window.IronWeb.initCreateAddressModal) {
    return;
  }

  var addressSelect = document.getElementById('id_address');

  if (!addressSelect) {
    return;
  }

  if (localStorage.getItem('address')) {
    addressSelect.value = JSON.parse(localStorage.getItem('address')).Line1;
  }

  var newAddressOption = document.createElement('option');
  newAddressOption.value = '';
  newAddressOption.textContent = 'Add new address';
  addressSelect.appendChild(newAddressOption);

  function addressCreated(data) {
    var option = document.createElement('option');
    option.value = data.id;
    option.textContent = data.choice_label;
    newAddressOption.insertAdjacentElement('beforebegin', option);
    addressSelect.value = data.id;
    triggerChange(addressSelect);
  }

  function triggerChange(element) {
    // TODO: use Event constructor when IE11 is no longer supported
    var event = document.createEvent('HTMLEvents');
    event.initEvent('change', true, false);
    element.dispatchEvent(event);
  }

  var modal = window.IronWeb.initCreateAddressModal(addressCreated);
  addressSelect.addEventListener('change', function () {
    if (addressSelect.value === '') {
      modal.modal();
      addressSelect.selectedIndex = 0;
    }
  });
}, 3000);
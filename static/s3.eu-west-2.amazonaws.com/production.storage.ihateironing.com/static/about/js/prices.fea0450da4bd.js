"use strict";

(function () {
  'use strict';
  /**
   * Categories
   */

  var content = document.getElementById('content');
  var categoryItems = document.querySelectorAll('.prices-category-item');

  if (categoryItems.length) {
    prepareCategorySection();
  }

  function prepareCategorySection() {
    var priceSections = document.querySelectorAll('.prices-item-section');
    Array.prototype.forEach.call(categoryItems, function (el, i) {
      el.addEventListener('click', function () {
        if (content.classList.contains('is-searching') || categoryItems[i].classList.contains('active')) {
          return;
        }

        showCategory(i);
      });
    });

    function showCategory(index) {
      var i;

      for (i = 0; i < categoryItems.length; i++) {
        categoryItems[i].classList.remove('active');
      }

      for (i = 0; i < priceSections.length; i++) {
        priceSections[i].classList.remove('active');
      }

      categoryItems[index].classList.add('active');
      priceSections[index].classList.add('active');
    }
  }
  /**
   * Search
   */


  var searchInput = document.querySelector('.prices-search-input');

  if (searchInput) {
    prepareSearch();
  }

  function prepareSearch() {
    var searchResultsSection = document.querySelector('.prices-search-results');
    var searchResults = searchResultsSection.querySelector('.prices-search-result-items');
    var resultColCount = document.querySelector('.prices-item-section.active > .row').childElementCount;
    var items = document.querySelectorAll('.prices-item-section:not(:first-child) .prices-item');
    var itemNames = Array.prototype.map.call(document.querySelectorAll('.prices-item-section:not(:first-child) .prices-item-name'), function (item) {
      return item.textContent.trim().toLowerCase();
    });
    var itemCount = itemNames.length;
    searchInput.addEventListener('input', function () {
      var searchTimeoutId;
      return function (event) {
        clearTimeout(searchTimeoutId);
        searchTimeoutId = setTimeout(function () {
          handleSearchInput(event);
        }, 200);
      };
    }());

    function handleSearchInput(event) {
      var query = event.target.value.trim().toLowerCase();
      searchResults.innerHTML = '';

      if (query.length < 3) {
        content.classList.remove('is-searching');
        return;
      }

      content.classList.add('is-searching');
      searchResultsSection.classList.remove('is-empty');
      var results = [];
      var i;

      for (i = 0; i < itemCount; i++) {
        if (itemNames[i].indexOf(query) > -1) {
          var resultItem = items[i].cloneNode(true);

          if (itemHasDetails(resultItem)) {
            addItemClickListener(resultItem);
          }

          results.push(resultItem);
        }
      }

      var resultCount = results.length;

      if (resultCount === 0) {
        searchResultsSection.classList.add('is-empty');
      } else {
        var colCount = Math.min(resultColCount, resultCount);
        var resultsPerCol = Math.floor(resultCount / colCount);
        var extraCount = resultCount % colCount;
        var offset = 0;

        for (i = 0; i < colCount; i++) {
          var start = i * resultsPerCol + offset;

          if (i < extraCount) {
            offset++;
          }

          var end = (i + 1) * resultsPerCol + offset;
          var col = document.createElement('div');
          col.className = 'col-md-6';

          for (var k = start; k < end; k++) {
            col.appendChild(results[k]);
          }

          searchResults.appendChild(col);
        }
      }
    } // Scroll to search on focus


    $('.prices-search').click(function () {
      $('html, body').animate({
        scrollTop: $(this).offset().top - 30
      }, 400);
    });
  }
  /**
   * Item modals
   */


  var handleItemClick = function () {
    var modal = document.querySelector('.item-modal');
    var $modal = $(modal);
    var title = modal.querySelector('.prices-item-modal-title');
    var description = modal.querySelector('.prices-item-modal-description');
    var details = modal.querySelector('.prices-item-modal-details');
    return function (event) {
      if (event.target.className !== 'prices-item-name') {
        return;
      }

      title.textContent = event.target.textContent;
      var item = event.currentTarget;
      var itemDescription = item.querySelector('.prices-item-description');
      description.textContent = itemDescription ? itemDescription.textContent : '';
      details.textContent = item.getAttribute('data-details');
      $modal.modal('show');
    };
  }();

  Array.prototype.map.call(document.querySelectorAll('.prices-item[data-details]'), addItemClickListener);

  function addItemClickListener(item) {
    item.addEventListener('click', handleItemClick);
  }

  function itemHasDetails(element) {
    return element.hasAttribute('data-details');
  }
})();

(function () {
  'use strict';
  /**
   * Order form
   */

  var form = document.querySelector('.prices-order-form');

  if (!form) {
    return;
  } // If there any form errors, scroll there


  if (form.classList.contains('has-error')) {
    window.scrollTo(0, document.querySelector('.prices-footer-row').offsetTop - document.querySelector('.prices-header').offsetTop);
  }
})();
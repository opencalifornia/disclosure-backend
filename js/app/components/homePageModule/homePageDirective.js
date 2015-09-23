(function() {
'use strict';

  var template = require('./homePage.html');

  module.exports = function homePage() {
      return {
          controller: 'HomePageController', // Called from HomeController.js
          controllerAs: 'ctrl',
          bindToController: true,
          restrict: 'EA',
          scope: true,
          template: template
      };
  };
})();
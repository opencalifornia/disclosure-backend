(function() {
  'use strict';

  var template = require('./appMainFooter.html');

  module.exports = function appMainFooter() {
    return {
      //controller: 'AppMainFooterController', // Called from AppMainFooterController.js
      template: template,
      restrict: 'EA'
      //replace: true
    };
  };
})();
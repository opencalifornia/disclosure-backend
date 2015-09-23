(function() {
  'use strict';

  //var appMainFooterModule = require('./appMainFooter');
  var appMainFooterDirective = require('./appMainFooterDirective');

  module.exports = angular.module('appMainFooterModule', [])
    .directive('appMainFooter', appMainFooterDirective);

})();
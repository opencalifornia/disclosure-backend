(function() {
  'use strict';

  //var appMainNavModule = require('./appMainNav');
  var appMainNavDirective = require('./appMainNavDirective');

  module.exports = angular.module('appMainNavModule', [])
    .directive('appMainNav', appMainNavDirective);

})();
(function() {
  'use strict';

  var template = require('./appMainNav.html');

  module.exports = function appMainNav() {
    return {
      //controller: 'AppMainNavController', // Called from AppMainNavController.js
      restrict: 'E',
      scope: true,
      //scope: {},
      template: template
    };
  };
  //var appMainNav = function() {
  //  return {
  //    restrict: 'EA',
  //    //replace: true,
  //    template: template
  //    //link: function() {
  //    //
  //    //}
  //  };
  //};
  //
  //appMainNav.$inject = ['$scope'];
  //module.exports = appMainNav;
})();
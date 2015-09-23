(function() {
  'use strict';

  var template = require('./examplePage2.html');

  module.exports = function examplePage2() {
    return {
      controller: 'ExamplePage2Controller', // Called from ExamplePage2Controller.js
      // controllerAs: 'ctrl',
      //controllerAs: 'ExamplePage2Controller',
      //bindToController: true,
      restrict: 'E',
      //scope: true,
      scope: {},
      template: template
    };
  };
})();
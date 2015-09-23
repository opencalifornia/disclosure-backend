(function() {
  'use strict';
// Example Page 1

  //var examplePage1Module = require('./examplePage1');
  var examplePage1Directive = require('./examplePage1Directive');
  var ExamplePage1Controller = require('./ExamplePage1Controller');

  module.exports = angular.module('examplePage1Module', [])
    .directive('examplePage1', examplePage1Directive)
    .controller('ExamplePage1Controller', ExamplePage1Controller);

})();
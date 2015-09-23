(function() {
  'use strict';
// Example Page 2

  //var examplePage2Module = require('./examplePage2');
  var examplePage2Directive = require('./examplePage2Directive');
  var ExamplePage2Controller = require('./ExamplePage2Controller');

  module.exports = angular.module('examplePage2Module', [])
    .directive('examplePage2', examplePage2Directive)
    .controller('ExamplePage2Controller', ExamplePage2Controller);

})();
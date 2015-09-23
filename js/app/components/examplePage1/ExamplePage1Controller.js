(function() {
  'use strict';
  // Controller naming conventions should start with an uppercase letter
  function ExamplePage1Controller($scope) {
    $scope.exampleContents1 = 'We are up and running using a required module!';
    $scope.paragraphText = ' Example Page 1 explicitly references required files';
  }

  // $inject is necessary for minification. See http://bit.ly/1lNICde for explanation.
  ExamplePage1Controller.$inject = ['$scope'];
  module.exports = ExamplePage1Controller;
})();
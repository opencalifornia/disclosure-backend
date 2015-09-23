(function() {
  'use strict';
  // Controller naming conventions should start with an uppercase letter
  function ExamplePage2Controller($scope) {
    $scope.exampleContents2 = 'We are up and running using a required module!';
    $scope.paragraphText = ' Example Page 2 sets required files as variables';
  }

  // $inject is necessary for minification. See http://bit.ly/1lNICde for explanation.
  ExamplePage2Controller.$inject = ['$scope'];
  module.exports = ExamplePage2Controller;
})();
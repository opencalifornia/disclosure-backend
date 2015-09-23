(function() {
  'use strict';

  require('./homePageModule/homePage');
  require('./examplePage1/examplePage1');
  require('./examplePage2/examplePage2');

  module.exports = angular.module('components',
      [
        'homePageModule',
        'examplePage1Module',
        'examplePage2Module'
      ]);
      //.controller('MainCtrl', require('./MainController'));
})();



//TODO: (1) CREATE appMain in 'common'
// (2): move appMainHeader and appMainFooter into directory 'appMain'
//  (3): load a (nested (?)) UIview into the body of appMain, between appMainHeader and appMainFooter
//  (4): for homePageModule (change 'homePageModule' to h
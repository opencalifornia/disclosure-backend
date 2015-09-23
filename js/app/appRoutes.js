'use strict';

function appRoutes($stateProvider) {

  // var appMain = {
  //  name: 'appMain', // state name
  //  url: '/', // url path that activates this state
  //  template: '<app-main></app-main>', // generate the Directive "homeView" - when calling the directive in HTML, the name must not be camelCased
  //  controller: 'AppMainController'
  //  // data: {
  //  //  moduleClasses: 'page', // assign a module class to the <body> tag
  //  //  pageClasses: 'appMain', // assign a page-specific class to the <body> tag
  //  //  pageTitle: 'AppMain', // set the title in the <head> section of the index.html file
  //  //  pageDescription: 'Meta Description goes here' // meta description in <head>
  //  // }
  // };

  var home = {
    name: 'home', // state name
    url: '/', // url path that activates this state
    template: '<home-page></home-page>', // generate the Directive "homeView" - when calling the directive in HTML, the name must not be camelCased
    data: {
      moduleClasses: 'page', // assign a module class to the <body> tag
      pageClasses: 'home', // assign a page-specific class to the <body> tag
      pageTitle: 'Home', // set the title in the <head> section of the index.html file
      pageDescription: 'Meta Description goes here' // meta description in <head>
    }
  };

  var examplePage1 = {
    name: 'examplePage1',
    url: '/example-page-1',
    template: '<example-page-1></example-page-1>',
    //controller: 'ExamplePage1Controller',
    data: {
      moduleClasses: 'page',
      pageClasses: 'examplePage1',
      pageTitle: 'Example Page 1',
      pageDescription: 'Some description.'
    }
  };

  var examplePage2 = {
    name: 'examplePage2',
    url: '/example-page-2',
    template: '<example-page-2></example-page-2>',
    //controller: 'ExamplePage2Controller',
    data: {
      moduleClasses: 'page',
      pageClasses: 'examplePage2',
      pageTitle: 'Example Page 2',
      pageDescription: 'Some description.'
    }
  };

  $stateProvider.state(home);
  $stateProvider.state(examplePage1);
  $stateProvider.state(examplePage2);

}

appRoutes.$inject = ['$stateProvider'];
module.exports = appRoutes;
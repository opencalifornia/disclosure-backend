'use strict';

window.jQuery = window.$ = require('jquery');
window._ = require('lodash');

var angular = require('angular');
//require('../common/campaignFinanceApp/campaignFinanceApp');
var campaignFinanceAppDirective = require('./components/common/campaignFinanceApp/campaignFinanceAppDirective');

require('angular-bootstrap');
require('angular-ui-router');
require('angular-animate');
require('angular-cookies');
require('angular-resource');
require('angular-sanitize');
require('domready/ready');
require('lodash');
require('restangular');

require('./components/common/appMainNav/appMainNav');
require('./components/common/appMainFooter/appMainFooter');

require('./components/components');

module.exports = angular.module('campaignFinanceApp',
    [
      'ui.bootstrap',
      'ui.router',
      'ngAnimate',
      'ngCookies',
      'ngResource',
      'ngSanitize',
      'restangular',
      'components'
    ])
    .config(require('./appRoutes'))
    .config(require('./appConfig'))
    .constant('version', require('../../package.json').version)
    .run(require('./app-init'))
    .directive('campaignFinanceApp', campaignFinanceAppDirective);

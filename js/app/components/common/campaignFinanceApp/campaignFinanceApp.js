//(function() {
  'use strict';

  var campaignFinanceAppDirective = require('./campaignFinanceAppDirective');
  //var campaignFinanceAppDirective = require('./common/campaignFinanceApp/campaignFinanceAppDirective');

  //var CampaignFinanceAppController = require('./CampaignFinanceAppController');

  //module.exports = angular.module('campaignFinanceAppModule', ['appMainModule'])
  module.exports = angular.module('campaignFinanceAppModule', [])
    .directive('campaignFinanceApp', campaignFinanceAppDirective);
    //.controller('CampaignFinanceAppController', CampaignFinanceAppController);

//})();
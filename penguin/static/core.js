var toolShareApp = angular.module('toolShareApp', ['ui.bootstrap', 'angularCharts', 'ngRoute', 'toolShareControllers', 'toolShareServices']);

toolShareApp.config(function($routeProvider){
	$routeProvider

		.when('/', {
			templateUrl: '/static/pages/login.html',
			controller: 'mainController'
		})
		.when('/home', {
			templateUrl: '/static/pages/home.html',
			controller: 'homepageController'
		})
		.when('/tools',{
			templateUrl: '/static/pages/tools.html',
			controller: 'toolsController'	
		})
		.when('/profile',{
			templateUrl: '/static/pages/profile.html',
			controller: 'profileController'
		})
		.when('/community',{
			templateUrl: '/static/pages/community.html',
			controller: 'communityController'
		})
		.when('/newTool',{
			templateUrl: '/static/pages/newTool.html',
			controller: 'newToolController'
		})
		.when('/logout',{
			templateUrl: '/static/pages/login.html',
			controller: 'logoutController'
		})
		.when('/error',{
			templateUrl: '/static/pages/error.html',
			controller: 'errorController'
		})
});

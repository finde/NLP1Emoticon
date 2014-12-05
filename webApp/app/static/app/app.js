'use strict';

angular.module('flaskJumpstart', [
  'ngCookies',
  'ngResource',
  'ngSanitize',
  'ngRoute'
])
  .config(function ($routeProvider, $locationProvider, $httpProvider) {
    $routeProvider
      .when('/', {
        title: 'Predicting Emoticons',
        templateUrl: 'static/app/views/home.html'
      })
      .when('/averaged-multiclass-perceptron', {
        title: 'Average Multiclass Perceptron',
        templateUrl: 'static/app/views/averaged-multiclass-perceptron.html'
      })
      .when('/hidden-markov-model', {
        title: 'Hidden Markov Models',
        templateUrl: 'static/app/views/hidden-markov-model.html'
      })
      .otherwise({
        redirectTo: '/'
      });

//    $locationProvider.html5Mode(true);

    $httpProvider.interceptors.push(['$q', '$location', function($q, $location) {
      return {
        'responseError': function(response) {
          if(response.status === 401 || response.status === 403) {
            $location.path('/login');
            return $q.reject(response);
          }
          else {
            return $q.reject(response);
          }
        }
      };
    }]);
  })
  .run(function ($rootScope) {

    $rootScope.$on('$routeChangeSuccess', function (event, current) {
      $rootScope.title = current.$$route.title;
    });

  });

// js/services/todos.js
angular.module('toolShareServices', [])

        // super simple service
        // each function returns a promise object 
        .factory('User', function($http) {
                return {
                        get : function() {
                                return $http.get('/api/user');
                        },
			login: function(loginData){
				return $http.post('/api/login', loginData)
			},
                        create : function(userData) {
                                return $http.post('/api/user', userData);
                        },
			update : function(userData) {
				return $http.put('/api/user', userData);
			},
                        delete : function(userId) {
                                return $http.delete('/api/user/' + userId);
                        },
			getByAreaCode: function(areaCode){
				return $http.get('/api/user/areaCode/' + areaCode);
			}
                }
        })

	.factory('Tool', function($http) {
		return {
			get: function(toolId){
				return $http.get('/api/tool/' + id);
			},
			create: function(toolData){
				return $http.post('/api/tool', toolData);
			},
			update: function(toolData){
				return $http.put('/api/tool', toolData);
			},
			delete: function(toolId){
				return $http.delete('/api/tool/' + toolId);
			},
			getInArea: function(){
				return $http.get('/api/tools/area');
			},
			getByUser: function(){
				return $http.get('/api/tools');
			}
		}
	})


	.factory('BorrowTransaction', function($http){
		return {
			create: function(transactionData){
				//{toolId: 3, date: datetime}
				return $http.post('/api/borrowTransaction', transactionData);
			},
			update: function(transactionData){
				//{toolId: 3}
				return $http.put('/api/borrowTransaction', transactionData);
			},
			get: function(transactionId){
				return $http.get('/api/borrowTransaction/' + id);
			},
			getBorrowing: function(userId){
				return $http.get('/api/borrowTransactions/borrowing/' + userId);
			},
			getBorrowed: function(userId){
				return $http.get('/api/borrowTransactions/borrowed/' + userId);
			},
			getCommunityHistory: function(areaCode){
				return $http.get('/api/borrowTransactions/community/' + areaCode);
			}
		}
	}).

        service('username', function(){
                var username;
                return {
                        setUsername: function(usernameToSet){
                                username = usernameToSet;
                        },
                        getUsername: function(){
                                return username
                        }
                }
        });



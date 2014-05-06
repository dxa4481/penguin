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
				return $http.post('/api/login', loginData);
			},
			logout: function(){
				return $http.post('/api/logout');
			},
                        create : function(userData) {
                                return $http.post('/api/user', userData);
                        },
			update : function(userData) {
				return $http.put('/api/user/' + userData.id, userData);
			},
                        delete : function(userId) {
                                return $http.delete('/api/user/' + userId);
                        },
			getByAreaCode: function(areaCode){
				return $http.get('/api/user/areaCode/' + areaCode);
			},
			updatePassword: function(passwordData){
				return $http.put('/api/changePassword', passwordData);
			},
			getAdmins: function(){
				return $http.get('/api/admins');
			},
			changeShedCoordinator: function(coordinator){
				return $http.put('/api/admin/shedCoordinator', coordinator);
			},
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
			requestStart: function(transactionData){
				//{toolId: 3, date: datetime}
				console.log(transactionData)
				return $http.post('/api/borrowTransaction', transactionData);
			},
			resolveStartRequest: function(transactionData){
				//{toolId: 3}
				return $http.post('/api/borrowTransaction/resolve', transactionData);
			},
			getRejected: function(userId){
				return $http.get('/api/borrowTransaction/rejected/' + userId);
			},
			requestEnd: function(transactionData){
				return $http.put('/api/borrowTransaction', transactionData);
			},
			resolveEndRequest: function(transactionId){
				return $http.delete('/api/borrowTransaction/' + transactionId);
			},
			getBorrowing: function(userId){
				return $http.get('/api/borrowTransaction/borrowing/' + userId);	
			},
			getBorrowed: function(userId){
				return $http.get('/api/borrowTransaction/borrowed/' + userId);
			},
			getCommunityHistory: function(areaCode){
				return $http.get('/api/borrowTransactions/community/' + areaCode);
			},
			getPendingRequests: function(){
				return $http.get('/api/borrowTransaction/requestPending');
			},
			getEndRequests: function(){
				return $http.get('/api/borrowTransaction/endRequests');
			},
			getCommunityEndRequests: function(){
				return $http.get('/api/borrowTransactions/pendingCommunity');
			}
		}
	})


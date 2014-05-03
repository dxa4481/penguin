// js/controllers/main.js
//
var polling = false;
zip_code_regex = /(^\d{5}(-\d{4})?$)|(^[ABCEGHJKLMNPRSTVXY]{1}\d{1}[A-Z]{1} *\d{1}[A-Z]{1}\d{1}$)/;
phone_number_regex = /^[\s()+-]*([0-9][\s()+-]*){6,20}$/;


angular.module('toolShareControllers', [])
	// inject the Todo service factory into our controller
	.controller('mainController', function($scope, $rootScope, $timeout, $location, User) {
		$scope.register = false;
		$scope.tryLogin = function(user){
			console.log(user)
			User.login(user).
				success(function(data){
					$rootScope.user = data;
					console.log(data)
					$location.path('/home');
				}).
				error(function(data, status){
					if(typeof data === "object"){
                                                $scope.error = data;
                                        }
					else{
						$location.path('/');
					}
				});
			
		}
		$scope.backToLogin = function(){
			$scope.register = false;
		};

		$scope.tryRegister = function(user){
			User.create(user).
				success(function(data){
					$rootScope.user = data;
					$location.path('/home');
				}).
                                error(function(data, status){
                                        if(typeof data === "object"){
                                                $scope.error = data;
                                        }
                                        else{
                                                $location.path('/');
                                        }
                                });

			
		}


		$scope.switchToRegister = function(){
			$scope.zipCodePattern = zip_code_regex
			$scope.phoneNumberPattern = phone_number_regex
			$scope.register = true;
			$scope.error = undefined;
		};
		
	})
	.controller('logoutController', function($location, $rootScope, User){
		User.logout().
                	success(function(data){
				delete $rootScope.user;
                        	$location.path('/');
                        }).
                        error(function(data, status){
                                $location.path('/');
                        });


	})
	.controller('homepageController', function($scope, $timeout, $rootScope, $modal, $location, User, Tool, BorrowTransaction){
		setActive($rootScope, $timeout, BorrowTransaction, "home");		
		
		if($rootScope.user == undefined){getUser($location, $rootScope, User, function(){})};
		Tool.getInArea().
			success(function(data){
				var tools = set_tool_availability(data)
				$scope.tools = tools;
			}).
                        error(function(data, status){
                        	if(typeof data === "object"){
                                        $scope.error = data;
                                }
                                else{
                                        $location.path('/');
                                }
                        });

		$scope.openModal = function(tool){
			$scope.tool = tool
			var modalInstance = $modal.open({
				templateUrl: '/static/pages/borrowModal.html',
				controller: borrowModalController,
				resolve: {tool: function(){return $scope.tool}}
			});
			modalInstance.result.then(function(date){
				BorrowTransaction.create({date:date.getTime(), toolId:tool.id}).
					success(function(data){
						tool.is_available = false;
					}).
	                                error(function(data, status){
                                        	if(typeof data === "object"){
                                                	$scope.error = data;
                                        	}
                                        	else{
                                                	$location.path('/');
                                        	}
                                	});

			});

		};
	})

	.controller('toolsController', function($scope, $timeout, $rootScope, $location, User, Tool, BorrowTransaction){
		var cb = function(){
			BorrowTransaction.getBorrowing($rootScope.user.id).
				success(function(data){
					var tools = set_tool_availability(data)
                                        $scope.borrowingTools = tools;
                        	}).
                                error(function(data, status){
                                        if(typeof data === "object"){
                                                $scope.error = data;
                                        }
                                        else{
                                                $location.path('/');
                                        }
                                });

		};
		$scope.newTool = function(){
			$location.path('/newTool');
		}
		if($rootScope.user == undefined){getUser($location, $rootScope, User, cb)}else{cb()};
		setActive($rootScope, $timeout, BorrowTransaction, "tools");
		$scope.activeTools = 'myTools';
		$scope.myToolsClass = 'active';
		Tool.getByUser().
			success(function(data){
				var tools = set_tool_availability(data);
				$scope.myTools = tools;
			}).
                        error(function(data, status){
                                if(typeof data === "object"){
                                	$scope.error = data;
                                }
                                else{
                                        $location.path('/');
                                }
                       });
	})

	.controller('profileController', function($scope, $timeout, $rootScope, $location, User, Tool, BorrowTransaction){
		var cb = function(){$scope.user = $rootScope.user};
		if($rootScope.user == undefined){getUser($location, $rootScope, User, cb)};
		$scope.user = $rootScope.user;
		$scope.trySaving = function(user){
			console.log(user)
			User.update(user).
				success(function(data){
					$rootScope.user = data;
					$location.path('/home');
				}).
                                error(function(data, status){
                                        if(typeof data === "object"){
                                                $scope.error = data;
                                        }
                                        else{
                                                $location.path('/');
                                        }
                                });
		}
		setActive($rootScope, $timeout, $BorrowTransaction, "profile");
		$scope.register = false;
		$scope.editing = true;
		$scope.zipCodePattern = zip_code_regex;
		$scope.phoneNumberPattern = phone_number_regex;

	})

	.controller('newToolController', function($scope, $rootScope, $location, User, Tool){
		cb = function(){
			$scope.tool = {}; 
			$scope.tool.tool_pickup_arrangements = $rootScope.user.default_pickup_arrangements
			$scope.tool.in_community_shed = false
		}
		if($rootScope.user == undefined){getUser($location, $rootScope, User, cb)}else{cb()}
		$scope.tryAddingTool = function(tool){
			console.log(tool)
			Tool.create(tool).
				success(function(data){
                                        $location.path('/tools');
                                }).
                                error(function(data, status){
                                        if(typeof data === "object"){
                                                $scope.error = data;
                                        }
                                        else{
                                                $location.path('/');
                                        }
                                });

		}
	})

        .controller('communityController', function($scope, $timeout, $rootScope, $location, User, Tool, BorrowTransaction){
		if($rootScope.user == undefined){getUser($location, $rootScope, User, function(){})}
		setActive($rootScope, $timeout, BorrowTransaction, "community");
	})
var getUser = function($location, rootScope, User, cb){
	User.get().
		success(function(data){
                        rootScope.user = data;
			cb();
		}).
                error(function(data, status){
                	$location.path('/');
		});

}


var borrowModalController = function($scope, $modalInstance, tool){
	$scope.tool = tool;		
	$scope.tomorrow = function(){
		$scope.dt = new Date(new Date().getTime() + 24 * 60 * 60 * 1000);
		return $scope.dt;
	};

	$scope.minDate = $scope.tomorrow();

	$scope.dateOptions = {
		'year-format': "'yy'",
		'starting-day': 1
	};

	$scope.days_from_now = function(dt){
		return (Math.round((dt - new Date()) / 60 / 60 / 24 / 1000))
	}

	$scope.formats = ['dd-MMMM-yyyy', 'yyyy/MM/dd', 'shortDate'];
	$scope.format = $scope.formats[0];

	
	$scope.ok = function (dt) {
		$modalInstance.close(dt);
	};

	$scope.cancel = function () {
		$modalInstance.dismiss('cancel');
	};

}

var set_tool_availability = function(tools){
	for(var i=0; i<tools.length; i++){
		tools[i].is_available = new Date() > new Date(tools[i].available_date);
	}
	return tools;
}

var setActive = function($rootScope, $timeout, BorrowTransaction, activeThing){
	console.log("wat");
	if(!polling){
		polling = true;
		var notifications = function(){
                        BorrowTransaction.getPendingRequests().
                        	success(function(data){
                                	$rootScope.transactionRequests ? addToFirstArrayById($rootScope.transactionRequests, data) : $rootScope.transactionRequests = data;
                                }).
                                error(function(data, status){
                                	if(typeof data === "object"){
                                        	$scope.error = data;
                                        }
                                        else{
                                        	$location.path('/');
                                        }
                                });
                        BorrowTransaction.getEndRequests().
                        	success(function(data){
                                	$rootScope.endTransactionRequests ? addToFirstArrayById($rootScope.endTransactionRequests, data) : $rootScope.endTransactionRequests = data;
                                }).
                                error(function(data, status){
                                	if(typeof data === "object"){
                                        	$scope.error = data;
                                        }
                                        else{
                                        	$location.path('/');
                                        }
                                });
					
                        $timeout(notifications, 1000);
                }
		notifications();
	}
	delete $rootScope.active
	$rootScope.active = {}
	$rootScope.active[activeThing] = "active";
}

var addToFirstArrayById = function(array1, array2){
	for (var j = 0; j < array2.length; j++) {
		var inArray = false;
		for(var i = 0; i < array1.length; i++){
			if(array1[j].id = array2[i]){
				inArray = true;
				break;
			}
		}
		if(!inArray){
			array1.push(array2[j])
		}
	}
	return array1;
}

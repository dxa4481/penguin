// js/controllers/main.js
//
var polling = false;
zip_code_regex = /(^\d{5}(-\d{4})?$)|(^[ABCEGHJKLMNPRSTVXY]{1}\d{1}[A-Z]{1} *\d{1}[A-Z]{1}\d{1}$)/;
phone_number_regex = /^[\s()+-]*([0-9][\s()+-]*){6,20}$/;


angular.module('toolShareControllers', [])
	// inject the Todo service factory into our controller
	.controller('mainController', function($scope, $rootScope, $modal, $timeout, $location, User) {
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
						$location.path('/error');
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
					if($rootScope.user.is_shed_coordinator){
						var modalInstance = $modal.open({
                                			templateUrl: '/static/pages/communityShedModal.html',
                                			controller: shedCoordinatorModalController,
                                			resolve: {}
                        			});
                        			modalInstance.result.then(function(){
							$location.path('/home');
						});
					}else{
						$location.path('/home');
					}
				}).
                                error(function(data, status){
                                        if(typeof data === "object"){
                                                $scope.error = data;
                                        }
                                        else{
                                                $location.path('/error');
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
	.controller('logoutController', function($location, $timeout, $rootScope, User){
		User.logout().
                	success(function(data){
				$timeout.cancel($rootScope.cronJob);
				delete $rootScope.user;
                        	$location.path('/');
                        }).
                        error(function(data, status){
                                $location.path('/error');
                        });


	})
	.controller('homepageController', function($scope, $timeout, $rootScope, $modal, $location, User, Tool, BorrowTransaction){
		setActive($rootScope, $timeout, $location, User, BorrowTransaction, "home");		
		
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
                                        $location.path('/error');
                                }
                        });

		$scope.openModal = function(tool){
			$scope.tool = tool
			var modalInstance = $modal.open({
				templateUrl: '/static/pages/borrowModal.html',
				controller: borrowModalController,
				resolve: {tool: function(){return $scope.tool}}
			});
			modalInstance.result.then(function(transaction){
				BorrowTransaction.requestStart(transaction).
					success(function(data){
						tool.is_available = false;
					}).
	                                error(function(data, status){
                                        	if(typeof data === "object"){
                                                	$scope.error = data;
                                        	}
                                        	else{
                                                	$location.path('/error');
                                        	}
                                	});

			});

		};
	})
	.controller('errorController', function(){})
	.controller('toolsController', function($scope, $timeout, $rootScope, $location, $modal, User, Tool, BorrowTransaction){
		var cb = function(){
			BorrowTransaction.getBorrowing($rootScope.user.id).
				success(function(data){
					var tools = set_tool_availability(data)
                                        $scope.borrowingTransactions = tools;
                        	}).
                                error(function(data, status){
                                        if(typeof data === "object"){
                                                $scope.error = data;
                                        }
                                        else{
                                                $location.path('/error');
                                        }
                                });

		};
		$scope.newTool = function(){
			$location.path('/newTool');
		}
		if($rootScope.user == undefined){getUser($location, $rootScope, User, cb)}else{cb()};
		setActive($rootScope, $timeout, $location, User, BorrowTransaction, "tools");
		$scope.activeTools = 'myTools';
		$scope.myToolsClass = 'active';
		$scope.requestReturn = function(borrowTransaction){
			BorrowTransaction.requestEnd({toolId: borrowTransaction.tool.id}).
				success(function(data){
                                        borrowTransaction.status = data.status;
                                }).
                                error(function(data, status){
                                        if(typeof data === "object"){
                                                $scope.error = data;
                                        }
                                        else{
                                                $location.path('/error');
                                        }
                                });
		}
		$scope.editTool = function(tool){
                        $scope.tool = tool
                        var modalInstance = $modal.open({
                                templateUrl: '/static/pages/toolEditorModal.html',
                                controller: editToolModalController,
                                resolve: {tool: function(){return $scope.tool}}
                        });
                        modalInstance.result.then(function(tool){
                                Tool.update(tool).
                                        success(function(data){}).
                                        error(function(data, status){
                                                if(typeof data === "object"){
                                                        $scope.error = data;
                                                }
                                                else{
                                                        $location.path('/error');
                                                }
                                        });

                        });

                };
		$scope.deleteTool = function(tool){
			Tool.delete(tool.id).
                        	success(function(data){
					for(var i=0; i<$scope.myTools.length; i++){
						if($scope.myTools[i].id == tool.id){$scope.myTools.splice(i, 1)};
					}
				}).
                                error(function(data, status){
                                        if(typeof data === "object"){
                                                $scope.error = data;
                                        }
                                        else{
                                                $location.path('/error');
                                        }
			});

		}
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
                                        $location.path('/error');
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
                                                $location.path('/error');
                                        }
                                });
		}
		setActive($rootScope, $timeout, $location, User, BorrowTransaction, "profile");
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
                                                $location.path('/error');
                                        }
                                });

		}
	})

        .controller('communityController', function($scope, $timeout, $rootScope, $location, User, Tool, BorrowTransaction){
		var cb = function(){
			BorrowTransaction.getCommunityHistory($rootScope.user.zip_code).
				success(function(data){
					var borrowers = {};
					for(var i=0; i<data.length; i++){
						if(data[i].borrower in borrowers){
							borrowers[data[i].borrower]++
						}else{
							borrowers[data[i].borrower] = 1;
						}
					}
					var chart_data = {series: ['Borrows'], data: []};
					for(key in borrowers){
						chart_data.data.push({"x": key, "y": [borrowers[key]]})
					}
					console.log(chart_data);
					console.log("ass");
					$scope.data = chart_data;
				}).
				error(function(data, status){
                        		if(typeof data === "object"){
                                		$scope.error = data;
                                	}
                                	else{
                                        	$location.path('/error');
                                	}
                		});
		}
		if($rootScope.user == undefined){getUser($location, $rootScope, User, cb)}else{cb()};
		setActive($rootScope, $timeout, $location, User, BorrowTransaction, "community");
		$scope.chartType = 'bar';
		$scope.config = {
			title : '',
			tooltips: true,
			labels : false,
			mouseover: function() {},
			mouseout: function() {},
			click: function() {},
			legend: {
				display: true,
    				//could be 'left, right'
    				position: 'left'
  			}
		}
		
	})
var getUser = function($location, rootScope, User, cb){
	User.get().
		success(function(data){
                        rootScope.user = data;
			cb();
		}).
                error(function(data, status){
                	if(typeof data === "object"){
			}else{
				$location.path('/error');
			}
		});

}

var shedCoordinatorModalController = function($scope, $modalInstance){

        $scope.cancel = function () {
                $modalInstance.close();
        };

}


var editToolModalController = function($scope, $modalInstance, tool){
	$scope.tool = tool;
        $scope.ok = function (tool) {
                $modalInstance.close(tool);
        };

        $scope.cancel = function (tool) {
                $modalInstance.dismiss('cancel');
        };

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

	
	$scope.ok = function (transaction) {
		if(!transaction.borrower_message){transaction.borrower_message="No Message"};
		$modalInstance.close(transaction);
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

var setActive = function($rootScope, $timeout, $location, User, BorrowTransaction, activeThing){
	if(!polling){
		$rootScope.resolveTransaction = function(resolution, transactionRequest){
			if(!transactionRequest.owner_message){transactionRequest.owner_message = "No message"};
			BorrowTransaction.resolveStartRequest({toolId: transactionRequest.tool.id, resolution: resolution, owner_message: transactionRequest.owner_message}).
				success(function(data){	
					for(var i=0; i<$rootScope.transactionRequests.length; i++){
						if(transactionRequest.id == $rootScope.transactionRequests[i].id){
							$rootScope.transactionRequests.splice(i, 1);
							if($rootScope.transactionRequests.length == 0){delete $rootScope.transactionRequests};
							break;
						}
					}
				}).
				error(function(data, status){
                                        if(typeof data === "object"){
                                                console.log(data);
                                        }
                                        else{
                                                $location.path('/error');
                                        }
                                });
		}
		$rootScope.resolveEndTransaction = function(endTransactionRequest){
			BorrowTransaction.resolveEndRequest(endTransactionRequest.id).
				success(function(data){
                                        for(var i=0; i<$rootScope.endTransactionRequests.length; i++){
                                                if(endTransactionRequest.id == $rootScope.endTransactionRequests[i].id){
                                                        $rootScope.endTransactionRequests.splice(i, 1);
							if($rootScope.endTransactionRequests.length == 0){delete $rootScope.endTransactionRequests};
                                                        break;
                                                }
                                        }
                                }).
                                error(function(data, status){
                                        if(typeof data === "object"){
                                                console.log(data);
                                        }
                                        else{
                                                $location.path('/error');
                                        }
                                });

		}
		polling = true;
		$rootScope.messages = [];
		$rootScope.transactionRequests = [];
		$rootScope.endTransactionRequests = [];
		$rootScope.endCommunityTransactionRequests = [];
		var notifications = function(){
                         BorrowTransaction.getPendingRequests().
                        	success(function(data){
					var setData = {addToSet: data, removeFromSet: []}
					if($rootScope.transactionRequests){
						setData = addToSetById($rootScope.transactionRequests, data);
						console.log(setData);
					}else{$rootScope.transactionRequests = []}
					for(var i=0; i<setData.removeFromSet.length; i++){$rootScope.transactionRequests.splice(setData[i], 1);};
					for(var i=0; i<setData.addToSet.length; i++){$rootScope.transactionRequests.push(setData.addToSet[i]);};
                                }).
                                error(function(data, status){
                                	if(typeof data === "object"){
                                        	console.log("not logged in");
                                        }
                                        else{
                                        	$location.path('/error');
                                        }
                                });
                        if($rootScope.user.is_shed_coordinator)
				BorrowTransaction.getCommunityEndRequests().
					success(function(data){
						var setData = {addToSet: data, removeFromSet: []}
						if($rootScope.endCommunityTransactionRequests){
							setData = addToSetById($rootScope.endCommunityTransactionRequests, data);
						console.log(setData);
						}else{$rootScope.endCommunityTransactionRequests = []}
						for(var i=0; i<setData.removeFromSet.length; i++){$rootScope.endCommunityTransactionRequests.splice(setData[i], 1);};
						for(var i=0; i<setData.addToSet.length; i++){$rootScope.endCommunityTransactionRequests.push(setData.addToSet[i]);};
						}).
						error(function(data, status){
						if(typeof data === "object"){
							console.log("not logged in");
						}
						else{
							$location.path('/error');
						}
					});
			BorrowTransaction.getEndRequests().
                        	success(function(data){
					var setData = {addToSet: data, removeFromSet: []}
                                        if($rootScope.endTransactionRequests){
                                                setData = addToSetById($rootScope.endTransactionRequests, data);
                                        }else{$rootScope.endTransactionRequests = []}
                                        for(var i=0; i<setData.removeFromSet.length; i++){$rootScope.endTransactionRequests.splice(setData[i], 1);};
                                        for(var i=0; i<setData.addToSet.length; i++){$rootScope.endTransactionRequests.push(setData.addToSet[i]);};
                                }).
                                error(function(data, status){
                                	if(typeof data === "object"){
                                        	console.log("not logged in");
                                        }
                                        else{
                                        	$location.path('/error');
                                        }
                                });
					
			$rootScope.cronJob = $timeout(notifications, 1000);
                }
		getUser($location, $rootScope, User, notifications);
	}
	delete $rootScope.active
	$rootScope.active = {}
	$rootScope.active[activeThing] = "active";
}
var addToSetById = function(array1, array2){
	var set = {};
	var removeSet = [];
	for(var i=0; i<array2.length; i++){
		set[array2[i].id] = array2[i];
	}
	for(var i=0; i<array1.length; i++){
                if(array1[i].id in set){
			delete set[array1[i].id];
		}else{removeSet.push(i)}
        }
	var addSet = [];
	for(key in set){addSet.push(set[key])}
	return {addToSet: addSet, removeFromSet: removeSet};
}

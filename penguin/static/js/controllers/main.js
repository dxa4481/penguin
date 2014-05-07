// js/controllers/main.js
//
zip_code_regex = /(^\d{5}(-\d{4})?$)|(^[ABCEGHJKLMNPRSTVXY]{1}\d{1}[A-Z]{1} *\d{1}[A-Z]{1}\d{1}$)/;
phone_number_regex = /^\(?([0-9]{3})\)?[-. ]?([0-9]{3})[-. ]?([0-9]{4})$/;


angular.module('toolShareControllers', [])
	// inject the Todo service factory into our controller
	.controller('mainController', function($scope, $rootScope, $modal, $timeout, $location, User) {
		$scope.register = false;
		$rootScope.polling = false;
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
				$rootScope.polling = false;
                        	$location.path('/');
                        }).
                        error(function(data, status){
                                $location.path('/error');
                        });


	})
	.controller('homepageController', function($scope, $timeout, $rootScope, $modal, $location, User, Tool, BorrowTransaction){
		setActive($rootScope, $timeout, $location, User, BorrowTransaction, "home");		
		
		var cb = function(){
			Tool.getInArea().
				success(function(data){
					var tools = data;
					tools = removeOwnTools(tools, $rootScope.user.username)
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
		};
		if($rootScope.user == undefined){getUser($location, $rootScope, User, cb)}else{cb()};

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
					var tools = data;
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
			BorrowTransaction.getRejected($rootScope.user.id).
				success(function(data){
					var tools = data;
                                        $scope.rejectedTools = tools;
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
		$scope.now = new Date().getTime();
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
				var tools = data;
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
	.controller('changePasswordController', function($scope, $timeout, $rootScope, $location, User, BorrowTransaction){
		if($rootScope.user == undefined){getUser($location, $rootScope, User, function(){})};
		setActive($rootScope, $timeout, $location, User, BorrowTransaction, "profile");
		$scope.trySaving = function(passwordInfo){
			User.updatePassword(passwordInfo).
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

	})
	.controller('profileController', function($scope, $modal, $timeout, $rootScope, $location, User, Tool, BorrowTransaction){
		var tempCoordinator = false;
		var cb = function(){
			$scope.user = $rootScope.user; 
			tempCoordinator = $rootScope.user.is_shed_coordinator;
		};
		if($rootScope.user == undefined){getUser($location, $rootScope, User, cb)}
		else{tempCoordinator = $rootScope.user.is_shed_coordinator;}
		$scope.user = $rootScope.user;
		$scope.changePassword = function(){
			$location.path('/changePassword');
		}
		$scope.trySaving = function(user){
			User.update(user).
				success(function(data){
					$rootScope.user = data;
					console.log(tempCoordinator)
					console.log(data)
					console.log("FUCK YOU")
					if(tempCoordinator != data.is_shed_coordinator){
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
		$scope.borrower_data = {};
		$scope.lender_data = {};
		$scope.tool_data = {};
		var cb = function(){
			BorrowTransaction.getCommunityHistory($rootScope.user.zip_code).
				success(function(data){
					borrowers = {};
					lenders = {};
					tools = {};
					for(var i=0; i<data.length; i++){
						if(data[i].borrower in borrowers){
							borrowers[data[i].borrower]++;
						}else{
							borrowers[data[i].borrower] = 1;
						}
						if(data[i].tool.owner in lenders){
							lenders[data[i].tool.owner]++;
						}else{
							lenders[data[i].tool.owner] = 1;
						}
						if(data[i].tool.tool_type in tools){
						        tools[data[i].tool.tool_type]++;
                                                }else{
                                                        tools[data[i].tool.tool_type] = 1;
                                                }
					}
					$scope.borrower_data = {series: ['Borrows'], data: []};
					for(key in borrowers){
						$scope.borrower_data.data.push({"x": key, "y": [borrowers[key]]})
					}
					$scope.borrower_data.data = sortData($scope.borrower_data.data);
					$scope.lender_data = {series: ['Lends'], data: []};
                                        for(key in lenders){
                                                $scope.lender_data.data.push({"x": key, "y": [lenders[key]]})
                                        }
					$scope.lender_data.data = sortData($scope.lender_data.data);
					$scope.tool_data = {series: ['Borrows'], data: []};
                                        for(key in tools){
                                                $scope.tool_data.data.push({"x": key, "y": [tools[key]]})
                                        }
					$scope.tool_data.data = sortData($scope.tool_data.data);
					$scope.data = $scope.borrower_data;
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
		$scope.chartTypes = ['bar', 'pie'];
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
		$scope.graphSelections = ["Most active borrowers", "Most active lenders", "Most borrowed tools"];
		$scope.graphSelection = "Most active borrowers";
		$scope.changeData = function(graphSelection){
			if(graphSelection == "Most active borrowers"){
				$scope.data = $scope.borrower_data;
			}else if(graphSelection == "Most active lenders"){
				$scope.data = $scope.lender_data;
			}else if(graphSelection == "Most borrowed tools"){
				$scope.data = $scope.tool_data;
			}
		}
		
	})
var sortData = function(sortable){
	sortable.sort(function(a, b) {return a.y[1] - b.y[1]})
	return sortable.slice(0, 5);
}

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
	$scope.message = "";	
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
		$scope.tool.tool_available = false;
		if(!transaction.borrower_message){transaction.borrower_message="No Message"};
		$modalInstance.close(transaction);
	};

	$scope.cancel = function () {
		$modalInstance.dismiss('cancel');
	};

}
var removeOwnTools = function(tools, username){
	var return_list = []
	console.log(username)
	console.log(tools)
	for(var i=0; i<tools.length; i++){
		if(tools[i].owner != username){
			return_list.push(tools[i]);
		}
	}
	return return_list;
}


var setActive = function($rootScope, $timeout, $location, User, BorrowTransaction, activeThing){
	if(!$rootScope.polling){
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
		$rootScope.polling = true;
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
					
			if($rootScope.polling){$rootScope.cronJob = $timeout(notifications, 3000);}
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

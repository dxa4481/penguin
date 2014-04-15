// js/controllers/main.js
//
area_code_regex = /(^\d{5}(-\d{4})?$)|(^[ABCEGHJKLMNPRSTVXY]{1}\d{1}[A-Z]{1} *\d{1}[A-Z]{1}\d{1}$)/;
phone_number_regex = /^[\s()+-]*([0-9][\s()+-]*){6,20}$/;
angular.module('toolShareControllers', [])

	// inject the Todo service factory into our controller
	.controller('mainController', function($scope, $location, User) {
		$scope.register = false;
		$scope.tryLogin = function(user){
			console.log(user)
			User.login(user).
				success(function(data){
					if('error' in data){
						$scope.errors = data;
					}
					else{
						$location.path('/home');
					}
				});
			
		}
		$scope.backToLogin = function(){
			$scope.register = false;
		};

		$scope.tryRegister = function(user){
			User.create(user).
				success(function(data){
					if('error' in data){
						$scope.errors = data;
					}
					else{
						$location.path('/home');
					}
				});
			
		}


		$scope.switchToRegister = function(){
			$scope.areaCodePattern = area_code_regex
			$scope.phoneNumberPattern = phone_number_regex
			$scope.register = true;
			$scope.errors = undefined;
		};
		
	})

	.controller('homepageController', function($scope, $modal, $location, Tool, BorrowTransaction){
		$scope.active = "home"		
		
		Tool.getInArea().
			success(function(data){
				if('error' in data){
					$scope.errors = data;
				}
				else{
					for(var i=0; i<data.length; i++){
						data[i].is_available = new Date() > new Date(data[i].available_date);
					}
					$scope.tools = data;
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
				BorrowTransaction.create({date:date, toolId:tool.id}).
					 success(function(data){
						if("error" in data){
							$scope.errors = data.error;
						}else{
							tool.is_available = false;
						}

					 })
			});

		};
	})

	.controller('toolsController', function($scope, $location, User, Tool){
		$scope.active = "tools";
		Tool.getByUser().
			success(function(data){
				if("error" in data){
					$scope.errors = data.error;
				}else{
					$scope.tools = data;
				}
			})
	
	})

	.controller('profileController', function($scope, $location, User, Tool){
		User.get().
			success(function(data){
				if('error' in data){
					$scope.errors = data;
				}
				else{
					$scope.user = data;
				}
			});	
		$scope.trySaving = function(user){
			User.update(user).
				success(function(data){
					if('error' in data){
						$scope.errors = data;
					}
					else{
						$location.path('/home');
					}
				});
		}

		$scope.active = "profile";
		$scope.register = false;
		$scope.editing = true;
		$scope.areaCodePattern = area_code_regex;
		$scope.phoneNumberPattern = phone_number_regex;

	})

        .controller('communityController', function($scope, $location, User, Tool, BorrowTransaction){
		$scope.active = "community";
	})


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

	
	$scope.ok = function () {
		$modalInstance.close($scope.dt);
	};

	$scope.cancel = function () {
		$modalInstance.dismiss('cancel');
	};

}

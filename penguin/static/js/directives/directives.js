angular.module('toolShareControllers')
	.directive('match', [function(){
		return{
			require: 'ngModel',
			link: function(scope, elem, attrs, ctrl){
				scope.$watch('[' + attrs.ngModel + ', ' + attrs.match + ']', function(value){
					var otherInput = elem.inheritedData("$formController").password.$modelValue;
					ctrl.$setValidity('match', otherInput === value[0]);

				}, true);

			}
		}

	
	
	}])


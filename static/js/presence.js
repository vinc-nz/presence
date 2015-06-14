/**
 * 
 */

var app = angular.module('presence-web', []);
app.controller('presence-controller', function($scope, $http) {
	$scope.gates = [ {
		id : "internal",
		label : "Porta Interna",
		state : {
			label : "closed",
			cssClass : [ "label", "label-default" ]
		},
		button : {
			disabled : true
		}
	}, {
		id : "external",
		label : "Porta Esterna",
		state : {
			label : "closed",
			cssClass : [ "label", "label-default" ]
		},
		button : {
			disabled : true
		}
	} ];

	$scope.access_list = [ {
		"time" : "2015-06-13T15:05:45",
		"user" : "alivin70"
	} ];
	
	$scope.toggle = function() {
        $scope.myVar = !$scope.myVar;
    };
    
    $scope.open_gate = function(gate) {
    	var token = "Token " + localStorage.getItem("token");
    	$http.post("http://localhost:8000/gates/" + gate.id + "/", null, {
    	    headers: {'Authorization': token}
    	});
    };
    
    $scope.logged = function() {
    	return localStorage.getItem("token") != null;
    }
    
    $scope.login = function() {
    	$http.post("http://localhost:8000/api-token-auth/", $scope.user).success(function(data){
    		localStorage.setItem("token", data.token);
    	});
    }
    
    $scope.logout = function() {
    		localStorage.removeItem("token");
    }

	var ws = new WebSocket("ws://localhost:8000/socket");
	ws.onmessage = function(event) {
		var message = JSON.parse(event.data);
		$scope.gates.map(function(gate) {
			var newstate = message[gate.id];
			gate.state.label = newstate.description;
			gate.state.cssClass = getStateCssClasses(newstate.id);
			gate.button.disabled = newstate.id > 0;
		});
		$scope.$apply();
	}

});


angular.element(document).ready(function() {
	$(".timeago").timeago();

});

function getStateCssClasses(value) {
	if (value == 0) {
		return [ "label", "label-default" ];
	} else if (value == 1) {
		return [ "label", "label-success" ];
	}
	return [ "label", "label-warning" ];
}
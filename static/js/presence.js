/**
 * 
 */

var app = angular.module('presence-web', []);
app.controller('presence-controller', function($scope, $location, $http) {
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

	$scope.access_list = [ ];
	
    $scope.open_gate = function(gate) {
    	var token = "Token " + localStorage.getItem("token");
    	$http.post("/gates/" + gate.id + "/", null, {
    	    headers: {'Authorization': token}
    	});
    };
    
    $scope.logged = function() {
    	return localStorage.getItem("token") != null;
    }
    
    $scope.login = function() {
    	$http.post("/api-token-auth/", $scope.user).success(function(data){
    		localStorage.setItem("token", data.token);
    	});
    }
    
    $scope.logout = function() {
    		localStorage.removeItem("token");
    }

	var ws = new WebSocket("ws://" + $location.host() + ":" + $location.port() + "/socket");
	ws.onmessage = function(event) {
		var message = JSON.parse(event.data);
		$scope.gates.map(function(gate) {
			var newstate = message[gate.id];
			gate.state.label = newstate.description;
			gate.state.cssClass = getStateCssClasses(newstate.id);
		});
		
		var token = "Token " + localStorage.getItem("token");
		$http.get("/gates/internal/requests/", {
    	    headers: {'Authorization': token}
    	}).success(function(data){
    		$scope.access_list = data;
    	});
		
		$http.get("/capabilities/", {
    	    headers: {'Authorization': token}
    	}).success(function(data){
    		$scope.gates.map(function(gate) {
    			gate.button.disabled = data[gate.id] == false;
    		});
    	});
		
		$scope.$apply();
		
		$(".timeago").timeago();
	}

});



function getStateCssClasses(value) {
	if (value == 0) {
		return [ "label", "label-default" ];
	} else if (value == 1) {
		return [ "label", "label-success" ];
	}
	return [ "label", "label-warning" ];
}
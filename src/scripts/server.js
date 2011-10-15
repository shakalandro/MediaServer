function sendRequest(event){
	alert(event);
	new Ajax.Request("command.py" ,{
		method:post,
		parameters:{},
		onFailure: displayError
		
	});
}

function displayError(){
	alert("Ajax failure");	
}

window.onload = function(){
	$("quality").onchange = sendRequest;
	$("video").onchange = sendRequest;
	$("music").onchange = sendRequest;
}
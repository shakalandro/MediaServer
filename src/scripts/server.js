function sendRequest(event){
	var changed, val;
	changed = this.id;
	val = this.value;
	new Ajax.Request("/" ,{
		method:"post",
		parameters:{changed:val},
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
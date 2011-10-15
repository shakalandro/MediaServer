function sendRequest(event){
	var changed, val;
	changed = this.id;
	val = this.value;
	alert(val);
	alert(changed);
	new Ajax.Request("file://" ,{
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
function sendRequest(event){
	var changed, val, param;
	changed = this.id;
	val = this.value;
	param = "" + changed + "=" + val;
	
	 $.ajax({
        url: "http://10.0.7.112:8888",
        type: "POST",
        data: param,
        success: function(data){
        	alert("worked");
        }
    });

}

function worked(ajax){
	alert("returned");	
}

function displayError(){
	alert("Ajax failure");	
}

window.onload = function(){
	$("#quality").change(sendRequest);
	$("#video").change(sendRequest);
	$("#music").change(sendRequest);
}
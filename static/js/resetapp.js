function resetapp()
{
	loading = function() {}
	loading.start = function() {
		$('#loading').html('<img src="/static/media/loading.gif" alt="Loading"/>');
	}
	loading.stop = function() {
		$('#loading').html('')
	}

	loading.start();
	resetappalert = function() {}
	resetappalert.warning = function(message) {
            $('#resetapp-error-content').html('<div class="alert alert-error"><a class="close" data-dismiss="alert">×</a><span>'+message+'</span></div>')
        }
    resetappalert.success = function(message) {
            $('#resetapp-error-content').html('<div class="alert alert-success"><a class="close" data-dismiss="alert">×</a><span>'+message+'</span></div>')
        }
	var toresetappname=document.getElementById("toresetappname").value;
	if(toresetappname==null || toresetappname=="")
	{
		//$("#register-error-content").text("Please enter a valid name");
		resetappalert.warning("Please enter a valid app name!");
		$("#toresetappname").focus();
		loading.stop();
		return;
	}

	$.post("/socketbox/reset/app/",{toresetappname : toresetappname },function(result){
	console.log(result);
	result=JSON.parse(result);
	if(result.status=="success")
	{
		console.log("app resetted successfully");
		resetappalert.success("Congratulations! Your App credentials have been resetted successfully!");	
		$("#appname").val("");
		window.location.href='/socketbox/dashboard/'
	}
	else 
		{
			console.log("something went wrong");	
			resetappalert.warning("We're sorry , something went wrong . Please try again later!");
		}
  	//write response handle code here
  	loading.stop();
  });
}
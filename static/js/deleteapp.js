function deleteapp()
{
	loading = function() {}
	loading.start = function() {
		$('#loading').html('<img src="/static/media/loading.gif" alt="Loading"/>');
	}
	loading.stop = function() {
		$('#loading').html('')
	}
	loading.start();
	deleteappalert = function() {}
	deleteappalert.warning = function(message) {
            $('#deleteapp-error-content').html('<div class="alert alert-error"><a class="close" data-dismiss="alert">×</a><span>'+message+'</span></div>')
        }
    deleteappalert.success = function(message) {
            $('#deleteapp-error-content').html('<div class="alert alert-success"><a class="close" data-dismiss="alert">×</a><span>'+message+'</span></div>')
        }
	var todeleteappname=document.getElementById("todeleteappname").value;
	if(todeleteappname==null || todeleteappname=="")
	{
		//$("#register-error-content").text("Please enter a valid name");
		deleteappalert.warning("Please enter a valid app name!");
		$("#todeleteappname").focus();
		loading.stop();
		return;
	}

	$.post("/socketbox/delete/app/",{todeleteappname : todeleteappname },function(result){
	console.log(result);
	result=JSON.parse(result);
	if(result.status=="success")
	{
		console.log("App deleted successfully");
		deleteappalert.success("Congratulations! Your App has been deleted successfully!");	
		$("#todeleteappname").val("");
		window.location.href='/socketbox/dashboard/'
	}
	else if(result.status=="invalidappname")
	{
		console.log("app name problem");
		deleteappalert.warning("This app name is invalid!");	
		$("#todeleteappname").val("");
	}
	else 
		{
			console.log("something went wrong");	
			deleteappalert.warning("We're sorry , something went wrong . Please try again later!");
		}
  	//write response handle code here
  	loading.stop();
  });
}
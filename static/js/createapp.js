function createapp()
{
	loading = function() {}
	loading.start = function() {
		$('#loading').html('<img src="/static/media/loading.gif" alt="Loading"/>');
	}
	loading.stop = function() {
		$('#loading').html('')
	}

	loading.start();
	createappalert = function() {}
	createappalert.warning = function(message) {
            $('#createapp-error-content').html('<div class="alert alert-error"><a class="close" data-dismiss="alert">×</a><span>'+message+'</span></div>')
        }
    createappalert.success = function(message) {
            $('#createapp-error-content').html('<div class="alert alert-success"><a class="close" data-dismiss="alert">×</a><span>'+message+'</span></div>')
        }
	var appname=document.getElementById("appname").value;
	if(appname==null || appname=="")
	{
		//$("#register-error-content").text("Please enter a valid name");
		createappalert.warning("Please enter a valid app name!");
		$("#appname").focus();
		loading.stop();
		return;
	}

	$.post("/socketbox/create/app/",{appname : appname },function(result){
	console.log(result);
	result=JSON.parse(result);
	if(result.status=="success")
	{
		console.log("app created successfully");
		createappalert.success("Congratulations! Your App has been created successfully!");	
		$("#appname").val("");
	}
	else if(result.status=="appnameexists")
	{
		console.log("app name already exists");
		createappalert.warning("This app name already exists , please try using another app name");	
		$("#appname").val("");
	}
	else 
		{
			console.log("something went wrong");	
			createappalert.warning("We're sorry , something went wrong . Please try again later!");
		}
  	//write response handle code here
  	loading.stop();
  });
}
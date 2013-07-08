function renameapp()
{
	loading = function() {}
	loading.start = function() {
		$('#loading').html('<img src="/static/media/loading.gif" alt="Loading"/>');
	}
	loading.stop = function() {
		$('#loading').html('')
	}

	loading.start();
	renameappalert = function() {}
	renameappalert.warning = function(message) {
            $('#renameapp-error-content').html('<div class="alert alert-error"><a class="close" data-dismiss="alert">×</a><span>'+message+'</span></div>')
        }
    renameappalert.success = function(message) {
            $('#renameapp-error-content').html('<div class="alert alert-success"><a class="close" data-dismiss="alert">×</a><span>'+message+'</span></div>')
        }
	var newappname=document.getElementById("newappname").value;
	var oldappname=document.getElementById("oldappname").value;	
	if(newappname==null || newappname=="")
	{
		//$("#register-error-content").text("Please enter a valid name");
		renameappalert.warning("Please enter a valid app name!");
		$("#newappname").focus();
		loading.stop();
		return;
	}
	console.log("newappname="+newappname+" oldappname="+oldappname);
	$.post("/rename/app/",{newappname : newappname , oldappname : oldappname },function(result){
	console.log(result);
	result=JSON.parse(result);
	if(result.status=="success")
	{
		console.log("App renamed successfully");
		renameappalert.success("Congratulations! Your App has been rename successfully!");	
		$("#newappname").val("");
		window.location.href='/dashboard/'
	}
	else if(result.status=="appnameexists")
	{
		console.log("app name already exists");
		createappalert.warning("This app name already exists , please try using another app name");	
		$("#newappname").val("");
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
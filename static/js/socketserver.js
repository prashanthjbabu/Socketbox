var socket;
function sendmessage()
{
	loading = function() {}
	loading.start = function() {
		$('#loading').html('<img src="/static/media/loading.gif" alt="Loading"/>');
	}
	loading.stop = function() {
		$('#loading').html('')
	}

	loading.start();
	socketserveralert = function() {}
	socketserveralert.warning = function(message) {
            $('#server-content').html('<div class="alert alert-error"><a class="close" data-dismiss="alert">×</a><span>'+message+'</span></div>')
        }
    socketserveralert.success = function(message) {
            $('#server-content').html('<div class="alert alert-success"><a class="close" data-dismiss="alert">×</a><span>'+message+'</span></div>')
        }	

    var channelname=document.getElementById("serverchannelname").value;
	if(channelname==null || channelname=="")
	{
		//$("#register-error-content").text("Please enter a valid name");
		socketserveralert.warning("Please enter a valid channel name!");
		$("#serverchannelname").focus();
		loading.stop();
		return;
	}    
    var eventname=document.getElementById("servereventname").value;
	if(eventname==null || eventname=="")
	{
		//$("#register-error-content").text("Please enter a valid name");
		socketserveralert.warning("Please enter a valid event name!");
		$("#servereventname").focus();
		loading.stop();
		return;
	}
	var apikey=document.getElementById("apikey").value;
    var message=document.getElementById("message").value;
	$.post("/sendmessage/",{eventname : eventname , apikey : apikey , secret : secret , channelname : channelname ,message : message },function(result){
	console.log(result);
	result=JSON.parse(result);
	if(result.status=="success")
	{
		console.log("app created successfully");
		createappalert.success("Congratulations! Your App has been created successfully!");	
		$("#appname").val("");
		window.location.href='/dashboard/'
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
}

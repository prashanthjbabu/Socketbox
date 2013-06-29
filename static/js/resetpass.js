function resetpasstoserv()
{
	loading = function() {}
	loading.start = function() {
		$('#loading').html('<img src="/static/media/loading.gif" alt="Loading"/>');
	}
	loading.stop = function() {
		$('#loading').html('')
	}
	loading.start();
	//var resetcode = "{{resetcode}}";
	//var email="{{email}}";
	var email=document.getElementById("email").value;
	var resetcode=document.getElementById("resetcode").value;
	console.log("resetcode="+resetcode);
	console.log("email="+email);
	var password=document.getElementById("pass").value;
	var cpassword=document.getElementById("cpass").value;
	var emailfilter = /^([a-zA-Z0-9_\.\-])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/;
 	var passfilter=  /^[A-Za-z]\w{7,14}$/;  
 	resetpassservalert = function() {}
	resetpassservalert.error = function(message) {
            $('#resetpass-server-alerts').html('<div class="alert alert-error"><a class="close" data-dismiss="alert">×</a><span>'+message+'</span></div>')
        }
    resetpassservalert.success = function(message) {
            $('#resetpass-server-alerts').html('<div class="alert alert-success"><a class="close" data-dismiss="alert">×</a><span>'+message+'</span></div>')
        }
 	if (!emailfilter.test(email)) 
    {
		//$("#register-error-content").text("Please enter a valid email");
		resetpassservalert.error("Invalid Reset Link!");
		loading.stop();
		return;
 	}	
	if(!passfilter.test(password))   
	{   
		//$("#register-error-content").text("Password must be atleast 7 characters");
		resetpassservalert.error("Password must be atleast 7 characters!");
		$("#pass").focus();
		loading.stop();
		return;  
	}
	if(password!=cpassword)
	{
		//$("#register-error-content").text("Passwords do not match");
		resetpassservalert.error("Passwords do not match!");
		$("#cpass").focus();
		loading.stop();
		return;	
	}
	$.post("/socketbox/new/password/",{email : email,pass : password , resetcode : resetcode },function(result){
	console.log(result);
	result=JSON.parse(result);
	if(result.status=="success")
	{
		console.log("password changed successfully");
		resetpassservalert.success("Congratulations! You may now login with your new password!");	
		$("#pass").val("");
		$("#cpass").val("");
	}
	else if(result.status=="userdoesnotexist")
	{
		console.log("user does not exist");
		resetpassservalert.error("Invalid User Account!");	
	}
	else 
	{
		console.log("something went wrong");	
		resetpassservalert.error("We're sorry , something went wrong . Please try again later!");
	} 
	loading.stop();
	});
}

function resetpass()
{
	loading = function() {}
	loading.start = function() {
		$('#loading').html('<img src="/static/media/loading.gif" alt="Loading"/>');
	}
	loading.stop = function() {
		$('#loading').html('')
	}
	loading.start();
	forgotpassservalert = function() {}
	forgotpassservalert.warning = function(message) {
            $('#forgotpass-server-alerts').html('<div class="alert alert-error"><a class="close" data-dismiss="alert">×</a><span>'+message+'</span></div>')
        }
    forgotpassservalert.success = function(message) {
            $('#forgotpass-server-alerts').html('<div class="alert alert-success"><a class="close" data-dismiss="alert">×</a><span>'+message+'</span></div>')
        }   
	$("#forgotpass-server-alerts").text("");
	var email=document.getElementById("email").value;
	var emailfilter = /^([a-zA-Z0-9_\.\-])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/;
    if (!emailfilter.test(email)) 
    {
		//$("#register-error-content").text("Please enter a valid email");
		console.log("invalid email");
		forgotpassservalert.warning("Please enter a valid email!");
    	$("#email").focus();
    	return;
 	}	
 	$.post("/socketbox/reset/password/",{email : email},function(result){
		console.log(result);
		result=JSON.parse(result);
		if(result.status=="success")
		{
			console.log("email sent");
			forgotpassservalert.success("Please check your email for further instructions on how to reset your password!");	
			$("#email").val("");
		}
		else if(result.status=="userdoesnotexist")
		{
			console.log("does not exist");
			forgotpassservalert.warning("This Email ID is not associated with a socketbox account");	
			$("#email").val("");
		}
		else
		{
			console.log("communication error");
			forgotpassservalert.warning("Error in communicating with server . Please try again later!");	
		}
	loading.stop();

	});
}

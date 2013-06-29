function resetpass()
{
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
			regservalert.success("Please check your email for further instructions on how to reset your account!");	
			$("#email").val("");
		}
		else if(result.status=="userdoesnotexist")
		{
			console.log("does not exist");
			regservalert.warning("This Email ID is not associated with a socketbox account");	
			$("#email").val("");
		}
		else
		{
			console.log("communication error");
			regservalert.warning("Error in communicating with server . Please try again later!");	
		}
	});
}
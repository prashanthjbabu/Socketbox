function feedbacksubmit()
{
	$('#feedback-error-content').html("");
	loading = function() {}
	loading.start = function() {
		$('#loading').html('<img src="/static/media/loading.gif" alt="Loading"/>');
	}
	loading.stop = function() {
		$('#loading').html('')
	}
	loading.start();
	feedbackalert = function() {}
	feedbackalert.warning = function(message) {
            $('#feedback-error-content').html('<div class="alert alert-error"><a class="close" data-dismiss="alert">×</a><span>'+message+'</span></div>')
        }
    feedbackalert.success = function(message) {
            $('#feedback-error-content').html('<div class="alert alert-success"><a class="close" data-dismiss="alert">×</a><span>'+message+'</span></div>')
        }
    var name=document.getElementById("name").value;
    var email=document.getElementById("email").value;
    var subject=document.getElementById("subject").value;
    var message=document.getElementById("message").value;

    if(name=="" || name==null)
    {
    	feedbackalert.warning("Please enter a valid name!");
		$("#name").focus();
		loading.stop();
		return;
    }
    var emailfilter = /^([a-zA-Z0-9_\.\-])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/;

    if (!emailfilter.test(email)) 
    {
		//$("#register-error-content").text("Please enter a valid email");
		feedbackalert.warning("Please enter a valid email!");
    	$("#email").focus();
    	loading.stop();
    	return;
 	}
 	if(subject=="na")
 	{
 		feedbackalert.warning("Please enter a valid subject!");
		$("#subject").focus();
		loading.stop();
		return;
 	}
 	if(message=="" || message==null)
 	{
 		feedbackalert.warning("Please enter a valid message!");
		$("#message").focus();
		loading.stop();
		return;
 	}	

 	$.post("/socketbox/feedback/",{name : name,email : email,subject : subject,message : message },function(result){
	console.log(result);
	result=JSON.parse(result);
	if(result.status=="success")
	{
		console.log("thanks for feedback");
		feedbackalert.success("Thank you for your submission!We will surely check it out!");	
		clearfeedbackall();
	}
	else 
		{
			console.log("something went wrong");	
			feedbackalert.warning("We're sorry , something went wrong . Please try again later!");
		}
  	//write response handle code here
  	loading.stop();
  });

}
function clearfeedbackall()
{
	$("#name").val("");
	$("#email").val("");
	$("#subject").val("");
	$("#message").val("");
}
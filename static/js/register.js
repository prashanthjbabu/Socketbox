function validateregister()
{
	$("#register-error-content").text("");
	var name=document.getElementById("name").value;
	var email=document.getElementById("emailid").value;
	var password=document.getElementById("pass").value;
	var cpassword=document.getElementById("cpass").value;
	console.log("name="+name);
	console.log("email="+email);
	console.log("pass="+password);
	console.log("cpass="+cpassword);
	var emailfilter = /^([a-zA-Z0-9_\.\-])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/;

	if(name==null || name=="")
	{
		$("#register-error-content").text("Please enter a valid name");
		$("#name").focus();
		return;
	}

    if (!emailfilter.test(email)) 
    {
	   	console.log(email);
		$("#register-error-content").text("Please enter a valid email");
    	$("#email").focus();
    	return;
 	}	
}
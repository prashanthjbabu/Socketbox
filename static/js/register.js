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
 	var passfilter=  /^[A-Za-z]\w{7,14}$/;  
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
	if(!passfilter.test(password))   
	{   
		$("#register-error-content").text("Password must be atleast 7 characters");
		return;  
	}
	if(password!=cpassword)
	{
		$("#register-error-content").text("Passwords do not match");
		return;	
	}  
}
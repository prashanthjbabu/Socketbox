function validateregister()
{
	regservalert = function() {}
	regservalert.warning = function(message) {
            $('#register-server-alerts').html('<div class="alert"><a class="close" data-dismiss="alert">×</a><span>'+message+'</span></div>')
        }
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
	$.post("/socketbox/user/add/",{name : name,email : email,password : password },function(result){
	console.log(result);
	result=JSON.parse(result);
	if(result.status=="success")
	{
		console.log("user added successfully.. user id ="+result.user_id);
		console.log("user added successfully.. user id ="+result.user_id);

	}
	else if(result.status=="userexists")
	{
		console.log("user already exists");
		regservalert.warning("This user already exists , please try using another email id");	
	}
		else 
		console.log("something went wrong");	
  	//write response handle code here

  }); 
}
function validateregister()
{
	regservalert = function() {}
	regservalert.warning = function(message) {
            $('#register-server-alerts').html('<div class="alert alert-error"><a class="close" data-dismiss="alert">×</a><span>'+message+'</span></div>')
        }
    regservalert.success = function(message) {
            $('#register-server-alerts').html('<div class="alert alert-success"><a class="close" data-dismiss="alert">×</a><span>'+message+'</span></div>')
        }
    regerrorcontent=function() {}
    regerrorcontent.error=function(message) {
    		$("#register-error-content").html('<div class="control-group error"><div class="controls"><span class="help-inline">'+message+'</span></div></div>')
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
		//$("#register-error-content").text("Please enter a valid name");
		regerrorcontent.error("Please enter a valid name!");
		$("#name").focus();
		return;
	}

    if (!emailfilter.test(email)) 
    {
		//$("#register-error-content").text("Please enter a valid email");
		regerrorcontent.error("Please enter a valid email!");
    	$("#email").focus();
    	return;
 	}	
	if(!passfilter.test(password))   
	{   
		//$("#register-error-content").text("Password must be atleast 7 characters");
		regerrorcontent.error("Password must be atleast 7 characters!");
		return;  
	}
	if(password!=cpassword)
	{
		//$("#register-error-content").text("Passwords do not match");
		regerrorcontent.error("Passwords do not match!");
		return;	
	} 
	$.post("/socketbox/user/add/",{name : name,email : email,password : password },function(result){
	console.log(result);
	result=JSON.parse(result);
	if(result.status=="success")
	{
		console.log("user added successfully.. user id ="+result.user_id);
		regservalert.success("Congratulations! Account Created Succesfully . You may now Login with your credentials!");	
		clearall();
	}
	else if(result.status=="userexists")
	{
		console.log("user already exists");
		regservalert.warning("This user already exists , please try using another email id");	
	}
		else 
		{
			console.log("something went wrong");	
			regservalert.warning("We're sorry , something went wrong . Please try again later!");
		}
  	//write response handle code here

  }); 
}
function clearall()
{
	$("#name").val("");
	$("#emailid").val("");
	$("#pass").val("");
	$("#cpass").val("");
}

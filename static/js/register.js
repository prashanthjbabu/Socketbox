function toTitleCase(str)
{
    return str.replace(/\w\S*/g, function(txt){return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();});
}
function validateregister()
{
	loading = function() {}
	loading.start = function() {
		$('#loading').html('<img src="/static/media/loading.gif" alt="Loading"/>');
	}
	loading.stop = function() {
		$('#loading').html('')
	}

	loading.start();
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
		loading.stop();
		return;
	}

    if (!emailfilter.test(email)) 
    {
		//$("#register-error-content").text("Please enter a valid email");
		regerrorcontent.error("Please enter a valid email!");
    	$("#email").focus();
    	loading.stop();
    	return;
 	}	
	if(!passfilter.test(password))   
	{   
		//$("#register-error-content").text("Password must be atleast 7 characters");
		regerrorcontent.error("Password must be atleast 7 characters!");
		loading.stop();
		return;  
	}
	if(password!=cpassword)
	{
		//$("#register-error-content").text("Passwords do not match");
		regerrorcontent.error("Passwords do not match!");
		loading.stop();
		return;	
	} 
	$.post("/socketbox/user/add/",{name : name,email : email,password : password },function(result){
	console.log(result);
	result=JSON.parse(result);
	if(result.status=="success")
	{
		console.log("user added successfully.. user id ="+result.user_id);
		regservalert.success("Congratulations! Account Created Succesfully . Please activate your account by clicking on the activation link sent to your email!");	
		clearall();
	}
	else if(result.status=="userexists")
	{
		console.log("user already exists");
		regservalert.warning("This username already exists , please try using another email id");	
	}
	else 
		{
			console.log("something went wrong");	
			regservalert.warning("We're sorry , something went wrong . Please try again later!");
		}
  	//write response handle code here
  	loading.stop();
  }); 
}
function clearall()
{
	$("#name").val("");
	$("#emailid").val("");
	$("#pass").val("");
	$("#cpass").val("");
}

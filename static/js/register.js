function register()
{
	var name=document.getElementById("name").value;
	var email=document.getElementById("email").value;
	var password=document.getElementById("password").value;
	var cpassword=document.getElementById("cpassword").value;

	if(name==null || name=="")
	{
		$("#register-error-content").value("Please enter a valid name");
		return;
	}	
}
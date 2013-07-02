function editaccount()
{
    $('#account-error-content').html('');
	loading = function() {}
	loading.start = function() {
		$('#loading').html('<img src="/static/media/loading.gif" alt="Loading"/>');
	}
	loading.stop = function() {
		$('#loading').html('')
	}

	loading.start();
	accountservalert = function() {}
	accountservalert.warning = function(message) {
            $('#account-error-content').html('<div class="alert alert-error"><a class="close" data-dismiss="alert">×</a><span>'+message+'</span></div>')
        }
    accountservalert.success = function(message) {
            $('#account-error-content').html('<div class="alert alert-success"><a class="close" data-dismiss="alert">×</a><span>'+message+'</span></div>')
        }    
	$("#account-error-content").text("");
	var password=document.getElementById("pass").value;
	var newpassword=document.getElementById("newpass").value;
	var newcpassword=document.getElementById("newcpass").value;
 	var passfilter=  /^[A-Za-z]\w{7,14}$/;  
	if(!passfilter.test(password) || !passfilter.test(newpassword))   
	{   
		//$("#account-error-content").text("Password must be atleast 7 characters");
		accountservalert.warning("Password must be atleast 7 characters!");
		loading.stop();
		return;  
	}
	if(newpassword!=newcpassword)
	{
		//$("#account-error-content").text("Passwords do not match");
		accountservalert.warning("Passwords do not match!");
		loading.stop();
		return;	
	} 
	newpassword=$.md5(newpassword);
	$.post("/socketbox/account/edit/",{name : name, password : password , newpassword : newpassword },function(result){
	console.log(result);
	result=JSON.parse(result);
	if(result.status=="success")
	{
		console.log("account updated successfully");
		accountservalert.success("Congratulations! Account Updated Succesfully!");	
	}
	else if(result.status=="incorrectpassword")
	{
		console.log("wrong password");
		accountservalert.warning("You have entered an invalid current password . Please try again!");	
	}
	else 
	{
		console.log("something went wrong");	
		accountservalert.warning("We're sorry , something went wrong . Please try again later!");
	}
  	//write response handle code here
  	loading.stop();
  }); 
}
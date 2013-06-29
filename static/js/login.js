function userlogin()
{
	var navemail=document.getElementById("navemail").value;
	var navpass=document.getElementById("navpass").value;
	var emailfilter = /^([a-zA-Z0-9_\.\-])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/;
 	var passfilter=  /^[A-Za-z]\w{7,14}$/;

 	if (!emailfilter.test(navemail) || !passfilter.test(navpass)) 
    {
    	window.location.href='/socketbox/login/';
	}

}
function userlogout()
{
	
}
function encryptnavpass()
{

	document.getElementById("navpass").value=$.md5(document.getElementById("navpass").value);
	console.log(document.getElementById("navpass").value);
	alert("HI");
}
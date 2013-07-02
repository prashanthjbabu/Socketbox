function encryptnavpass()
{

	document.getElementById("navpass").value=$.md5(document.getElementById("navpass").value);
}
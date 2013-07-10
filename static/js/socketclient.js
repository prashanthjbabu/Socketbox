var socket;
function startclient()
{
	loading = function() {}
	loading.start = function() {
		$('#loading').html('<img src="/static/media/loading.gif" alt="Loading"/>');
	}
	loading.stop = function() {
		$('#loading').html('')
	}

	loading.start();
	socketclientalert = function() {}
	socketclientalert.warning = function(message) {
            $('#client-content').html('<div class="alert alert-error"><a class="close" data-dismiss="alert">×</a><span>'+message+'</span></div>')
        }
    socketclientalert.success = function(message) {
            $('#client-content').html('<div class="alert alert-success"><a class="close" data-dismiss="alert">×</a><span>'+message+'</span></div>')
        }	

    var channelname=document.getElementById("channelname").value;
	if(channelname==null || channelname=="")
	{
		//$("#register-error-content").text("Please enter a valid name");
		socketclientalert.warning("Please enter a valid channel name!");
		$("#channelname").focus();
		loading.stop();
		return;
	}    
    var eventname=document.getElementById("eventname").value;
	if(eventname==null || eventname=="")
	{
		//$("#register-error-content").text("Please enter a valid name");
		socketclientalert.warning("Please enter a valid event name!");
		$("#eventname").focus();
		loading.stop();
		return;
	}
	var apikey=document.getElementById("apikey").value
    socket = new SocketBox(apikey);
    socket.subscribe(channelname);
    socket.bind(eventname, function(data) {
        console.log(data);
    });

}
function stopclient()
{
	socket.removeAllListeners(document.getElementById("channelname").value);
}
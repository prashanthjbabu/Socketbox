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
        updatetable(channelname,eventname,data)
    });
    socketclientalert.success("SocketBox Client is running");
    //$("channelname").blur();
	//$("eventname").blur();
	$("#channelname").attr("disabled", "disabled");
	$("#eventname").attr("disabled", "disabled");
}
function updatetable(channel_name,event_name,data)
{
	to_append="<tr><td>"+channel_name+"</td><td>"+event_name+"</td><td>"+data+"</td></tr>"
	$("#tablebody").html(to_append+$("#tablebody").html());
}
function stopclient()
{
	socket.removelisteners();
	//$("eventname").focus();
    //$("channelname").focus();
    $("#channelname").removeAttr("disabled");
    $("#eventname").removeAttr("disabled");
    socketclientalert.warning("SocketBox Client has stopped");

}
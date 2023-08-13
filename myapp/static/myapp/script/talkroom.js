document.addEventListener("DOMContentLoaded", function () {
    const URL = window.location.href;
    var URLparts = URL.split('/');
    const friendID = parseInt(URLparts[URLparts.length - 1]);
    const myID = parseInt(URLparts[URLparts.length - 2]);
    const chatSocket = new WebSocket(
        'ws://' + window.location.host + '/ws/talk_room/' + myID + '/' + friendID + '/'
    );
    chatSocket.onclose = function (e) {
        window.alert("Chat Socket Closed Unexpectedly");
    };
    chatSocket.onmessage = function (e) {
        const data = JSON.parse(e.data);
        var cn = document.getElementById("cn");
        var mes = document.createElement("div");
        mes.className = "message";
        var name_time = document.createElement("div");
        name_time.className = "name_time";
        var name = document.createElement("div");
        name.className = "name";
        var time = document.createElement("div");
        time.className = "time";
        var text = document.createElement("div");
        text.className = "text";
        var p_name = document.createElement("p");
        var p_time = document.createElement("p");
        var p_text = document.createElement("p");
        name.appendChild(p_name);
        name_time.appendChild(name);
        time.appendChild(p_time);
        name_time.appendChild(time);
        text.appendChild(p_text);
        mes.appendChild(name_time);
        mes.appendChild(text);
        cn.appendChild(mes);
        // 実装必要
        var today = new Date();
        p_time.textContent = today.getFullYear() + '年' + today.getMonth() + '月' + today.getDate() + '日' + today.getHours() + ':' + today.getMinutes();
        // window.alert(p_time.textContent);
        p_text.textContent = data.message;
        if (myID === parseInt(data.myID)) {
            p_name.textContent = "> 自分";
        }else{
            var friendname = "> " + document.getElementById("friends_name").textContent;
            p_name.textContent = friendname;
        }
    
    }
    document.getElementById("id_message").addEventListener("keydown", function (e) {
        if (e.keyCode === 13) {
            const message = document.getElementById("id_message").value;
            chatSocket.send(JSON.stringify({
                'myID': myID,
                'friendID': friendID,
                'message': message,
            }));
            document.getElementById("id_message").value = "";
        }
    }, false);

}, false);



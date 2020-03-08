function getNow(){
    var nowTime = new Date();
    var nowHour = ('0' + nowTime.getHours()).slice(-2);
    var nowMin = ('0' + nowTime.getMinutes()).slice(-2);
    var nowSec = ('0' + nowTime.getSeconds()).slice(-2);
    var msg = nowHour+":"+nowMin+":"+nowSec
    document.getElementById("Clock").innerHTML = msg
    return msg
}


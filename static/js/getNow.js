function getNow(){
    var nowTime = new Date();
    var nowHour = nowTime.getHours();
    var nowMin = nowTime.getMinutes();
    var nowSec = nowTime.getSeconds();
    var msg = nowHour+":"+nowMin+":"+nowSec
    document.getElementById("Clock").innerHTML = msg
    return msg
}


function display(id){
	var traget=document.getElementById(id);
	traget.style.display="";
}

function dismiss(id){
    document.getElementById(id).style.display='none';
}

function apply_for_use(){
	var obj = document.getElementById('select_period');
	var obj2 = document.getElementById('select_type');
	var index = obj.selectedIndex;
	var index2 = obj2.selectedIndex;
	var now = new Date();
	var yy = now.getFullYear();      //年
	var mm = now.getMonth() + 1;     //月
	var dd = now.getDate();          //日
	var hh = now.getHours();         //时
	var ii = now.getMinutes();       //分
	var ss = now.getSeconds();       //秒
	var clock = yy + "-";
	if(mm < 10) clock += "0";
	clock += mm + "-";
	if(dd < 10) clock += "0";
	clock += dd + " ";
	if(hh < 10) clock += "0";
	clock += hh + ":";
	if (ii < 10) clock += '0';
	clock += ii + ":";
	if (ss < 10) clock += '0';
	clock += ss;
    r = new XMLHttpRequest();
	r.open('GET','/account_sharing/add_log/'+clock+'/'+obj.options[index].value+'/'+obj2.options[index2].value,true);
	r.send();
    r.onload = function() {
        console.log(this.responseText);
        var resp = JSON.parse(this.responseText);

        document.getElementById("apply_use_result_info").innerHTML=resp['apply_use_result_info'];
        document.getElementById("download_code_url").innerHTML=resp['download_code_url']
        document.getElementById('log_content').innerHTML = resp['log_content'];
        display('apply_use_result_info');
    }
}
function delete_account(obj) {
    console.log(obj.name);
    var c = window.confirm('是否删除账号：' + obj.name);
    if (c == true) {
        r = new XMLHttpRequest();
        r.open('GET', '/account_sharing/admin/delete_account/?aid=' + obj.id, true);
        r.send();
        r.onload = function () {
            if (this.responseText == 'success') {
                alert('申请成功');
                location.reload();
            } else {
                alert(this.responseText);
            }

        }
    }
}

function delete_history(obj) {
    var c = window.confirm('是否提前终止使用');
    if (c == true) {
        r = new XMLHttpRequest();
        r.open('GET', '/account_sharing/admin/delete_history/?id=' + obj.name, true);
        r.send();
        r.onload = function () {
            if (this.responseText == 'success') {
                alert('删除成功');
                location.reload();
            } else {
                alert(this.responseText);
            }

        }
    }
}

function delete_apply(obj) {
    var c = window.confirm('是否撤销、删除该申请记录');
    if (c == true) {
        r = new XMLHttpRequest();
        r.open('GET', '/account_sharing/admin/delete_apply/?apply_id=' + obj.name, true);
        r.send();
        r.onload = function () {
            if (this.responseText == 'success') {
                alert('删除成功');
                location.reload();
            } else {
                alert('删除失败');
            }
        }
    }
}
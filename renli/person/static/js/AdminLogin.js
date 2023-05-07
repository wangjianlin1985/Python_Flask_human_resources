// 浏览器写入cookie
function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(function(){
     // var superadminloginform = $('#superadminloginform')
    // form表单提交
    $("#Adminloginbtn").click(function(){
        var admin_id = $("#adminuser").val()
        var admin_psw = $("#adminpsw").val()


        // 发起登录请求
        var params = {
            'admin_id':admin_id,
            'admin_psw':admin_psw
        };
        // 发起ajax请求
        $.ajax({
            url:'/adminlogin',
            type:'post',
            data:JSON.stringify(params),
            contentType:'application/json',
            headers: {
                    "X-CSRFToken": getCookie('csrf_token')
                },
            success:function(data){
                if (data.errno == 0){
                    window.location.href='/AdminChoose.html'
                }else{
                    alert('用户名或密码错误!')
                }
            }
        })


    })


})
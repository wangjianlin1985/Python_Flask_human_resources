// 浏览器写入cookie
function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}
$(function () {
    $('#ret').click(function () {
        window.location.href = '/AdminChoose.html'
    })
    var index_=-1
    $('.edit').click(function(){
        index_ = $('.edit').index($(this))
        var userId=$(this).parent().parent().children('td').eq(0).text()
        window.userId=userId
    })
    $('#add_btn').click(function () {
        var user_id = $(".userID").val()
        var user_name = $(".userName").val()
        var user_age = $(".userAge").val()
        var user_gender = $("#user_gender option:selected").val()
        var user_department = $("#user_department option:selected").val()
        var user_tel = $(".userTel").val()
        var user_email = $(".userEmail").val()

        if(index_!=-1){
            if($('#show_tbody').children('tr').eq(index_).attr('class')=='has_case'){
                // 发起编辑请求
                var params = {
                    'userId': userId,
                    'euser_id': user_id,
                    'euser_name': user_name,
                    'euser_age': user_age,
                    'euser_gender': user_gender,
                    'euser_department': user_department,
                    'euser_tel': user_tel,
                    'euser_email': user_email
                }
                // 发起ajax请求
                $.ajax({
                    url: '/editor_admindepartment',
                    type: 'put',
                    data: JSON.stringify(params),
                    async: false,
                    contentType: 'application/json',
                    headers: {
                        "X-CSRFToken": getCookie('csrf_token')
                    },
                    success: function (data) {
                        if (data.errno == 0) {
                            //刷新当前页面
                            window.location.reload()
                            alert('修改员工数据成功!')


                        } else {
                            alert('修改员工数据失败!')
                            window.location.reload()
                        }
                    },
                })
                index_=-1
            }
        }else{

            var params = {
                'auser_id': user_id,
                'auser_name': user_name,
                'auser_age': user_age,
                'auser_gender': user_gender,
                'auser_department': user_department,
                'auser_tel': user_tel,
                'auser_email': user_email
            }
            // 发起ajax请求
            $.ajax({
                url: '/add_admindepartment',
                type: 'post',
                data: JSON.stringify(params),
                contentType: 'application/json',
                headers: {
                    "X-CSRFToken": getCookie('csrf_token')
                },
                success: function (data) {
                    if (data.errno == '0') {
                        //刷新当前页面
                        alert('新增员工数据成功!')
                        window.location.reload()
                    } else {
                        alert('新增员工数据失败!')
                        window.location.reload()
                    }
                }
            })
            index_=-1
        }
    })
    $('#show_tbody').on('click', '.edit', function () {
        trIndex = $('.edit', '#show_tbody').index($(this));
        addEnter = false;
        $(this).parents('tr').addClass('has_case');
        methods.editHandle(trIndex);
    })
    $('#search_btn').click(function () {
        methods.seachName();
    })
    $('#back_btn').click(function () {
        $('#Ktext').val(' ');
        methods.resectList();
    })
    $('.del').click(function () {
        $(this).parents('tr').remove();
        var userId = $(this).parents('tr').children().eq(0).text()

        // 发起新增请求
        var params = {
            'userId': userId
        }
        // 发起删除ajax请求
        $.ajax({
            url: '/delete_user',
            type: 'delete',
            data: JSON.stringify(params),
            contentType: 'application/json',
            headers: {
                "X-CSRFToken": getCookie('csrf_token')
            },
            success: function (data) {
                if (data.errno == 0) {
                    //刷新当前页面
                    window.location.reload()
                    alert('删除员工数据成功!')

                } else {
                    alert('删除员工数据失败!')
                    window.location.reload()
                }
            }
        })
    })

    // 监控退出登录按钮
    $('#exit').click(function () {
        // 发起ajax请求
        $.ajax({
            url: '/exit_admin',
            type: 'post',
            contentType: 'application/json',
            headers: {
                "X-CSRFToken": getCookie('csrf_token')
            },
            success: function (data) {
                if (data.errno == 0) {
                    //刷新当前页面
                    window.location.href = '/'
                    alert('退出登录成功!')

                } else {
                    window.location.reload()
                    alert('退出登录失败!')
                }
            }
        })
    })

    $('#renyuan').on('hide.bs.modal', function () {
        addEnter = true;
        $('#show_tbody tr').removeClass('has_case');
        $('#xztb input').val(' ');
        $('#xztb select').find('option:first').prop('selected', true)
    });
})
var addEnter = true,
    noRepeat = true,
    jobArr = [],
    phoneArr = [],
    tdStr = '',
    trIndex, hasNullMes = false,
    tarInp = $('#xztb input'),
    tarSel = $('#xztb select');
var methods = {
    addHandle: function (the_index) {
        hasNullMes = false;
        methods.checkMustMes();
        if (hasNullMes) {
            return;
        }
        if (addEnter) {
            methods.checkRepeat();
            if (noRepeat) {
                methods.setStr();
                $('#show_tbody').append('<tr>' + tdStr + '</tr>');
                $('#renyuan').modal('hide');
            }
        } else {
            methods.setStr();
            $('#show_tbody tr').eq(trIndex).empty().append(tdStr);
            $('#renyuan').modal('hide');
        }
    }, editHandle: function (the_index) {
        var tar = $('#show_tbody tr').eq(the_index);
        var nowConArr = [];
        for (var i = 0; i < tar.find('td').length - 1; i++) {
            var a = tar.children('td').eq(i).html();
            nowConArr.push(a);
        }
        $('#renyuan').modal('show');
        for (var j = 0; j < tarInp.length; j++) {
            tarInp.eq(j).val(nowConArr[j])
        }
        for (var p = 0; p < tarSel.length; p++) {
            var the_p = p + tarInp.length;
            tarSel.eq(p).val(nowConArr[the_p]);
        }
    }, setStr: function () {
        tdStr = '';
        for (var a = 0; a < tarInp.length; a++) {
            tdStr += '<td>' + tarInp.eq(a).val() + '</td>'
        }
        for (var b = 0; b < tarSel.length; b++) {
            tdStr += '<td>' + tarSel.eq(b).val() + '</td>'
        }
        tdStr += '<td><a href="#" class="edit">编辑</a> <a href="#" class="del">删除</a></td>';
    }, seachName: function () {
        var a = $('#show_tbody tr');
        var nameVal = $('#Ktext').val().trim();
        var nameStr = '',
            nameArr = [];
        if (nameVal === '') {
            bootbox.alert({
                title: "来自火星的提示",
                message: "搜索内容不能为空",
                closeButton: false
            })
            return;
        }
        for (var c = 0; c < a.length; c++) {
            var txt = $('td:first', a.eq(c)).html().trim();
            nameArr.push(txt);
        }
        a.hide();
        for (var i = 0; i < nameArr.length; i++) {
            if (nameArr[i].indexOf(nameVal) > -1) {
                a.eq(i).show();
            }
        }
    }, resectList: function () {
        $('#show_tbody tr').show();
    }, checkMustMes: function () {
        if ($('.userName').val().trim() === '') {
            bootbox.alert({
                title: "来自火星的提示",
                message: "姓名为必选项，请填写",
                closeButton: false
            })
            hasNullMes = true;
            return
        }
        if ($('.jobNum').val().trim() === '') {
            bootbox.alert({
                title: "来自火星的提示",
                message: "工号为必选项，请填写",
                closeButton: false
            })
            hasNullMes = true;
            return
        }
        if ($('.phoneNum').val().trim() === '') {
            bootbox.alert({
                title: "来自火星的提示",
                message: "手机号为必选项，请填写",
                closeButton: false
            })
            hasNullMes = true;
            return
        }
    }, checkRepeat: function () {
        jobArr = [], phoneArr = [];
        for (var i = 0; i < $('#show_tbody tr:not(".has_case")').length; i++) {
            var par = '#show_tbody tr:not(".has_case"):eq(' + i + ')';
            var a = $('td:eq(1)', par).html().trim(),
                b = $('td:eq(2)', par).html().trim();
            jobArr.push(a);
            phoneArr.push(b);
        }
        var jobNum = $('.jobNum').val().trim(),
            phoneNum = $('.phoneNum').val().trim();
        if (jobArr.indexOf(jobNum) > -1) {
            noRepeat = false;
            bootbox.alert({
                title: "来自火星的提示",
                message: "工号重复了，请重新输入",
                closeButton: false
            })
            return;
        }
        if (phoneArr.indexOf(phoneNum) > -1) {
            noRepeat = false;
            bootbox.alert({
                title: "来自火星的提示",
                message: "手机号码重复了，请重新输入",
                closeButton: false
            })
            return;
        }
        noRepeat = true;
    }
}
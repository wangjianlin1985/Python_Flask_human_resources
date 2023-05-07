// 浏览器写入cookie
function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}
$(function () {
    var index_ = -1
    $('.edit').click(function () {
        index_ = $('.edit').index($(this))
        var admin_id_ = $(this).parent().parent().children('td').eq(0).text()
        window.admin_id_ = admin_id_
    })
    $('#add_btn').click(function () {
        var admin_id = $(".userName").val()
        var admin_psw = $(".jobNum").val()

        if (index_ != -1) {
            if ($('#show_tbody').children('tr').eq(index_).attr('class') == 'has_case') {
                // 发起编辑请求
                var params = {
                    'admin_id_': admin_id_,
                    'editor_admin_id': admin_id,
                    'editor_admin_psw': admin_psw
                }
                // 发起ajax请求
                $.ajax({
                    url: '/editor_admin',
                    type: 'put',
                    data: JSON.stringify(params),
                    contentType: 'application/json',
                    headers: {
                        "X-CSRFToken": getCookie('csrf_token')
                    },
                    success: function (data) {
                        if (data.errno == 0) {
                            //刷新当前页面
                            window.location.reload()
                            alert('修改管理员数据成功!')

                        } else {
                            window.location.reload()
                            alert('修改管理员数据失败!')

                        }
                    }
                })
                index_ = -1
            }
        } else {
            var params = {
                'admin_id': admin_id,
                'admin_psw': admin_psw
            }
            // 发起ajax请求
            $.ajax({
                url: '/add_admin',
                type: 'post',
                data: JSON.stringify(params),
                contentType: 'application/json',
                headers: {
                    "X-CSRFToken": getCookie('csrf_token')
                },
                success: function (data) {
                    if (data.errno == 0) {
                        //刷新当前页面
                        window.location.reload()
                        alert('新增管理员数据成功!')
                    } else {
                        alert('新增管理员数据失败!')
                        window.location.reload()
                    }
                }
            })
            index_ = -1
        }
    })

    $('#exit').click(function () {
        // 发起ajax请求
        $.ajax({
            url: '/exit_superadminpsw',
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
                    alert('退出登录失败!')
                }
            }
        })
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

        // 发送ajax请求

        var admin_id = $(this).parents('tr').children().eq(0).text()
        var admin_psw = $(this).parents('tr').children().eq(1).text()

        // 发起新增请求
        var params = {
            'admin_id': admin_id,
            'admin_psw': admin_psw
        }
        // 发起ajax请求
        $.ajax({
            url: '/delete_admin',
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
                    alert('删除管理员数据成功!')

                } else {
                    alert('删除管理员数据失败！')
                    window.location.reload()
                }
            }
        })
    })

    // 监控修改密码按钮
    $('.submitBtn').click(function () {
        // 发送ajax请求
        var superadminpsw = $("#superadminpsw").val()
        var editorsuperadminpsw = $("#editorsuperadminpsw").val()


        // 请求参数
        var params = {
            'superadminpsw': superadminpsw,
            'editorsuperadminpsw': editorsuperadminpsw
        };
        // 发起ajax请求
        $.ajax({
            url: '/editor_superadminpsw',
            type: 'post',
            data: JSON.stringify(params),
            contentType: 'application/json',
            headers: {
                "X-CSRFToken": getCookie('csrf_token')
            },
            success: function (data) {
                if (data.errno == 0) {
                    //刷新当前页面
                    window.location.href = '/SuperadminLogin.html'
                    alert('修改超级管理员密码成功,请重新登录!')
                } else {
                    alert('修改超级管理员密码失败!')
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
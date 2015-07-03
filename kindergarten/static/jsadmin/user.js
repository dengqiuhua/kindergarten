/**
 * Created with PyCharm.
 * User: Administrator
 * Date: 15-7-3
 * Time: 下午6:03
 * To change this template use File | Settings | File Templates.
 */
//初始化用户输入框的值
var initTextUserName=$.trim($("input[name=txtUserName]").attr("placeholder"));

$(function(){


});//end jq


//搜索条件
var data_search={};
//搜索
function seachData(){
    var name= $.trim($("input[name=txtName]").val());
    data_search["name"]=name;
    getDataList(1, urls.url_get);
}

//获取数据分页列表
function getDataList(pageindex,url){
    var data2 = new pageData({url: url, callback: "getDataList",data:data_search, pageindex: pageindex}, function (msg) {
        $("#datalist").html(fillDataList(msg,pageindex));
    });
}

//解析数据列表
function fillDataList(msg,pageindex){
    var html = "";
    if (msg != null && msg != "") {
        html = "<tr><th>姓名</th><th>用户名</th><th>邮箱</th><th>修改 | 重置密码 | 删除</th></tr>";
        $.each(msg, function (i, n) {
            var name = n.first_name != null && n.first_name != "" ? n.first_name : n.username;
            html += "<tr>";
            html += "<td><a href=\"#\" title=\"" + n.first_name + "\">" + n.first_name + "</a></td>";
            html += "<td>" + n.username + "</td>";
            html += "<td>" + (n.email!=null?n.email:"") + "</td>";
            html += "<td>";
            html += "<a href=\"javascript:;\" onclick=\"initEditUser(" + n.id + ",'" + name + "','" + n.email + "'," + pageindex + ");\"><i class=\"icon-edit\"></i>修改</a> | ";
            html += "<a href=\"javascript:;\" onclick=\"initResetPwd(" + n.id + ",'" + name + "'," + pageindex + ");\"><i class=\"icon-edit\"></i>重置密码</a> | ";
            html += "<a href=\"javascript:;\" onclick=\"deleteData('" + name + "'," + n.id + "," + pageindex + ");\"><i class=\"icon-trash\"></i>删除</a>";
            html += "</td>";
            html += "</tr>";
        });
    }else{
        html = "没有用户";
    }
    return html;
}

//删除
function deleteData(title,id,pageindex){
    if(confirm("您要删除【"+title+"】吗？")){
        $.post(urls.url_delete.replace("0",id),{},function(msg){
            if (msg != null && msg !="") {
                if (msg.result) {
                    alert2("删除成功",1);
                    getDataList(pageindex, urls.url_get);
                }
            }else{
                alert2("删除失败", 2);
            }
            return false;
        });
    }
}

//注册验证
var validateRegForm = function () {
    if ($.trim($("input[name=username]").val()) == "") {
        $("input[name=username]").focus().css("border", "1px solid red");
        return false;
    } else {
        var username = $.trim($("input[name=username]").val());
        if (username.length < 4 || username.length > 30) {
            $("input[name=username]").focus().css("border", "1px solid red");
            $("#reg_tipmsg").text("请输入4-30位的用户名，可以是账号、手机号或邮箱").removeClass("hide");
            return false;
        }
    }
    if ($.trim($("input[name=name]").val()) == "") {
        $("input[name=name]").focus().css("border", "1px solid red");
        return false;
    }

    if ($.trim($("input[name=email]").val()) == "") {
        $("input[name=email]").focus().css("border", "1px solid red");
        return false;
    } else {
        //邮件校验
        if (/^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$/.test($.trim($("input[name=email]").val())) == false) {
            $("input[name=email]").focus().css("border", "1px solid red");
            $("#reg_tipmsg").text("邮箱格式不正确。").removeClass("hide");
            return false;
        }
    }

    if ($.trim($("input[name=password]").val()) == "") {
        $("input[name=password]").focus().css("border", "1px solid red");
        return false;
    }
    if ($.trim($("input[name=password2]").val()) == "") {
        $("input[name=password2]").focus().css("border", "1px solid red");
        return false;
    }
    if ($.trim($("input[name=password2]").val()) != $.trim($("input[name=password]").val())) {
        $("input[name=password2]").focus().css("border", "1px solid red");
        $("#reg_tipmsg").text("两次输入密码不一致。").removeClass("hide");
        return false;
    }
    return true;
};//end validate

//添加
function Register(){
    var username= $.trim($("input[name=username]").val());
    var name = $.trim($("input[name=name]").val());
    var email = $.trim($("input[name=email]").val());
    var password = $.trim($("input[name=password]").val());
    var password2 = $.trim($("input[name=password2]").val());

    if(validateRegForm()){
        var postdata={username:username,name:name,email:email,password:password};
        $.post(urls.url_add, postdata, function (msg) {
            if (msg != null && msg !="") {
                if(msg.result){
                    alert2("注册成功", 1);
                    $("input[type=text],input[type=password]").val("");
                    setTimeout(function(){
                        window.location.href = urls.url_user;
                    })

                }
            }else{
                alert2("操作失败", 2);
            }
            return false;
        });
    }
}


//重置密码弹框
function initResetPwd(userid, username,pageindex) {
    if ($("#password_modal").length > 0)$("#password_modal").remove();
    var html = "";
    html += "<div id=\"password_modal\" class=\"modal hide\" style=\"width:420px;\">";
    html += '<div class="modal-header">';
    html += '<button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>';
    html += '<p style="margin: 0;">';
    html += "<h4>";
    html += "重置用户【" + username + "】的密码";
    html += "</h4>";
    html += '</p>';
    html += '</div>';
    html += "<div class=\"modal-body\" style=\"overflow-y: inherit;\">";

    html += "<form class=\"form-horizontal\">";
    html += "<div class=\"control-group\">";
    html += "<label for=\"inputEmail\" class=\"control-label\">新密码</label><span class=\"text-require\">*</span>";
    html += "<div class=\"controls\">";
    html += "<input type=\"text\" class=\"span4\" placeholder=\"新密码\" value=\"\" id=\"inputEmail\" name=\"password\">";
    html += "</div>";
    html += "</div>";

    html += "</form>";
    html += "<div class=\"alert hide\" style=\"margin:2px;\"></div>";
    html += "</div>";
    html += "<div class=\"modal-footer\">";
    html += "<a href=\"javascript:;\" name=\"a_btn_submit\" class=\"btn btn-info\" onclick=\"setUserPwd(" + userid + "," + pageindex + ");\">保存修改</a>";
    html += "<a href=\"javascript:;\" class=\"btn a_close\" data-dismiss=\"modal\" >关闭</a>";
    html += "</div>";
    html += "</div>";
    //填充
    $("body").append(html);
    //显示弹框
    $("#password_modal").modal('show');
    $("#password_modal input[name=password]").focus();
    $("#password_modal div.alert").text("").addClass("hide").removeClass("alert-success");
    return false;
}

//重置密码
function setUserPwd(userid,pageindex) {
    var password = $.trim($("#password_modal input[name=password]").val());
    if (password == "") {
        $("#password_modal div.alert").text("请输入新密码").removeClass("hide").removeClass("alert-success");
        $("#password_modal input[name=password]").focus();
        return false;
    }
    Ajax(urls.url_password.replace("0", userid), {data: {password: password}}, function (msg) {
        if (msg.result) {
            $("#password_modal .alert").removeClass("hide").addClass("alert-success").text("操作成功！请牢记您的密码。");
            setTimeout(function () {
                $("#password_modal").modal('hide');
            }, 1700)
        } else {
            $("#password_modal .alert").removeClass("hide").addClass("alert-error").text(msg.error);
        }
    })
}


//修改信息弹框
function initEditUser(userid, username,email,pageindex) {
    if ($("#edit_modal").length > 0)$("#edit_modal").remove();
    var html = "";
    html += "<div id=\"edit_modal\" class=\"modal hide\" style=\"width:420px;\">";
    html += '<div class="modal-header">';
    html += '<button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>';
    html += '<p style="margin: 0;">';
    html += "<h4>";
    html += "修改用户【" + username + "】信息";
    html += "</h4>";
    html += '</p>';
    html += '</div>';
    html += "<div class=\"modal-body\" style=\"overflow-y: inherit;\">";

    html += "<form class=\"form-horizontal\">";
    html += "<div class=\"control-group\">";
    html += "<label for=\"inputName\" class=\"control-label\">姓名</label><span class=\"text-require\">*</span>";
    html += "<div class=\"controls\">";
    html += "<input type=\"text\" class=\"span4\" placeholder=\"姓名\" id=\"inputName\" name=\"name\" value=\""+ username +"\">";
    html += "</div>";
    html += "</div>";

    html += "<form class=\"form-horizontal\">";
    html += "<div class=\"control-group\">";
    html += "<label for=\"inputEmail\" class=\"control-label\">邮箱</label>";
    html += "<div class=\"controls\">";
    html += "<input type=\"text\" class=\"span4\" placeholder=\"邮箱\"  value=\""+ email +"\" id=\"inputEmail\" name=\"email\">";
    html += "</div>";
    html += "</div>";

    html += "</form>";
    html += "<div class=\"alert hide\" style=\"margin:2px;\"></div>";
    html += "</div>";
    html += "<div class=\"modal-footer\">";
    html += "<a href=\"javascript:;\" name=\"a_btn_submit\" class=\"btn btn-info\" onclick=\"updateUser(" + userid + "," + pageindex + ");\">保存修改</a>";
    html += "<a href=\"javascript:;\" class=\"btn a_close\" data-dismiss=\"modal\" >关闭</a>";
    html += "</div>";
    html += "</div>";
    //填充
    $("body").append(html);
    //显示弹框
    $("#edit_modal").modal('show');
    $("#edit_modal input[name=name]").focus();
    $("#edit_modal div.alert").text("").addClass("hide").removeClass("alert-success");
    return false;
}

//修改
function updateUser(userid,pageindex) {
    var name = $.trim($("#edit_modal input[name=name]").val());
    var email = $.trim($("#edit_modal input[name=email]").val());
    if (name == "") {
        $("#edit_modal div.alert").text("姓名不能为空").removeClass("hide").removeClass("alert-success");
        $("#edit_modal input[name=name]").focus();
        return false;
    }
    Ajax(urls.url_update.replace("0", userid), {data: {first_name: name,email: email}}, function (msg) {
        if (msg.result) {
            $("#edit_modal .alert").removeClass("hide").addClass("alert-success").text("操作成功！");
            getDataList(pageindex, urls.url_get);
            setTimeout(function () {
                $("#edit_modal").modal('hide');
            }, 1700)
        } else {
            $("#edit_modal .alert").removeClass("hide").addClass("alert-error").text(msg.error);
        }
    })
}

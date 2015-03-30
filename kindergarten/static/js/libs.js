/**
 * Created with PyCharm.
 * User: dengqiuhua
 * Date: 14-7-16
 * Time: 上午10:21
 * To change this template use File | Settings | File Templates.
 */
$(function(){
    //提示框
    setTimeout('$("*[data-toggle=tooltip]").tooltip();',2000);

    //date plus时间日历插件
    if($('input[name="daterange"]').length>0 ){
        var myDate = new Date();
        $('input[name="daterange"]').daterangepicker({
                format: 'YYYY/MM/DD HH:mm',
                timePicker: true,
                timePicker12Hour: false,
                timePickerIncrement: 10,
                startDate: myDate.toLocaleDateString() + " " + myDate.getHours() + ":00"
            }, function (start, end, label) {
                //alert('A date range was chosen: ' + start.format('YYYY-MM-DD HH:mm') + ' to ' + end.format('YYYY-MM-DD HH:mm'));
            }
        );//end date
    }

    //人员搜索弹框
    $(".btn_user_add").on('click',function(e){
        if (e.stopPropagation) {//需要阻止冒泡
            e.stopPropagation();
        } else {
            e.cancelBubble = true;
        }
    });

    //部门机构搜索弹框
    $(".btn_org_add").on('click', function (e) {
        if (e.stopPropagation) {//需要阻止冒泡
            e.stopPropagation();
        } else {
            e.cancelBubble = true;
        }
    });

    //关闭任务详细弹框
    $("#task_detail_modal .close").on('click', function () {
        $("#task_detail_modal").addClass('hide');
    });

    //关闭计划详细弹框
    $("#plan_detail_modal .close").on('click', function () {
        $("#plan_detail_modal").addClass('hide');
    });

    //所有Ajax的post请求需要csrftoken，否则403
    var csrftoken = $.cookie('csrftoken');
    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

});

//点击页面，关闭弹框
document.onclick = function(e){
    if ($("#user_search_modal").length > 0&&!$("#user_search_modal").hasClass("hide")){
        //防止点击自身关闭
        var $target = $(e.target);
        if(!$target.hasClass("btn_user_add")&&!$target.hasClass("btn_org_add")&&$(".btn_user_add,.btn_org_add").has($target).length<1){
            var count=$("#user_search_modal").has($target).length ;
            if(count<1&&$target.attr("id")!="user_search_modal")
                close_user_dialog();
        }
    }
};

//查询用户
function searchUser(username,functionName,isOrg,targetData,projectid){
    //机构查询或者同事查询
    var url = "/api/user/list/?format=json";
    var res_tip = "没有找到同事";
    //机构
    if (isOrg) {
        url = "/api/user/org/?format=json";
        res_tip = "没有找到机构";
    }
    var data_user = {name: username};
    //项目的人
    if (projectid != null && projectid != "") {
        $("#user_search_modal input").attr("placeholder", "输入机构/同事");
        res_tip = "没有找到机构或同事，请先添加项目参与人员和机构";
        data_user['projectid'] = projectid;
    } else {
        if (data_user.projectid != null) {
            data_user.projectid = null;
            data_user.projectid.remove();
        }
    }
    $.get(url,data_user,function(msg){
        var html = "";
        if (msg != null && msg != "") {
            if(msg==-1){
                html = "<tr><td><p>未登入，请先<a href=\"javascript:;\" onclick=\"showLogin();\" style=\"display:inline-block;\">登入</a></p></td></tr>";
            }else{
                $.each(msg, function (i, n) {
                    html += " <tr><td>";
                    var name=n.first_name != '' ? n.first_name : n.username;
                    html += " <a href=\"javascript:;\" target-data=\"" + targetData + "\" onclick=\""+functionName+"(" + n.id + ",'" + name + "',this)\">" + name + "</a>";
                    html += " </td></tr>";
                });
            }
        } else {
            html = "<tr><td><span>" + res_tip + "</span></td></tr>";
        }
        $("#user_search_modal #tb_userlist").html(html);
    });

}

//获取用户弹框
function getUser(functionName,_this,isOrg,targetData,projectid){
    var msg = isOrg ? "机构名称" : "同事姓名或手机号码";
    if ($("#user_search_modal").length < 1) {
        var html = "";
        html += "<div id=\"user_search_modal\" class=\"modal\">";
        html += "<div class=\"modal-header\">";
        html += "<button type=\"button\" class=\"close\" data-dismiss=\"modal\" aria-hidden=\"true\" onclick=\"close_user_dialog();\">&times;</button>";
        html += "<p>";
        html += "<input type=\"text\" name=\"txtUserName\" data-provide=\"typeahead\" placeholder=\"输入" + msg + "\">";
        html += "</p>";
        html += "</div>";
        html += "<div class=\"modal-body\">";
        html += "<p>";
        html += "<table id=\"tb_userlist\" class=\"table table-hover\">";
        html += "<tr>";
        html += "<td>正在努力寻找...</td>";
        html += "</tr>";
        html += "</table>";
        html += "</p>";
        html += "</div>";
        html += "<div class=\"modal-footer\">";
        html += "<a href=\"javascript:;\" class=\"btn a_close\" onclick=\"close_user_dialog();\">关闭</a>";
        html += "</div>";
        html += "</div>";
        //填充
        $("body").append(html);
        //搜索提示
        $('#user_search_modal input[name=txtUserName]').on('keyup', function () {
            var username = $.trim($(this).val());
            searchUser(username, functionName, isOrg, targetData, projectid);
            return false;
        });
    } else {
        if ($("#user_search_modal").hasClass('hide')) {
            $("#user_search_modal input[name=txtUserName]").attr('placeholder', "输入" + msg);
            $("#user_search_modal").removeClass('hide');
            $('#user_search_modal input[nametxtUserName]').focus();
        }
    }
    //查询用户
    searchUser("", functionName, isOrg, targetData, projectid);
    //获取焦点
    $('#user_search_modal input[name=txtUserName]').val("").focus();
    var _offset_top = $(_this).position().top;
    var _offset_left = $(_this).position().left;
    var _height = $(_this).height() + 5;
    var _width_page = document.body.scrollWidth;
    //不能超过右边
    _offset_left = _offset_left > (_width_page - $("#user_search_modal").width()) ? _width_page - $("#user_search_modal").width() - 12 : _offset_left;
    //设置弹框的位置
    $("#user_search_modal").removeClass('hide').css({"top": _offset_top, "left": _offset_left, "margin-top": _height});
}

//关闭搜索同事弹框
function close_user_dialog(){
    //关闭人员搜索弹框
    if ($("#user_search_modal").length >0) {
        $("#user_search_modal").addClass('hide');
    }
}

//sleep
function sleep(numberMillis) {
    var now = new Date();
    var exitTime = now.getTime() + numberMillis;
    while (true) {
        now = new Date();
        if (now.getTime() > exitTime)
            return;
    }
}

//获取文件扩展名
function getFileExt(str){
    var d=/\.[^\.]+$/.exec(str);
    return d;
}

//获取文件的显示图标
function getFileIcon(ext){
    ext=ext.toString();
    var ext_img=[".jpg",".jpeg",".gif",".png",".bmp"];
    var ext_package=[".rar",".zip"];
    var ext_media = [".mp4", ".mp3",".3gp",".flv",".wav"];
    if($.inArray(ext,ext_img)>-1){
        return "/static/img/icon/img.png";
    }else if($.inArray(ext,ext_package)>-1){
        return "/static/img/icon/zip.png";
    }else if ($.inArray(ext, ext_media) > -1) {
        return "/static/img/icon/media.png";
    }else{
        return "/static/img/icon/text.png";
    }
}

//提示消息
function alert2(msg,type){
    var _type=["alert-info","alert-success","alert-error"];
    type=type==null||type==""?0:type;
    var rd=Math.random().toString();
    var alert_id="alert_"+rd.substring(2,rd.length-2);
    var html_alert="";
    html_alert += "<div id=\""+alert_id+"\" class=\"alert "+_type[type]+" fade hide in myalert\">";
    html_alert += "<button data-dismiss=\"alert\" class=\"close\" type=\"button\">×</button>";
    html_alert += "<strong>"+msg+"</strong>";
    html_alert += "</div>";
    $(html_alert).appendTo("body").fadeIn(500);
    setTimeout('$("#'+alert_id+'.alert").fadeOut(1000);',3000);
    setTimeout('$("#' + alert_id + '.alert").remove();', 4000);
}

//按回车，评论框的高度自动增加
function setCommentTextarea(_this){
    var _h=$(_this).height();
    //if(event.keyCode ==13){
        $(_this).height(_h+16);
    //}
}

//获取两个时间差
function getDateDiff(strDateStart,strDateEnd,isHour){
    isHour=isHour!=null&&isHour!="" ?isHour:false;
    var oDate1, oDate2;
    var iDays;
    var strDateS,strDateE;

    if(strDateStart=="" || strDateEnd=="")
        return "";

    if(isHour){
        var time_start = strDateStart.split(' ');
        var time_end = strDateEnd.split(' ');
        oDate1 = time_start[0].split("-");
        oDate2 = time_end[0].split("-");
        strDateS = new Date(oDate1[0], oDate1[1] - 1, oDate1[2],time_start[1].split(':')[0],time_start[1].split(':')[1]);
        strDateE = new Date(oDate2[0], oDate2[1] - 1, oDate2[2],time_end[1].split(':')[0],time_end[1].split(':')[1]);
        iDays = parseInt((strDateS - strDateE) / 1000 / 60 / 60);//把相差的毫秒数转换为小时数
    }else{
        oDate1 = strDateStart.split("-");
        oDate2 = strDateEnd.split("-");
        strDateS = new Date(oDate1[0], oDate1[1] - 1, oDate1[2]);
        strDateE = new Date(oDate2[0], oDate2[1] - 1, oDate2[2]);
        iDays = parseInt((strDateS - strDateE) / 1000 / 60 / 60 / 24);//把相差的毫秒数转换为天数
    }
    return iDays;
}

//Ajax请求参数
var param={
    url: "",
    type: "get",
    dataType: "json",
    contentType: "application/x-www-form-urlencoded; charset=utf-8",
    success: null
};

//获取数据
var pageData=function(option,callback){
    var op={
        pageindex:1,
        pagesize:10,
        ispage:true,
        pagecontainer:$(".pagination"),
        url:"",
        type:"get",
        callback:"",
        islogin:true,
        data:{}
    };
    $.extend(op,option);
    op.data['pageindex']=op.pageindex;
    op.data['pagesize'] = op.pagesize;
    param.url=op.url;
    param.data=op.data;
    param.type=op.type;
    param.success=function(msg){
        if(msg!=null&&msg!=""){
            if(msg==-1&&islogin){
                showLogin();
                return false;
            }
            //分页
            var html_page="";
            if (msg.counts > op.pagesize)
                html_page=getPage(op, msg.counts);
            if (op.pagecontainer!=null && op.ispage && op.pagecontainer.length > 0) {
               op.pagecontainer.html(html_page);
            }
            return callback(msg.data, msg.counts, html_page);
        }else{
            return callback(msg, 0,"");
        }
    };
    $.ajax(param);
};

//获取分页
function getPage(op,counts){
    var pagesize=op.pagesize;
    var pageindex=op.pageindex;
    var callback=op.callback;
    var pagecount=0;

    //计算总页数
    if(counts%pagesize==0){
        pagecount= Math.floor(counts/pagesize);
        pagecount=pagecount==0?1:pagecount;//至少一页
    }else{
        pagecount = Math.floor(counts / pagesize+1);
    }
    var html = '<div class="pagination">';
    html += '<ul>';
    //上一页
    if(pageindex>1){
        html += '<li><a href="javascript:;" onclick="'+callback+'('+(pageindex-1)+',\''+op.url+'\')">上一页</a></li>';
    }else{
        html += '<li class="disabled"><a href="javascript:;">上一页</a></li>';
    }
    //页码
    for(var i=1;i<=pagecount;i++){
        html += '<li '+(i==pageindex?"class=\"active\"":"")+'><a href="javascript:;"  onclick="' + callback + '(' + i + ',\''+op.url+'\')">'+i+'</a></li>';
    }
    //下一页
    if(pageindex < pagecount){
        html += '<li><a href="javascript:;" onclick="'+callback+'('+(pageindex+1)+',\''+op.url+'\')">下一页</a></li>';
    }else{
        html += '<li class="disabled"><a href="javascript:;">下一页</a></li>';
    }
    html += '</ul>';
    html += '</div>';
    return html;
}

//指定日期转换时间戳
function js_strto_time(str_time){
    var new_str = str_time.replace(/:/g,'-');
    new_str = new_str.replace(/ /g,'-');
    var arr = new_str.split("-");
    var datum = new Date(Date.UTC(arr[0],arr[1]-1,arr[2],arr[3]-8,arr[4],arr[5]));
    return strtotime = datum.getTime()/1000;
}

//删除临时上传的附件
function deleteUploadFile(fileid,type){
    if($("input[type=checkbox][name="+fileid+"]").length>0){
        var filepath = $("input[type=checkbox][name="+fileid+"]").val();
        if(filepath!=""){
            $.post("/api/attachement/remove/",{"filepath":filepath},function(msg){
                $("input[type=checkbox][name=" + fileid + "]").remove();
                if ($.cookie("fileuploading" + type) != null){
                    $.cookie("fileuploading" + type,null);
                }
            });
        }
    }
    $("#" + fileid + "").remove();
}

//删除全部临时上传的附件
function deleteAllUploadFile(){
    if(confirm("您确定要清除所有上传吗？"))
        $("#filelist,#div-upload-btn").html("");
}

//初始化上传附件
function InitUploadfiles(type,flag){
    if($.cookie("fileuploading"+type)!=null&&$.cookie("fileuploading"+type)!="null"&&$.cookie("fileuploading"+type)!=""){
        var username = "self";
        if ($.cookie("username") != null && $.cookie("username") != "")username = $.cookie("username");
        var files=$.cookie("fileuploading"+type);
        var html_files="";
        var html_res="";
        files=eval("("+files+")");
        if(files==null)return "";
        $.each(files,function(i,n){
            if(n.type==type&& n.username==username){
                html_files += '<div id="' + n.id + '">' + n.filename + ' <b></b>\t<a href="javascript:;" onclick="deleteUploadFile(\'' + n.id + '\','+type+');">删除</a></div>';
                html_res += '<input type="checkbox" name="' + n.id + '" value="' + n.filepath + '" alt="' + n.filename + '" title="' + n.filesize + '"/>';
            }
        });
        if(flag=="res")
            return html_res;
        else
            return html_files;
    }else{
        return "";
    }
}

//浏览器保存文件上传的附件
function SaveUploadFile(file,info,type){
    var username="self";
    if($.cookie("username")!=null&&$.cookie("username")!="")username=$.cookie("username");
    var fileinfo = '{"id": "' + file.id + '","filename": "' + file.name + '","filepath":"' + info.response + '","filesize":' + file.size + ',"type":'+type +',"username":"'+username+'" }';
    var files = '[';
    if ($.cookie("fileuploading"+type) != null && $.cookie("fileuploading"+type) != "") {
        files = $.cookie("fileuploading"+type);
        files = files.substring(0, files.length - 1);
        files += "," + fileinfo + "]";
    } else {
        files += fileinfo + "]";
    }
    $.cookie("fileuploading"+type, files,{expires: 7});
}

//标题闪烁
var titleFlash=true;
var count_flash=0;
function setTitleFlash(title,newtitle){
    count_flash+=1;
    if(titleFlash){
        document.title = newtitle;
        titleFlash=false;
    }else{
        document.title = title;
        titleFlash = true
    }
    timeout_flash=setTimeout('setTitleFlash("'+title+'","'+newtitle+'")',1000);
    if(count_flash==10){
        count_flash = 0;
        document.title = title;
        return false;
    }
}

//初始化弹框的日期
function initClockDate(_this,st_start){
    _this.daterangepicker({
            format: 'YYYY/MM/DD',
            singleDatePicker: true,
            //timePicker: true,
            timePicker12Hour: false,
            minDate:st_start,
            parentEl:$("#div_date_pick")
        }
    );
}

//打开登入对话框
function showLogin(){
    if ($("#login_modal").length < 1) {
        var username="";
        if ($.cookie("username") != null && $.cookie("username") != "")username = $.cookie("username");
        var html = "";
        html += "<div id=\"login_modal\" class=\"modal hide\" style=\"width:360px;z-index:1052;\">";
        html += '<div class="modal-header">';
        html += '<button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>';
        html += '<p style="margin: 0;">';
        html += "<h3>登入</h3>";
        html += '</p>';
        html += '</div>';
        html += "<div class=\"modal-body\" style=\"overflow-y: inherit;\">";
        html += "<form class=\"form-horizontal\">";
        html += "<div class=\"control-group\">";
        html += "<label for=\"inputEmail\" class=\"control-label\">用户名</label>";
        html += "<div class=\"controls\">";
        html += "<input type=\"text\" placeholder=\"用户名\" value=\""+username+"\" id=\"inputEmail\" name=\"username\">";
        html += "</div>";
        html += "</div>";
        html += "<div class=\"control-group\">";
        html += "<label for=\"inputPassword\" class=\"control-label\">密码</label>";
        html += "<div class=\"controls\">";
        html += "<input type=\"password\" value=\"\" placeholder=\"密码\" id=\"inputPassword\" name=\"password\">";
        html += "</div>";
        html += "</div>";
        html += "</form>";
        html += "<div class=\"alert hide\" style=\"margin:2px;\">fff</div>";
        html += "</div>";
        html += "<div class=\"modal-footer\">";
        html += "<a href=\"javascript:;\" name=\"a_btn_submit\" class=\"btn btn-info\" onclick=\"login();\">登入</a>";
        html += "<a href=\"javascript:;\" class=\"btn a_close\" onclick=\"close_login_dialog();\">取消</a>";
        html += "</div>";
        html += "</div>";
        //填充
        $("body").append(html);
    }
    $("#login_modal input[name=password]").val("");
    //显示弹框
    $("#login_modal").modal('show');
    //初始化弹框
    if ($("#login_modal input[name=username]").val() == "") {
        $("#login_modal input[name=username]").focus();
        return false;
    }
    if ($("#login_modal input[name=password]").val() == "") {
        $("#login_modal input[name=password]").focus();
        return false;
    }
    $("#login_modal div.alert").text("").addClass("hide").removeClass("alert-success");
    return false;
}

//登入
function login(){
    var username = $.trim($("#login_modal input[name=username]").val());
    var password = $.trim($("#login_modal input[name=password]").val());
    if(username==""){
        $("#login_modal input[name=username]").focus();
        return false;
    }
    if(password==""){
        $("#login_modal input[name=password]").focus();
        return false;
    }
    var csrftoken = $.cookie('csrftoken');
    //login
    $.post("/api/user/login/",{username:username,password:password,csrftoken:csrftoken},function(msg){
        if (msg != null && msg != "") {
            var data=eval("("+msg+")");
            if(data.status){
                $("#login_modal div.alert").text("登入成功。").removeClass("hide").addClass("alert-success");
                setTimeout('close_login_dialog();',720);
                $("#login_modal div.alert").text("").addClass("hide").removeClass("alert-success");
            }else{
                $("#login_modal div.alert").text("登入失败，请检查用户名或密码。").removeClass("hide");
            }
        }
    });
}
//取消登入
function close_login_dialog(){
    $("#login_modal").modal('hide');
}

//ajax请求数据
var Ajax=function(url,option,callback){
    var op={
        type:"post",
        data:{},
        islogin:true
    };
    $.extend(op,option);
    param.url=url;
    param.data=op.data;
    param.type=op.type;
    param.success=function(msg){
        if(msg!=null&&msg!=""){
            if(msg.code==-1&&op.islogin){
                showLogin();
                return false;
            }
            return callback(msg);
        }else{
            return callback(null);
        }
    };
    $.ajax(param);
};

/**
 * Created with PyCharm.
 * User: Administrator
 * Date: 14-10-14
 * Time: 下午6:03
 * To change this template use File | Settings | File Templates.
 */
//初始化用户输入框的值
var initTextUserName=$.trim($("input[name=txtUserName]").attr("placeholder"));

$(function(){

    //用户名查询条件的焦点
    $("input[name=txtUserName]").on("focus", function () {
        if ($.trim($(this).val()) == initTextUserName) {
            $(this).val("");
        }
    });
    $("input[name=txtUserName]").on("blur", function () {
        if ($.trim($(this).val()) == "") {
            $(this).val(initTextUserName);
        }
    });

});//end jq


//搜索条件
var data_search={};
//搜索
function seachData(){
    var classname= $.trim($("input[name=txtName]").val());
    data_search["classname"]=title;
    getDataList(1, urls.url_get);
}

//获取数据列表
function getDataList(url){
    $.get(url,data_search,function(msg){
        $("#datalist").html(fillDataList(msg.data));
    });
}

//解析数据列表
function fillDataList(msg){
    var html = "";
    if (msg != null && msg != "") {
        html = "<tr><th>班级名称</th><th>简介</th><th>班级容量</th><th>班级人数</th><th>班主任</th><th>班长</th><th>修改 | 学生 | 删除</th></tr>";

        $.each(msg, function (i, n) {
            //同事姓名
            var username = n.userid!=null?(n.userid.first_name != '' ? n.userid.first_name : n.userid.username):"--";
            html += "<tr>";
            html += "<td><a href=\""+(urls.url_student.replace('0',n.id))+"\" title=\"" + n.classname + "\">" + n.classname + "</a></td>";
            html += "<td>" + (n.description!=null?n.description.substr(0,20): "无") + "</td>";
            html += "<td>" + (n.container != null ? n.container : "--") + "</td>";
            html += "<td>" + n.student_counts + "</td>";
            html += "<td>" + n.headteacher + "</td>";
            html += "<td>" + n.monitor + "</td>";
            html += "<td>";
            html += "<a href=\""+(urls.url_edit + "?act=edit&id=" + n.id)+"\"><i class=\"icon-edit\"></i>修改</a> | ";
            html += "<a href=\""+(urls.url_student.replace('0',n.id))+"\">学生</a> | ";
            html += "<a href=\"javascript:;\" onclick=\"deleteData('" + n.classname + "'," + n.id + ");\"><i class=\"icon-trash\"></i>删除</a>";
            html += "</td>";
            html += "</tr>";
        });
    }else{
        html = "没有班级";
    }
    return html;
}

//删除
function deleteData(title,id){
    if(confirm("您要删除【"+title+"】吗？")){
        $.post(urls.url_delete.replace("0",id),{},function(msg){
            if (msg != null && msg !="") {
                if (msg.result) {
                    alert2("删除成功",1);
                    getDataList( urls.url_get);
                }
            }else{
                alert2("删除失败", 2);
            }
            return false;
        });
    }
}

//添加/修改
function Add(id){
    var classname= $.trim($("input[name=classname]").val());
    var container = $.trim($("input[name=container]").val());
    var headteacher = $.trim($("input[name=headteacher]").val());
    var headteacher_phone = $.trim($("input[name=headteacher_phone]").val());
    var monitor = $.trim($("input[name=monitor]").val());
    var description = $.trim($("textarea[name=description]").val());
    if(validateForm(classname)){
        var postdata={classname:classname,container:container,headteacher:headteacher,headteacher_phone:headteacher_phone,monitor:monitor,description:description};
        if(id!=null&&id!=""){
            postdata['id']=id;
        }
        $.post(urls.url_add, postdata, function (msg) {
            if (msg != null && msg !="") {
                if(msg.result){
                    if (id != null && id != "") {
                        alert2("修改成功", 1);
                    }else{
                        alert2("添加成功", 1);
                        $("form input,form textarea").val("");//清空表单
                    }
                    window.location.href="/manage/class/";
                }
            }else{
                alert2("操作失败", 2);
            }
            return false;
        });
    }
}

//表单验证
function validateForm(classname){
    if(classname==""){
        alert2("班级名称不能为空！",2);
        $("input[name=classname]").focus();
        return false;
    }
    return true;
}

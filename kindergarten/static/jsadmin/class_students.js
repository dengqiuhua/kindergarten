/**
 * Created with PyCharm.
 * User: Administrator
 * Date: 14-11-10
 * Time: 上午10:45
 * To change this template use File | Settings | File Templates.
 */

$(function(){

    //注册日期
    if($("input#inputRegisteredDate").length>0){
        $("input#inputRegisteredDate").daterangepicker({
            format: 'YYYY-MM-DD',
            singleDatePicker: true,
            showDropdowns: true,
            startDate: $("input#inputRegisteredDate").val() != "" ? $("input#inputRegisteredDate").val() : "2014/01/01"
        });
    }

});//end jq


//搜索条件
var data_search={};
var roles = ["","普通学生","班长","学习委员"];
//搜索
function seachData(){
    var name= $.trim($("input[name=txtName]").val());
    data_search["name"]=title;
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
        html = "<tr><th>姓名</th><th>性别</th><th>入园日期</th><th>角色</th><th>修改 | 删除</th></tr>";

        $.each(msg, function (i, n) {
            html += "<tr>";
            html += "<td><a href=\"#\" title=\"" + n.student.name + "\">" + n.student.name + "</a></td>";
            html += "<td>" + (n.student.sex != null&& n.student.sex!=0 ? n.student.sex == 1? "男" :"女" : "--") + "</td>";
            html += "<td>" + (n.joindate != null ? n.joindate : '') + "</td>";
            html += "<td>" + roles[n.role] + "</td>";
            html += "<td>";
            html += "<a href=\""+(urls.url_student_edit + "?act=edit&id=" + n.student.id)+"\"><i class=\"icon-edit\"></i>修改</a> | ";
            html += "<a href=\"javascript:;\" onclick=\"deleteData('" + n.student.name + "'," + n.id + "," + pageindex + ");\"><i class=\"icon-trash\"></i>从班级中删除</a>";
            html += "</td>";
            html += "</tr>";
        });
    }else{
        html = "没有学生";
    }
    return html;
}

//删除
function deleteData(title,id,pageindex){
    if(confirm("您要删除【"+title+"】吗？")){
        $.post(urls.url_student_delete.replace("0",id),{},function(msg){
            if (msg != null && msg !="") {
                if (msg.result) {
                    alert2("删除成功",1);
                    getDataList(pageindex, urls.urls.url_student_get.replace("0",classid));
                }
            }else{
                alert2("删除失败", 2);
            }
            return false;
        });
    }
}


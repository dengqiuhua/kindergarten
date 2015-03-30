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
    var title= $.trim($("input[name=txtTitle]").val());
    data_search["title"]=title;
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
        html = "<tr><th>学生</th><th>拜访者</th><th>拜访者身份</th><th>拜访者电话</th><th>预约时间</th><th>预约地点</th><th>是否已结束</th><th>备注</th><th>创建时间</th><th>已读 | 删除</th></tr>";
        $.each(msg, function (i, n) {

            html += "<tr>";
            html += "<td><a href=\"#\" title=\"" + n.student + "\">" + n.student + "</a></td>";
            html += "<td>" + n.name + "</td>";
            html += "<td>" + n.role + "</td>";
            html += "<td>" + n.phone + "</td>";
            html += "<td>" + n.reserve_date + "</td>";
            html += "<td>" + n.address + "</td>";
            html += "<td>" + (n.ismeet ? "是" : "否") + "</td>";
            html += "<td>" + (n.remark != null ? n.remark.substr(0, 20) : "无") + "</td>";
            html += "<td>" + n.createtime + "</td>";
            html += "<td>";
            //html += "<a href=\""+(urls.url_edit + "?act=edit&id=" + n.id)+"\"><i class=\"icon-edit\"></i>修改</a> | ";
            if(n.isread){
                html += "<span class=\"muted\">已读</span> | ";
            }else{
                html += "<a href=\"javascript:;\" onclick=\"setRead(" + n.id + "," + pageindex + ");\"><i class=\"icon-check\"></i>设置已读</a> | ";
            }
            html += "<a href=\"javascript:;\" onclick=\"deleteData('" + n.name + "'," + n.id + "," + pageindex + ");\"><i class=\"icon-trash\"></i>删除</a>";
            html += "</td>";
            html += "</tr>";
        });
    }else{
        html = "没有预约";
    }
    return html;
}

//删除
function deleteData(title,id,pageindex){
    if(confirm("您要删除【"+title+"】的预约吗？")){
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

//置顶/取消置顶
function setRead(id,pageindex){
    $.post(urls.url_read.replace("0",id), {}, function (msg) {
        if (msg != null && msg != "") {
            if (msg.result) {
                alert2("操作成功", 1);
                getDataList(pageindex, urls.url_get);
            }
        } else {
            alert2("操作失败", 2);
        }
        return false;
    });

}


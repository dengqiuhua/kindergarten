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
        html = "<tr><th>类型</th><th>标题</th><th>摘要</th><th>作者</th><th>是否置顶</th><th>添加人</th><th>创建时间</th><th>修改 | 置顶 | 删除</th></tr>";

        $.each(msg, function (i, n) {
            //同事姓名
            var username = n.userid!=null?(n.userid.first_name != '' ? n.userid.first_name : n.userid.username):"--";
            var title=n.title.replace(/'/g,"“").replace(/"/g,"“");
            html += "<tr>";
            html += "<td>" + (n.news_type != null ? n.news_type==1? '公告' : '新闻' : "--") + "</td>";
            html += "<td><a href=\"#\" title=\"" + title + "\">" + title + "</a></td>";
            html += "<td>" + (n.content!=null?n.content.substr(0,20): "无") + "</td>";
            html += "<td>" + (n.author != null ? n.author : "--") + "</td>";
            html += "<td>" + (n.is_top ? "<i class='icon icon-top'></i>" : "否") + "</td>";
            html += "<td>" + username + "</td>";
            html += "<td>" + n.createtime + "</td>";
            html += "<td>";
            html += "<a href=\""+(urls.url_edit + "?act=edit&id=" + n.id)+"\"><i class=\"icon-edit\"></i>修改</a> | ";
            if(n.is_top){
                html += "<a href=\"javascript:;\" onclick=\"setTop(false,'" + title + "'," + n.id + "," + pageindex + ");\"><i class=\"icon-minus-sign\"></i>取消置顶</a> | ";
            }else{
                html += "<a href=\"javascript:;\" onclick=\"setTop(true,'" + title + "'," + n.id + "," + pageindex + ");\"><i class=\"icon-circle-arrow-up\"></i>置顶</a> | ";
            }
            html += "<a href=\"javascript:;\" onclick=\"deleteData('" + title + "'," + n.id + "," + pageindex + ");\"><i class=\"icon-trash\"></i>删除</a>";
            html += "</td>";
            html += "</tr>";
        });
    }else{
        html = "没有新闻";
    }
    return html;
}

//删除
function deleteData(title,id,pageindex){
    if(confirm("您要删除【"+title+"】吗？")){
        Ajax(urls.url_delete.replace("0",id),{},function(msg){
            if (msg.result) {
                alert2("删除成功",1);
                getDataList(pageindex, urls.url_get);
            }else{
                alert2("删除失败", 2);
            }
            return false;
        });
    }
}

//置顶/取消置顶
function setTop(istop,title,id,pageindex){

    if (confirm("您要"+(istop?"":"取消")+"【" + title + "】置顶吗？")) {
        $.post(urls.url_settop, {id: id,istop:istop}, function (msg) {
            if (msg != null && msg != "") {
                if (msg > 0) {
                    alert2("操作成功", 1);
                    getDataList(pageindex, urls.url_get);
                }
            } else {
                alert2("操作失败", 2);
            }
            return false;
        });
    }
}

//添加/修改
function Add(id){
    var news_type = $("select[name=news_type]").val()
    var title= $.trim($("input[name=title]").val());
    var author = $.trim($("input[name=author]").val());
    var content = $.trim($("textarea[name=content]").val());
    if(validateForm(title)){
        var postdata={news_type:news_type,title:title,author:author,content:content};
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
                    window.location.href = urls.url_home;
                }
            }else{
                alert2("操作失败", 2);
            }
            return false;
        });
    }
}

//表单验证
function validateForm(title){
    if(title==""){
        alert2("标题不能为空！",2);
        $("input[name=title]").focus();
        return false;
    }
    return true;
}

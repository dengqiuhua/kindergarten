/**
 * Created by dengqiuhua on 15-5-2.
 */

$(function(){
    //获取评论列表
    getCommentList(1,url_comment);
});

//添加评论
function addComment(){
    var content = $.trim($("#form-comment").val());
    if(content == ""){
        alert2("评论内容不能为空！");
        $("#form-comment").focus();
        return false;
    }

    Ajax(url_comment,{data:{content:content}},function(msg){
        if(msg.result){
            alert2("评论成功",1);
            $("#form-comment").val("");
            getCommentList(1,url_comment);
        }
    })
}

//获取评论列表
function getCommentList(pageindex,url){
    var data2 = new pageData({url: url, callback: "getCommentList", pageindex: pageindex}, function (msg) {
        $("#datalist").html(fillCommentList(msg,pageindex));
    });
}

//解析评论
function fillCommentList(msg,pageindex){
    var html = "";
    if (msg != null && msg != "") {
        html += "<table class=\"table\">";
        $.each(msg, function (i, n) {
            html += "<tr><td>";
            html += "<div class=\"media\">";
            html += "<span class=\"pull-left\"><i class=\"icon-comment\"></i></span>";
            html += "<div class=\"media-body\">";
            html += "<div>";
            //html +=  n.userid.name;
            if (n.parentid != null && n.parentid != "") {
                //html += "回复<a href=\"/home/u/"+( n.parentid.user.id)+"\">" + n.parentid.user.name+"</a>";
            }
            html += "："+ n.content + "\t<span class=\"muted\">(" + getGamTime(n.createtime) + ")</span>";
            if(n.isedit){
                html += "<a onclick=\"deleteComment(" + n.id + ",this);\" href=\"javascript:;\" title=\"删除\"><i class=\"icon-trash\"></i></a>";
            }else{
                //html += "<a onclick=\"initWorkComment(" + objectid + ",'" +  n.user.name + "'," + n.id + ");\" href=\"javascript:;\" title=\"回复\"><i class=\"icon-comment\"></i></a>";
            }
            html += "</div></div>";
            html += "</div>";
            html += "</td></tr>";
        });
        html += "</table>";
    }else{
        html = "<span><i class=\"icon-filter\"></i> 没有评论，去抢沙发！</span>";
    }
    return html;
}
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

    //班级的选择
    $("input[name=activity_type]").on('click',function(){
        initClass();
    });
    initClass();

    //活动日期
    if ($("input[name=activity_date]").length > 0) {
        var myDate = new Date();
        date_today = myDate.toLocaleDateString();
        if($("input[name=activity_date_start]").val()=="" )
            $("input[name=activity_date_start]").val(date_today);
        if ($("input[name=activity_date_end]").val() == "")
            $("input[name=activity_date_end]").val(date_today);
        $("input[name=activity_date]").daterangepicker({
                format: 'YYYY-MM-DD',
                //singleDatePicker: true,
                timePicker12Hour: false,
                maxDate: date_today
            }, function (start, end, label) {
                $("input[name=activity_date_start]").val(start.format('YYYY-MM-DD'));
                $("input[name=activity_date_end]").val(end.format('YYYY-MM-DD'));
                //alert('A date range was chosen: ' + start.format('YYYY-MM-DD HH:mm') + ' to ' + end.format('YYYY-MM-DD HH:mm'));
            }
        );
    }

});//end jq


//搜索条件
var data_search={};
var activity_types=["","全体活动","班级活动","其他活动"];
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
        html = "<tr><th>活动标题</th><th>描述</th><th>活动类型</th><th>负责人</th><th>参与人数</th><th>活动地点</th><th>活动时间</th><th>修改 | 照片 | 删除</th></tr>";

        $.each(msg, function (i, n) {
            var title=n.title.replace(/'/g,"“").replace(/"/g,"“");
            html += "<tr>";
            html += "<td><a href=\""+(urls.url_photo+'?id='+ n.id)+"\" title=\"" + title + "\">" + title + "</a></td>";
            html += "<td>" + (n.description!=null?n.description.substr(0,20): "无") + "</td>";
            html += "<td>" + (n.activity_type != null ? activity_types[n.activity_type] : "--") + "</td>";
            html += "<td>" + (n.master != null ? n.master : "--") + "</td>";
            html += "<td>" + n.usercounts + "</td>";
            html += "<td>" + n.address + "</td>";
            html += "<td>" + (n.activity_date_start!=null?n.activity_date_start==n.activity_date_end?n.activity_date_start:n.activity_date_start+'--'+n.activity_date_end:'') + "</td>";
            html += "<td>";
            html += "<a href=\""+(urls.url_edit + "?act=edit&id=" + n.id)+"\"><i class=\"icon-edit\"></i>修改</a> | ";
            html += "<a href=\"javascript:;\" onclick=\"deleteData('" + title + "'," + n.id + "," + pageindex + ");\"><i class=\"icon-trash\"></i>删除</a>";
            html += "</td>";
            html += "</tr>";
        });
    }else{
        html = "没有活动";
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

//添加/修改
function Add(id){
    var title= $.trim($("input[name=title]").val());
    var activity_type = $.trim($("input[name=activity_type]:checked").val());
    var master = $.trim($("input[name=master]").val());
    var usercounts = $.trim($("input[name=usercounts]").val());
    var address = $.trim($("input[name=address]").val());
    var activity_date_start = $.trim($("input[name=activity_date_start]").val());
    var activity_date_end = $.trim($("input[name=activity_date_end]").val());
    var description = $.trim($("textarea[name=description]").val());
    var classid=$("select[name=class] option:selected").val();
    if(validateForm(title)){
        var postdata={title:title,activity_type:activity_type,master:master,usercounts:usercounts,address:address,description:description,classid:classid};
        if(id!=null&&id!=""){
            postdata['id']=id;
        }

        if ($.trim($("input[name=activity_date]").val()) != "") {

            postdata['activity_date_start']=activity_date_start.replace(/\//g,"-");
            postdata['activity_date_end'] = activity_date_end.replace(/\//g,"-");
        }
        $.post(urls.url_add, postdata, function (msg) {
            if (msg != null && msg !="") {
                if(msg.result){
                    if (id != null && id != "") {
                        alert2("修改成功", 1);
                    }else{
                        alert2("添加成功", 1);
                        $("form input,form textarea").val("");//清空表单
                        //跳转
                        setTimeout(function(){
                            window.location.href = urls.url_photo + "?id=" + msg.data;
                        },1600);

                    }
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

//初始化类型
function initClass(){
    if($("input[name=activity_type]:checked").val()==2){
        $("#div_class").removeClass("hide");
    }else{
        $("#div_class").addClass("hide");
    }
}
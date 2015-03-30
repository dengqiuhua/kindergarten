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
            }
        );
    }

});//end jq


//搜索条件
var data_search={};
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
        html = "<tr><th>姓名</th><th>学号</th><th>性别</th><th>生日/年龄</th><th>居住地址</th><th>监护人</th><th>监护人电话</th><th>班级</th><th>爱好</th><th>修改 | 删除</th></tr>";

        $.each(msg, function (i, n) {
            html += "<tr>";
            html += "<td><a href=\"#\" title=\"" + n.student.name + "\">" + n.student.name + "</a></td>";
            html += "<td>" + n.student.number + "</td>";
            html += "<td>" + (n.student.sex != null&& n.student.sex!=0 ? n.student.sex == 1? "男" :"女" : "--") + "</td>";
            html += "<td>" + n.student.birthday + "</td>";
            html += "<td>" + n.student.address + "</td>";
            html += "<td>" + n.student.guardian + "</td>";
            html += "<td>" + n.student.guardian_phone + "</td>";
            html += "<td>" + 0 + "</td>";
            html += "<td>" + n.student.hobby + "</td>";
            html += "<td>";
            html += "<a href=\""+(urls.url_edit + "?act=edit&id=" + n.student.id)+"\"><i class=\"icon-edit\"></i>修改</a> | ";
            html += "<a href=\"javascript:;\" onclick=\"deleteData('" + n.student.name + "'," + n.student.id + "," + pageindex + ");\"><i class=\"icon-trash\"></i>删除</a>";
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
        $.post(urls.url_delete,{id:id},function(msg){
            if (msg != null && msg !="") {
                if (msg > 0) {
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
    var name= $.trim($("input[name=name]").val());
    var number = $.trim($("input[name=number]").val());
    var sex = $.trim($("input[name=sex]:checked").val());
    var birth_year = $.trim($("select[name=year]").val());
    var birth_month = $.trim($("select[name=month]").val());
    var birth_day = $.trim($("select[name=day]").val());
    var birth="";
    if(birth_year!="" && birth_month!=""&&birth_day!=""){
        birth= birth_year + "-" +  birth_month + "-" + birth_day;
    }
    var phone = $.trim($("input[name=phone]").val());
    var city = $.trim($("input[name=city]").val());
    var address = $.trim($("input[name=address]").val());
    var guardian = $.trim($("input[name=guardian]").val());
    var guardian_phone = $.trim($("input[name=guardian_phone]").val());
    var emergency_contact = $.trim($("input[name=emergency_contact]").val());
    var emergency_phone = $.trim($("input[name=emergency_phone]").val());
    var hobby = $.trim($("input[name=hobby]").val());
    var remark = $.trim($("input[name=remark]").val());

    if(validateForm(name)){
        var postdata={name:name,number:number,sex:sex,phone:phone,city:city,address:address,guardian:guardian,guardian_phone:guardian_phone,emergency_contact:emergency_contact,emergency_phone:emergency_phone,hobby:hobby,remark:remark};
        if (birth != "") {
            postdata['birthday'] = birth;
        }
        if(id!=null&&id!=""){
            postdata['id']=id;
        }
        $.post(urls.url_add, postdata, function (msg) {
            if (msg != null && msg !="") {
                if(msg>0){
                    if (id != null && id != "") {
                        alert2("修改成功", 1);
                    }else{
                        alert2("添加成功", 1);
                        $("form input,form textarea").val("");//清空表单
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
function validateForm(name){
    if(name==""){
        alert2("姓名不能为空！",2);
        $("input[name=name]").focus();
        return false;
    }
    return true;
}


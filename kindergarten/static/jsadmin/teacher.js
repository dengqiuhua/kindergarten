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
    //初始化年月日
    initBirth();
    //下拉选择年月
    $("#select_birthday select[name=year],#select_birthday select[name=month]").on('change',function(){
        var year=$("#select_birthday select[name=year]").val();
        var month = $("#select_birthday select[name=month]").val();
        if(year!=""&&month!=""){
            getMonthDays(year,month,"");
        }
    });

    //入园日期
    if($("input[name=joindate]").length>0){
        $("input[name=joindate]").daterangepicker({
                format: 'YYYY-MM-DD',
                startDate: new Date().toLocaleDateString(),
                singleDatePicker: true
            }
        );
    }

});//end jq


//搜索条件
var data_search={};
var degrees=["","小学","初中","高级中学","中专","高职","大专","本科","硕士研究生","博士研究生","海外留学生","其他"];

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
        html = "<tr><th>姓名</th><th>性别</th><th>生日/年龄</th><th>居住地址</th><th>学历</th><th>教学范围</th><th>班级</th><th>修改 | 删除</th></tr>";
        $.each(msg, function (i, n) {
            html += "<tr>";
            html += "<td><a href=\"#\" title=\"" + n.name + "\">" + n.name + "</a></td>";
            html += "<td>" + (n.sex != null&& n.sex!=0 ? n.sex == 1? "男" :"女" : "--") + "</td>";
            html += "<td>" + (n.birthday!=null?n.birthday:"") + "</td>";
            html += "<td>" + (n.address!=null?n.address:"") + "</td>";
            html += "<td>" + (n.degree!=null?degrees[n.degree]:"") + "</td>";
            html += "<td>" + (n.teaching!=null?n.teaching:"") + "</td>";
            html += "<td>" + getClassHtml2(n.classinfo) + "<a href=\"javascript:;\" onclick=\"showAddClass(" + n.id + ",'" + n.name + "')\"><i class=\"icon-pencil\"></i>设置</a></td>";
            html += "<td>";
            html += "<a href=\""+(urls.url_edit + "?act=edit&id=" + n.id)+"\"><i class=\"icon-edit\"></i>修改</a> | ";
            html += "<a href=\"javascript:;\" onclick=\"deleteData('" + n.name + "'," + n.id + "," + pageindex + ");\"><i class=\"icon-trash\"></i>删除</a>";
            html += "</td>";
            html += "</tr>";
        });
    }else{
        html = "没有教师";
    }
    return html;
}

//教师的班级
function getClassHtml2(classinfo){
    var html="";
    if(classinfo!=null&&classinfo!=""){
        $.each(classinfo, function (i, n) {
            html+="<span>"+ n.classname+"<span>";
        });
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
    var name= $.trim($("input[name=name]").val());
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
    var degree = $.trim($("select[name=degree] option:selected").val());
    var educate_school = $.trim($("input[name=educate_school]").val());
    var joindate = $.trim($("input[name=joindate]").val());
    var teaching = $.trim($("input[name=teaching]").val());
    var photo = $.trim($("input[name=photo]").val());

    if(validateForm(name)){
        var postdata={name:name,sex:sex,phone:phone,city:city,address:address,degree:degree,educate_school:educate_school,joindate:joindate,teaching:teaching,photo:photo};
        if (birth != "") {
            postdata['birthday'] = birth;
        }
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


//初始化出生年月日
function initBirth(){
    var birthday=$("#hd_birthday").length > 0 ? $("#hd_birthday").val():"";
    var birth_arr=null;
    if(birthday!=""){
        birthday=birthday.replace(/\//g,"-");
        birth_arr = birthday.split('-');
    }
    var mydate= new Date();
    var year_now=mydate.getFullYear();//当前年
    var option_year="<option></option>";
    var option_month = "<option></option>";
    for(i=year_now;i>=1900;i--){
        option_year+="<option value='"+i+"' "+(birth_arr&&birth_arr[0]==i?'selected=\"selected\"':'')+">"+i+"</option>";
    }
    for (i = 1; i <= 12; i++) {
        option_month += "<option value='" + i + "' "+(birth_arr&&birth_arr[1]==i?'selected=\"selected\"':'')+">" + i + "</option>";
    }
    //年
    $("#select_birthday select[name=year]").html(option_year);
    //月
    $("#select_birthday select[name=month]").html(option_month);
    //日初始化
    if(birth_arr)getMonthDays(birth_arr[0],birth_arr[1],Number(birth_arr[2]));
}

//根据年月获取本月的天数
function getMonthDays(year,month,day){
    var d = new Date(year, month, 0);
    var daysCount = d.getDate();
    var option_day = "<option></option>";
    for(i=1;i<=daysCount;i++){
        option_day += "<option value='" + i + "' "+(day!=""&&day==i?'selected=\"selected\"':'')+">" + i + "</option>";
    }
    //日
    $("#select_birthday select[name=day]").html(option_day);
}


/*----------------------------------------------分派到班级------------------------------------------*/
//打开添加班级对话框
function showAddClass(teacherid,name){
    if ($("#class_modal").length > 0)$("#class_modal").remove();
    var catname="";
    //if ($.cookie("username") != null && $.cookie("username") != "")username = $.cookie("username");
    var html = "";
    html += "<div id=\"class_modal\" class=\"modal hide\" style=\"width:420px;\">";
    html += '<div class="modal-header">';
    html += '<button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>';
    html += '<p style="margin: 0;">';
    html += "<h3>"+name+"</h3>";
    html += '</p>';
    html += '</div>';
    html += "<div class=\"modal-body\" style=\"overflow-y: inherit;\">";
    html += "<form class=\"form-horizontal\">";
    html += "<div class=\"control-group\">";
    html += "<label for=\"inputEmail\" class=\"control-label\">班级名称</label>";
    html += "<div class=\"controls\">";
    html += "<select name=\"class\"><option value=\"\"></option></select>";
    html += "</div>";
    html += "</div>";
    html += "<div class=\"control-group\">";
    html += "<label for=\"inputEmail2\" class=\"control-label\">角色</label>";
    html += "<div class=\"controls\">";
    html += "<label class=\"checkbox inline\"><input type=\"radio\" name=\"role\" value=\"1\" checked=\"checked\" />教师</label>" ;
    html += "<label class=\"checkbox inline\"><input type=\"radio\" name=\"role\" value=\"2\"/>辅导员</label>";
    html += "<label class=\"checkbox inline\"><input type=\"radio\" name=\"role\" value=\"3\"/>生活助理</label>";
    html += "</div>";
    html += "</div>";
    html += "</form>";
    html += "<div class=\"alert hide\" style=\"margin:2px;\">fff</div>";
    html += "</div>";
    html += "<div class=\"modal-footer\">";
    html += "<a href=\"javascript:;\" name=\"a_btn_submit\" class=\"btn btn-info\" onclick=\"AddClass("+teacherid+");\">添加</a>";
    html += "<a href=\"javascript:;\" class=\"btn a_close\" onclick=\"close_class_modal_dialog();\">取消</a>";
    html += "</div>";
    html += "</div>";
    //填充
    $("body").append(html);
    //班级列表
    GetUnJoinClass(teacherid);
    //显示弹框
    $("#class_modal").modal('show');

    $("#class_modal div.alert").text("").addClass("hide").removeClass("alert-success");
    return false;
}

//获取班级列表，下拉框用
function GetUnJoinClass(teacherid){
    if(teacherid!=null&&teacherid!=""){
        $.get(urls.url_class_notjoin.replace("0",teacherid),{teacherid:teacherid},function(msg){
            getClassHtml(msg.data);
        });
    }
}

function getClassHtml(msg){
    if (msg != null && msg != "") {
        var html = "";
        $.each(msg, function (i, n) {
             html += "<option value=\"" + n.id + "\">" + n.classname + "</option>";
        });
        $("#class_modal select[name=class]").html(html);
    }
}

//添加班级
function AddClass(teacherid,id){
    var classid = $.trim($("#class_modal select[name=class] option:selected").val());
    var role = $.trim($("#class_modal input[name=role]:checked").val());
    if(classid==""){
        $("#class_modal input[name=class]").focus();
        return false;
    }
    var data={teacherid:teacherid,role:role};
    //修改
    if(id!=null&&id!=""){
        data['id']=id;
    }
    Ajax(urls.url_class_add.replace("0",classid),{data:data},function(msg){
        if (msg.result) {
            $("#class_modal div.alert").text("操作成功。").removeClass("hide").addClass("alert-success");
            setTimeout('close_class_modal_dialog();',1620);
            //重新加载教师列表
            getDataList(1, urls.url_get);
        } else {
            $("#class_modal div.alert").text("操作失败。").removeClass("hide");
        }
    });
}

//取消添加分类
function close_class_modal_dialog(){
    $("#class_modal").modal('hide');
}

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
        html = "<tr><th>标题</th><th>摘要</th><th>作者</th><<th>来源</th><th>视频</th><th>创建时间</th><th>修改 | 删除</th></tr>";

        $.each(msg, function (i, n) {
            var title=n.title.replace(/'/g,"“").replace(/"/g,"“");
            html += "<tr>";
            html += "<td><a href=\"#\" title=\"" + title + "\">" + title + "</a></td>";
            html += "<td>" + (n.description!=null?n.description.substr(0,20): "无") + "</td>";
            html += "<td>" + (n.author != null ? n.author : "--") + "</td>";
            html += "<td>" + (n.source != null? n.source:'') + "</td>";
            html += "<td>" + (n.video != null? n.video:'') + "</td>";
            html += "<td>" + n.createtime + "</td>";
            html += "<td>";
            html += "<a href=\""+(urls.url_edit + "?act=edit&id=" + n.id)+"\"><i class=\"icon-edit\"></i>修改</a> | ";
            html += "<a href=\"javascript:;\" onclick=\"deleteData('" + title + "'," + n.id + "," + pageindex + ");\"><i class=\"icon-trash\"></i>删除</a>";
            html += "</td>";
            html += "</tr>";
        });
    }else{
        html = "没有文章";
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
    var author = $.trim($("input[name=author]").val());
    var source = $.trim($("input[name=source]").val());
    var video = $.trim($("input[name=video]").val());
    //视频
    var fileid="";
    if($("input[name=fileid]").length>0&&$("input[name=fileid]").val()!=""){
        fileid = $.trim($("input[name=fileid]").val());
    }

    var description = $.trim($("textarea[name=description]").val());
    if(validateForm(title)){
        var postdata={title:title,author:author,source:source,video:video,fileid:fileid,description:description};
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


function initCourseFile(){

    //相册弹框
    var param_uploader= {
        headers: {'X-Requested-With': 'XMLHttpRequest', 'X-CSRFToken': $.cookie('csrftoken'),'Accept':'application/json,text/javascript'},
        runtimes: 'html5,flash,silverlight,html4',
        browse_button: 'pickfiles', // you can pass in id...
        container: document.getElementById('upload_container'), // ... or DOM Element itself
        url:urls.url_course_file,
        flash_swf_url : '/static/js/plupload/Moxie.swf',
        filters: {
            max_file_size: '100mb',
            mime_types: [
                {title: "视频", extensions: "mp4,wav,flv"}
            ]
        },
        init: {
            PostInit: function () {

            },
            FilesAdded: function (up, files) {
                var html_init_img ="" ;
                plupload.each(files, function (file) {
                    //var html_init_img='<div id="' + file.id + '" >' + file.name + ' (' + plupload.formatSize(file.size) + ') <b></b>\t<a href="javascript:;" onclick="deleteUploadFile(\'' + file.id + '\',1);">删除</a></div>';
                    html_init_img = "<div class=\"image-uploading\" id=\"" + file.id + "\">" ;
                    html_init_img += "<div class=\"image-title\">"+file.name+"</div>";
                    html_init_img += "<div class=\"image-status\">";
                    html_init_img += "<span class=\"image-persent\">0%</span><span>"+plupload.formatSize(file.size)+"</span><a href=\"javascript:;\" onclick=\"deleteUploadFile('" + file.id + "',1);\"><i class=\"icon-trash\"></i> 删除</a>";
                    html_init_img += "</div></div>";
                    document.getElementById('fileList').innerHTML +=html_init_img;
                });

                //自动上传
                uploader.start();
                return false;
            },
            UploadProgress: function (up, file) {
                document.getElementById(file.id).getElementsByTagName('span')[0].innerHTML =  file.percent + "%";
            },
            FileUploaded: function (up, file, info) {
                //返回值
                if (info.response != null&&info.response!="") {
                    var msg = eval("(" + info.response + ")");
                    if (msg.result) {
                        var fileid = msg.data;
                        document.getElementById("fileid").innerHTML = "<input name=\"fileid\" type=\"hidden\" value=\"" + fileid + "\" />"
                    }
                }
            },
            Error: function (up, err) {
                document.getElementById('console').innerHTML += "\nError #" + err.code + ": " + err.message;
            }
        }
    };


    //文件上传[相册]
    if(document.getElementById('pickfiles')!=null){
        var uploader = new plupload.Uploader(param_uploader);
        uploader.init();
    }

}

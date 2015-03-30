/**
 * Created with PyCharm.
 * User: Administrator
 * Date: 14-11-6
 * Time: 下午3:52
 * To change this template use File | Settings | File Templates.
 */

var activityid=$("input[name=activityid]").val();

//添加活动照片
function AddActivityPhoto(filename,filepath,fileid){
    var data={filename:filename,filepath:filepath};
    $.post(urls.url_activity_photo_add.replace("0",activityid),data,function(msg){
        if(msg!=null&&msg!=""){
            if(msg.result){
                $("#"+fileid).remove();
                getDataList(1, urls.url_activity_photo.replace("0",activityid));
            }
        }else{
            alert2("本张上传错误！");
        }
    });
}


//搜索条件
var data_search={};
//搜索
function seachData(){
    var title= $.trim($("input[name=txtTitle]").val());
    data_search["title"]=title;
    getDataList(1, urls.url_activity_photo.replace("0",activityid));
}

//获取数据分页列表
function getDataList(pageindex,url){
    var data2 = new pageData({url: url, callback: "getDataList",data:data_search, pageindex: pageindex}, function (msg) {
        $("#imagelist").html(fillDataList(msg,pageindex));
    });
}

//解析数据列表
function fillDataList(msg,pageindex){
    var html = "";
    if (msg != null && msg != "") {
        $.each(msg, function (i, n) {
            var title=n.title.replace(/'/g,"“").replace(/"/g,"“");
            //var path_img=urls.url_path_photo+"?filename="+n.title+"&filepath="+n.filepath;
            html+="<div class=\"span2\">";
            html += "<div class=\"thumbnail\">";
            html += "<img src=\""+ n.filepath+"\" alt=\""+n.title+"\"/>";
            html += "</div>";
            html += "<div class=\"caption\"> ";
            html += "<p>";
            html += "<a href=\"javascript:;\" onclick=\"deletePhoto("+n.id+");\" title=\"删除\"><i class=\"icon-trash\"></i>删除</a> | ";
            if(n.is_face){
                html += "<span><i class=\"icon-heart\"></i>当前封面</span>";
            }else{
                html += "<a href=\"javascript:;\" onclick=\"setFace("+n.id+");\" title=\"设为封面\"><i class=\"icon-ok-sign\"></i>设为封面</a>";
            }

            html += "</p>";
            html += "</div>";

            html += "</div>";
        });
    }else{
        html = "没有活动照片";
    }
    return html;
}

//相册弹框
var param_uploader= {
    headers: {'X-Requested-With': 'XMLHttpRequest', 'X-CSRFToken': $.cookie('csrftoken'),'Accept':'application/json,text/javascript'},
    runtimes: 'html5,flash,silverlight,html4',
    browse_button: 'pickfiles', // you can pass in id...
    container: document.getElementById('upload_container'), // ... or DOM Element itself
    url:urls.url_upload_photo.replace("0",activityid),
    flash_swf_url : '/static/js/plupload/Moxie.swf',
    filters: {
        max_file_size: '10mb',
        mime_types: [
            {title: "图像", extensions: "jpg,gif,png"}
        ]
    },
    init: {
        PostInit: function () {
            document.getElementById('filelist').innerHTML = InitUploadfiles(1,"show");
            document.getElementById('file_result').innerHTML = InitUploadfiles(1,"res");
            //点击上传
            /*document.getElementById('uploadfiles').onclick = function() {
             uploader.start();
             return false;
             }; */
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
                document.getElementById('filelist').innerHTML +=html_init_img;
            });
            var btn_upload="<button type=\"button\" class=\"btn btn-inverse\" onclick=\"startUpload();\">上传</button>\t\t";
            btn_upload += "<button type=\"button\" class=\"btn\" onclick=\"deleteAllUploadFile();\">全部取消</button>";
            document.getElementById('div-upload-btn').innerHTML = btn_upload;
            //自动上传
            //uploader.start();
            return false;
        },
        UploadProgress: function (up, file) {
            document.getElementById(file.id).getElementsByTagName('span')[0].innerHTML =  file.percent + "%";
        },
        FileUploaded: function (up, file, info) {
            //返回值
            if (info.response != null&&info.response!="") {
                var msg = eval("(" + info.response + ")");
                if(msg.result){
                    document.getElementById(file.id).innerHTML = "";
                    $("#"+file.id).remove();
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

function startUpload(){
    uploader.start();
}
//删除照片
function deletePhoto(id){
    if(confirm('您确定要删除此照片吗？')){
        $.post(urls.url_activity_photo_delete.replace("0",id),{},function(msg){
            if (msg != null && msg != "") {
                if (msg.result) {
                    alert2("删除成功", 1);
                    getDataList(1, urls.url_activity_photo.replace("0",activityid));
                }
            } else {
                alert2("删除失败", 2);
            }
            return false;
         })
    }
}

//设置为封面
function setFace(id){
    if(confirm('您确定要把此照片设置为活动封面吗？')){
        $.post(urls.url_activity_photo_face.replace("0",id),{},function(msg){
            if (msg != null && msg != "") {
                if (msg.result) {
                    alert2("设置成功", 1);
                    getDataList(1, urls.url_activity_photo.replace("0",activityid));
                }
            } else {
                alert2("设置失败", 2);
            }
            return false;
         })
    }
}
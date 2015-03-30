/**
 * Created with PyCharm.
 * User: Administrator
 * Date: 14-7-22
 * Time: 下午3:28
 * To change this template use File | Settings | File Templates.
 */

//任务附件弹框
var param_uploader= {
    headers: {'X-Requested-With': 'XMLHttpRequest', 'X-CSRFToken': $.cookie('csrftoken')},
    runtimes: 'html5,flash,silverlight,html4',
    browse_button: 'pickfiles', // you can pass in id...
    container: document.getElementById('upload_container'), // ... or DOM Element itself
    url: '/home/files/fileupload/',
    flash_swf_url : '/static/js/plupload/Moxie.swf',
    //silverlight_xap_url : '../js/Moxie.xap',
    filters: {
        max_file_size: '10mb',
        mime_types: [
            {title: "图像", extensions: "jpg,gif,png"},
            {title: "视频", extensions: "mp4"},
            {title: "音频", extensions: "mp3"},
            {title: "其他文件", extensions: "zip,rar,txt,doc,docx,xls,xlsx,ppt,pptx,pdf"}
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
             };*/
        },
        FilesAdded: function (up, files) {
            plupload.each(files, function (file) {
                document.getElementById('filelist').innerHTML += '<div id="' + file.id + '">' + file.name + ' (' + plupload.formatSize(file.size) + ') <b></b>\t<a href="javascript:;" onclick="deleteUploadFile(\'' + file.id + '\',1);">删除</a></div>';
            });
            //自动上传
            uploader.start();
            return false;
        },
        UploadProgress: function (up, file) {
            document.getElementById(file.id).getElementsByTagName('b')[0].innerHTML = '<span>' + file.percent + "%</span>";
        },
        FileUploaded: function (up, file, info) {
            //返回值
            if (info.response != null&&info.response!="") {
                // var jsonstr = eval("(" + info.response + ")");
                //取消重复
                if(document.getElementById("input"+file.id)!=null)return false;
                document.getElementById('file_result').innerHTML += '<input type="checkbox" id="input' + file.id + '" name="' + file.id + '" value="' + info.response + '" alt="' + file.name + '" title="' + file.size + '"/>';
                //把文件信息临时保存在cookie里，防止刷新，不见了
                SaveUploadFile(file, info, 1);
            }
        },
        Error: function (up, err) {
            document.getElementById('console').innerHTML += "\nError #" + err.code + ": " + err.message;
        }
    }
};


//文件上传[任务附件]
if(document.getElementById('pickfiles')!=null){
    var uploader = new plupload.Uploader(param_uploader);
    uploader.init();
}

/*****************************************任务，计划弹框的附件选项*****************************************************/
var param_uploader2 = {
    headers: {'X-Requested-With': 'XMLHttpRequest', 'X-CSRFToken': $.cookie('csrftoken')},
    runtimes: 'html5,html4',
    browse_button: 'pickfiles_dialog_task', // you can pass in id...
    container: document.getElementById('upload_container_dialog'), // ... or DOM Element itself
    url: '/home/files/fileupload/',
    flash_swf_url: '/static/js/plupload/Moxie.swf',
    //silverlight_xap_url : '../js/Moxie.xap',
    filters: {
        max_file_size: '10mb',
        mime_types: [
            {title: "图像", extensions: "jpg,gif,png"},
            {title: "视频", extensions: "mp4"},
            {title: "其他文件", extensions: "zip,rar,txt,doc,docx,xls,xlsx,ppt,pptx,pdf"}
        ]
    },
    init: {
        PostInit: function () {
            document.getElementById('filelist_comment').innerHTML = InitUploadfiles(3,"show");
            document.getElementById('file_result_comment').innerHTML = InitUploadfiles(3,"res");

        },
        FilesAdded: function (up, files) {
            plupload.each(files, function (file) {
                document.getElementById('filelist_comment').innerHTML += '<div id="' + file.id + '">' + file.name + ' (' + plupload.formatSize(file.size) + ') <b></b>\t<a href="javascript:;" onclick="deleteUploadFile(\'' + file.id + '\',3);">删除</a></div>';
            });
            //自动上传
            uploader2.start();
            return false;
        },
        UploadProgress: function (up, file) {
            document.getElementById(file.id).getElementsByTagName('b')[0].innerHTML = '<span>' + file.percent + "%</span>";
        },
        FileUploaded: function (up, file, info) {
            //返回值
            if (info.response != null&&info.response!="") {
                // var jsonstr = eval("(" + info.response + ")");
                //取消重复
                if (document.getElementById("input" + file.id) != null)return false;
                document.getElementById('file_result_comment').innerHTML += '<input type="checkbox" id="input' + file.id + '" name="' + file.id + '" value="' + info.response + '" alt="' + file.name + '" title="' + file.size + '"/>';
                //把文件信息临时保存在cookie里，防止刷新，不见了
                SaveUploadFile(file, info, 3);
            }
        },
        Error: function (up, err) {
            document.getElementById('console_comment').innerHTML += "\nError #" + err.code + ": " + err.message;
        }
    }
};

//文件上传[任务评论/计划沟通附件]
if(document.getElementById('pickfiles_dialog_task')!=null){
    var uploader2 = new plupload.Uploader(param_uploader2);
    uploader2.init();

}
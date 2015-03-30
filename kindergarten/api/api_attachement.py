#coding=utf-8
#date:14-11-6
__author__ = 'monica'
from rest_framework.views import APIView
from kindergarten.models import User,ActivityInfo,ActivityPhoto
from django.http import HttpResponse
from django.conf import settings
from kindergarten.script.util import Util

'''文件上传'''
class FileUpload(APIView):
    def post(self, request, **kwargs):
        if 'file' in request.FILES:
            filedata=request.FILES["file"]

            if filedata:
                #是否使用云存储
                if settings.USE_STORAGE:
                    filename, filepath,filesize,guid = Util.profile_upload_storage(filedata)
                else:
                    filename, filepath,filesize,guid = Util.profile_upload(filedata)
                fileinfo={}
                fileinfo["filename"]=filename
                fileinfo["filepath"]=filepath
                fileinfo["filesize"]=filesize
                request.session[guid]=fileinfo
                return Util.GetResponseData(True,0,guid)
        return Util.GetResponseData(False,-3)

'''活动照片上传'''
class FileActivity(APIView):
    def post(self, request, **kwargs):
        if 'file' in request.FILES and "activityid" in kwargs and kwargs["activityid"]:
            filedata=request.FILES["file"]
            activityid=kwargs["activityid"]
            if filedata:
                #是否使用云存储
                if settings.USE_STORAGE:
                    filename, filepath,filesize,guid = Util.profile_upload_storage(filedata,"/activity")
                else:
                    filename, filepath,filesize,guid = Util.profile_upload(filedata,"/activity")
                try:
                    activity = ActivityInfo.objects.get(id=activityid)
                except ActivityInfo.DoesNotExist:
                    return Util.GetResponseData(False,310)
                userid=request.user.id
                #是否是封面,默认第一张
                is_face = True
                if activity.activeImage:
                    is_face = False
                photo=ActivityPhoto.objects.create(activity=activity,title=filename,filepath=filepath,userid=userid,is_face=is_face)
                #photo.save()
                return Util.GetResponseData(True,0,photo.id)
        return Util.GetResponseData(False,-3)

'''课程文件上传'''
class FileCourse(APIView):
    def post(self, request, **kwargs):
        if 'file' in request.FILES:
            filedata=request.FILES["file"]
            if filedata:
                #是否使用云存储
                if settings.USE_STORAGE:
                    filename, filepath,filesize,guid = Util.profile_upload_storage(filedata,"/course")
                else:
                    filename, filepath,filesize,guid = Util.profile_upload(filedata,"/course")
                fileinfo={}
                fileinfo["filename"]=filename
                fileinfo["filepath"]=filepath
                fileinfo["filesize"]=filesize
                request.session[guid]=fileinfo
                return Util.GetResponseData(True,0,guid)
        return Util.GetResponseData(False,-3)

'''文件下载'''
class Download(APIView):
    def get(self, request, **kwargs):
        if 'filepath' in request.GET and request.GET['filepath']!="":
            filepath = request.GET['filepath']
            #中文解码
            filename=""
            if 'filename' in request.GET and request.GET['filename']!="":
                filename=request.GET['filename'].replace('%u', '\\u').encode('utf-8')
            return  HttpResponse(Util.profile_download(filepath,filename))
        return HttpResponse('404!很抱歉，附件已经不存在！')

'''删除目录的附件[未写到数据库部分]'''
class DeleteDirFile(APIView):
    def post(self, request, *args, **kwargs):
        if 'fileid' in kwargs and kwargs['fileid'] != "":
            fileid=kwargs['fileid']
            if fileid in request.session and request.session[fileid]:
                fileinfo=request.session[fileid]
                filepath=fileinfo['filepath']
                Util.profile_delete(filepath)
            return Util.GetResponseData(True)
        return Util.GetResponseData(False,-3)

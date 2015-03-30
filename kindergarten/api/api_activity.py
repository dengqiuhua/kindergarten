#coding=utf-8
#date:14-11-6
__author__ = 'monica'

from rest_framework.views import APIView
from kindergarten.models import User,ActivityInfo,ActivityPhoto,ClassInfo
from django.http import HttpResponse
from kindergarten.script.util import Util
from model_serializer import ActivityInfoSerializer,ActivityPhotoSerializer
from kindergarten.script.func import Func
import time
func=Func()

'''获取活动列表'''
class GetActivityList(APIView):
    def get(self, request, **kwargs):
        #分页
        pagesize, pageindex = Util.getPageSizeAndIndex(request)
        args={}        
        #查询条件
        if 'title' in request.GET and request.GET['title']:
            args['title__contains'] = request.GET['title'].strip()
        datalist , counts = func.GetActivityList(pagesize, pageindex,**args)
        data=ActivityInfoSerializer(datalist).data
        return Util.GetResponseData(True,0,data,counts)

'''添加/修改'''
class AddActivity(APIView):
    def post(self, request, **kwargs):
        if 'title' in request.POST and request.POST['title']:
            title=request.POST['title'].strip()
            #如果有id，则修改
            if 'id' in request.POST and request.POST['id']:
                activityid=request.POST['id']
                try:
                    activity=ActivityInfo.objects.get(id=activityid)
                except ActivityInfo.DoesNotExist:
                    return Util.GetResponseData(False,310)
                activity.title = title
            else:
                #新建
                activity=ActivityInfo.objects.create(title=title,userid=request.user.id)
            #添加班级
            if 'classid' in request.POST and request.POST['classid']:
                classid = request.POST['classid'].strip()
                try:
                    classinfo = ClassInfo.objects.get(id=classid)
                except ClassInfo.DoesNotExist:
                    pass
                else:
                    activity.classinfo= classinfo
            if 'activity_type' in request.POST and request.POST['activity_type']:
                activity.activity_type = request.POST['activity_type'].strip()
            if 'master' in request.POST:
                activity.master = request.POST['master'].strip()
            if 'address' in request.POST:
                activity.address = request.POST['address'].strip()
            if 'activity_date_start' in request.POST:
                activity.activity_date_start = request.POST['activity_date_start'].strip()
            if 'activity_date_end' in request.POST:
                activity.activity_date_end = request.POST['activity_date_end'].strip()
            if 'usercounts' in request.POST and request.POST['usercounts']:
                activity.usercounts = request.POST['usercounts'].strip()
            if 'description' in request.POST:
                activity.description = request.POST['description'].strip()
            activity.save()
            return Util.GetResponseData(True,0,activity.id)

        return Util.GetResponseData(False,-3)

'''获取活动照片列表'''
class GetActivityPhotoList(APIView):
    def get(self, request, **kwargs):
        if 'activityid' in kwargs and kwargs['activityid']:
            activityid = kwargs['activityid']
            try:
                activity = ActivityInfo.objects.get(id=activityid)
            except ActivityInfo.DoesNotExist:
                return Util.GetResponseData(False,310)
            #分页
            pagesize, pageindex = Util.getPageSizeAndIndex(request)
            args = {}
            args['activity']= activity
            #查询条件
            if 'title' in request.QUERY_PARAMS and request.GET['title']:
                args['title__contains'] = request.GET['title'].strip()
            datalist , counts = func.GetActivityPhotoList(pagesize, pageindex, **args)
            data=ActivityPhotoSerializer(datalist).data
            return Util.GetResponseData(True,0,data,counts)
        return Util.GetResponseData(False,-3)

'''添加活动照片'''
class AddActivityPhoto(APIView):
    def post(self, request, **kwargs):
        if 'activityid' in kwargs and kwargs['activityid'] and 'filepath' in request.POST and request.POST['filepath']:
            activityid = kwargs['id']
            try:
                activity = ActivityInfo.objects.get(id=activityid)
            except ActivityInfo.DoesNotExist:
                return Util.GetResponseData(False,310)
            #文件名称和路径
            filepath=filename=request.POST['filepath']
            #文件名称
            if 'filename' in request.POST and request.POST['filename']:
                filename = request.POST['filename']
            userid=1
            photo=ActivityPhoto.objects.create(activity=activity,title=filename,filepath=filepath,userid=userid)
            photo.save()
            return Util.GetResponseData(True,0,photo.id)
        return Util.GetResponseData(False,-3)

'''设置活动封面'''
class SetActivityFace(APIView):
    def post(self, request, **kwargs):
        if 'id' in kwargs and kwargs['id']:
            photoid = kwargs['id']
            try:
                photo = ActivityPhoto.objects.get(id=photoid)
            except ActivityPhoto.DoesNotExist:
                return Util.GetResponseData(False,910)
            photo.setFace()
            return Util.GetResponseData(True)
        return Util.GetResponseData(False,-3)

'''删除活动照片'''
class DeleteActivityPhoto(APIView):
    def post(self, request, **kwargs):
        if 'id' in kwargs and kwargs['id']:
            photoid = kwargs['id']
            try:
                photo = ActivityPhoto.objects.get(id=photoid)
            except ActivityPhoto.DoesNotExist:
                return Util.GetResponseData(False,910)
            photo.delete()
            return Util.GetResponseData(True)
        return Util.GetResponseData(False,-3)

'''删除'''
class DeleteActivity(APIView):
    def post(self, request, **kwargs):
        if 'activityid' in kwargs and kwargs['activityid']:
            activityid=kwargs['activityid']
            try:
                activity=ActivityInfo.objects.get(id=activityid)
            except ActivityInfo.DoesNotExist:
                return Util.GetResponseData(False,-3)
            #删除照片
            ActivityPhoto.objects.filter(activity=activity).delete()
            activity.delete()
            return Util.GetResponseData(True)
        return Util.GetResponseData(False,-3)

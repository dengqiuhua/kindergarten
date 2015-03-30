#coding=utf-8
#date:14-11-7
__author__ = 'monica'

from rest_framework.views import APIView
from rest_framework import viewsets,generics
from kindergarten.models import User,EducationCare
from django.http import HttpResponse
from kindergarten.script.util import Util
from model_serializer import EducationSerializer
from kindergarten.script.func import Func
import time
func=Func()

'''获取列表'''
class GetEducationList(APIView):
    def get(self, request, **kwargs):
        #分页
        pagesize, pageindex = Util.getPageSizeAndIndex(self.request)
        args={}
        #查询条件
        if 'title' in request.GET and request.GET['title']:
            args['title__contains'] = request.GET['title'].strip()
        datalist , counts = func.GetEducationList(pagesize, pageindex,**args)
        data=EducationSerializer(datalist).data
        return Util.GetResponseData(True,0,data,counts)

'''添加/修改'''
class AddEducation(APIView):
    def post(self, request, **kwargs):
        if 'title' in request.POST and request.POST['title']:
            title=request.POST['title'].strip()
            #如果有id，则修改
            if 'id' in request.POST and request.POST['id']:
                newid=request.POST['id']
                try:
                    education=EducationCare.objects.get(id=newid)
                except EducationCare.DoesNotExist:
                    return Util.GetResponseData(False,710)
                education.title = title
                education.modifytime = time.time()
            else:
                #新建
                education=EducationCare.objects.create(title=title,userid=request.user.id)
            if 'author' in request.POST:
                education.author= request.POST['author'].strip()
            if 'description' in request.POST:
                education.description = request.POST['description'].strip()
            if 'source' in request.POST:
                education.source = request.POST['source'].strip()
            if 'video' in request.POST:
                education.video = request.POST['video'].strip()
            #视频
            if 'fileid' in request.POST and request.POST['fileid']:
                fileid = request.POST['fileid'].strip()
                if fileid in request.session and request.session[fileid]:
                    fileinfo=request.session[fileid]
                    education.video = fileinfo["filepath"]

            education.save()
            return Util.GetResponseData(True,0,education.id)
        else:
            return Util.GetResponseData(False,-3)

'''删除'''
class DeleteEducation(APIView):
    def post(self, request, **kwargs):
        if 'educationid' in kwargs and kwargs['educationid']:
            educationid=kwargs['educationid']
            try:
                education=EducationCare.objects.get(id=educationid)
            except EducationCare.DoesNotExist:
                return Util.GetResponseData(False,710)
            education.delete()
            return Util.GetResponseData(True,0)
        else:
            return Util.GetResponseData(False,-3)

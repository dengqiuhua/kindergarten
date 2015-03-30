#coding=utf-8
#date:14-11-4
__author__ = 'monica'

from rest_framework.views import APIView
from kindergarten.models import User,TeacherInfo
from django.http import HttpResponse
from kindergarten.script.util import Util
from model_serializer import TeacherListSerializer
from kindergarten.script.func import Func
import time
func=Func()

'''获取列表'''
class GetTeacherList(APIView):
    def get(self, request, **kwargs):
        #分页
        pagesize, pageindex = Util.getPageSizeAndIndex(request)
        args={}
        #查询条件
        if 'name' in request.GET and request.GET['name']:
            args['name__contains'] = request.GET['name'].strip()
        datalist , counts = func.GetTeacherPageList(pagesize, pageindex,**args)
        data=TeacherListSerializer(datalist).data
        return Util.GetResponseData(True,0,data,counts)

'''添加/修改'''
class AddTeacher(APIView):
    def post(self, request, **kwargs):
        if 'name' in request.POST and request.POST['name']:
            name = request.POST['name'].strip()
            #如果有id，则修改
            if 'id' in request.POST and request.POST['id']:
                teacherid=request.POST['id']
                try:
                    teacher=TeacherInfo.objects.get(id=teacherid)
                except TeacherInfo.DoesNotExist:
                    return Util.GetResponseData(False,410)
                teacher.name = name
                teacher.modifytime = time.time()
            else:
                #新建
                teacher=TeacherInfo.objects.create(name=name)
            if 'sex' in request.POST and request.POST['sex']:
                teacher.sex = request.POST['sex'].strip()
            if 'birthday' in request.POST and request.POST['birthday']:
                teacher.birthday = request.POST['birthday'].strip()
            if 'phone' in request.POST:
                teacher.phone = request.POST['phone'].strip()
            if 'city' in request.POST:
                teacher.city = request.POST['city'].strip()
            if 'address' in request.POST:
                teacher.address = request.POST['address'].strip()
            if 'joindate' in request.POST and request.POST['joindate']:
                teacher.joindate = request.POST['joindate'].strip()
            if 'educate_school' in request.POST:
                teacher.educate_school = request.POST['educate_school'].strip()
            if 'degree' in request.POST and request.POST['degree']:
                teacher.degree = request.POST['degree'].strip()
            if 'teaching' in request.POST:
                teacher.teaching = request.POST['teaching'].strip()
            if 'photo' in request.POST and request.POST['photo']:
                teacher.photo = request.POST['photo'].strip()
            teacher.save()
            return Util.GetResponseData(True,0,teacher.id)
        else:
            return Util.GetResponseData(False,-3)

'''设置教师头像'''
class SetTeacherPhoto(APIView):
    def post(self, request, **kwargs):
        if 'teacherid' in kwargs and kwargs['teacherid']:
            teacherid = kwargs['teacherid']
            try:
                teacher = TeacherInfo.objects.get(id=teacherid)
            except TeacherInfo.DoesNotExist:
                return Util.GetResponseData(False,410)
            istop=True
            if 'photo' in kwargs and kwargs['istop']:
                teacher.photo = kwargs['photo'].strip()
                teacher.save()
                return Util.GetResponseData(True)
        return Util.GetResponseData(False,-3)

'''删除'''
class DeleteTeacher(APIView):
    def post(self, request, **kwargs):
        if 'teacherid' in kwargs and kwargs['teacherid']:
            teacherid=kwargs['teacherid']
            try:
                teacher=TeacherInfo.objects.get(id=teacherid)
            except TeacherInfo.DoesNotExist:
                return Util.GetResponseData(False,410)
            teacher.delete()
            return Util.GetResponseData(True)
        else:
            return Util.GetResponseData(False,-3)

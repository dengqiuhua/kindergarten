#coding=utf-8
#date:14-11-4
__author__ = 'monica'

from rest_framework.views import APIView
from kindergarten.models import User,StudentInfo,ClassInfo,ClassStudents
from django.http import HttpResponse
from kindergarten.script.util import Util
from model_serializer import StudentsListSerializer
from kindergarten.script.func import Func
import time
func=Func()

'''获取列表'''
class GetStudentsList(APIView):
    def get(self, request, **kwargs):
        #分页
        pagesize, pageindex = Util.getPageSizeAndIndex(request)
        args={}
        #查询条件
        if 'name' in request.GET and request.GET['name']:
            args['name__contains'] = request.GET['name'].strip()
        if 'classid' in request.GET and request.GET['classid']:
            args['name__contains'] = request.GET['classid'].strip()
        datalist , counts = func.GetStudentsPageList(pagesize, pageindex,**args)
        data=StudentsListSerializer(datalist).data
        return Util.GetResponseData(True,0,data,counts)

'''添加/修改'''
class AddStudent(APIView):
    def post(self, request, **kwargs):
        if 'name' in request.POST and request.POST['name']:
            name=request.POST['name'].strip()
            #如果有id，则修改
            if 'id' in request.POST and request.POST['id']:
                studentid=request.POST['id']
                try:
                    student=StudentInfo.objects.get(id=studentid)
                except StudentInfo.DoesNotExist:
                    return Util.GetResponseData(False,510)
                student.name = name
                student.modifytime = time.time()
            else:
                #新建
                student=StudentInfo.objects.create(name=name,userid=request.user.id)
            if 'number' in request.POST:
                student.number= request.POST['number'].strip()
            if 'sex' in request.POST and request.POST['sex']:
                student.sex = request.POST['sex'].strip()
            if 'birthday' in request.POST and request.POST['birthday']:
                student.birthday = request.POST['birthday'].strip()
            if 'phone' in request.POST:
                student.phone = request.POST['phone'].strip()
            if 'city' in request.POST:
                student.city = request.POST['city'].strip()
            if 'address' in request.POST:
                student.address = request.POST['address'].strip()
            if 'guardian' in request.POST:
                student.guardian = request.POST['guardian'].strip()
            if 'guardian_phone' in request.POST:
                student.guardian_phone = request.POST['guardian_phone'].strip()
            if 'emergency_contact' in request.POST:
                student.emergency_contact = request.POST['emergency_contact'].strip()
            if 'emergency_phone' in request.POST:
                student.emergency_phone = request.POST['emergency_phone'].strip()
            if 'qq' in request.POST:
                student.qq = request.POST['qq'].strip()
            if 'photo' in request.POST:
                student.photo = request.POST['photo'].strip()
            if 'hobby' in request.POST:
                student.hobby = request.POST['hobby'].strip()
            if 'remark' in request.POST:
                student.remark = request.POST['remark'].strip()
            student.save()
            #添加班级
            if 'classid' in request.POST and request.POST['classid']:
                classid = request.POST['classid'].strip()
                try:
                    classinfo = ClassInfo.objects.get(id=classid)
                except ClassInfo.DoesNotExist:
                    pass
                else:
                    try:
                        cs=ClassStudents.objects.get(student=student)
                    except ClassStudents.DoesNotExist:
                        cs=ClassStudents.objects.create(student=student, classinfo=classinfo)
                    cs.classinfo=classinfo
                    cs.save()
            return Util.GetResponseData(True,0,student.id)
        else:
            return Util.GetResponseData(False,-3)

'''设置学生头像'''
class SetStudentPhoto(APIView):
    def post(self, request, **kwargs):
        if 'studentid' in kwargs and kwargs['studentid']:
            studentid = kwargs['studentid']
            try:
                student = StudentInfo.objects.get(id=studentid)
            except StudentInfo.DoesNotExist:
                return Util.GetResponseData(False,510)
            istop=True
            if 'photo' in kwargs and kwargs['istop']:
                student.photo = kwargs['photo'].strip()
                student.save()
                return Util.GetResponseData(True)
        return Util.GetResponseData(False,-3)

'''删除'''
class DeleteStudent(APIView):
    def post(self, request, **kwargs):
        if 'studentid' in kwargs and kwargs['studentid']:
            studentid=kwargs['studentid']
            try:
                student=StudentInfo.objects.get(id=studentid)
            except StudentInfo.DoesNotExist:
                return Util.GetResponseData(False,510)
            student.delete()
            return Util.GetResponseData(True)
        else:
            return Util.GetResponseData(False,-3)

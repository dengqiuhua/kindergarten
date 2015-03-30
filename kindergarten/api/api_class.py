#coding=utf-8
#date:14-11-4
__author__ = 'monica'

from rest_framework.views import APIView
from kindergarten.models import User,ClassInfo,StudentInfo,TeacherInfo,ClassStudents,ClassTeachers
from django.http import HttpResponse
from kindergarten.script.util import Util
from model_serializer import ClassInfoSerializer,ClassTeacherSerializer,ClassStudentSerializer
from kindergarten.script.func import Func
import time
func=Func()

'''获取班级列表'''
class GetClassList(APIView):
    def get(self, request, **kwargs):
        args={}
        #查询条件
        if 'classname' in request.GET and request.GET['classname']:
            args['classname__contains'] = request.GET['classname'].strip()
        datalist = func.GetClassList(**args)
        data=ClassInfoSerializer(datalist).data
        return Util.GetResponseData(True,0,data,datalist.count())

'''获取未加入的班级列表'''
class GetClassListUnJoinForTeacher(APIView):
    def get(self, request, **kwargs):
        if 'teacherid' in request.GET and request.GET['teacherid']:
            teacherid = request.GET['teacherid'].strip()
            args={}
            try:
                teacher = TeacherInfo.objects.get(id=teacherid)
            except TeacherInfo.DoesNotExist:
                return func.GetClassList(**args)
            datalist = func.GetClassListUnJoinForTeacher(teacher, **args)
            data=ClassInfoSerializer(datalist).data
            return Util.GetResponseData(True,0,data,datalist.count())
        return Util.GetResponseData(False,-3)

'''获取班级学生列表'''
class GetClassStudentList(APIView):
    def get(self, request, **kwargs):
        if 'classid' in kwargs and kwargs['classid']:
            classid=kwargs['classid']
            #分页
            pagesize, pageindex = Util.getPageSizeAndIndex(request)
            args={}
            args["classinfo__id"]=classid
            #查询条件
            if 'name' in request.GET and request.GET['name']:
                args['student__name__contains'] = request.GET['name'].strip()
            datalist , counts = func.GetClassStudentsPageList(pagesize, pageindex,**args)
            data=ClassStudentSerializer(datalist).data
            return Util.GetResponseData(True,0,data,counts)
        return Util.GetResponseData(False,-3)

'''获取班级教师列表'''
class GetClassTeacherList(APIView):
    def get(self, request, **kwargs):
        if 'classid' in kwargs and kwargs['classid']:
            classid=kwargs['classid']
            #分页
            pagesize, pageindex = Util.getPageSizeAndIndex(request)
            args = {}
            args["classinfo__id"]=classid
            #查询条件
            if 'name' in request.GET and request.GET['name']:
                args['teacher__name__contains'] = request.GET['name'].strip()
            datalist , counts = func.GetClassTeacherPageList(pagesize, pageindex,**args)
            data=ClassTeacherSerializer(datalist).data
            return Util.GetResponseData(True,0,data,counts)
        return Util.GetResponseData(False,-3)

'''添加/修改'''
class AddClass(APIView):
    def post(self, request, **kwargs):
        if 'classname' in request.POST and request.POST['classname']:
            classname=request.POST['classname'].strip()
            #如果有id，则修改
            if 'id' in request.POST and request.POST['id']:
                classid=request.POST['id']
                try:
                    classinfo=ClassInfo.objects.get(id=classid)
                except ClassInfo.DoesNotExist:
                    return Util.GetResponseData(False,610)
                classinfo.classname= classname
                classinfo.modifytime = time.time()
            else:
                #新建
                classinfo=ClassInfo.objects.create(classname=classname)
            if 'description' in request.POST:
                classinfo.description= request.POST['description'].strip()
            if 'container' in request.POST:
                classinfo.container = request.POST['container'].strip()
            if 'headteacher' in request.POST:
                classinfo.headteacher = request.POST['headteacher'].strip()
            if 'headteacher_phone' in request.POST:
                classinfo.headteacher_phone = request.POST['headteacher_phone'].strip()
            if 'monitor' in request.POST:
                classinfo.monitor = request.POST['monitor'].strip()
            classinfo.save()
            return Util.GetResponseData(True,0,classinfo.id)
        else:
            return Util.GetResponseData(False,-3)

'''获取一条班级学生'''
class GetClassStudent(APIView):
    def get(self, request, **kwargs):
        if 'id' in kwargs and kwargs['id']:
            csid= kwargs['id']
            try:
                class_student = ClassStudents.objects.get(id=csid)
            except ClassInfo.DoesNotExist:
                return Util.GetResponseData(False,610)
            data=ClassStudentSerializer(class_student).data
            return Util.GetResponseData(True,0,data,1)
        return Util.GetResponseData(False,-3)

'''获取教师所在的班级'''
class GetTeacherClass(APIView):
    def get(self, request, **kwargs):
        if 'teacherid' in kwargs and kwargs['teacherid']:
            teacherid= kwargs['teacherid']
            try:
                teacher = TeacherInfo.objects.get(id=teacherid)
            except TeacherInfo.DoesNotExist:
                return Util.GetResponseData(False,410)
            datalist = func.GetClassByTeacher(teacher)
            data=ClassInfoSerializer(datalist).data
            return Util.GetResponseData(True,0,data,1)
        return Util.GetResponseData(False,-3)

'''添加班级学生'''
class AddClassStudent(APIView):
    def post(self, request, **kwargs):
        if 'classid' in kwargs and kwargs['classid'] and 'studentid' in request.POST and request.POST['studentid']:
            classid = kwargs['classid']
            studentid = request.POST['studentid']
            try:
                classinfo = ClassInfo.objects.get(id=classid)
                student = StudentInfo.objects.get(id=studentid)
            except ClassInfo.DoesNotExist or StudentInfo.DoesNotExist:
                return Util.GetResponseData(False,610)
            #如果有id，则修改
            if 'id' in request.POST and request.POST['id']:
                csid = request.POST['id']
                try:
                    class_student = ClassStudents.objects.get(id=csid)
                    class_student.classinfo = classinfo
                except ClassInfo.DoesNotExist:
                    class_student = ClassStudents.objects.create(student=student,classinfo = classinfo)
            else:
                class_student=ClassStudents.objects.create(student=student,classinfo = classinfo)
            if 'year' in request.POST and request.POST['year']:
                class_student.year= request.POST['year']
            if 'joindate' in request.POST and request.POST['joindate']:
                class_student.joindate = request.POST['joindate']
            if 'role' in request.POST and request.POST['role']:
                class_student.role = request.POST['role']
            class_student.save()
            return Util.GetResponseData(True,0,class_student.id)
        return Util.GetResponseData(False,-3)

'''添加班级教师'''
class AddClassTeacher(APIView):
    def post(self, request, **kwargs):
        if 'classid' in kwargs and kwargs['classid'] and 'teacherid' in request.POST and request.POST[ 'teacherid']:
            classid = kwargs['classid']
            teacherid = request.POST['teacherid']
            try:
                classinfo = ClassInfo.objects.get(id=classid)
                teacher = TeacherInfo.objects.get(id=teacherid)
            except ClassInfo.DoesNotExist or TeacherInfo.DoesNotExist:
                return Util.GetResponseData(False,610)
            #如果有id，则修改
            if 'id' in request.POST and request.POST['id']:
                ctid = request.POST['id']
                try:
                    class_teacher = ClassTeachers.objects.get(id=ctid)
                    class_teacher.classinfo = classinfo
                except ClassTeachers.DoesNotExist:
                    class_teacher = ClassTeachers.objects.create(teacher=teacher,classinfo=classinfo)
            else:
                class_teacher = ClassTeachers.objects.create(teacher=teacher,classinfo=classinfo)
            if 'role' in request.POST and request.POST['role']:
                class_teacher.role = request.POST['role']
            class_teacher.save()
            return Util.GetResponseData(True,0,class_teacher.id)
        return Util.GetResponseData(False,-3)

'''删除'''
class DeleteClass(APIView):
    def post(self, request, **kwargs):
        if 'classid' in kwargs and kwargs['classid']:
            classid=kwargs['classid']
            try:
                classinfo=ClassInfo.objects.get(id=classid)
            except ClassInfo.DoesNotExist:
                return Util.GetResponseData(False,610)
            classinfo.delete()
            return Util.GetResponseData(True,0)
        else:
            return Util.GetResponseData(False,-3)

'''删除班级学生'''
class DeleteClassStudent(APIView):
    def post(self, request, **kwargs):
        if 'id' in kwargs and kwargs['id']:
            classid=kwargs['id']
            try:
                info=ClassStudents.objects.get(id=classid)
            except ClassStudents.DoesNotExist:
                return Util.GetResponseData(False,510)
            info.delete()
            return Util.GetResponseData(True,0)
        else:
            return Util.GetResponseData(False,-3)

'''删除班级教师'''
class DeleteClassTeacher(APIView):
    def post(self, request, **kwargs):
        if 'id' in kwargs and kwargs['id']:
            classid=kwargs['id']
            try:
                info=ClassTeachers.objects.get(id=classid)
            except ClassTeachers.DoesNotExist:
                return Util.GetResponseData(False,410)
            info.delete()
            return Util.GetResponseData(True,0)
        else:
            return Util.GetResponseData(False,-3)
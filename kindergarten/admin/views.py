#coding=utf-8
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView
from kindergarten.models import Recommendation,NewsInfo,User,ClassInfo,StudentInfo,TeacherInfo,ActivityInfo,CourseInfo,ClassStudents,EducationCare
from django import forms
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import time
# Create your views here.

'''首页推荐'''
class RecommendHome(TemplateView):
    @method_decorator(login_required(login_url='/login/'))
    def get(self, request, *args, **kwargs):
        context={}
        context["topnav"]=1
        context["leftnav"] = 1
        return render_to_response("block_recommend_home.html",context,context_instance=RequestContext(request))

'''首页推荐添加/编辑页'''
class RecommendAdd(TemplateView):
    @method_decorator(login_required(login_url='/login/'))
    def get(self, request, *args, **kwargs):
        context={}
        context["topnav"]=1
        context["leftnav"] = 2
        form = UeditorModelForm()
        if 'id' in request.GET and request.GET['id']:
            recommendid=int(request.GET['id'])
            try:
                recommend=Recommendation.objects.get(id=recommendid)
            except Recommendation.DoesNotExist:
                pass
            else:
                context['recommend'] = recommend
        return render_to_response("block_recommend_add.html",context,context_instance=RequestContext(request))

'''新闻公告'''
class NewsHome(TemplateView):
    @method_decorator(login_required(login_url='/login/'))
    def get(self, request, *args, **kwargs):
        context={}
        context["topnav"]=2
        context["leftnav"] = 1
        return render_to_response("block_news_home.html",context,context_instance=RequestContext(request))

'''新闻公告添加/编辑页'''
class NewsAdd(TemplateView):
    @method_decorator(login_required(login_url='/login/'))
    def get(self, request, *args, **kwargs):
        context={}
        context["topnav"]=2
        context["leftnav"] = 2
        form = UeditorModelForm()
        if 'id' in request.GET and request.GET['id']:
            newsid=int(request.GET['id'])
            try:
                news=NewsInfo.objects.get(id=newsid)
            except NewsInfo.DoesNotExist:
                pass
            else:
                context['news'] = news
            form = UeditorModelForm(initial={'content':news.content})
        context["content_form"] = form
        return render_to_response("block_news_add.html",context,context_instance=RequestContext(request))

'''班级管理'''
class ClassHome(TemplateView):
    @method_decorator(login_required(login_url='/login/'))
    def get(self, request, *args, **kwargs):
        context={}
        context["topnav"]=3
        context["leftnav"] = 1
        return render_to_response("block_class_home.html",context,context_instance=RequestContext(request))

'''班级添加/编辑页'''
class ClassAdd(TemplateView):
    @method_decorator(login_required(login_url='/login/'))
    def get(self, request, *args, **kwargs):
        context={}
        context["topnav"]=3
        context["leftnav"] = 1
        if 'id' in request.GET and request.GET['id']:
            classid=int(request.GET['id'])
            try:
                classinfo=ClassInfo.objects.get(id=classid)
            except ClassInfo.DoesNotExist:
                pass
            else:
                context['profile'] = classinfo
        return render_to_response("block_class_add.html",context,context_instance=RequestContext(request))

'''班级学生/教师'''
class ClassManage(TemplateView):
    @method_decorator(login_required(login_url='/login/'))
    def get(self, request, *args, **kwargs):
        context={}
        context["topnav"]=3
        context["leftnav"] = 1
        context["mod"] = ''
        if 'id' in kwargs and kwargs['id']:
            classid=int(kwargs['id'])
            try:
                classinfo=ClassInfo.objects.get(id=classid)
            except ClassInfo.DoesNotExist:
                pass
            else:
                context['classinfo'] = classinfo
        return render_to_response("block_class_manage.html",context,context_instance=RequestContext(request))

'''学生管理'''
class StudentsHome(TemplateView):
    @method_decorator(login_required(login_url='/login/'))
    def get(self, request, *args, **kwargs):
        context = {}
        context["topnav"] = 3
        context["leftnav"] = 2
        return render_to_response("block_students_home.html", context, context_instance=RequestContext(request))

'''学生添加/编辑页'''
class StudentAdd(TemplateView):
    @method_decorator(login_required(login_url='/login/'))
    def get(self, request, *args, **kwargs):
        context={}
        context["topnav"]=3
        context["leftnav"] = 2
        #班级列表
        context["classlist"] = ClassInfo.objects.filter()
        if 'id' in request.GET and request.GET['id']:
            studentid=int(request.GET['id'])
            try:
                student=StudentInfo.objects.get(id=studentid)
            except StudentInfo.DoesNotExist:
                pass
            else:
                #班级
                csinfo=ClassStudents.objects.filter(student=student)
                student.classid=0
                if csinfo and csinfo[0].classinfo:
                    student.classid=csinfo[0].classinfo.id
                if student.birthday:
                    student.birthday = student.birthday.strftime('%Y-%m-%d')
                context['profile'] = student
        return render_to_response("block_students_add.html",context,context_instance=RequestContext(request))

'''教师管理'''
class TeacherHome(TemplateView):
    @method_decorator(login_required(login_url='/login/'))
    def get(self, request, *args, **kwargs):
        context = {}
        context["topnav"] = 3
        context["leftnav"] = 3
        return render_to_response("block_teacher_home.html", context, context_instance=RequestContext(request))

'''教师添加/编辑页'''
class TeacherAdd(TemplateView):
    @method_decorator(login_required(login_url='/login/'))
    def get(self, request, *args, **kwargs):
        context={}
        context["topnav"]=3
        context["leftnav"] = 3
        if 'id' in request.GET and request.GET['id']:
            teacherid=int(request.GET['id'])
            try:
                teacher=TeacherInfo.objects.get(id=teacherid)
            except TeacherInfo.DoesNotExist:
                pass
            else:
                if teacher.birthday:
                    teacher.birthday = teacher.birthday.strftime('%Y-%m-%d')
                context['profile'] = teacher
        return render_to_response("block_teacher_add.html",context,context_instance=RequestContext(request))

'''活动管理'''
class ActivityHome(TemplateView):
    @method_decorator(login_required(login_url='/login/'))
    def get(self, request, *args, **kwargs):
        context = {}
        context["topnav"] = 4
        context["leftnav"] = 1
        return render_to_response("block_activity_home.html", context, context_instance=RequestContext(request))

'''活动添加/编辑页'''
class ActivityAdd(TemplateView):
    @method_decorator(login_required(login_url='/login/'))
    def get(self, request, *args, **kwargs):
        context = {}
        context["topnav"] = 4
        context["leftnav"] = 1
        #班级列表
        context["classlist"] = ClassInfo.objects.filter()
        if 'id' in request.GET and request.GET['id']:
            activityid = int(request.GET['id'])
            try:
                activity = ActivityInfo.objects.get(id=activityid)
            except ActivityInfo.DoesNotExist:
                pass
            else:
                if activity.activity_date_start:
                    activity.activity_date_start = activity.activity_date_start.strftime('%Y-%m-%d')
                if activity.activity_date_end:
                    activity.activity_date_end = activity.activity_date_end.strftime('%Y-%m-%d')
                context['activity'] = activity
        return render_to_response("block_activity_add.html", context, context_instance=RequestContext(request))

'''活动照片添加/编辑页'''
class ActivityPhoto(TemplateView):
    @method_decorator(login_required(login_url='/login/'))
    def get(self, request, *args, **kwargs):
        context = {}
        context["topnav"] = 4
        context["leftnav"] = 1
        if 'id' in request.GET and request.GET['id']:
            activityid = int(request.GET['id'])
            try:
                activity = ActivityInfo.objects.get(id=activityid)
            except ActivityInfo.DoesNotExist:
                pass
            else:
                context['activity'] = activity
        return render_to_response("block_activity_photo.html", context, context_instance=RequestContext(request))

'''课程管理'''
class CourseHome(TemplateView):
    @method_decorator(login_required(login_url='/login/'))
    def get(self, request, *args, **kwargs):
        context = {}
        context["topnav"] = 5
        context["leftnav"] = 1
        return render_to_response("block_course_home.html", context, context_instance=RequestContext(request))

'''课程添加/编辑页'''
class CourseAdd(TemplateView):
    @method_decorator(login_required(login_url='/login/'))
    def get(self, request, *args, **kwargs):
        context = {}
        context["topnav"] = 5
        context["leftnav"] = 2
        form = UeditorModelForm_Course()
        if 'id' in request.GET and request.GET['id']:
            courseid = int(request.GET['id'])
            try:
                course = CourseInfo.objects.get(id=courseid)
            except CourseInfo.DoesNotExist:
                pass
            else:
                context['course'] = course
                form = UeditorModelForm_Course(initial={'description': course.description})
        context["content_form"] = form
        return render_to_response("block_course_add.html", context, context_instance=RequestContext(request))

'''育儿宝典管理'''
class EducationHome(TemplateView):
    @method_decorator(login_required(login_url='/login/'))
    def get(self, request, *args, **kwargs):
        context = {}
        context["topnav"] = 7
        context["leftnav"] = 1
        return render_to_response("block_education_home.html", context, context_instance=RequestContext(request))

'''育儿宝典添加/编辑页'''
class EducationAdd(TemplateView):
    @method_decorator(login_required(login_url='/login/'))
    def get(self, request, *args, **kwargs):
        context = {}
        context["topnav"] = 7
        context["leftnav"] = 2
        form = UeditorModelForm_Course()
        if 'id' in request.GET and request.GET['id']:
            educationid = int(request.GET['id'])
            try:
                education = EducationCare.objects.get(id=educationid)
            except EducationCare.DoesNotExist:
                pass
            else:
                context['education'] = education
                form = UeditorModelForm_Course(initial={'description': education.description})
        context["content_form"] = form
        return render_to_response("block_education_add.html", context, context_instance=RequestContext(request))

'''用户管理'''
class UserHome(TemplateView):
    @method_decorator(login_required(login_url='/login/'))
    def get(self, request, *args, **kwargs):
        context = {}
        context["topnav"] = 8
        context["leftnav"] = 1
        return render_to_response("block_user_home.html", context, context_instance=RequestContext(request))

'''添加用户'''
class UserAdd(TemplateView):
    @method_decorator(login_required(login_url='/login/'))
    def get(self, request, *args, **kwargs):
        context = {}
        context["topnav"] = 8
        context["leftnav"] = 1
        return render_to_response("block_user_add.html", context, context_instance=RequestContext(request))

'''预约管理'''
class ReservationHome(TemplateView):
    @method_decorator(login_required(login_url='/login/'))
    def get(self, request, *args, **kwargs):
        context = {}
        context["topnav"] = 6
        context["leftnav"] = 1
        return render_to_response("block_reservation_home.html", context, context_instance=RequestContext(request))

'''百度文本编辑器'''
class UeditorModelForm(forms.ModelForm):
    class Meta:
        model=NewsInfo
        fields = ['content']

'''百度文本编辑器'''
class UeditorModelForm_Course(forms.ModelForm):
    class Meta:
        model = CourseInfo
        fields = ['description']
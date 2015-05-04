#coding=utf-8
#date:14-11-4
__author__ = 'monica'
from kindergarten.models import *
from django.core.urlresolvers import reverse
from kindergarten.script.util import Util
class Func:

    '''获取首页推荐分页列表'''
    def GetRecommendList(self,pagesize, pageindex,**args):
        datalist=Recommendation.objects.filter(**args).order_by("-createtime")[(pageindex - 1) * pagesize:pagesize * pageindex]
        counts = Recommendation.objects.filter(**args).count()
        return self.InitRecommendList(datalist),counts

    '''格式化推荐数据'''
    def InitRecommendList(self, datalist):
        reslist = []
        if datalist:
            for data in datalist:
                if not data:
                    continue
                data.createtime = Util.GetGamTime(data.createtime, True)
                if data.imagepath:
                    data.imagepath = Util.getFileUrl(data.imagepath)
                reslist.append(data)
        return reslist

    '''获取新闻分页列表'''
    def GetNewsPageList(self,pagesize, pageindex,**args):
        datalist=NewsInfo.objects.filter(**args).order_by("-createtime")[(pageindex - 1) * pagesize:pagesize * pageindex]
        counts = NewsInfo.objects.filter(**args).count()
        return self.InitNewsList(datalist),counts

    '''格式化新闻数据'''
    def InitNewsList(self, datalist):
        reslist = []
        if datalist:
            for data in datalist:
                if not data:
                    continue
                data.createtime = Util.GetGamTime(data.createtime, True)
                data.content = Util.trimHtmlTag(data.content)
                reslist.append(data)
        return reslist

    '''获取班级列表'''
    def GetClassList(self, **args):
        datalist = ClassInfo.objects.filter(**args).order_by("-createtime")
        return datalist

    '''获取没有参加的班级列表[教师]'''
    def GetClassListUnJoinForTeacher(self, teacher, **args):
        datalist = ClassInfo.objects.exclude(
            id__in=(ClassTeachers.objects.filter(teacher=teacher).values_list('teacher', flat=True)))
        return datalist

    '''获取班级学生分页列表'''
    def GetClassStudentsPageList(self, pagesize, pageindex, **args):
        datalist = ClassStudents.objects.filter(**args).order_by("-id")[(pageindex - 1) * pagesize:pagesize * pageindex]
        counts = ClassStudents.objects.filter(**args).count()
        return datalist, counts

    '''获取班级教师分页列表'''
    def GetClassTeacherPageList(self, pagesize, pageindex, **args):
        datalist = ClassTeachers.objects.filter(**args).order_by("-id")[(pageindex - 1) * pagesize:pagesize * pageindex]
        counts = ClassTeachers.objects.filter(**args).count()
        return datalist, counts

    '''格式化教师数据'''
    def InitTeacherList(self, datalist):
        reslist = []
        if datalist:
            for data in datalist:
                if not data:
                    continue
                data.classinfo = self.GetClassByTeacher(data)
                if data.birthday:
                    data.birthday = data.birthday.strftime('%Y-%m-%d')
                reslist.append(data)
        return reslist

    '''获取学生分页列表'''
    def GetStudentsPageList(self, pagesize, pageindex, **args):
        datalist = StudentInfo.objects.filter(**args).order_by("-id")[(pageindex - 1) * pagesize:pagesize * pageindex]
        counts = StudentInfo.objects.filter(**args).count()
        return self.InitStudentsList(datalist), counts

    '''获取教师的班级列表'''
    def GetClassByTeacher(self,teacher):
        datalist = ClassInfo.objects.filter(
            id__in=(ClassTeachers.objects.filter(teacher=teacher).values_list('teacher', flat=True)))
        return datalist

    '''获取学生的班级列表'''
    def GetClassByStudent(self, student):
        datalist =ClassStudents.objects.filter(student=student)
        return datalist

    '''格式化学生数据'''
    def InitStudentsList(self, datalist):
        reslist = []
        if datalist:
            for data in datalist:
                if not data:
                    continue
                data.classinfo = self.GetClassByStudent(data)
                if data.birthday:
                    data.birthday = data.birthday.strftime('%Y-%m-%d')
                reslist.append(data)
        return reslist

    '''获取教师分页列表'''
    def GetTeacherPageList(self, pagesize, pageindex, **args):
        datalist = TeacherInfo.objects.filter(**args).order_by("-createtime")[(pageindex - 1) * pagesize:pagesize * pageindex]
        counts = TeacherInfo.objects.filter(**args).count()
        return self.InitTeacherList(datalist),counts

    '''活动分页列表'''
    def GetActivityList(self,pagesize, pageindex,**args):
        datalist=ActivityInfo.objects.filter(**args).order_by("-createtime")[(pageindex - 1) * pagesize:pagesize * pageindex]
        counts = ActivityInfo.objects.filter(**args).count()
        return self.InitActivityList(datalist),counts

    '''获取活动照片分页列表'''
    def GetActivityPhotoList(self, pagesize, pageindex, **args):
        datalist = ActivityPhoto.objects.filter(**args).order_by("-createtime")[(pageindex - 1) * pagesize:pagesize * pageindex]
        counts = ActivityPhoto.objects.filter(**args).count()
        return self.InitActivityPhotoList(datalist), counts

    '''格式化活动照片数据'''
    def InitActivityPhotoList(self, datalist):
        reslist = []
        if datalist:
            for data in datalist:
                if not data:
                    continue
                if data.filepath:
                    data.filepath = Util.getFileUrl(data.filepath)
                reslist.append(data)
        return reslist

    '''格式化活动数据'''
    def InitActivityList(self, datalist):
        reslist = []
        if datalist:
            for data in datalist:
                if not data:
                    continue
                if data.activity_date_start:
                    data.activity_date_start = data.activity_date_start.strftime('%Y-%m-%d')
                if data.activity_date_end:
                    data.activity_date_end = data.activity_date_end.strftime('%Y-%m-%d')
                data.description = Util.trimHtmlTag(data.description)
                reslist.append(data)
                #分页
        return reslist

    '''获取课程分页列表'''
    def GetCourseList(self, pagesize, pageindex, **args):
        datalist = CourseInfo.objects.filter(**args).order_by("-createtime")[(pageindex - 1) * pagesize:pagesize * pageindex]
        counts = CourseInfo.objects.filter(**args).count()
        return self.InitCourseList(datalist), counts

    '''格式化课程数据'''
    def InitCourseList(self, datalist):
        reslist = []
        if datalist:
            for data in datalist:
                if not data:
                    continue
                data.createtime = Util.GetGamTime(data.createtime, True)
                data.description = Util.trimHtmlTag(data.description)
                if data.imagepath:
                    data.imagepath = Util.getFileUrl( data.imagepath)
                reslist.append(data)
        return reslist

    '''获取育儿宝典分页列表'''
    def GetEducationList(self, pagesize, pageindex, **args):
        datalist = EducationCare.objects.filter(**args).order_by("-createtime")[(pageindex - 1) * pagesize:pagesize * pageindex]
        counts = EducationCare.objects.filter(**args).count()
        return self.InitEducationList(datalist), counts

    '''格式化育儿宝典数据'''
    def InitEducationList(self, datalist):
        reslist = []
        if datalist:
            for data in datalist:
                if not data:
                    continue
                data.createtime = Util.GetGamTime(data.createtime, True)
                data.description = Util.trimHtmlTag(data.description)
                reslist.append(data)
        return reslist

    '''获取预约分页列表'''
    def GetReservationPageList(self, pagesize, pageindex, **args):
        datalist = Reservation.objects.filter(**args).order_by("-createtime")[ (pageindex - 1) * pagesize:pagesize * pageindex]
        counts = Reservation.objects.filter(**args).count()
        return datalist, counts

    '''获取评论分页列表'''
    def GetCommentPageList(self, pagesize, pageindex, **args):
        datalist = CommentInfo.objects.filter(**args).order_by("-createtime")[ (pageindex - 1) * pagesize:pagesize * pageindex]
        counts = CommentInfo.objects.filter(**args).count()
        return datalist, counts

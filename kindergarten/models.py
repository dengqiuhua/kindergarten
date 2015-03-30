#coding=utf-8
#date:14-11-4
__author__ = 'monica'
from django.db import models
from django.contrib.auth.models import User
from kindergarten.plugin.Ueditor.models import UEditorField
from kindergarten.plugin.Ueditor.commands import UEditorEventHandler
import time

'''推荐'''
class Recommendation(models.Model):
    class Meta:
        db_table = 'kg_recommendation'

    type = models.IntegerField(default=0,null=True)
    title = models.CharField(max_length=200, null=True)
    imagepath = models.CharField(max_length=200, null=True)
    url = models.CharField(max_length=200, null=True)
    userid = models.IntegerField(null=True)
    createtime = models.IntegerField(null=True)

'''学生信息'''
class StudentInfo(models.Model):
    class Meta:
        db_table = 'kg_user_profile'
    #user = models.ForeignKey(User, unique=True)
    name = models.CharField(max_length=20, null=True)
    number = models.CharField(max_length=20, null=True)
    sex=models.IntegerField(default=0,null=True)
    birthday=models.DateTimeField(null=True)
    phone = models.CharField(max_length=20, null=True)
    city = models.CharField(max_length=20,null=True)#城市
    address = models.CharField(max_length=50,null=True)#地址
    guardian = models.CharField(max_length=20, null=True)#监护人
    guardian_phone = models.CharField(max_length=20, null=True)
    parents = models.CharField(max_length=20, null=True)#家长
    parents_phone = models.CharField(max_length=20, null=True)
    emergency_contact = models.CharField(max_length=20, null=True)#紧急联系人
    emergency_phone = models.CharField(max_length=20, null=True)
    qq = models.CharField(max_length=20,null=True)
    wechat = models.CharField(max_length=40,null=True)#微信
    identify = models.CharField(max_length=20,null=True)#身份证
    photo = models.CharField(max_length=100, null=True)
    activecode = models.CharField(max_length=50, null=True)#激活码
    isvalidated = models.IntegerField(default=0, null=True)#是否激活
    hobby = models.CharField(max_length=100, null=True)#特长、爱好
    remark = models.CharField(max_length=300, null=True)#备注，如饮食禁忌等
    userid = models.IntegerField(null=True)
    createtime = models.IntegerField(null=True)
    modifytime = models.IntegerField(default=time.time())

'''班级'''
class ClassInfo(models.Model):
    class Meta:
        db_table = 'kg_class_info'
    classname = models.CharField(max_length=20)
    description = models.CharField(max_length=500,null=True)
    container = models.IntegerField(default=0, null=True)#班级容量
    headteacher = models.CharField(max_length=20,null=True)
    headteacher_phone = models.CharField(max_length=20,null=True)
    monitor = models.CharField(max_length=20,null=True)
    remark = models.CharField(max_length=200,null=True)
    userid = models.IntegerField(null=True)
    createtime = models.IntegerField(null=True)
    modifytime = models.IntegerField(default=time.time())

'''教师'''
class TeacherInfo(models.Model):
    class Meta:
        db_table = 'kg_teacher_info'
    name = models.CharField(max_length=20,null=True)
    sex = models.IntegerField(default=0, null=True)
    birthday = models.DateTimeField(null=True)
    phone = models.CharField(max_length=20, null=True)
    address = models.CharField(max_length=50, null=True)#地址
    degree = models.IntegerField(default=0, null=True)
    educate_school = models.CharField(max_length=50,null=True)
    joindate = models.DateTimeField(null=True)
    city = models.CharField(max_length=20, null=True)
    photo = models.CharField(max_length=100, null=True)
    teaching = models.CharField(max_length=20, null=True)
    createtime = models.IntegerField(null=True)
    modifytime = models.IntegerField(default=time.time())

'''班级学生'''
class ClassStudents(models.Model):
    class Meta:
        db_table = 'kg_class_students'
    student = models.ForeignKey(StudentInfo)
    classinfo = models.ForeignKey(ClassInfo)
    year = models.IntegerField(null=True)
    joindate = models.DateTimeField(null=True)
    role = models.IntegerField(default=0,null=True)
    status = models.IntegerField(default=0,null=True)
    createtime = models.IntegerField(null=True)
    modifytime = models.IntegerField(default=time.time())

'''班级教师'''
class ClassTeachers(models.Model):
    class Meta:
        db_table = 'kg_class_teachers'
    teacher = models.ForeignKey(TeacherInfo)
    classinfo = models.ForeignKey(ClassInfo)
    role = models.IntegerField(default=0,null=True)
    status = models.IntegerField(default=0,null=True)
    createtime = models.IntegerField(null=True)
    modifytime = models.IntegerField(default=time.time())

'''获奖信息'''
class AwardInfo(models.Model):
    class Meta:
        db_table = 'kg_award_info'
    honor = models.CharField(max_length=50, null=True)
    teacher = models.ForeignKey(TeacherInfo)
    classinfo = models.ForeignKey(ClassInfo)
    student = models.ForeignKey(StudentInfo)
    awarddate = models.DateTimeField(null=True)
    photo = models.CharField(max_length=100, null=True)
    is_garden = models.BooleanField(default=False)
    remark = models.CharField(max_length=300, null=True)
    createtime = models.IntegerField(null=True)
    modifytime = models.IntegerField(default=time.time())

class myEventHander(UEditorEventHandler):
    def on_selectionchange(self):
        pass

'''新闻公告'''
class NewsInfo(models.Model):
    class Meta:
        db_table="kg_news_info"
    news_type=models.IntegerField(null=True,default=0)
    title=models.CharField(max_length=200)
    #content=models.TextField(null=True)
    content= UEditorField('', width=700, height=300, toolbars="mini", imagePath="", filePath="", upload_settings={"imageMaxSize": 1204000},
                          settings={}, command=None, event_handler= myEventHander(), blank=True)#toolbars="full"
    author=models.CharField(max_length=50,null=True)
    summary=models.CharField(max_length=500,null=True)#概要
    is_wechat=models.BooleanField(default=False)#是否发送到微信
    is_top = models.BooleanField(default=False)#是否置顶
    viewcounts=models.IntegerField(null=True,default=0)
    userid=models.ForeignKey(User,null=True)
    status=models.IntegerField(null=True,default=0)
    createtime=models.IntegerField(default=time.time())
    modifytime=models.IntegerField(null=True)
    #置顶
    def setTop(self,is_top=True):
        self.is_top=is_top;
        self.save()

'''活动'''
class ActivityInfo(models.Model):
    class Meta:
        db_table = "kg_activity_info"
    title = models.CharField(max_length=200)
    description = models.TextField(null=True)
    activity_type = models.IntegerField(null=True,default=0)
    master = models.CharField(max_length=50,null=True)
    classinfo = models.ForeignKey(ClassInfo,null=True)
    address = models.CharField(max_length=50,null=True)
    activity_date_start = models.DateTimeField(null=True)
    activity_date_end = models.DateTimeField(null=True)
    usercounts = models.IntegerField(null=True,default=0)
    viewcounts = models.IntegerField(null=True, default=0)
    is_wechat = models.BooleanField(default=False)#是否发送到微信
    userid = models.IntegerField(null=True)
    createtime = models.IntegerField(default=time.time())
    modifytime = models.IntegerField(null=True)

    @property
    def activeImage(self):
        images = ActivityPhoto.objects.filter(activity=self,is_face=True)
        if images :
            return images[0].filepath
        return None

'''活动照片'''
class ActivityPhoto(models.Model):
    class Meta:
        db_table = "kg_activity_photo"
    activity = models.ForeignKey(ActivityInfo)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=500, null=True)
    filepath = models.CharField(max_length=200)
    is_face = models.BooleanField(default=False)
    userid = models.IntegerField(null=True)
    createtime = models.IntegerField(default=time.time())

    #设置封面
    def setFace(self):
        #清除封面
        ActivityPhoto.objects.filter(activity=self.activity,is_face=True).update(is_face=False)
        self.is_face = True
        self.save()

'''附件'''
class Attachement(models.Model):
    class Meta:
        db_table = "kg_attachement"
    type = models.IntegerField(null=True)
    obj_id = models.IntegerField()
    filename = models.CharField(max_length=50, null=True)
    filepath = models.CharField(max_length=200)
    status = models.IntegerField(null=True, default=0)
    userid = models.IntegerField(null=True)
    createtime = models.IntegerField(default=time.time())

'''课程'''
class CourseInfo(models.Model):
    class Meta:
        db_table = "kg_course_info"
    course_type = models.IntegerField(null=True,default=0)
    title = models.CharField(max_length=200)
    #description = models.TextField(null=True)
    description = UEditorField('', width=700, height=300, toolbars="mini", imagePath="", filePath="", upload_settings={"imageMaxSize": 1204000},
                           settings={}, command=None, event_handler=myEventHander(), blank=True)
    teacher = models.CharField(max_length=50,null=True)
    imagepath = models.CharField(max_length=100,null=True)
    source = models.CharField(max_length=50,null=True)
    parentid = models.IntegerField(null=True,default=0)
    video = models.CharField(max_length=100,null=True)
    viewcounts = models.IntegerField(null=True, default=0)
    userid = models.IntegerField(null=True)
    createtime = models.IntegerField(default=time.time())
    modifytime = models.IntegerField(null=True)

'''评论'''
class CommentInfo(models.Model):
    class Meta:
        db_table = "kg_comment_info"
    content = models.CharField(max_length=500)
    parentid = models.IntegerField(null=True, default=0)
    mod = models.IntegerField(null=True)
    obj_id = models.IntegerField()
    userid = models.ForeignKey(User,null=True)
    createtime = models.IntegerField(default=time.time())
    modifytime = models.IntegerField(null=True)

'''育儿宝典'''
class EducationCare(models.Model):
    class Meta:
        db_table = "kg_education_care"
    title = models.CharField(max_length=200)
    description = UEditorField('', width=700, height=300, toolbars="mini", imagePath="", filePath="", upload_settings={"imageMaxSize": 1204000},
                           settings={}, command=None, event_handler=myEventHander(), blank=True)
    author = models.CharField(max_length=50,null=True)
    source = models.CharField(max_length=50,null=True)
    video = models.CharField(max_length=100,null=True)
    viewcounts = models.IntegerField(null=True, default=0)
    userid = models.IntegerField(null=True)
    createtime = models.IntegerField(default=time.time())
    modifytime = models.IntegerField(null=True)

'''预约'''
class Reservation(models.Model):
    class Meta:
        db_table = "kg_reservation"
    student = models.CharField(max_length=50,null=True)#学生
    name = models.CharField(max_length=50,null=True)#拜访者姓名
    role = models.CharField(max_length=50,null=True)#拜访者身份
    reserve_date = models.DateTimeField(null=True)#预约日期
    address = models.CharField(max_length=50, null=True)
    remark = models.CharField(max_length=100,null=True)
    reserve_others = models.CharField(max_length=50,null=True)#预约其他人
    isread = models.BooleanField(default=False)
    ismeet = models.BooleanField(default=False)
    callback = models.CharField(max_length=300, null=True)
    phone = models.CharField(max_length=50,null=True)
    createtime = models.IntegerField(default=time.time())
    #设置是否已结束及反馈
    def set_meet(self,ismeet=True,callback=""):
        self.callback=callback
        self.ismeet=ismeet
        self.save()
    #设置是否已知晓
    def read(self):
        self.isread=True
        self.save()

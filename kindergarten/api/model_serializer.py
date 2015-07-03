# coding=utf-8
from rest_framework import serializers

'''用户信息序列化'''
class UserInfoSerializer(serializers.Serializer):
    id=serializers.IntegerField()
    username=serializers.CharField()
    email= serializers.CharField()
    first_name=serializers.CharField()

'''用户序列化'''
class UserSerializer(serializers.Serializer):
    id=serializers.IntegerField()
    username=serializers.CharField()
    #email= serializers.CharField()
    first_name=serializers.CharField()

'''首页推荐序列化'''
class RecommendationSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    type = serializers.IntegerField()
    title = serializers.CharField()
    imagepath = serializers.CharField()
    url = serializers.CharField()
    userid = UserSerializer()
    createtime = serializers.CharField()

'''新闻公告序列化'''
class NewsListSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    news_type = serializers.IntegerField()
    title = serializers.CharField()
    content = serializers.CharField()
    author = serializers.CharField()
    summary = serializers.CharField()#概要
    is_wechat = serializers.BooleanField()#是否发送到微信
    is_top = serializers.BooleanField()#是否置顶
    userid = UserSerializer()
    status = serializers.IntegerField()
    createtime = serializers.CharField()

'''班级'''
class ClassInfoSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    classname = serializers.CharField()
    description = serializers.CharField()
    container = serializers.IntegerField()#班级容量
    headteacher = serializers.CharField()
    headteacher_phone = serializers.CharField()
    monitor = serializers.CharField()
    remark = serializers.CharField()
    student_counts = serializers.IntegerField()

class ClassInfoShortSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    classname = serializers.CharField()

'''学生短信息'''
class StudentsShortSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name =serializers.CharField()
    sex=serializers.IntegerField()
    birthday=serializers.DateTimeField()

'''班级学生'''
class ClassStudentSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    classinfo = ClassInfoShortSerializer()
    student = StudentsShortSerializer()
    year = serializers.IntegerField()
    joindate = serializers.DateTimeField()
    role = serializers.IntegerField()
    status = serializers.IntegerField()

'''学生信息'''
class StudentsListSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name =serializers.CharField()
    number =serializers.CharField()
    sex=serializers.IntegerField()
    birthday=serializers.DateTimeField()
    phone =serializers.CharField()
    city =serializers.CharField()#城市
    address =serializers.CharField()#地址
    guardian =serializers.CharField()#监护人
    guardian_phone =serializers.CharField()
    parents =serializers.CharField()#家长
    parents_phone =serializers.CharField()
    emergency_contact =serializers.CharField()#紧急联系人
    emergency_phone =serializers.CharField()
    qq =serializers.CharField()
    wechat =serializers.CharField()#微信
    identify =serializers.CharField()#身份证
    photo =serializers.CharField()
    activecode =serializers.CharField()#激活码
    isvalidated =serializers.IntegerField()#是否激活
    hobby =serializers.CharField()#特长、爱好
    remark =serializers.CharField()#备注，如饮食禁忌等
    classinfo = ClassStudentSerializer()

'''教师'''
class TeacherListSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    sex = serializers.IntegerField()
    birthday = serializers.DateTimeField()
    phone = serializers.CharField()
    address = serializers.CharField()#地址
    degree = serializers.IntegerField()
    educate_school = serializers.CharField()
    joindate = serializers.DateTimeField()
    city = serializers.CharField()
    teaching = serializers.CharField()
    photo = serializers.CharField()
    classinfo = ClassInfoShortSerializer()

'''班级教师'''
class ClassTeacherSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    teacher = TeacherListSerializer()
    classinfo = ClassInfoSerializer()
    role = serializers.IntegerField()
    status = serializers.IntegerField()


'''活动序列化'''
class ActivityInfoSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    activity_type = serializers.IntegerField()
    master = serializers.CharField()
    classinfo = ClassInfoSerializer()
    address = serializers.CharField()
    activity_date_start = serializers.CharField()
    activity_date_end = serializers.CharField()
    is_wechat = serializers.BooleanField()#是否发送到微信
    usercounts = serializers.IntegerField()
    description = serializers.CharField()
    createtime = serializers.CharField()

'''活动照片序列化'''
class ActivityPhotoSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    filepath = serializers.CharField()
    description = serializers.CharField()
    is_face = serializers.BooleanField(default=False)
    createtime = serializers.CharField()

'''课程序列化'''
class CourseInfoSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    course_type = serializers.IntegerField()
    title = serializers.CharField()
    description = serializers.CharField()
    teacher = serializers.CharField()
    source = serializers.CharField()#来源
    parentid = serializers.IntegerField()
    video = serializers.CharField()
    imagepath = serializers.CharField()
    viewcounts = serializers.IntegerField()
    createtime = serializers.CharField()

'''育儿宝典序列化'''
class EducationSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    description = serializers.CharField()
    author = serializers.CharField()
    source = serializers.CharField()#来源
    video = serializers.CharField()
    viewcounts = serializers.IntegerField()
    createtime = serializers.CharField()

'''预约序列化'''
class ReservationSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    student = serializers.CharField()#学生
    name = serializers.CharField()#拜访者
    role = serializers.CharField()#拜访者身份
    reserve_date = serializers.DateTimeField()#预约日期
    address = serializers.CharField()
    remark = serializers.CharField()
    reserve_others = serializers.CharField()#预约其他人
    isread = serializers.BooleanField()
    ismeet = serializers.BooleanField()
    callback = serializers.CharField()
    phone = serializers.CharField()
    createtime = serializers.CharField()

'''评论回复序列化'''
class CommentParentSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    userid = UserSerializer()

'''评论序列化'''
class CommentSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    content = serializers.CharField()
    #parentid = CommentParentSerializer()
    mod = serializers.IntegerField()#1:新闻，2:课程，3:活动
    obj_id = serializers.IntegerField()
    userid = UserSerializer()
    createtime = serializers.IntegerField()


#coding=utf-8
#date:14-11-4
__author__ = 'monica'
from django.conf.urls import patterns,include, url
from rest_framework import routers
from api_recommend import AddRecommend,GetRecommendList,DeleteRecommend
from api_news import AddNews,DeleteNews,GetNewsList,SetNewsTop
from api_class import AddClass,GetClassList,DeleteClass,GetClassStudentList,GetClassTeacherList,AddClassStudent,AddClassTeacher,DeleteClassStudent,DeleteClassTeacher,GetClassListUnJoinForTeacher,GetClassStudent,GetTeacherClass
from api_students import AddStudent,GetStudentsList,SetStudentPhoto,DeleteStudent
from api_teacher import AddTeacher,GetTeacherList,SetTeacherPhoto,DeleteTeacher
from api_activity import AddActivity,GetActivityList,DeleteActivity,AddActivityPhoto,GetActivityPhotoList,DeleteActivityPhoto,SetActivityFace
from api_attachement import FileUpload,Download,DeleteDirFile,FileActivity,FileCourse
from api_course import AddCourse,GetCourseList,DeleteCourse
from api_education import AddEducation,GetEducationList,DeleteEducation
from api_reservation import AddReservation,GetReservationList,GetReservationDetail,SetCallBack,SetReservationRead,DeleteReservation

patterns_recommend=patterns('',
    url(r'^$', GetRecommendList.as_view(),name="api-recommend-get"),
    url(r'^add/$', AddRecommend.as_view(),name="api-recommend-add"),
    url(r'^(?P<recommendid>\d+)/delete/$', DeleteRecommend.as_view(),name="api-recommend-delete"),
)

patterns_news=patterns('',
    url(r'^$', GetNewsList.as_view(),name="api-news-get"),
    url(r'^add/$', AddNews.as_view(),name="api-news-add"),
    url(r'^(?P<newsid>\d+)/set/top/$', SetNewsTop.as_view(), name="api-news-settop"),
    url(r'^(?P<newsid>\d+)/delete/$', DeleteNews.as_view(),name="api-news-delete"),
)

patterns_class=patterns('',
    url(r'^$', GetClassList.as_view(),name="api-class-get"),
    url(r'^add/$', AddClass.as_view(),name="api-class-add"),
    url(r'^(?P<classid>\d+)/delete/$', DeleteClass.as_view(),name="api-class-delete"),
    url(r'^(?P<classid>\d+)/students/$', GetClassStudentList.as_view(), name="api-class-students"),
    url(r'^(?P<classid>\d+)/student/add/$', AddClassStudent.as_view(), name="api-class-students-add"),
    url(r'^(?P<id>\d+)/student/get/$', GetClassStudent.as_view(), name="api-class-students-get"),
    url(r'^(?P<id>\d+)/student/delete/$', DeleteClassStudent.as_view(), name="api-class-students-delete"),
    url(r'^(?P<classid>\d+)/teacher/$', GetClassTeacherList.as_view(), name="api-class-teacher"),
    url(r'^(?P<classid>\d+)/teacher/add/$', AddClassTeacher.as_view(), name="api-class-teacher-add"),
    url(r'^(?P<id>\d+)/teacher/delete/$', DeleteClassTeacher.as_view(), name="api-class-teacher-delete"),
    url(r'^(?P<teacherid>\d+)/teacher/class/$', GetTeacherClass.as_view(), name="api-class-teacher-class"),
    url(r'^(?P<teacherid>\d+)/notjoin/teacher', GetClassListUnJoinForTeacher.as_view(), name="api-class-notjoin-teacher"),
)

patterns_students=patterns('',
    url(r'^$', GetStudentsList.as_view(),name="api-student-get"),
    url(r'^add/$', AddStudent.as_view(),name="api-student-add"),
    url(r'^(?P<studentid>\d+)/set/photo/$', SetStudentPhoto.as_view(), name="api-student-photo"),
    url(r'^(?P<studentid>\d+)/delete/$', DeleteStudent.as_view(),name="api-student-delete"),
)

patterns_teacher=patterns('',
    url(r'^$', GetTeacherList.as_view(),name="api-teacher-get"),
    url(r'^add/$', AddTeacher.as_view(),name="api-teacher-add"),
    url(r'^(?P<teacherid>\d+)/set/photo/$', SetTeacherPhoto.as_view(), name="api-teacher-photo"),
    url(r'^(?P<teacherid>\d+)/delete/$', DeleteTeacher.as_view(),name="api-teacher-delete"),
)

patterns_activity=patterns('',
    url(r'^$', GetActivityList.as_view(),name="api-activity-get"),
    url(r'^add/$', AddActivity.as_view(),name="api-activity-add"),
    url(r'^(?P<activityid>\d+)/photo/$', GetActivityPhotoList.as_view(), name="api-activity-photo"),
    url(r'^(?P<activityid>\d+)/photo/add/$', AddActivityPhoto.as_view(), name="api-activity-photo-add"),
    url(r'^(?P<id>\d+)/photo/delete/$', DeleteActivityPhoto.as_view(), name="api-activity-photo-delete"),
    url(r'^(?P<activityid>\d+)/delete/$', DeleteActivity.as_view(),name="api-activity-delete"),
    url(r'^(?P<id>\d+)/face/$', SetActivityFace.as_view(),name="api-activity-photo-face"),
)

patterns_attachement=patterns('',
    url(r'^$', Download.as_view(),name="api-attachement-download"),
    url(r'^add/$', FileUpload.as_view(),name="api-attachement-add"),
    url(r'^(?P<activityid>\d+)/activity/$', FileActivity.as_view(), name="api-attachement-activity"),
    url(r'^(?P<fileid>\d+)/remove/$', DeleteDirFile.as_view(), name="api-attachement-remove"),
    url(r'^(?P<activityid>\d+)/delete/$', DeleteActivity.as_view(),name="api-attachement-delete"),
)

patterns_course=patterns('',
    url(r'^$', GetCourseList.as_view(),name="api-course-get"),
    url(r'^add/$', AddCourse.as_view(),name="api-course-add"),
    url(r'^(?P<courseid>\d+)/delete/$', DeleteCourse.as_view(),name="api-course-delete"),
    url(r'^file/$', FileCourse.as_view(),name="api-course-file"),
)

patterns_education=patterns('',
    url(r'^$', GetEducationList.as_view(),name="api-education-get"),
    url(r'^add/$', AddEducation.as_view(),name="api-education-add"),
    url(r'^(?P<educationid>\d+)/delete/$', DeleteEducation.as_view(),name="api-education-delete"),
    url(r'^file/$', FileCourse.as_view(),name="api-course-file"),
)

patterns_reservation=patterns('',
    url(r'^$', GetReservationList.as_view(),name="api-reservation-get"),
    url(r'^(?P<reservationid>\d+)/detail/$', GetReservationDetail.as_view(), name="api-reservation-detail"),
    url(r'^add/$', AddReservation.as_view(),name="api-reservation-add"),
    url(r'^(?P<reservationid>\d+)/set/read/$', SetReservationRead.as_view(), name="api-reservation-read"),
    url(r'^(?P<reservationid>\d+)/set/callback/$', SetCallBack.as_view(), name="api-reservation-callback"),
    url(r'^(?P<reservationid>\d+)/delete/$', DeleteReservation.as_view(),name="api-reservation-delete"),
)

urlpatterns = patterns('',
    #首页推荐接口
    (r'^recommend/', include(patterns_recommend)),
    #新闻公告接口
    (r'^news/', include(patterns_news)),
    #班级接口
    (r'^class/', include(patterns_class)),
    #学生接口
    (r'^student/', include(patterns_students)),
    #教师接口
    (r'^teacher/', include(patterns_teacher)),
    #活动接口
    (r'^activity/', include(patterns_activity)),
    #附件接口
    (r'^attachement/', include(patterns_attachement)),
    #课程接口
    (r'^course/', include(patterns_course)),
    #育儿宝典接口
    (r'^education/', include(patterns_education)),
    #预约接口
    (r'^reservation/', include(patterns_reservation)),

)

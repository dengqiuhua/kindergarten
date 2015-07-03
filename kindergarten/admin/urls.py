#coding=utf-8
from django.conf.urls import patterns, include, url
from views import *

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'testblog.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$',NewsHome.as_view() , name='admin-index'),
    url(r'^recommend/$', RecommendHome.as_view(), name='admin-recommend'),
    url(r'^recommend/add$', RecommendAdd.as_view(), name='admin-recommend-add'),

    url(r'^news/$', NewsHome.as_view(), name='admin-news'),
    url(r'^news/add$', NewsAdd.as_view(), name='admin-news-add'),

    url(r'^class/$', ClassHome.as_view(), name='admin-class'),
    url(r'^class/add/$', ClassAdd.as_view(), name='admin-class-add'),
    url(r'^class/(?P<id>\d+)/$', ClassManage.as_view(), name='admin-class-manage'),
    url(r'^students/$', StudentsHome.as_view(), name='admin-students'),
    url(r'^students/add/$', StudentAdd.as_view(), name='admin-student-add'),
    url(r'^teacher/$', TeacherHome.as_view(), name='admin-teacher'),
    url(r'^teacher/add/$', TeacherAdd.as_view(), name='admin-teacher-add'),

    url(r'^activity/$', ActivityHome.as_view(), name='admin-activity'),
    url(r'^activity/add/$', ActivityAdd.as_view(), name='admin-activity-add'),
    url(r'^activity/photo/$', ActivityPhoto.as_view(), name='admin-activity-photo'),

    url(r'^course/$', CourseHome.as_view(), name='admin-course'),
    url(r'^course/add/$', CourseAdd.as_view(), name='admin-course-add'),

    url(r'^education/$', EducationHome.as_view(), name='admin-education'),
    url(r'^education/add/$', EducationAdd.as_view(), name='admin-education-add'),

    url(r'^user/$', UserHome.as_view(), name='admin-user'),
    url(r'^user/add/$', UserAdd.as_view(), name='admin-user-add'),

    url(r'^yuyue/$', ReservationHome.as_view(), name='admin-reservation'),

    #url(r'^(?P<id>\d+)$', BlogDetail.as_view(), name='blog-detail'),

)
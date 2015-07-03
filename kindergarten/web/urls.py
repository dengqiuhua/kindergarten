#coding=utf-8
#date:14-11-10
__author__ = 'monica'
from django.conf.urls import patterns,include, url
from views import *

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'testblog.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$',Index.as_view() , name='web-index'),
    url(r'^news/$', NewsList.as_view(), name='web-news'),
    url(r'^news/(?P<id>\d+)/$', NewsDetail.as_view(), name='web-news-detail'),
    url(r'^hd/$', ActivityList.as_view(), name='web-activity'),
    url(r'^hd/(?P<id>\d+)/$', ActivityDetail.as_view(), name='web-activity-detail'),
    url(r'^kc/$', CourseList.as_view(), name='web-course'),
    url(r'^kc/(?P<id>\d+)/$', CourseDetail.as_view(), name='web-course-detail'),
    url(r'^edu/$', EducationList.as_view(), name='web-education'),
    url(r'^edu/(?P<id>\d+)/$', EducationDetail.as_view(), name='web-education-detail'),
    url(r'^bj/$', ClassList.as_view(), name='web-class'),
    url(r'^bj/(?P<id>\d+)/$', ClassList.as_view(), name='web-class-detail'),
    url(r'^yuyue/$', ReservationAdd.as_view(), name='web-reservation'),
    url(r'^yuyue/(?P<id>\d+)/$', ReservationAdd.as_view(), name='web-reservation-detail'),
    url(r'^about/$', AboutUs.as_view(), name='web-about'),
    url(r'^files/$', Download.as_view(), name='web-file-download'),
    url(r'^login/$',Login.as_view() , name='web-login'),
    url(r'^logout/$',Logout.as_view() , name='web-logout'),
)

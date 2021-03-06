#coding=utf-8
#date:14-11-7
__author__ = 'monica'

from rest_framework.views import APIView
from kindergarten.models import User,CourseInfo,CommentInfo
from kindergarten.script.util import Util
from model_serializer import CourseInfoSerializer,CommentSerializer
from kindergarten.script.func import Func
import time
func=Func()

'''获取列表'''
class GetCourseList(APIView):
    def get(self, request, **kwargs):
        #分页
        pagesize, pageindex = Util.getPageSizeAndIndex(self.request)
        args={}
        #查询条件
        if 'title' in request.GET and request.GET['title']:
            args['title__contains'] = request.GET['title'].strip()
        datalist , counts = func.GetCourseList(pagesize, pageindex,**args)
        data=CourseInfoSerializer(datalist).data
        return Util.GetResponseData(True,0,data,counts)

'''添加/修改'''
class AddCourse(APIView):
    def post(self, request, **kwargs):
        if 'title' in request.POST and request.POST['title']:
            title=request.POST['title'].strip()
            #如果有id，则修改
            if 'id' in request.POST and request.POST['id']:
                newid=request.POST['id']
                try:
                    course=CourseInfo.objects.get(id=newid)
                except CourseInfo.DoesNotExist:
                    return Util.GetResponseData(False,710)
                course.title = title
                course.modifytime = time.time()
            else:
                #新建
                course=CourseInfo.objects.create(title=title,userid=request.user.id)
            if 'teacher' in request.POST:
                course.teacher= request.POST['teacher'].strip()
            if 'description' in request.POST:
                course.description = request.POST['description'].strip()
            if 'source' in request.POST:
                course.source = request.POST['source'].strip()
            if 'video' in request.POST:
                course.video = request.POST['video'].strip()
            #视频
            if 'fileid' in request.POST and request.POST['fileid']:
                fileid = request.POST['fileid'].strip()
                if fileid in request.session and request.session[fileid]:
                    fileinfo=request.session[fileid]
                    course.video = fileinfo["filepath"]
            #封面
            if 'imageid' in request.POST and request.POST['imageid']:
                imageid = request.POST['imageid'].strip()
                if imageid in request.session and request.session[imageid]:
                    fileinfo=request.session[imageid]
                    course.imagepath = fileinfo["filepath"]
            course.save()
            return Util.GetResponseData(True,0,course.id)
        else:
            return Util.GetResponseData(False,-3)

'''删除'''
class DeleteCourse(APIView):
    def post(self, request, **kwargs):
        if 'courseid' in kwargs and kwargs['courseid']:
            courseid=kwargs['courseid']
            try:
                course=CourseInfo.objects.get(id=courseid)
            except CourseInfo.DoesNotExist:
                return Util.GetResponseData(False,710)
            course.delete()
            return Util.GetResponseData(True,0)
        else:
            return Util.GetResponseData(False,-3)

'''评论'''
class CourseComment(APIView):
    def post(self, request, **kwargs):
        if 'content' in request.POST and request.POST['content'] and 'courseid' in kwargs and kwargs['courseid']:
            content = Util.GetFilterString(request.POST['content'])
            courseid = kwargs['courseid']
            user = User()
            if request.user and request.user.is_authenticated():
                user = request.user
            #1:新闻，2:课程，3:活动
            comment = CommentInfo.objects.create(content=content,userid=user,mod=2,obj_id=courseid)
            return Util.GetResponseData(True,0,comment.id)
        return Util.GetResponseData(False,-3)
    def get(self, request, **kwargs):
        if 'courseid' in kwargs and kwargs['courseid']:
            courseid = kwargs['courseid']
            #分页
            pagesize, pageindex = Util.getPageSizeAndIndex(request)
            args={}
            args['mod'] = 2
            args['obj_id'] = courseid
            #查询条件
            if 'content' in request.GET and request.GET['content']:
                args['content__contains'] = request.GET['content'].strip()
            datalist,counts = func.GetCommentPageList(pagesize, pageindex,**args)
            data=CommentSerializer(datalist).data
            return Util.GetResponseData(True,0,data,counts)
        return Util.GetResponseData(False,-3)


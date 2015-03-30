#coding=utf-8
#date:14-11-4
__author__ = 'monica'

from rest_framework.views import APIView
from kindergarten.models import User,NewsInfo
from django.http import HttpResponse
from kindergarten.script.util import Util
from model_serializer import NewsListSerializer
from kindergarten.script.func import Func
import time
func=Func()

'''获取列表'''
class GetNewsList(APIView):
    def get(self, request, **kwargs):
        #分页
        pagesize, pageindex = Util.getPageSizeAndIndex(request)
        args={}
        #查询条件
        if 'title' in request.GET and request.GET['title']:
            args['title__contains'] = request.GET['title'].strip()
        datalist , counts = func.GetNewsPageList(pagesize, pageindex,**args)
        data=NewsListSerializer(datalist).data
        return Util.GetResponseData(True,0,data,counts)

'''添加/修改'''
class AddNews(APIView):
    def post(self, request, **kwargs):
        if 'title' in request.POST and request.POST['title']:
            title=request.POST['title'].strip()
            #如果有id，则修改
            if 'id' in request.POST and request.POST['id']:
                newid=request.POST['id']
                try:
                    news=NewsInfo.objects.get(id=newid)
                except NewsInfo.DoesNotExist:
                    return Util.GetResponseData(False,210)
                news.title = title
                news.modifytime = time.time()
            else:
                #新建
                news=NewsInfo.objects.create(title=title)
            if 'author' in request.POST:
                news.author= request.POST['author'].strip()
            if 'content' in request.POST:
                news.content = request.POST['content'].strip()
            if 'news_type' in request.POST:
                news.news_type = request.POST['news_type'].strip()
            news.save()
            return Util.GetResponseData(True,0,news.id)
        else:
            return Util.GetResponseData(False,-3)

'''置顶/取消置顶'''
class SetNewsTop(APIView):
    def post(self, request, **kwargs):
        if 'newsid' in kwargs and kwargs['newsid']:
            newsid = kwargs['newsid']
            try:
                news = NewsInfo.objects.get(id=newsid)
            except NewsInfo.DoesNotExist:
                return Util.GetResponseData(False,210)
            istop=True
            if 'istop' in request.POST and request.POST['istop'] and request.POST['istop']=='false':
                istop=False
            news.setTop(istop)
            return Util.GetResponseData(True)
        return Util.GetResponseData(False,-3)

'''删除'''
class DeleteNews(APIView):
    def post(self, request, **kwargs):
        if 'newsid' in kwargs and kwargs['newsid']:
            newsid=kwargs['newsid']
            try:
                news=NewsInfo.objects.get(id=newsid)
            except NewsInfo.DoesNotExist:
                return Util.GetResponseData(False,210)
            news.delete()
            return Util.GetResponseData(True)
        else:
            return Util.GetResponseData(False,-3)

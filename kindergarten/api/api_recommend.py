#coding=utf-8
#date:14-11-4
__author__ = 'monica'

from rest_framework.views import APIView
from kindergarten.models import User,Recommendation
from kindergarten.script.util import Util
from model_serializer import RecommendationSerializer
from kindergarten.script.func import Func
import time
func=Func()

'''获取列表'''
class GetRecommendList(APIView):
    def get(self, request, **kwargs):
        #分页
        pagesize, pageindex = Util.getPageSizeAndIndex(request)
        args={}
        #查询条件
        if 'title' in request.GET and request.GET['title']:
            args['title__contains'] = request.GET['title'].strip()
        datalist , counts = func.GetRecommendList(pagesize, pageindex,**args)
        data=RecommendationSerializer(datalist).data
        return Util.GetResponseData(True,0,data,counts)

'''添加/修改'''
class AddRecommend(APIView):
    def post(self, request, **kwargs):
        if 'title' in request.POST and request.POST['title']:
            title=request.POST['title'].strip()
            #如果有id，则修改
            if 'id' in request.POST and request.POST['id']:
                recommendid=request.POST['id']
                try:
                    recommend=Recommendation.objects.get(id=recommendid)
                except Recommendation.DoesNotExist:
                    return Util.GetResponseData(False,210)
                recommend.title = title
            else:
                #新建
                recommend=Recommendation.objects.create(title=title,userid=request.user.id,createtime=time.time())
            if 'type' in request.POST and request.POST['type']:
                recommend.type = request.POST['type'].strip()
            if 'url' in request.POST:
                recommend.url= request.POST['url'].strip()
            #图片
            if 'fileid' in request.POST and request.POST['fileid']:
                fileid = request.POST['fileid'].strip()
                if fileid in request.session and request.session[fileid]:
                    fileinfo=request.session[fileid]
                    recommend.imagepath = fileinfo["filepath"]

            recommend.save()
            return Util.GetResponseData(True,0,recommend.id)
        else:
            return Util.GetResponseData(False,-3)

'''删除'''
class DeleteRecommend(APIView):
    def post(self, request, **kwargs):
        if 'recommendid' in kwargs and kwargs['recommendid']:
            recommendid=kwargs['recommendid']
            try:
                recommend=Recommendation.objects.get(id=recommendid)
            except Recommendation.DoesNotExist:
                return Util.GetResponseData(False,210)
            recommend.delete()
            return Util.GetResponseData(True)
        else:
            return Util.GetResponseData(False,-3)

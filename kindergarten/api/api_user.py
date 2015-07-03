#coding=utf-8
#date:15-7-3
__author__ = 'monica'

from rest_framework.views import APIView
from kindergarten.models import User
from kindergarten.script.util import Util
from model_serializer import UserInfoSerializer
from kindergarten.script.func import Func
import time
from django.contrib.auth import authenticate
func=Func()

'''获取列表'''
class GetUserList(APIView):
    def get(self, request, **kwargs):
        #分页
        pagesize, pageindex = Util.getPageSizeAndIndex(request)
        args={}
        #查询条件
        if 'name' in request.GET and request.GET['name']:
            args['first_name__contains'] = request.GET['name'].strip()
        if not request.user.is_superuser:
            args['is_superuser'] = False
        datalist , counts = func.GetUserList(pagesize, pageindex,**args)
        data=UserInfoSerializer(datalist).data
        return Util.GetResponseData(True,0,data,counts)

'''注册'''


class Register(APIView):
    def post(self, request, *args, **kwargs):
        if 'username' in request.POST and request.POST['username'].strip() and 'password' in request.POST and \
                request.POST['password'].strip() and 'name' in request.POST and request.POST['name'].strip():
            username = Util.GetFilterString(request.POST['username'].strip()).replace(" ", "")
            password = Util.GetFilterString(request.POST['password'].strip())
            name = request.POST['name'].strip().replace(" ", "")

            if User.objects.filter(username=username).count()>0:
                return Util.GetResponseData(False, 115)
            user = User.objects.create_user(username=username, password=password)
            user.first_name = name
            user.is_staff = True  # 个人
            # 邮箱
            if 'email' in request.POST and request.POST["email"]:
                user.email= request.POST['email'].strip()
            user.save()
            profile = UserInfoSerializer(user).data
            return Util.GetResponseData(True, 0, profile)
        return Util.GetResponseData(False, -3)

'''获取一条用户信息'''
class GetUserInfo(APIView):
    def get(self, request, **kwargs):
        if 'userid' in kwargs and kwargs['userid']:
            userid = kwargs['userid']
            try:
                user = User.objects.get(id=userid)
            except User.DoesNotExist:
                return Util.GetResponseData(False, 110)
            profile = UserInfoSerializer(user).data
            return Util.GetResponseData(True, 0, profile)
        return Util.GetResponseData(False,-3)

'''修改'''
class UpdateUser(APIView):
    def post(self, request, **kwargs):
        if 'userid' in kwargs and kwargs['userid']:
            userid = kwargs['userid']
            try:
                user = User.objects.get(id=userid)
            except User.DoesNotExist:
                return Util.GetResponseData(False, 110)
            if 'first_name' in request.POST and request.POST["first_name"]:
                user.first_name= request.POST['first_name'].strip()
            if 'email' in request.POST and request.POST["email"]:
                user.email= request.POST['email'].strip()
            user.save()
            return Util.GetResponseData(True,0,user.id)
        else:
            return Util.GetResponseData(False,-3)

'''修改密码'''


class ChangePassword(APIView):
    def post(self, request, *args, **kwargs):
        if 'userid' in kwargs and kwargs['userid'] and 'password' in request.POST and request.POST['password']:
            userid = kwargs['userid']
            password = request.POST['password'].strip()
            try:
                user = User.objects.get(id=userid)
            except User.DoesNotExist:
                return Util.GetResponseData(False, 110)
            user.set_password(password)
            user.save()
            return Util.GetResponseData(True)
        return Util.GetResponseData(False, -3)

'''删除'''
class DeleteUser(APIView):
    def post(self, request, **kwargs):
        if 'userid' in kwargs and kwargs['userid']:
            userid=kwargs['userid']
            try:
                user=User.objects.get(id=userid)
            except User.DoesNotExist:
                return Util.GetResponseData(False,210)
            user.delete()
            return Util.GetResponseData(True)
        else:
            return Util.GetResponseData(False,-3)

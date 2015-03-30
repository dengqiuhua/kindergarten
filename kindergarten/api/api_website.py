__author__ = 'Administrator'
# coding=utf-8
from rest_framework.views import APIView
from rest_framework import viewsets,generics
from cava.common.util import Util
from cava.models import ProvinceArea,User
from django.http import HttpResponse
from cava.function.class_website import WebSite
cla_website=WebSite()

from cava.apps.captcha.models import CaptchaStore
from cava.apps.captcha.helpers import captcha_image_url
import json
from django import forms
from cava.apps.captcha.fields import CaptchaField#验证码

'''获取省市区'''
class GetProvinceArea(generics.ListAPIView):
    model = ProvinceArea
    #serializer_class = PlanSerializer
    def get_queryset(self):
        parentcode = 0 if self.request.QUERY_PARAMS.get('parentcode') ==None else self.request.QUERY_PARAMS.get('parentcode')
        return cla_website.GetProvinceAreaByParent(parentcode)

'''获取随机验证码以及判断验证码的正确性'''
class GetRandCode(APIView):
    template_name = ''
    def get(self, request, **kwargs):
        to_json_responce = dict()
        to_json_responce['status'] = 1
        to_json_responce['new_code_key'] = CaptchaStore.generate_key()
        to_json_responce['new_code_image'] = captcha_image_url(to_json_responce['new_code_key'])
        return HttpResponse(json.dumps(to_json_responce), content_type='application/json')
    def post(self, request, **kwargs):
        if 'captcha_1' in request.POST and request.POST['captcha_1'] != "":
            form = CaptchaTestForm(request.POST)
            if form.is_valid():
                return HttpResponse(True)
        return HttpResponse(False)

'''验证码表单'''
class CaptchaTestForm(forms.Form):
    captcha = CaptchaField()

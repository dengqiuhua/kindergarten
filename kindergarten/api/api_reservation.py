#coding=utf-8
#date:14-11-7
__author__ = 'monica'

from rest_framework.views import APIView
from kindergarten.models import User,Reservation
from django.http import HttpResponse
from kindergarten.script.util import Util
from model_serializer import ReservationSerializer
from kindergarten.script.func import Func
import time
func=Func()

'''获取列表'''
class GetReservationList(APIView):
    def get(self, request, **kwargs):
        #分页
        pagesize, pageindex = Util.getPageSizeAndIndex(request)
        args={}
        #查询条件
        if 'title' in request.GET and request.GET['title']:
            args['title__contains'] = request.GET['title'].strip()
        datalist , counts = func.GetReservationPageList(pagesize, pageindex,**args)
        data=ReservationSerializer(datalist).data
        return Util.GetResponseData(True,0,data,counts)

'''获取详细'''
class GetReservationDetail(APIView):
    def get(self, request, **kwargs):
        if 'reservationid' in kwargs and kwargs['reservationid']:
            reservationid = kwargs['reservationid']
            try:
                reservation = Reservation.objects.get(id=reservationid)
            except Reservation.DoesNotExist:
                return Util.GetResponseData(False,810)
            data=ReservationSerializer(reservation).data
            return Util.GetResponseData(True,0,data,1)
        return Util.GetResponseData(False,-3)

'''添加/修改'''
class AddReservation(APIView):
    def post(self, request, **kwargs):
        if 'title' in request.POST and request.POST['title']:
            title=request.POST['title'].strip()
            #如果有id，则修改
            if 'id' in request.POST and request.POST['id']:
                reservationid=request.POST['id']
                try:
                    reservation=Reservation.objects.get(id=reservationid)
                except Reservation.DoesNotExist:
                    return Util.GetResponseData(False,810)
                reservation.title = title
                reservation.modifytime = time.time()
            else:
                #新建
                reservation=Reservation.objects.create(title=title)
            if 'student' in request.POST:
                reservation.student= request.POST['student'].strip()
            if 'name' in request.POST:
                reservation.name = request.POST['name'].strip()
            if 'role' in request.POST:
                reservation.role = request.POST['role'].strip()
            if 'reserve_date' in request.POST:
                reservation.reserve_date = request.POST['reserve_date'].strip()
            if 'address' in request.POST:
                reservation.address = request.POST['address'].strip()
            if 'remark' in request.POST:
                reservation.remark = request.POST['remark'].strip()
            if 'reserve_others' in request.POST:
                reservation.reserve_others = request.POST['reserve_others'].strip()
            if 'phone' in request.POST:
                reservation.phone = request.POST['phone'].strip()
            reservation.save()
            return Util.GetResponseData(True,0,reservation.id)
        else:
            return Util.GetResponseData(False,-3)

'''已读'''
class SetReservationRead(APIView):
    def post(self, request, **kwargs):
        if 'reservationid' in kwargs and kwargs['reservationid']:
            reservationid = kwargs['reservationid']
            try:
                reservation = Reservation.objects.get(id=reservationid)
            except Reservation.DoesNotExist:
                return Util.GetResponseData(False,810)
            reservation.read()
            return Util.GetResponseData(True)
        return Util.GetResponseData(False,-3)

'''反馈'''
class SetCallBack(APIView):
    def post(self, request, **kwargs):
        if 'reservationid' in kwargs and kwargs['reservationid']:
            reservationid = kwargs['reservationid']
            try:
                reservation = Reservation.objects.get(id=reservationid)
            except Reservation.DoesNotExist:
                return Util.GetResponseData(False,810)
            ismeet = True
            if 'ismeet' in request.POST and request.POST['ismeet'] and request.POST['ismeet'] == 'false':
                ismeet = False
            callback=""
            if 'callback' in request.POST and request.POST['callback']:
                callback = request.POST['callback']
            reservation.set_meet(ismeet,callback)
            return Util.GetResponseData(True)
        return Util.GetResponseData(False,-3)

'''删除'''
class DeleteReservation(APIView):
    def post(self, request, **kwargs):
        if 'reservationid' in kwargs and kwargs['reservationid']:
            reservationid=kwargs['reservationid']
            try:
                reservation=Reservation.objects.get(id=reservationid)
            except Reservation.DoesNotExist:
                return Util.GetResponseData(False,810)
            reservation.delete()
            return Util.GetResponseData(True)
        else:
            return Util.GetResponseData(False,-3)
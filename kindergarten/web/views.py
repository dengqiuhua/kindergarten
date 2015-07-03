#coding=utf-8
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView
from django.conf import settings
import os,time
from kindergarten.script.util import Util
from kindergarten.models import Recommendation,NewsInfo,User,ClassInfo,StudentInfo,TeacherInfo,ActivityInfo,ActivityPhoto,CourseInfo,ClassTeachers,EducationCare,Reservation,CommentInfo
from kindergarten.script.func import Func
func=Func()

'''首页'''
class Index(TemplateView):
    def get(self, request, *args, **kwargs):
        context={}
        context["topnav"]=1
        #推荐
        typelist = ["","新闻资讯","活动","课程"];
        recommendationlist = Recommendation.objects.filter().order_by("-createtime")[0:5]
        if recommendationlist:
            recommendlist_new = []
            index = 0
            for recommend in recommendationlist:
                recommend.index = index
                recommend.type = typelist[recommend.type]
                if recommend.imagepath:
                    recommend.imagepath = Util.getFileUrl(recommend.imagepath)
                recommendlist_new.append(recommend)
                index = index + 1
            context["recommendationlist"] = recommendlist_new
        #公告
        context["noticelist"] = NewsInfo.objects.filter(news_type=1).order_by("-createtime")[0:2]
        #新闻
        context["newslist"] = NewsInfo.objects.filter(news_type=0).order_by("-createtime")[0:10]
        #活动
        activitylist = ActivityInfo.objects.filter().order_by("-createtime")[0:6]
        if activitylist:
            activitylist_new = []
            for activity in activitylist:
                if activity.activeImage:
                    activity.Image = Util.getFileUrl(activity.activeImage)
                else:
                    activity.Image = "/static/img/banner/noimg_active.png"
                activitylist_new.append(activity)
        context["activitylist"] = activitylist
        #课程
        courselist = CourseInfo.objects.filter().order_by("-createtime")[0:6]
        if courselist:
            courselist_new = []
            for course in courselist:
                if course.imagepath:
                    course.imagepath = Util.getFileUrl(course.imagepath)
                else:
                    course.imagepath = "/static/img/banner/noimg_course.png"
                courselist_new.append(course)
        context["courselist"] = courselist
        #育儿宝典
        context["educationlist"] = EducationCare.objects.filter().order_by("-createtime")[0:8]
        #班级
        context["classlist"] = ClassInfo.objects.all()

        return render_to_response("index.html",context,context_instance=RequestContext(request))

'''新闻公告'''
class NewsList(TemplateView):
    def get(self, request, *args, **kwargs):
        context = {}
        context["topnav"] = 2
        pageindex,pagesize = Util.InitPagenation(request)
        #新闻
        newslist = NewsInfo.objects.filter().order_by("-createtime")[(pageindex - 1) * pagesize:pagesize * pageindex]
        if newslist:
            newslist_new = []
            for news in newslist:
                news.createtime = Util.timeFormat(news.createtime,True)
                newslist_new.append(news)
            context["newslist"] = newslist_new
        counts = NewsInfo.objects.filter().count()
        context["pagenationHtml"] = Util.GetPagenation(request,counts,pagesize)
        return render_to_response("web-news.html", context, context_instance=RequestContext(request))

'''新闻公告详细页'''
class NewsDetail(TemplateView):
    def get(self, request, *args, **kwargs):
        context = {}
        context["topnav"] = 2
        #新闻
        if 'id' in kwargs and kwargs['id']:
            newsid = int(kwargs['id'])
            try:
                news = NewsInfo.objects.get(id=newsid)
            except NewsInfo.DoesNotExist:
                return HttpResponseRedirect(reverse('web-news'))
            news.createtime = Util.timeFormat(news.createtime,True)
            context["news"] = news
            #新闻
            context["newslist"] = NewsInfo.objects.filter().order_by("-createtime")[0:10]
        return render_to_response("web-news-detail.html", context, context_instance=RequestContext(request))

'''活动列表'''
class ActivityList(TemplateView):
    def get(self, request, *args, **kwargs):
        context = {}
        context["topnav"] = 3
        pageindex,pagesize = Util.InitPagenation(request)
        #活动
        activitylist = ActivityInfo.objects.filter().order_by("-createtime")[(pageindex - 1) * pagesize:pagesize * pageindex]
        counts = ActivityInfo.objects.filter().count()
        if activitylist:
            activitylist_new = []
            for activity in activitylist:
                if activity.activeImage:
                    activity.Image = Util.getFileUrl(activity.activeImage)
                else:
                    activity.Image = "/static/img/banner/noimg_active.png"
                activitylist_new.append(activity)
        context["activitylist"] = activitylist
        context["pagenationHtml"] = Util.GetPagenation(request,counts,pagesize)
        return render_to_response("web-activity.html", context, context_instance=RequestContext(request))

'''活动详细页'''
class ActivityDetail(TemplateView):
    def get(self, request, *args, **kwargs):
        context = {}
        context["topnav"] = 3
        activity_types=["","全体活动","班级活动","其他活动"];
        #活动
        if 'id' in kwargs and kwargs['id']:
            activityid = int(kwargs['id'])
            try:
                activity = ActivityInfo.objects.get(id=activityid)
            except ActivityInfo.DoesNotExist:
                return HttpResponseRedirect(reverse('web-activity'))
            activity.activity_type = activity_types[activity.activity_type]
            context["activity"] = activity
            where={'activity':activity}
            activityphoto = ActivityPhoto.objects.filter(activity=activity)
            photocounts = activityphoto.count()

            if activityphoto:
                photolist = []
                index = 0
                for photo in activityphoto:
                    photo.filepath = Util.getFileUrl( photo.filepath)
                    photo.index = index
                    index = index+1
                    photolist.append(photo)
                context["photocounts"] = range(0,photocounts)
                context["activityphoto"] = photolist
            #活动
            activitylist = ActivityInfo.objects.filter().order_by("-createtime")[0:6]
            if activitylist:
                activitylist_new = []
                for activity in activitylist:
                    if activity.activeImage:
                        activity.Image = Util.getFileUrl( activity.activeImage)
                    else:
                        activity.Image = "/static/img/banner/noimg_active.png"
                    activitylist_new.append(activity)
            context["activitylist"] = activitylist
        return render_to_response("web-activity-detail.html", context, context_instance=RequestContext(request))

'''班级'''
class ClassList(TemplateView):
    def get(self, request, *args, **kwargs):
        context = {}
        context["topnav"] = 4
        classinfo=teacher={}
        sex = ["--","男","女"]
        degree = ["","小学","初中","高级中学","中专","高职","大专","本科","硕士研究生","博士研究生","海外留学生","其他"]
        #班级列表
        classlist= ClassInfo.objects.all()
        if 'id' in kwargs and kwargs['id']:
            classid = int(kwargs['id'])
            try:
                classinfo = ClassInfo.objects.get(id=classid)
            except ClassInfo.DoesNotExist:
                return HttpResponseRedirect(reverse('web-class'))
        elif classlist:
            classinfo=classlist[0]
        if classinfo:
            #班级活动
            activitylist = ActivityInfo.objects.filter(classinfo=classinfo).order_by("-createtime")[0:6]
            if activitylist:
                activitylist_new = []
                for activity in activitylist:
                    if activity.activeImage:
                        activity.Image = Util.getFileUrl(activity.activeImage)
                    else:
                        activity.Image = "/static/img/banner/noimg_active.png"
                    activitylist_new.append(activity)
            context["activitylist"] = activitylist
            #班级教师
            class_teacher = TeacherInfo.objects.filter(id__in=ClassTeachers.objects.filter(classinfo=classinfo).values('teacher'))
            if class_teacher:
                teacher_new = []
                for teacher in class_teacher:
                    teacher.sex = sex[teacher.sex]
                    teacher.degree = degree[teacher.degree]
                    teacher.photo = Util.getFileUrl( teacher.photo)
                    teacher_new.append(teacher)
                context["class_teacher"] = teacher_new
        context["classlist"] = classlist
        context["classinfo"]=classinfo
        return render_to_response("web-class.html", context, context_instance=RequestContext(request))

'''课程'''
class CourseList(TemplateView):
    def get(self, request, *args, **kwargs):
        context = {}
        context["topnav"] = 5
        pageindex,pagesize = Util.InitPagenation(request)
        #课程
        courselist = CourseInfo.objects.filter().order_by("-createtime")[(pageindex - 1) * pagesize:pagesize * pageindex]
        counts = CourseInfo.objects.filter().count()
        if courselist:
            courselist_new = []
            for course in courselist:
                if course.imagepath:
                    course.imagepath = Util.getFileUrl(course.imagepath)
                else:
                    course.imagepath = "/static/img/banner/noimg_course.png"
                courselist_new.append(course)
        context["courselist"] = courselist
        context["pagenationHtml"] = Util.GetPagenation(request,counts,pagesize)
        return render_to_response("web-course.html", context, context_instance=RequestContext(request))

'''课程详细页'''
class CourseDetail(TemplateView):
    def get(self, request, *args, **kwargs):
        context = {}
        context["topnav"] = 5
        #课程
        if 'id' in kwargs and kwargs['id']:
            courseid = int(kwargs['id'])
            try:
                course = CourseInfo.objects.get(id=courseid)
            except CourseInfo.DoesNotExist:
                return HttpResponseRedirect(reverse('web-course'))
            #阅读数＋1
            course.viewcounts = course.viewcounts + 1
            course.save()
            #图片
            if course.imagepath:
                course.imagepath = Util.getFileUrl(course.imagepath)
            #视频
            if course.video :
                course.video = Util.getFileUrl(course.video)
            course.createtime = Util.timeFormat(course.createtime,True)
            context["course"] = course
            context["commentObjId"] = course.id
            #评论数,#1:新闻，2:课程，3:活动
            context["commentCounts"] = CommentInfo.objects.filter(mod=2,obj_id=course.id).count()
            #课程
            context["courselist"] = CourseInfo.objects.filter().order_by("-viewcounts")[0:10]
        return render_to_response("web-course-detail.html", context, context_instance=RequestContext(request))

'''育儿宝典'''
class EducationList(TemplateView):
    def get(self, request, *args, **kwargs):
        context = {}
        context["topnav"] = 6
        pageindex,pagesize = Util.InitPagenation(request)
        #育儿宝典
        context["educationlist"] = EducationCare.objects.filter().order_by("-createtime")[(pageindex - 1) * pagesize:pagesize * pageindex]
        counts = EducationCare.objects.filter().count()
        context["pagenationHtml"] = Util.GetPagenation(request,counts,pagesize)
        return render_to_response("web-education.html", context, context_instance=RequestContext(request))

'''育儿宝典详细页'''
class EducationDetail(TemplateView):
    def get(self, request, *args, **kwargs):
        context = {}
        context["topnav"] = 6
        #育儿宝典id
        if 'id' in kwargs and kwargs['id']:
            educationid = int(kwargs['id'])
            try:
                education = EducationCare.objects.get(id=educationid)
            except EducationCare.DoesNotExist:
                return HttpResponseRedirect(reverse('web-education'))
            #阅读数＋1
            education.viewcounts = education.viewcounts + 1
            education.save()

            #视频
            if education.video :
                education.video = Util.getFileUrl( education.video)
            education.createtime = Util.timeFormat(education.createtime,True)
            context["education"] = education
            #育儿宝典
            context["educationlist"] = EducationCare.objects.filter().order_by("-viewcounts")[0:10]
        return render_to_response("web-education-detail.html", context, context_instance=RequestContext(request))

'''预约添加页'''
class ReservationAdd(TemplateView):
    def get(self, request, *args, **kwargs):
        context = {}
        context["topnav"] = 1

        if "id" in kwargs and kwargs["id"]:
            id = kwargs["id"]
            try:
                reservation = Reservation.objects.get(id=id)
            except Reservation.DoesNotExist:
                return HttpResponseRedirect(reverse("web-reservation"))
            #两分钟内可见
            if reservation.createtime < (time.time()-2*60):
                return HttpResponseRedirect(reverse("web-reservation"))
            context["reservation"] = reservation

        return render_to_response("web-reservation.html", context, context_instance=RequestContext(request))
    def post(self, request, *args, **kwargs):
        context = {}
        if request.POST["student"] and request.POST["name"] and request.POST["role"] and request.POST["reserve_date"] :

            student = Util.GetFilterString(request.POST["student"])
            name = Util.GetFilterString(request.POST["name"])
            role = Util.GetFilterString(request.POST["role"])
            reserve_date = Util.GetFilterString(request.POST["reserve_date"])
            phone = Util.GetFilterString(request.POST["phone"])
            address = Util.GetFilterString(request.POST["address"])
            remark = Util.GetFilterString(request.POST["remark"])
            reservation = Reservation.objects.create(student=student,name=name,role=role,reserve_date=reserve_date,phone=phone,address=address,remark=remark,createtime=time.time())
            reservationid = str(reservation.id)
            return HttpResponseRedirect(reverse("web-reservation-detail",args=(reservationid)))
        return render_to_response("web-reservation.html", context, context_instance=RequestContext(request))


'''关于我们【学园介绍】'''
class AboutUs(TemplateView):
    def get(self, request, *args, **kwargs):
        context = {}
        context["mod"] = 1
        #联系我们
        if "lx" in request.GET:
            context["mod"] = 2
        context["topnav"] = 7
        return render_to_response("web-about.html", context, context_instance=RequestContext(request))

'''文件下载'''
class Download(TemplateView):
    def get(self, request, *args, **kwargs):
        if 'filepath' in request.GET and request.GET['filepath']!="":
            filepath = request.GET['filepath']

            #中文解码
            if 'filename' in request.GET and request.GET['filename']!="":
                filename=request.GET['filename'].replace('%u', '\\u').encode('utf-8')
            else:
                filename=filepath.split("/")[-1]
            path = settings.SITEROOT + filepath#附件全路径
            #path = path.replace('/', '\\')#转换为物理路径
            if os.path.isfile(path):
                f = open(path, 'rb')
                data = f.read()
                f.close()
                ext = filename[filename.rfind('.'):]
                if ext == ".mp4":
                    response = HttpResponse(data, mimetype='video/mp4')
                elif ext == ".flv":
                    response = HttpResponse(data, mimetype='video/flv')
                else:
                    response = HttpResponse(data, mimetype='application/octet-stream')
                #response = HttpResponse(data, mimetype='application/octet-stream')
                response['Content-Disposition'] = 'attachment; filename=%s' % filename
                return response
        return HttpResponse(path)

'''登录'''
class Login(TemplateView):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse('admin-index'))
        context = {}
        context['topnav'] = 1
        #context['form'] =form
        context['username']=""
        if 'username' in request.COOKIES:
            context['username'] =request.COOKIES.get('username','')
        if 'username' in request.GET:
            context['username'] = request.GET['username']
        if 'status' in request.GET:
            context['status'] = request.GET['status']
        if 'type' in request.GET:
            context['type'] = request.GET['type']
        #context["topnav"] = 5

        return render_to_response("web-login.html", context, context_instance=RequestContext(request))
    def post(self, request, *args, **kwargs):
        if 'username' in request.POST and 'password' in request.POST:
            username=request.POST['username']
            password = request.POST['password']
            context={}
            #跳转链接
            url_next = reverse('admin-index')
            if 'next' in request.GET:
                url_next = request.GET['next']
            flag=True
            type_error=''
            if username=="" or password =="":
                flag = False
                type_error='empty'
            #验证码

            #验证失败
            if not flag:
                #form = CaptchaTestForm()
                #context['form'] = form
                context["username"]=username
                context["password"] = password
                context['status'] = "fail"
                context['type'] = type_error
                return render_to_response('web-login.html', context, context_instance=RequestContext(request))
            user = authenticate(username=username, password=password)
            if user:
                if not user.is_active:
                    #context['form'] = form
                    context["username"] = username
                    context['status'] = "fail"
                    context['type'] = "un_active"
                    return render_to_response('web-login.html', context, context_instance=RequestContext(request))
                login(request,user)
                #获取用户的机构
                #request.session['orgid']=Util.GetUserOrg(user)
                request.session.set_expiry(0)#过期时间，关闭浏览器
                response= HttpResponseRedirect(url_next)
                response.set_cookie('username', username, 3600*24*7)
                return response
            else:
                #return HttpResponseRedirect('/login/?status=fail&username='+username+'&type=invilid')
                url=reverse('web-login')+'?status=fail&username=%s&type=invilid&next=%s' % (username,url_next)
                return HttpResponseRedirect(url)
        return HttpResponseRedirect(reverse('web-login'))

'''退出'''
class Logout(TemplateView):
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse('web-login'))
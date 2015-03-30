__author__ = 'Administrator'
# coding=utf-8
#from django.contrib.auth import authenticate
from django.http import HttpResponse
from rest_framework.response import Response
#from DjangoVerifyCode import Code
from django.core.cache import cache
import time,datetime,calendar,os,pickle,re,random,uuid
from django.conf import settings
from django.core.urlresolvers import reverse
from kindergarten.script.error_code import ErrorMsg

class Util:
    '''时间格式化'''
    @staticmethod
    def timeFormat(t,isShort=False):
        if t !=None and t != "":
            try:
                if t <0:
                    t=-t
                    timeArray = time.gmtime(t)
                    y=1970-(timeArray.tm_year-1970+1)
                    m =  13-timeArray.tm_mon
                    d =  31-timeArray.tm_mday
                    return "%s-%s-%s" %(y,m,d)
                else:
                    timeArray = time.localtime(t)
                if isShort:
                    return time.strftime("%Y-%m-%d", timeArray)
                else:
                    return time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
            except:
                return ""
        return ""

    '''获取时间戳'''
    @staticmethod
    def GetStampTime(strTime, isShort=False):
        if strTime != "":
            strTime=strTime.replace("/","-")
            FORMAT = "%Y-%m-%d %H:%M"
            if isShort:
                FORMAT = "%Y-%m-%d"
            arrTime = time.strptime(strTime, FORMAT)
            stramTime = time.mktime(arrTime)
            return stramTime
        return ""


    '''过滤html标签'''
    @staticmethod
    def trimHtmlTag(s):
        r=re.compile('</?\w+[^>]*>')
        if s:
            return r.sub('',s)
        return ""


    ##过滤HTML中的标签
    #将HTML中标签等信息去掉
    #@param htmlstr HTML字符串.
    @staticmethod
    def filter_tags(htmlstr):
        #先过滤CDATA
        re_cdata = re.compile('//<!\[CDATA\[[^>]*//\]\]>', re.I) #匹配CDATA
        re_script = re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>', re.I)#Script
        re_style = re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>', re.I)#style
        re_br = re.compile('<br\s*?/?>')#处理换行
        re_h = re.compile('</?\w+[^>]*>')#HTML标签
        re_comment = re.compile('<!--[^>]*-->')#HTML注释
        s = re_cdata.sub('', htmlstr)#去掉CDATA
        s = re_script.sub('', s) #去掉SCRIPT
        s = re_style.sub('', s)#去掉style
        s = re_br.sub('\n', s)#将br转换为换行
        s = re_h.sub('', s) #去掉HTML 标签
        s = re_comment.sub('', s)#去掉HTML注释
        #去掉多余的空行
        blank_line = re.compile('\n+')
        s = blank_line.sub('\n', s)
        s = Util.replaceCharEntity(s)#替换实体
        return s

    ##替换常用HTML字符实体.
    #使用正常的字符替换HTML中特殊的字符实体.
    #你可以添加新的实体字符到CHAR_ENTITIES中,处理更多HTML字符实体.
    #@param htmlstr HTML字符串.
    @staticmethod
    def replaceCharEntity(htmlstr):
        CHAR_ENTITIES = {'nbsp': ' ', '160': ' ',
                         'lt': '<', '60': '<',
                         'gt': '>', '62': '>',
                         'amp': '&', '38': '&',
                         'quot': '"', '34': '"', }

        re_charEntity = re.compile(r'&#?(?P<name>\w+);')
        sz = re_charEntity.search(htmlstr)
        while sz:
            entity = sz.group()#entity全称，如&gt;
            key = sz.group('name')#去除&;后entity,如&gt;为gt
        try:
            htmlstr = re_charEntity.sub(CHAR_ENTITIES[key], htmlstr, 1)
            sz = re_charEntity.search(htmlstr)
        except KeyError:
        #以空串代替
            htmlstr = re_charEntity.sub('', htmlstr, 1)
            sz = re_charEntity.search(htmlstr)
        return htmlstr

    def repalce(s, re_exp, repl_string):
        return re_exp.sub(repl_string, s)


    '''根据年月日就算周的开始日期和截止日期'''
    @staticmethod
    def CalculateStartTime(year,quarter=-1,month=0,week=0):
        FORMAT = "%d/%d/%d"
        day=datetime.datetime.now().day
        if year is None:
            year=datetime.datetime.now().year
        if quarter==0:
            return  FORMAT % (year,01,01),FORMAT % (year,12,31),
        if quarter>0:
            return  FORMAT % (year,(quarter-1)*4+1,01),  FORMAT % (year,quarter*4-1,31),
        if week == 0 and month>0:
            return  Util.GetFirstAndLastDayForMonth(year,month)
        if week > 0 and month > 0:
            week_list=calendar.monthcalendar(year, month)
            week_current=week_list[week-1]
            day_last=week_current[6]
            for d in week_current:
                if d>0:
                    day=d
                    break
            for d in range(1,7):
                if week_current[-d] > 0:
                    day_last = week_current[-d]
                    break
            return FORMAT % (year,month,day), FORMAT % (year,month ,day_last)

    '''获取某月的第一天和最后一天'''
    @staticmethod
    def GetFirstAndLastDayForMonth(year,month):
        FORMAT = "%d-%d-%d"
        d = calendar.monthrange(year, month)
        return FORMAT % (year, month, 01), FORMAT %(year, month, d[1])

    '''获取本月共有几周以及当前在哪一周'''
    @staticmethod
    def GetWeeksAndCurrentWeekForMonth(year, month):
        week_list = calendar.monthcalendar(year, month)
        count=len(week_list)
        month_current= datetime.datetime.now().month
        year_current= datetime.datetime.now().year
        #如果不是本年的本月，从1号开始
        if year==year_current and month==month_current:
            day = datetime.datetime.now().day
        else:
            day=1
        current_week=1
        for w in range(0,count):
            for d in week_list[w]:
                if int(day)==int(d):
                    current_week=w+1
                    break
        return count,current_week

    '''获取社交时间'''
    @staticmethod
    def GetGamTime(datetimes,isTimeStamp=False):
        if datetimes==None or datetimes=="":
            return ""
        localtime=time.localtime(datetimes)
        today = datetime.date.today()
        #当月第一天0点的Unix时间戳
        datetime_this_month= int(time.mktime(datetime.date(datetime.date.today().year, datetime.date.today().month, 1).timetuple()))
        #本日0点的Unix时间戳
        datetime_today = int(time.mktime(today.timetuple()))
        #昨天0点的Unix时间戳
        yesterday = today - datetime.timedelta(days=1)
        datetime_yesterday = int(time.mktime(yesterday.timetuple()))
        #今年元旦的时间戳
        year=datetime.datetime.now().year
        datetime_year = int(time.mktime(datetime.date(year, 1, 1).timetuple()))
        if datetimes > datetime_today:
            return "今天" + time.strftime('%H:%M', localtime)
        elif datetimes > datetime_yesterday:
            return "昨天" + time.strftime('%H:%M', localtime)
        elif datetimes > datetime_year:
            return time.strftime('%m月%d日', localtime)
        else:
            return time.strftime('%Y年%m月%d日', localtime)

    '''文件上传'''
    @staticmethod
    def profile_upload(file,folder=""):
        if file:
            import  uuid
            strTimePath=time.strftime('/%Y/%m/')#日期文件夹
            path_folder = "%s%s%s" % ( settings.UPLOADPATH, folder, strTimePath)#相对路径
            path_map = "%s%s" % (settings.SITEROOT,path_folder)#附件物理路径
            if not os.path.exists(path_map):
                os.makedirs(path_map)
                #file_name=str(uuid.uuid1())+".jpg"
            ext=file.name[file.name.rfind('.'):]
            guid=str(uuid.uuid1())
            #新文件名
            file_name = guid + ext
            #fname = os.path.join(settings.MEDIA_ROOT,filename)
            path_file = os.path.join(path_map, file_name)
            fp = open(path_file, 'wb')
            for content in file.chunks():
                fp.write(content)
            fp.close()
            filepath_new=path_folder+file_name#相对路径
            fileseze=os.path.getsize(path_file)/1024.0
            return (file.name,filepath_new ,fileseze,guid) #change
        return None   #change

    '''文件上传[云文件]'''
    @staticmethod
    def profile_upload_storage(file,domain_name="file"):
        if file:
            from os import environ
            import  uuid
            online = environ.get("APP_NAME", "")
            if online:
                import sae.const
                access_key = sae.const.ACCESS_KEY
                secret_key = sae.const.SECRET_KEY
                appname = sae.const.APP_NAME
                guid=str(uuid.uuid1())
                import sae.storage
                s = sae.storage.Client()
                ob = sae.storage.Object(file.read())
                url = s.put(domain_name, file.name, ob)
                fileseze=1024.0
                return (file.name,url ,fileseze,guid) #change
        return None   #change

    '''文件下载'''
    @staticmethod
    def profile_download(filepath, filename=""):
        if filepath:
            #中文解码
            if not filename:
                filename = filepath.split("/")[-1]
            path = settings.SITEROOT + filepath#附件全路径
            path = path.replace('/', '\\')#转换为物理路径
            if os.path.isfile(path):
                #return path
                f = open(path, 'rb')
                data = f.read()
                f.close()
                response = HttpResponse(data, mimetype='application/octet-stream')
                response['Content-Disposition'] = 'attachment; filename=%s' % filename
                return response
        return ""

    '''附件路径'''
    @staticmethod
    def getFileUrl(files):
        if settings.USE_STORAGE:
            return files
        else:
             return  reverse("web-file-download")+"?filepath=%s" % files

    '''删除目录文件'''
    @staticmethod
    def profile_delete(filepath):
        path=settings.SITEROOT+filepath#附件全路径
        if os.path.isfile(path):
            os.remove(path)

    '''判断用户是否登入'''
    @staticmethod
    def validateLogin(request,redicturl=''):
        if request.user.is_authenticated():     #判断用户是否已登录
            return True
        else:
            return False


    '''随机验证码'''
    @staticmethod
    def getRandCode(length=0,isdigit=False):
        feed=["1","2","3","4","5","6","7","8","9","0","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
        code=""
        if isdigit:
            feed=range(0, 11)
            if length == 0:
                code="%d%d%d%d" % (datetime.datetime.now().year,datetime.datetime.now().month,datetime.datetime.now().day,random.randint(10000, 99999))
            else:
                for i in range(1, length + 1):
                    item = random.choice(feed)
                    code += str(item)
            return code
        else:
            if length==0:
                code = str(uuid.uuid1()).replace('-','')
            else:
                for i in range(1, length + 1):
                    item = random.choice(feed)
                    code += item
            return code

    '''获取分页的页码'''
    @staticmethod
    def getPageSizeAndIndex(request):
        pagesize = 10
        pageindex = 1
        if 'pagesize' in request.QUERY_PARAMS:
            pagesize = int(request.QUERY_PARAMS.get('pagesize'))
        if 'pageindex' in request.QUERY_PARAMS:
            pageindex = int(request.QUERY_PARAMS.get('pageindex'))
        return pagesize,pageindex

    @staticmethod
    def get_xmlnode(node, name):
        return node.getElementsByTagName(name) if node else []

    @staticmethod
    def get_nodevalue(node, index=0):
        return node.childNodes[index].nodeValue if node else ''

    '''获取XML文件的值'''
    @staticmethod
    def getXMLValue(nodename):
        path_xml=os.path.dirname(__file__)+"/config.xml"
        from xml.dom import minidom
        if path_xml != None and os.path.isfile(path_xml):
            try:
                doc = minidom.parse(path_xml)
                root = doc.documentElement
                node_name = Util.get_xmlnode(root, nodename)
                value = Util.get_nodevalue(node_name[0]).encode('utf-8', 'ignore')
            except:
                return ""
            else:
                return value.strip()
        return ""

    '''获取cache'''
    @staticmethod
    def GetCache(key,data=None):
        if cache.get(key, None):
            return cache.get(key, None)
        return ''

    '''设置cache'''
    @staticmethod
    def SetCache(key, data=None,hour=1):
        cache.set(key, data, 60 * 60 * hour)

    '''字符过滤'''
    @staticmethod
    def GetFilterString(string):
        if string != "":
            string =string.strip()
            #string=string.replace("<","＜")
            #string = string.replace(">", "＞")
            string = string.replace("<script>", "")
            string = string.replace("<script", "")
            string = string.replace("</script>", "")
            string = string.replace("javascript:", "")
            string = string.replace("jscript:", "")
            string = string.replace("vbscript:", "")
        return string

    @staticmethod
    def GetResponseData(result,error_code=0,data=None,counts=None):
        context={}
        context['result']=result
        context['data']=data
        context['code']=error_code
        if error_code and error_code !=0:
            context['error']=ErrorMsg[error_code]
        if counts:
            context['counts']=counts
        return Response(context)

    #分页
    @staticmethod
    def InitPagenation(request):
        page = 1
        if "page" in request.GET and request.GET["page"]:
            page = int(request.GET["page"])
        return page,15
    #分页
    @staticmethod
    def GetPagenation(request,counts,pagesize=15):
        page = 1
        if "page" in request.GET and request.GET["page"]:
            page = int(request.GET["page"])
        if counts>pagesize:
            #计算总页数
            if counts%pagesize==0:
                pagecount= counts/pagesize
                if pagecount==0:
                    pagecount = 1
            else:
                pagecount = int(counts / pagesize+1);

            html = '<div class="pagination">'
            html += '<ul>'
            #上一页
            if page>1:
                html += '<li><a href="?page=%d">上一页</a></li>' % (page-1)
            else:
                html += '<li class="disabled"><a href="javascript:;">上一页</a></li>'

            #页码
            for i in range(1,pagecount+1):
                if i == page :
                    html += '<li class="active"><a href="javascript:;" >%s</a></li>' % i
                else:
                    html += '<li><a href="?page=%s">%s</a></li>' % (i,i)
            #下一页
            if page < pagecount:
                html += '<li><a href="?page=%d">下一页</a></li>' % (page-1)
            else:
                html += '<li class="disabled"><a href="javascript:;">下一页</a></li>'

            html += '</ul>'
            html += '</div>'
            return html
        return ""
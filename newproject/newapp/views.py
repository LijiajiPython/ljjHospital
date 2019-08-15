from . import models
from .models import UserForm,Hospital,Room,Country,News,Doctor,Subject,DetailSubject,Illness,Message,User,Board
from .forms import RegisterForm
from django.db.models import Min,Sum,Max,Count
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage, InvalidPage
from django.http import HttpResponse
import time
from django.shortcuts import render, redirect, HttpResponse
from .pay import AliPay
import json

# Create your views here.





def home(request):
    # levelList = Hospital.objects.values('hlevel').distinct().order_by('hlevel')
    # print(levelList)
    hospitalList = Hospital.objects.all()
    hospitalList1 = Hospital.objects.filter(hlevel=1)
    hospitalList2 = Hospital.objects.filter(hlevel=2)
    hospitalList3 = Hospital.objects.filter(hlevel=3)
    hospitalList4 = Hospital.objects.filter(hlevel=4)
    hospitalList5 = Hospital.objects.filter(hlevel=5)
    hospitalList6 = Hospital.objects.filter(hlevel=6)
    hospitalList7 = Hospital.objects.filter(hlevel=7)
    hospitalList8 = Hospital.objects.filter(hlevel=8)
    hospitalList9 = Hospital.objects.filter(hlevel=9)
    countryList = Country.objects.all()
    # roomList = Room.objects.all()
    subjectList = Subject.objects.all()
    dsList=DetailSubject.objects.filter(sid_id__in=subjectList)
    illnessList = Illness.objects.filter(sid_id__in=subjectList)
    noticeList = News.objects.order_by('-createtime')[:10]
    print(illnessList)
    return render(request,'maApp/home.html',{'hospitalList':hospitalList,'hospitalList1':hospitalList1,
                'hospitalList2':hospitalList2,'hospitalList3':hospitalList3,'hospitalList4':hospitalList4,
                'hospitalList5':hospitalList5,'hospitalList6':hospitalList6,'hospitalList7':hospitalList7,
                'hospitalList8':hospitalList8,'hospitalList9':hospitalList9,'countryList':countryList,
                'subjectList':subjectList,'dsList':dsList,'illnessList':illnessList,'noticeList':noticeList})


def login(request):
    if request.session.get('is_login',None):
        return redirect('/back/')
    if request.method == 'POST':
        login_form = UserForm(request.POST)
        isdoctor = request.POST.get('isdoctor')
        message = "请检查填写的内容！"
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            if isdoctor == '0':
                try:
                    user = models.User.objects.get(uname=username)
                    if user.upasswd == password:
                        request.session['is_login'] = True
                        request.session['is_user'] = True
                        request.session['user_id'] = user.id
                        request.session['user_name'] = user.uname
                        return redirect('/back/')
                    else:
                        message = "密码不正确！"
                except:
                    message = "用户不存在！"
            else:
                try:
                    doctor = models.Doctor.objects.get(dname=username)
                    if doctor.dpasswd == password:
                        request.session['is_login'] = True
                        request.session['is_doctor'] = True
                        request.session['user_id'] = doctor.id
                        request.session['user_name'] = doctor.dname
                        return redirect('/back/')
                    else:
                        message = "密码不正确！"
                except:
                    message = "用户不存在！"
        return render(request, 'maApp/login.html', locals())
    login_form = UserForm()
    return render(request, 'maApp/login.html', locals())


def register(request):
    if request.session.get('is_login', None):
        return redirect("/back/")
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        message = "请检查填写的内容！"
        if register_form.is_valid():  # 获取数据
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            tel = register_form.cleaned_data['tel']
            email = register_form.cleaned_data['email']
            birth = register_form.cleaned_data['birth']
            birth=str(birth)
            address = register_form.cleaned_data['address']
            sex = register_form.cleaned_data['sex']
            if password1 != password2:  # 判断两次密码是否相同
                message = "两次输入的密码不同！"
                return render(request, 'maApp/register.html', locals())
            else:
                same_name_user = models.User.objects.filter(uname=username)
                if same_name_user:  # 用户名唯一
                    message = '用户已经存在，请重新选择用户名！'
                    return render(request, 'maApp/register.html', locals())
                same_email_user = models.User.objects.filter(uemail=email)
                if same_email_user:  # 邮箱地址唯一
                    message = '该邮箱地址已被注册，请使用其他邮箱！'
                    return render(request, 'maApp/register.html', locals())
                same_tel_user = models.User.objects.filter(utel=tel)
                if same_tel_user:  # 电话号码唯一
                    message = '该号码被注册，请使用其他号码！'
                    return render(request, 'maApp/register.html', locals())
                # 当一切都成功的情况下，创建新用户
                new_user = models.User.objects.create()
                new_user.uname = username
                new_user.upasswd = password1
                new_user.uemail = email
                new_user.ugender = sex
                new_user.utel = tel
                new_user.ubirth = birth
                new_user.uaddress = address
                new_user.save()
                return redirect('/login/')  # 自动跳转到登录页面
    register_form = RegisterForm()
    return render(request, 'maApp/register.html',locals())


def logout(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录
        return redirect("/back/")
    request.session.flush()
    return redirect("/back/")

def back(request):
    docList=Doctor.objects.all()
    return render(request,'maApp/back.html',{'docList':docList})


def news(request):
    newsList = News.objects.order_by('-createtime')
    paginator = Paginator(newsList, 10)
    if request.method == "GET":
        page = request.GET.get('page')
        try:
            newspages = paginator.page(page)
        except PageNotAnInteger:
            newspages = paginator.page(1)
        except InvalidPage:
            return HttpResponse('找不到页面的内容')
        except EmptyPage:
            newspages = paginator.page(paginator.num_pages)
    return render(request,'maApp/news.html',{'newsList':newsList,'newspages':newspages})


def fords(request,num):
    num = int(num)
    dsList = DetailSubject.objects.get(id=num)
    roomList=Room.objects.filter(dsid_id=num)
    print(roomList)
    doctorList = Doctor.objects.filter(rid_id__in=roomList)
    return render(request,'maApp/fords.html',{'dsList':dsList,'roomList':roomList,'doctorList':doctorList,'num':num})


def hospitals(request,num):
    num=int(num)
    hospitalList = Hospital.objects.get(id=num)
    roomList = Room.objects.filter(hid_id=num)
    doctorList = Doctor.objects.filter(rid_id__in=roomList)
    print(doctorList)
    return render(request,'maApp/hospitals.html',{'num':num,'doctorList':doctorList,'hospitalList':hospitalList,'roomList':roomList})

def rooms(request,num):
    num=int(num)
    message = Message.objects.values('rid_id').annotate(Min('id')).all()
    minidList=[]
    for i in message:
        minidList.append(i['id__min'])
    for i in minidList:
        for j in Message.objects.all().values('id','mname','mprice','rid_id'):
            # print(j['id'],j['mname'])
            if i == j['id']:
                print(j['id'],j['mname'],j['mprice'],j['rid_id'])
                messagestr = str(j['mname'])
                locTime = messagestr
                locSec1 = int(time.mktime(time.strptime(locTime,'%Y-%m-%d')))+(24*60*60)
                locSec2 = time.time()
                # print(locSec1,locSec2)
                locSec3 = locSec1 + (6 * 24 * 60 * 60)
                x = time.localtime(locSec3)
                locSec3 = time.strftime('%Y-%m-%d',x)
                # print(locSec1,locSec2,locSec3)
                if locSec1 < locSec2:
                    # print('删除loc1',i,messagestr,'新增loc3',locSec3,rid)
                    models.Message.objects.filter(id=i).delete()
                    models.Message.objects.create(mname=locSec3,mprice=j['mprice'],rid_id=j['rid_id'])
    roomList = Room.objects.get(id=num)
    messageList = Message.objects.filter(rid_id=num)
    doctorList = Doctor.objects.filter(rid_id=roomList.id)
    return render(request,'maApp/rooms.html',{'num':num,'doctorList':doctorList,'roomList':roomList,'messageList':messageList})

def forillness(request,num):
    num=int(num)
    illnessList = Illness.objects.get(id=num)
    dsList = DetailSubject.objects.get(id=illnessList.dsid_id)
    print(dsList)
    roomList = Room.objects.filter(dsid_id=dsList)
    print(roomList)
    doctorList = Doctor.objects.filter(rid_id__in=roomList)
    return render(request,'maApp/forillness.html',{'num':num,'doctorList':doctorList,'dsList':dsList,'roomList':roomList,'illnessList':illnessList})

def doctors(request,num):
    num=int(num)
    doctorList = Doctor.objects.get(id=num)
    boardList = Board.objects.filter(did_id=doctorList.id).order_by('-createtime')
    paginator = Paginator(boardList, 10)
    if request.method == "GET":
        page = request.GET.get('page')
        try:
            boardpages = paginator.page(page)
        except PageNotAnInteger:
            boardpages = paginator.page(1)
        except InvalidPage:
            return HttpResponse('找不到页面的内容')
        except EmptyPage:
            boardpages = paginator.page(paginator.num_pages)
    elif request.method == "POST":
        page = request.POST.get('page')
        try:
            boardpages = paginator.page(page)
        except PageNotAnInteger:
            boardpages = paginator.page(1)
        except InvalidPage:
            return HttpResponse('找不到页面的内容')
        except EmptyPage:
            boardpages = paginator.page(paginator.num_pages)
    if request.method == 'POST':
        userid = request.POST.get('uid_id')
        doctorid = request.POST.get('did_id')
        breply = request.POST.get('breply')
        btext = request.POST.get('btext')
        print(btext)
        models.Board.objects.create(uid_id=userid, did_id=doctorid, breply=breply, btext=btext)
        return render(request, 'maApp/doctors.html',locals())
    return render(request, 'maApp/doctors.html', {'doctorList': doctorList,'boardList':boardList,'boardpages':boardpages})

def messagesubmit(request,num):
    num = int(num)
    messageList = Message.objects.get(id=num)
    return render(request,'maApp/messagesubmit.html',{'num':num,'messageList':messageList})


def success(request,userid,messageid):
    userid = int(userid)
    messageid = int(messageid)
    try:
        messageList = Message.objects.get(id=messageid)
        if messageList.muid1 == userid and messageList.mpay1 == '1':
            models.Message.objects.filter(id=messageid).update(mpay1=2)
        elif messageList.muid2 == userid and messageList.mpay2 == '1':
            models.Message.objects.filter(id=messageid).update(mpay2=2)
        elif messageList.muid3 == userid and messageList.mpay3 == '1':
            models.Message.objects.filter(id=messageid).update(mpay3=2)
        elif messageList.muid4 == userid and messageList.mpay4 == '1':
            models.Message.objects.filter(id=messageid).update(mpay4=2)
        elif messageList.muid5 == userid and messageList.mpay5 == '1':
            models.Message.objects.filter(id=messageid).update(mpay5=2)
        elif messageList.muid6 == userid and messageList.mpay6 == '1':
            models.Message.objects.filter(id=messageid).update(mpay6=2)
        elif messageList.muid7 == userid and messageList.mpay7 == '1':
            models.Message.objects.filter(id=messageid).update(mpay7=2)
        elif messageList.muid8 == userid and messageList.mpay8 == '1':
            models.Message.objects.filter(id=messageid).update(mpay8=2)
        elif messageList.muid9 == userid and messageList.mpay9 == '1':
            models.Message.objects.filter(id=messageid).update(mpay9=2)
        elif messageList.muid10 == userid and messageList.mpay10 == '1':
            models.Message.objects.filter(id=messageid).update(mpay10=2)
        return render(request, 'maApp/success.html')
    except:
        return render(request, 'maApp/success.html')




def userhome(request,num):
    num = int(num)
    userList = User.objects.get(id=num)
    messageList = Message.objects.all()
    boardList = Board.objects.filter(uid_id=userList.id).order_by('-createtime')
    paginator = Paginator(boardList, 5)
    if request.method == "GET":
        page = request.GET.get('page')
        try:
            boardpages = paginator.page(page)
        except PageNotAnInteger:
            boardpages = paginator.page(1)
        except InvalidPage:
            return HttpResponse('找不到页面的内容')
        except EmptyPage:
            boardpages = paginator.page(paginator.num_pages)
    return render(request, 'maApp/userhome.html',{'userList':userList,'messageList':messageList,'boardpages':boardpages})

def dochome(request,num):
    num = int(num)
    doctorList = Doctor.objects.get(id=num)
    messageList = Message.objects.all()
    roomList = Room.objects.get(id=doctorList.rid_id)
    boardList = Board.objects.filter(did_id=doctorList.id).order_by('-createtime')
    paginator = Paginator(boardList, 5)
    if request.method == "GET":
        page = request.GET.get('page')
        try:
            boardpages = paginator.page(page)
        except PageNotAnInteger:
            boardpages = paginator.page(1)
        except InvalidPage:
            return HttpResponse('找不到页面的内容')
        except EmptyPage:
            boardpages = paginator.page(paginator.num_pages)
    if request.method == 'POST':
        docname = request.POST.get('docname')
        worktime = request.POST.get('worktime')
        boardid = request.POST.get('boardid')
        breply = request.POST.get('breply')
        models.Board.objects.filter(id=boardid).update(breply=breply)
        print(docname)
        print(worktime)
        if worktime == "mon1":
            models.Room.objects.filter(id=roomList.id).update(mon1=docname)
        elif worktime == "tue1":
            models.Room.objects.filter(id=roomList.id).update(tue1=docname)
        elif worktime == "wed1":
            models.Room.objects.filter(id=roomList.id).update(wed1=docname)
        elif worktime == "thu1":
            models.Room.objects.filter(id=roomList.id).update(thu1=docname)
        elif worktime == "fri1":
            models.Room.objects.filter(id=roomList.id).update(fri1=docname)
        elif worktime == "sat1":
            models.Room.objects.filter(id=roomList.id).update(sat1=docname)
        elif worktime == "sun1":
            models.Room.objects.filter(id=roomList.id).update(sun1=docname)
        elif worktime == "mon2":
            models.Room.objects.filter(id=roomList.id).update(mon2=docname)
        elif worktime == "tue2":
            models.Room.objects.filter(id=roomList.id).update(tue2=docname)
        elif worktime == "wed2":
            models.Room.objects.filter(id=roomList.id).update(wed2=docname)
        elif worktime == "thu2":
            models.Room.objects.filter(id=roomList.id).update(thu2=docname)
        elif worktime == "fri2":
            models.Room.objects.filter(id=roomList.id).update(fri2=docname)
        elif worktime == "sat2":
            models.Room.objects.filter(id=roomList.id).update(sat2=docname)
        elif worktime == "sun2":
            models.Room.objects.filter(id=roomList.id).update(sun2=docname)
        return redirect('/success/0/0')
    return render(request, 'maApp/dochome.html',{'doctorList': doctorList, 'messageList': messageList, 'roomList': roomList,'boardList':boardList,'boardpages':boardpages})

def onenews(request,num):
    num=int(num)
    newsList = News.objects.get(id=num)
    return render(request, 'maApp/onenews.html',{'newsList':newsList})

def userchange(request,num):
    num=int(num)
    userList = User.objects.get(id=num)
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        message = "请检查填写的内容！"
        if register_form.is_valid():  # 获取数据
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            tel = register_form.cleaned_data['tel']
            email = register_form.cleaned_data['email']
            birth = register_form.cleaned_data['birth']
            birth=str(birth)
            address = register_form.cleaned_data['address']
            sex = register_form.cleaned_data['sex']
            if password1 != password2:  # 判断两次密码是否相同
                message = "两次输入的密码不同！"
                return render(request, 'maApp/userchange.html', locals())
            else:
                same_name_user = models.User.objects.filter(uname=username)
                if same_name_user:  # 用户名唯一
                    if username != userList.uname:
                        message = '用户已经存在，请重新选择用户名！'
                        return render(request, 'maApp/userchange.html', locals())
                same_email_user = models.User.objects.filter(uemail=email)
                if same_email_user:  # 邮箱地址唯一
                    if email != userList.uemail:
                        message = '该邮箱地址已被注册，请使用别的邮箱！'
                        return render(request, 'maApp/userchange.html', locals())
                same_tel_user = models.User.objects.filter(utel=tel)
                if same_tel_user:  # 电话号码唯一
                    if tel != userList.utel:
                        message = '该号码被注册，请使用别的号码！'
                        return render(request, 'maApp/userchange.html', locals())
                models.User.objects.filter(id=num).update(uname=username,utel=tel,uemail=email,upasswd=password1,ubirth=birth,uaddress=address,ugender=sex)
                return redirect('/logout/')
    register_form = RegisterForm()
    return render(request, 'maApp/userchange.html', locals())


def get_ali_object(userid,messageid):
    # 沙箱环境地址：https://openhome.alipay.com/platform/appDaily.htm?tab=info
    app_id = "2016092900624238"  # APPID （沙箱应用）
    # 支付完成后，支付偷偷向这里地址发送一个post请求，识别公网IP,如果是 192.168.20.13局域网IP ,支付宝找不到，def page2()
    # 接收不到这个请求j
    notify_url = "http://127.0.0.1:8000"
    # 支付完成后，跳转的地址。
    return_url = "http://127.0.0.1:8000/success/"+userid+"/"+messageid
    merchant_private_key_path = "keys/app_private_2048.txt"  # 应用私钥
    alipay_public_key_path = "keys/alipay_public_2048.txt"  # 支付宝公钥
    alipay = AliPay(
        appid=app_id,
        app_notify_url=notify_url,
        return_url=return_url,
        app_private_key_path=merchant_private_key_path,
        alipay_public_key_path=alipay_public_key_path,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥
        debug=True,  # 默认False,
    )
    return alipay


def pay(request):
    return render(request, 'maApp/pay.html')


def page1(request):
    userid = request.POST.get('message_uid')
    messageid = request.POST.get('message_id')
    thismessage = Message.objects.get(id=messageid)
    number = int(thismessage.mnumber)
    print(number)
    price = thismessage.mprice
    if thismessage.mpay1 == '0':
        models.Message.objects.filter(id=messageid).update(muid1=userid)
        models.Message.objects.filter(id=messageid).update(mpay1=1)
        number+=1
        models.Message.objects.filter(id=messageid).update(mnumber=number)
    elif thismessage.mpay2 == '0':
        models.Message.objects.filter(id=messageid).update(muid2=userid)
        models.Message.objects.filter(id=messageid).update(mpay2=1)
        number+=1
        models.Message.objects.filter(id=messageid).update(mnumber=number)
    elif thismessage.mpay3 == '0':
        models.Message.objects.filter(id=messageid).update(muid3=userid)
        models.Message.objects.filter(id=messageid).update(mpay3=1)
        number+=1
        models.Message.objects.filter(id=messageid).update(mnumber=number)
    elif thismessage.mpay4 == '0':
        models.Message.objects.filter(id=messageid).update(muid4=userid)
        models.Message.objects.filter(id=messageid).update(mpay4=1)
        number+=1
        models.Message.objects.filter(id=messageid).update(mnumber=number)
    elif thismessage.mpay5 == '0':
        models.Message.objects.filter(id=messageid).update(muid5=userid)
        models.Message.objects.filter(id=messageid).update(mpay5=1)
        number+=1
        models.Message.objects.filter(id=messageid).update(mnumber=number)
    elif thismessage.mpay6 == '0':
        models.Message.objects.filter(id=messageid).update(muid6=userid)
        models.Message.objects.filter(id=messageid).update(mpay6=1)
        number+=1
        models.Message.objects.filter(id=messageid).update(mnumber=number)
    elif thismessage.mpay7 == '0':
        models.Message.objects.filter(id=messageid).update(muid7=userid)
        models.Message.objects.filter(id=messageid).update(mpay7=1)
        number+=1
        models.Message.objects.filter(id=messageid).update(mnumber=number)
    elif thismessage.mpay8 == '0':
        models.Message.objects.filter(id=messageid).update(muid8=userid)
        models.Message.objects.filter(id=messageid).update(mpay8=1)
        number+=1
        models.Message.objects.filter(id=messageid).update(mnumber=number)
    elif thismessage.mpay9 == '0':
        models.Message.objects.filter(id=messageid).update(muid9=userid)
        models.Message.objects.filter(id=messageid).update(mpay9=1)
        number+=1
        models.Message.objects.filter(id=messageid).update(mnumber=number)
    elif thismessage.mpay10 == '0':
        models.Message.objects.filter(id=messageid).update(muid10=userid)
        models.Message.objects.filter(id=messageid).update(mpay10=1)
        number+=1
        models.Message.objects.filter(id=messageid).update(mnumber=number)
    else:
        error = '该科室当前日期预约人数已满，请选择其他科室或日期'
        return render(request, 'maApp/messagesubmit.html', {'error': error, 'messageList': thismessage})
    # 根据当前用户的配置，生成URL，并跳转。
    money = price
    # money = request.POST.get('money')
    print(money)
    alipay = get_ali_object(userid,messageid)
    # 生成支付的url
    query_params = alipay.direct_pay(
        subject="预约挂号费",  # 商品简单描述
        out_trade_no="x2" + str(time.time()),  # 用户购买的商品订单号（每次不一样） 20180301073422891
        total_amount=money,  # 交易金额(单位: 元 保留俩位小数)
    )
    pay_url = "https://openapi.alipaydev.com/gateway.do?{0}".format(query_params)  # 支付宝网关地址（沙箱应用）
    return redirect(pay_url)

# def page2(request):
#     alipay = get_ali_object()
#     if request.method == "POST":
#         # 检测是否支付成功
#         # 去请求体中获取所有返回的数据：状态/订单号
#         from urllib.parse import parse_qs
#         # name&age=123....
#         body_str = request.body.decode('utf-8')
#         print("#"*80)
#         print(body_str)
#         post_data = parse_qs(body_str)
#         post_dict = {}
#         for k, v in post_data.items():
#             post_dict[k] = v[0]
#         # post_dict有10key： 9 ，1
#         sign = post_dict.pop('sign', None)
#         status = alipay.verify(post_dict, sign)
#         print('------------------开始------------------')
#         print('POST验证', status)
#         print(post_dict)
#         out_trade_no = post_dict['out_trade_no']
#         # 修改订单状态
#         # models.Order.objects.filter(trade_no=out_trade_no).update(status=2)
#         print('------------------结束------------------')
#         # 修改订单状态：获取订单号
#         return HttpResponse('POST返回')
#     else:
#         params = request.GET.dict()
#         sign = params.pop('sign', None)
#         status = alipay.verify(params, sign)
#         print('==================开始==================')
#         print('GET验证', status)
#         print('==================结束==================')
#         return HttpResponse('支付成功')



def search(request):
    word = request.POST.get('word')
    hospitalList = Hospital.objects.filter(hname__contains=word)
    roomList = Room.objects.filter(rname__contains=word)
    doctorList = Doctor.objects.filter(dname__contains=word)
    return render(request, 'maApp/search.html',{'hospitalList':hospitalList,'roomList':roomList,'doctorList':doctorList})
import random
from datetime import datetime, timedelta
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from django.shortcuts import render
from django.contrib.auth.hashers import check_password, make_password


# Create your views here.
from App_yxr.models import User, Cart, Orders, Goods, Goodsorder


# 用户登录
def login(request,id,code=1):
    if request.method == 'GET':
        return render(request,'user/user_login.html')
    if request.method == 'POST':
        u_name = request.POST.get('username')
        u_pwb = request.POST.get('password')
        # 验证用户是否存在
        user = User.objects.filter(u_name=u_name)
        if user:
            # 校验密码
            if check_password(u_pwb,user[0].u_pwd):
                u_ticket = ''
                s = 'qwertyuiopasdfghjklzxcvbnm0123456789'
                for i in range(8):
                    u_ticket += random.choice(s)
                # 设置cookie
                if code =='1':
                    response = HttpResponseRedirect(reverse('yxr:user'))
                elif code == '1000':
                    response = HttpResponseRedirect(reverse('zl:show',args=(id,)))
                u_outtime = datetime.now() + timedelta(days=1)
                response.set_cookie('u_ticket',u_ticket,expires=u_outtime)
                user[0].u_ticket=u_ticket
                user[0].u_outtime=u_outtime
                user[0].save()
                request.session['user_id'] = user[0].id

                return response

# 用户注册
def register(request):
    if request.method == 'GET':
        return render(request,'user/user_register.html')
    if request.method == 'POST':
        u_name = request.POST.get('username')
        u_pwb = request.POST.get('password')
        u_tel = request.POST.get('telphone')
        u_pwb = make_password(u_pwb)

        User.objects.create(
            u_name=u_name,
            u_pwd=u_pwb,
            u_tel=u_tel
        )
        return HttpResponseRedirect('/App_yxr/login/')

# 用户注销
def logout(request):
    del request.session['user_id']
    return HttpResponseRedirect('/App_yxr/login/')


# 用户主页
def user(request):
    data = {}
    if request.method == 'GET':
        if 'user_id' in request.session:

            user_id = request.session.get('user_id')
            user = User.objects.filter(id=user_id)[0]
            u_name = user.u_name
            if user:
                orders = user.orders_set.all()
                waitpay,endpay =0,0
                for order in orders:
                    if order.o_status == 0:
                        waitpay +=1
                    elif order.o_status == 1:
                        endpay += 1
                data['waitpay'] = waitpay
                data['endpay'] = endpay

            data['username'] = u_name

            return render(request, 'user/user.html', data)
        else:
            return HttpResponseRedirect('/App_yxr/login/')
    else:
        return HttpResponseRedirect('/App_yxr/login/')


def allorders(requset):
    if requset.method == 'GET':
        u_id = requset.session.get('user_id')
        orders = Orders.objects.filter(pk=u_id).all()
        data = {
            'orders':orders
        }
        return render(requset,'user/gengduodingdan.html',data)

def wait_pay(request):
    if request.method == 'GET':
        if 'user_id' in request.session:

            user_id = request.session.get('user_id')
            orders = Orders.objects.filter(pk=user_id).all()
            olist = []
            for i in orders:
                if i.o_status == 0:
                    olist.append(i)
                else:
                    pass

            return render(request,'user/daizhifu.html',{'olist':olist})

def end_pay(request):
    if request.method == 'GET':
        if 'user_id' in request.session:

            user_id = request.session.get('user_id')
            orders = Orders.objects.filter(pk=user_id).all()

            olist1 = []
            for i in orders:
                if i.o_status == 1:
                    olist1.append(i)
                else:
                    pass
            return render(request,'user/daishouhuo.html',{'olist1':olist1})

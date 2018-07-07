import datetime
import platform
import socket

from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
import os
from time import time
from django.contrib.auth.hashers import check_password, make_password
from io import BytesIO

from App.models import GCategory, GCategory2, Goods
from Beauty.settings import MEDIA_ROOT
from adminutil.verifications import create_validate_code
from App.models import Orders, User, Address, Admin


def is_login(fn):
    def wrapper(request,*args, **kwargs):
        if request.session.get('id', None):
            test = fn(request, *args, **kwargs)
            return test
        else:
            return HttpResponseRedirect('/admin/login/')

    return wrapper

@is_login
def index(request):
    data = {
        'username': Admin.objects.get(id=int(request.session.get('id'))).a_account,
    }
    return render(request, 'admin/index.html', data)

@is_login
def weclome(request):
    data = {
        # 系统名称和版本号
        'goods': Goods.objects.all().count(),
        'orders': Orders.objects.all().count(),
        'users': User.objects.all().count(),
        'admins': Admin.objects.all().count(),
        'sys_name': platform.platform(),
        'hostname': socket.gethostname(),
        'ip': socket.gethostbyname(socket.gethostname()),
        'nowtime': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'cpu_info':platform.processor(),
        'nowuser': Admin.objects.get(id=int(request.session.get('id'))).a_account,
        'sessionid': request.session.session_key,
    }



    return render(request, 'admin/welcome.html', data)

@is_login
def log(request):
    return render(request, 'admin/system-log.html')

@is_login
def changepass(request):
    if request.method == 'GET':
        id = request.session.get('id')
        if id:
            administrator = Admin.objects.filter(pk=id).first()
            return render(request, 'admin/change-password.html', {'ad': administrator})
    if request.method == 'POST':
        id = request.session.get('id')
        a = Admin.objects.filter(pk=id).first()
        p1 = request.POST.get('newpassword')
        p2 = request.POST.get('newpassword2')
        if p1 == p2:
            p1 = make_password(p1)
            a.a_pwd = p1
            a.save()
            return HttpResponseRedirect(
                '/admin/changepass/'
            )

@is_login
def charts7(request):
    return render(request, 'admin/charts-7.html')

@is_login
def charts6(request):
    return render(request, 'admin/charts-6.html')

@is_login
def charts5(request):
    return render(request, 'admin/charts-5.html')

@is_login
def charts4(request):
    return render(request, 'admin/charts-4.html')

@is_login
def charts3(request):
    return render(request, 'admin/charts-3.html')

@is_login
def charts2(request):
    return render(request, 'admin/charts-2.html')

@is_login
def charts1(request):
    return render(request, 'admin/charts-1.html')

@is_login
def alist(request):
    return render(request, 'admin/admin-list.html')

@is_login
def aper(request):
    return render(request, 'admin/admin-permission.html')

@is_login
def arol(request):
    return render(request, 'admin/admin-role.html')

@is_login
def alist(request):
    if request.method == 'GET':
        admins = Admin.objects.all()
        return render(request, 'admin/admin-list.html', {'admins':admins})

@is_login
def mlist(request):
    data = {
        'code': '200',
        'msg': '修改成功'
    }
    if request.method == 'GET':
        users = User.objects.all()
        addrs = Address.objects.all()
        return render(request, 'admin/member-list.html', {'users': users, 'addrs': addrs})
    if request.method == 'POST':
        addr_id = request.POST.get('sid')
        addrs = Address.objects.filter(id=addr_id).first()
        if addrs.u_addrstatus:
            addrs.u_addrstatus = 0
            data['u_addrstatus'] = 0
            addrs.save()
        else:
            addrs.u_addrstatus = 1
            data['u_addrstatus'] = 1
            addrs.save()
        return JsonResponse(data)

@is_login
def ulist(request):
    data = {
        'code': '200',
        'msg': '修改成功'
    }
    if request.method == 'GET':
        users = User.objects.all()
        addrs = Address.objects.all()
        return render(request, 'admin/userlist.html', {'users': users, 'addrs': addrs})
    # if request.method == 'POST':
    #     addr_id = request.POST.get('sid')
    #     addrs = Address.objects.filter(id=addr_id).first()
    #     if addrs.u_addrstatus:
    #         addrs.u_addrstatus = 0
    #         data['u_addrstatus'] = 0
    #         addrs.save()
    #     else:
    #         addrs.u_addrstatus = 1
    #         data['u_addrstatus'] = 1
    #         addrs.save()
    #     return JsonResponse(data)

@is_login
def olist(request):
    data = {
        'code':'200',
        'msg': '请求成功'
    }
    if request.method == 'GET':
        orders = Orders.objects.all()
        users = User.objects.all()
        return render(request, 'admin/picture-list.html', {'orders': orders, 'users':users})
    if request.method == 'POST':
        o_status = request.POST.get('o_status')
        o_id = request.POST.get('o_id')
        myorder = Orders.objects.filter(id=o_id).first()
        myorder.o_status = o_status
        myorder.o_changetime = datetime.datetime.now()
        myorder.save()
        return JsonResponse(data)

@is_login
def madd(request):
    if request.method == 'GET':
        return render(request, 'admin/member-add.html')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        tel = request.POST.get('mobile')
        if username and password and tel:
            User.objects.create(
                u_name=username,
                u_pwd=password,
                u_tel=tel
            )
            return render(request, 'admin/member-list.html')


@is_login
def adminadd(request):
    if request.method == 'GET':
        return render(request, 'admin/admin-add.html')
    if request.method == 'POST':
        username = request.POST.get('adminName')
        password = request.POST.get('password')
        password = make_password(password)
        admins = Admin.objects.filter(a_account=username)
        if not admins:
            Admin.objects.create(
                a_account=username,
                a_pwd=password
            )
        return HttpResponseRedirect(
            '/admin/alist/'
        )


@is_login
def addcate(request, who, num):
    if request.method == 'GET':
        data = {
            'cate': None,
        }
        if who == '1':
            if num != '0':
                data['cate'] = GCategory.objects.get(id=int(num))
            return render(request, 'admin/product-category-add.html', data)
        else:
            data['first'] = GCategory.objects.values()
            if num != '0':
                data['cate'] = GCategory2.objects.get(id=int(num))
            return render(request, 'admin/product-category-add2.html', data)
    else:
        if who == '1':
            if num == '0':
                cate = GCategory()
            else:
                cate = GCategory.objects.get(id=int(num))
            cate.c_name = request.POST.get('name')
            cate.c_desc = request.POST.get('text')
            cate.c_code = request.POST.get('code')
            cate.save()
        else:
            if num == '0':
                cate = GCategory2()
            else:
                cate = GCategory2.objects.get(id=int(num))
            cate.c_code_id = request.POST.get('sele')
            cate.c2_name = request.POST.get('name')
            cate.c2_desc = request.POST.get('text')
            cate.c2_code = request.POST.get('code')

            cate.save()
        return HttpResponseRedirect('/admin/pcate/')

@is_login
def delcate(request, who, num):
    if who == '1':
        GCategory.objects.get(id=num).delete()
    else:
        GCategory2.objects.get(id=num).delete()
    return JsonResponse({"code": 200})


def save_image(lists):
    g_info = ''
    for image in lists:

        save_name = str(int(time())) + image.name

        url = os.path.join(MEDIA_ROOT, save_name)
        destination = open(url, 'wb')
        for chunk in image.chunks():
            destination.write(chunk)
            g_info = g_info + str(os.path.join('/static/medias/', save_name)) + ','
        destination.close()
    return g_info

@is_login
def addproduct(request, who, num):
    if request.method == 'GET':

        first = GCategory.objects.values()
        data = {
            'first': first,
            'cate2': None,
        }
        if who != '1':
            # H = Goods.objects.all()
            u_data = Goods.objects.filter(id=int(num)).values()[0]
            u_data['number'] = u_data['g_goodsprops'].split(',')[0].split('：')[1]

            data['cate2'] = u_data
        return render(request, 'admin/pro-add.html', data)
    else:
        if who == '1':
            good = Goods()
        else:
            good = Goods.objects.get(id=int(num))
        good.g_name = request.POST.get('pname')
        good.g_desc = request.POST.get('desc')
        good.g_mktprice = request.POST.get('mktprice')
        good.g_price = request.POST.get('price')
        good.g_inventory = request.POST.get('inven')
        good.g_sale = request.POST.get('sale')
        good.c_code = request.POST.get('cate1')
        good.c2_code = request.POST.get('cate2')
        good.g_goodsprops = '商品编号：' + request.POST.get('number') + ','
        pic1, pic2 = [], []
        if 'pic1' in request.FILES:
            pic1 = request.FILES.getlist('pic1')
        if 'pic2' in request.FILES:
            pic2 = request.FILES.getlist('pic2')
        if pic2 and pic1 or who != '1':
            good.g_info = save_image(pic1)
            good.g_pics = save_image(pic2)
        else:
            return HttpResponseRedirect('/admin/index/')
        good.g_status = 0
        good.g_class = 0
        if who == '1':
            good.g_createtime = datetime.datetime.now()
        good.g_changetime = datetime.datetime.now()
        good.save()
        return HttpResponseRedirect('/admin/plist/')

@is_login
def getcate(request):
    code = request.GET.get('catecode')
    code = GCategory.objects.get(c_code=int(code)).id
    data = {
        'cate2': list(GCategory2.objects.filter(c_code=code).values())
    }

    return JsonResponse(data)

@is_login
def delpro(request, num):
    # Goods.objects.get(id=int(num)).remove()
    return JsonResponse({'code': 200})


def login(request):
    if request.method == 'GET':
        return render(request, 'admin/login.html')
    else:
        data = {
            'code': 200,
        }
        post = request.POST
        if not post.get('name', None):
            data['code'] = 1001
            data['msg'] = '用户名不能为空'
            return JsonResponse(data)

        if not post.get('pass', None):
            data['code'] = 1002
            data['msg'] = '密码不能为空'
            return JsonResponse(data)
        if not post.get('check_code', None):
            data['code'] = 1003
            data['msg'] = '验证码不能为空'
            return JsonResponse(data)
        if post.get('check_code').lower() != request.session['CheckCode'].lower():
            data['code'] = 1004
            data['msg'] = '验证码错误!'
            return JsonResponse(data)
        else:
            name = post.get('name')
            user = Admin.objects.filter(a_account=name)[0]
            if user:
                passwd = post.get('pass')
                if check_password(passwd, user.a_pwd):
                    request.session['id'] = user.id
                    # request.session.set_expiry(0)
                    return JsonResponse(data)
                else:
                    data['code'] = 2002
                    data['msg'] = '用户名或者密码错误'
                    return JsonResponse(data)
            else:
                data['code'] = 2001
                data['msg'] = '该用户不存在'
                return JsonResponse(data)

def logout(request):
    request.session.delete()
    return HttpResponseRedirect('/admin/login/')

def set_code(request):
    stream = BytesIO()  # 开辟一块内存空间，不用写在外存，减少读写操作
    img, code = create_validate_code()
    img.save(stream, 'PNG')
    request.session['CheckCode'] = code
    request.session.set_expiry(0)
    # print(code)
    return HttpResponse(stream.getvalue())

@is_login
def pcate(request):
    data = {
        'first': GCategory.objects.all(),
        'second': GCategory2.objects.all(),
    }
    return render(request, 'admin/product-category.html', data)


@is_login
def plist(request):
    allgoods = Goods.objects.values()
    for good in allgoods:
        del good['g_info']
        good['g_pics'] = good['g_pics'].split(',')[0]

    data = {
        'all': allgoods,
    }

    return render(request, 'admin/product-list.html', data)



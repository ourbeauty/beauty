from datetime import datetime
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render


# Create your views here.

from App.models import Orders, User, Address, Admin


def index(request):
    return render(request, 'admin/index.html')


def weclome(request):
    return render(request, 'admin/welcome.html')


def log(request):
    return render(request, 'admin/system-log.html')


def changepass(request):
    if request.method == 'GET':
        user = request.user
        if user and user.id:
            administrator = Admin.objects.filter(pk=user.id).first()
            return render(request, 'admin/change-password.html', {'ad': administrator})
    if request.method == 'POST':
        a = Admin()
        p1 = request.POST.get('newpassword')
        p2 = request.POST.get('newpassword2')
        if p1 == p2:
            a.a_pwd = p1
            a.save()
            return HttpResponseRedirect(
                '/admin/changepass/'
            )

def charts7(request):
    return render(request, 'admin/charts-7.html')


def charts6(request):
    return render(request, 'admin/charts-6.html')

def charts5(request):
    return render(request, 'admin/charts-5.html')

def charts4(request):
    return render(request, 'admin/charts-4.html')


def charts3(request):
    return render(request, 'admin/charts-3.html')

def charts2(request):
    return render(request, 'admin/charts-2.html')

def charts1(request):
    return render(request, 'admin/charts-1.html')

def alist(request):
    if request.method == 'GET':
        admins = Admin.objects.all()
        return render(request, 'admin/admin-list.html', {'admins':admins})

def aper(request):
    return render(request, 'admin/admin-permission.html')

def arol(request):
    return render(request, 'admin/admin-role.html')

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


def plist(request):
    return render(request, 'admin/product-list.html')

def pcate(request):
    return render(request, 'admin/product-category.html')

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
        myorder.o_changetime = datetime.now()
        myorder.save()
        return JsonResponse(data)


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


def adminadd(request):
    if request.method == 'GET':
        return render(request, 'admin/admin-add.html')
    if request.method == 'POST':
        username = request.POST.get('adminName')
        password = request.POST.get('password')
        admins = Admin.objects.filter(a_account=username)
        if not admins:
            Admin.objects.create(
                a_account=username,
                a_pwd=password
            )
        return HttpResponseRedirect(
            '/admin/alist/'
        )
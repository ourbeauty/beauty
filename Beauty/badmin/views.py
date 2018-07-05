from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse

# Create your views here.
from App.models import GCategory, GCategory2, Goods


def index(request):
    return render(request, 'admin/index.html')


def weclome(request):
    return render(request, 'admin/welcome.html')


def log(request):
    return render(request, 'admin/system-log.html')


def changepass(request):
    return render(request, 'admin/change-password.html')


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
    return render(request, 'admin/admin-list.html')


def aper(request):
    return render(request, 'admin/admin-permission.html')


def arol(request):
    return render(request, 'admin/admin-role.html')


def mlist(request):
    return render(request, 'admin/member-list.html')


def plist(request):
    allgoods = Goods.objects.values()
    for good in allgoods:
        del good['g_info']
        good['g_pics'] = good['g_pics'].split(',')[0]

    data = {
        'all': allgoods,
    }

    return render(request, 'admin/product-list.html', data)


def pcate(request):
    data = {
        'first': GCategory.objects.all(),
        'second': GCategory2.objects.all(),
    }
    return render(request, 'admin/product-category.html', data)


def olist(request):
    return render(request, 'admin/picture-list.html')


def addcate(request, who, num):
    if request.method == 'GET':
        if who == '1':
            data = {
                'cate': None,
            }
            if num != '0':
                data = {
                    'cate': GCategory.objects.get(id=int(num)),
                }
            return render(request, 'admin/product-category-add.html', data)
        else:
            data = {
                'first': GCategory.objects.all(),
                'cate': None,
            }
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
            cate.c2_name = request.POST.get('name')
            cate.c2_desc = request.POST.get('text')
            cate.c2_code = request.POST.get('code')
            cate.c_code_id = request.POST.get('sele')
            cate.save()
        return HttpResponseRedirect('/admin/pcate/')


def delcate(request, who, num):
    if who == '1':
        GCategory.objects.get(id=num).delete()
    else:
        GCategory2.objects.get(id=num).delete()
    return JsonResponse({"code": 200})

def addproduct(request, who, num):

    return render(request, 'admin/pro-add.html')

def getcate(request):
    code = request.GET.get('catecode')
    code = GCategory.objects.get(c_code=int(code)).id
    data = {
        'cate2': list(GCategory2.objects.filter(c_code=code).values())
    }

    return JsonResponse(data)

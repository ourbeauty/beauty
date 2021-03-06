from django.core.paginator import Paginator

from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse

# Create your views here.
from App_zl.models import GCategory, GCategory2, Goods, Cart, Orders, Goodsorder, User, Address


def dizhi(request):
    if request.method == 'GET':
        id = request.session.get('user_id')
        if id:
            users = User.objects.all()
            addrs = Address.objects.filter(use_id=id)
            return render(request, 'dizhi_liebiao.html', {'addrs': addrs, 'users': users})
        else:
            return HttpResponseRedirect(reverse('zl:classify'))
        # users = User.objects.all()
        # addrs = Address.objects.filter(use_id=1)
        # return render(request, 'dizhi_liebiao.html', {'addrs': addrs, 'users': users})


# 增加地址
def adddizhi(request):
    if request.method == 'GET':
        id = request.session.get('user_id')
        if id:
            return render(request, 'tianxie_dizhi.html')
        # return render(request, 'tianxie_dizhi.html')
    elif request.method == 'POST':
        tel = request.POST.get('mobile')
        province = request.POST.get('province')
        city = request.POST.get('city')
        county = request.POST.get('county')
        street = request.POST.get('street')
        addrstatus = request.POST.get('addstatus')
        email = request.POST.get('email')
        address = request.POST.get('address')
        id = request.session.get('user_id')
        if id:
            if addrstatus == '1':
                addrs = Address.objects.filter(use_id=id)
                for a in addrs:
                    a.u_addrstatus = 0
                    a.save()
                Address.objects.create(
                    use_id=id,
                    u_tel=tel,
                    u_provinces=province,
                    u_city=city,
                    u_county=county,
                    u_addrstatus=addrstatus,
                    u_street=street,
                    u_email=email,
                    u_detailaddr=address
                )
            elif addrstatus == '0':
                Address.objects.create(
                    use_id=id,
                    u_tel=tel,
                    u_provinces=province,
                    u_city=city,
                    u_county=county,
                    u_street=street,
                    u_addrstatus=addrstatus,
                    u_email=email,
                    u_detailaddr=address
                )
            else:
                return HttpResponseRedirect(
                reverse('zl:dizhi')
            )
            return HttpResponseRedirect(
                reverse('zl:dizhi')
            )


def deldizhi(request, id):
    if request.method == 'GET':
        Address.objects.filter(id=id).delete()
        return HttpResponseRedirect(reverse('zl:dizhi'))


# 改变地址
def changedizhi(request, id):
    if request.method == 'GET':
        s_id = request.session.get('user_id')
        if s_id:
            addrs = Address.objects.filter(id=id)
            return render(request, 'xiugai_dizhi.html', {'addrs': addrs})
    if request.method == 'POST':
        tel = request.POST.get('mobile')
        province = request.POST.get('province')
        city = request.POST.get('city')
        county = request.POST.get('county')
        addrstatus = request.POST.get('addstatus')
        email = request.POST.get('email')
        address = request.POST.get('address')
        addr = Address.objects.filter(id=id).first()
        user = request.user
        if addrstatus == '1':
            addrs = Address.objects.filter(use_id=user.id)
            for a in addrs:
                a.u_addrstatus = 0
                a.save()
            addr.u_tel = tel
            addr.u_provinces = province
            addr.u_city = city
            addr.u_county = county
            addr.u_addrstatus = addrstatus
            addr.u_email = email
            addr.u_detailaddr = address
            addr.save()
        elif addrstatus == '0':
            addr.u_tel = tel
            addr.u_provinces = province
            addr.u_city = city
            addr.u_county = county
            addr.u_addrstatus = addrstatus
            addr.u_email = email
            addr.u_detailaddr = address
            addr.save()
        else:
            return HttpResponseRedirect(
                reverse('zl:dizhi')
            )
        return HttpResponseRedirect(
            reverse('zl:dizhi')
        )


def classify(request):
    if request.method == 'GET':
        gcategorys = GCategory.objects.all()
        gcategory2s = GCategory2.objects.all()
        data = {
            'gcategorys': gcategorys,
            'gcategory2s': gcategory2s,
        }
        return render(request, 'fenlei.html', data)


def classify_list(request, code):
    if request.method == 'GET':
        goods = Goods.objects.filter(c_code=code) or Goods.objects.filter(c2_code=code)
        if goods:

            for good in goods:
                images_list = good.g_pics
                image = images_list.split(',')[0]
                good.g_pics = image
                good.discount = round(10 * (float(good.g_price) / float(good.g_mktprice)))

            # 分页
            page_id = request.GET.get('page_id', 1)
            paginator = Paginator(goods, 3)
            page = paginator.page(int(page_id))

            data = {'goods': page, 'code': code}
            return render(request, 'liebiao.html', data)
        else:
            return HttpResponseRedirect(
                reverse('zl:classify')
            )


def add_one_cart(request):
    goods_id = request.GET.get('id')
    g_inventory= request.GET.get('g_inventory')
    g_code = request.GET.get('code')
    id = request.session.get('user_id')
    if id:
        if int(g_inventory) >= 1:
            # if user and user.id:
            user_carts = Cart.objects.filter(g_id=goods_id).first()
            if user_carts:
                user_carts.g_num += 1
                user_carts.save()
            else:
                Cart.objects.create(
                    u_id=id,
                    g_id=goods_id,
                    g_num=1,
                    is_select=1
                )
            data = {'code': 200}
            return JsonResponse(data)
        else:
            data = {'code': 900}
            return JsonResponse(data)
    else:
        data = {'code': 2000,'g_code':g_code}
        return JsonResponse(data)


def show(request, goods_id=70):
    if request.method == 'GET':
        goods = Goods.objects.filter(id=goods_id).first()

        # 详情图片
        images_info = goods.g_info
        image_info = images_info[:-1].split(',')
        goods.g_info = image_info

        # 小图
        images_pics = goods.g_pics
        image_pics = images_pics[:-1].split(',')
        goods.g_pics = image_pics

        # 炫罗兰http://www.maxfactorcn.com/images//20170714/fb74bf8f934c2e2a.jpg,
        # 颜色图
        image_colors = goods.g_class
        if len(image_colors) != 1:
            image_color_list = image_colors[:-1].split(',')

            dict = {}
            for image_color in image_color_list:
                image_p_w = image_color.split('http')
                image_p_w[1] = 'http' + image_p_w[1]
                url = image_p_w[1]
                dict[url] = image_p_w[0]

            goods.g_class = dict
        else:
            dict = {}
            goods.g_class = dict

        goods.discount = round(10 * (float(goods.g_price) / float(goods.g_mktprice)))

        data = {'goods': goods}

        return render(request, 'chanpin_xx.html', data)


def subgoods(request):
    number = int(request.GET.get('number'))

    if number >= 2 and number < 200:
        number -= 1
        data = {'number': number, 'code': 200}
        return JsonResponse(data)
    else:
        data = {'number': 0, 'code': 900}
        return JsonResponse(data)


def addgoods(request):
    number = int(request.GET.get('number'))

    if number > 0 and number < 200:
        number += 1
        data = {'number': number, 'code': 200}
        return JsonResponse(data)
    else:
        data = {'number': 0, 'code': 900}
        return JsonResponse(data)


def add_cart(request):
    number1 = request.GET.get('number')
    goods_id = request.GET.get('id')
    g_inventory = request.GET.get('g_inventory')


    id = request.session.get('user_id')
    if id:
        if int(g_inventory) >= int(number1):
            # if user and user.id:
            user_carts = Cart.objects.filter(g_id=goods_id).first()
            if user_carts:
                user_carts.g_num += int(number1)
                user_carts.save()
            else:
                Cart.objects.create(
                    u_id=id,
                    g_id=goods_id,
                    g_num=number1,
                    is_select=1
                )
            data = {'code': 200}
            return JsonResponse(data)
        else:
            data = {'code': 900}
            return JsonResponse(data)
    else:
        data = {'code': 1000, 'goods_id': goods_id}
        return JsonResponse(data)



def cart(request):
    return render(request,'cart.html')


def buy(request):
    number1 = request.GET.get('number')
    goods_id = request.GET.get('id')
    g_inventory = request.GET.get('g_inventory')
    if int(g_inventory) >= int(number1):
        u_id = request.session.get('user_id')
        if u_id:
            goods = Goods.objects.filter(id=goods_id).first()
            price = goods.g_price

            Orders.objects.create(
                u_id=u_id,
                o_price=price,
                o_num=number1,
                o_status=0
            )
            o_id = Orders.objects.filter(u_id=u_id).last().id
            Goodsorder.objects.create(
                g_id=goods_id,
                ord_id=o_id,
                g_order_num=number1
            )
            data = {'code': 200}

            return JsonResponse(data)
        else:
            data = {'code':1000,'goods_id':goods_id}
            return JsonResponse(data)


    else:
        data = {'code': 900}
        return JsonResponse(data)


def order(request):
    return HttpResponseRedirect(
        reverse('yxr:allorders')
    )

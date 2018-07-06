from django.shortcuts import render
import re
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from App.models import Address, User
from App.models import GCategory, GCategory2, Goods, Cart, Orders, Goodsorder

def dizhi(request):
    if request.method == 'GET':
        user = request.user
        if user and user.id:
            users = User.objects.all()
            addrs = Address.objects.filter(use_id=user.id)
            return render(request, 'dizhi_liebiao.html', {'addrs': addrs, 'users': users})
        # users = User.objects.all()
        # addrs = Address.objects.filter(use_id=1)
        # return render(request, 'dizhi_liebiao.html', {'addrs': addrs, 'users': users})

# 增加地址
def adddizhi(request):
    if request.method == 'GET':
        user = request.user
        if user and user.id:
            return render(request,'tianxie_dizhi.html')
        # return render(request, 'tianxie_dizhi.html')
    if request.method == 'POST':
        tel = request.POST.get('mobile')
        province = request.POST.get('province')
        city = request.POST.get('city')
        county = request.POST.get('county')
        street = request.POST.get('street')
        addrstatus = request.POST.get('addstatus')
        email = request.POST.get('email')
        address = request.POST.get('address')
        user = request.user
        if user and user.id:
            if addrstatus == '1':
                addrs = Address.objects.filter(use_id=user.id)
                for a in addrs:
                    a.u_addrstatus = 0
                    a.save()
                Address.objects.create(
                    use_id=user.id,
                    u_tel=tel,
                    u_provinces=province,
                    u_city=city,
                    u_county=county,
                    u_addrstatus=addrstatus,
                    u_street=street,
                    u_email=email,
                    u_detailaddr=address
                )
            else:
                Address.objects.create(
                    use_id=user.id,
                    u_tel=tel,
                    u_provinces=province,
                    u_city=city,
                    u_county=county,
                    u_street=street,
                    u_addrstatus=addrstatus,
                    u_email=email,
                    u_detailaddr=address
                )
            return HttpResponseRedirect(
                reverse('a:dizhi')
            )
        # user = request.user
        # if user and user.id:
        #     if addrstatus:
        #         addrs = Address.objects.filter(use_id=user.id)
        #         for a in addrs:
        #             a.u_addrstatus = 0
        #             a.save()
        #         Address.objects.create(
        #             use_id=user.id,
        #             u_tel=tel,
        #             u_provinces=province,
        #             u_city=city,
        #             u_county=county,
        #             u_addrstatus=addrstatus,
        #             u_email=email,
        #             u_detailaddr=address
        #         )
        #     else:
        #         Address.objects.create(
        #             use_id=user.id,
        #             u_tel=tel,
        #             u_provinces=province,
        #             u_city=city,
        #             u_county=county,
        #             u_addrstatus=addrstatus,
        #             u_email=email,
        #             u_detailaddr=address
        #         )
        #     return HttpResponseRedirect(
        #         reverse('a:dizhi')
        #     )



# 改变地址
def changedizhi(request,id):
    if request.method == 'GET':
        addrs = Address.objects.filter(id=id)
        return render(request, 'xiugai_dizhi.html',{'addrs': addrs})
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
        else:
            addr.u_tel = tel
            addr.u_provinces = province
            addr.u_city = city
            addr.u_county = county
            addr.u_addrstatus = addrstatus
            addr.u_email = email
            addr.u_detailaddr = address
            addr.save()
        return HttpResponseRedirect(
            reverse('a:dizhi')
        )

        """if addrstatus == '1':
            addrs = Address.objects.filter(use_id=1)
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
        else:
            addr.u_tel = tel
            addr.u_provinces = province
            addr.u_city = city
            addr.u_county = county
            addr.u_addrstatus = addrstatus
            addr.u_email = email
            addr.u_detailaddr = address
            addr.save()
        return HttpResponseRedirect(
            reverse('a:dizhi')
        )"""

        # user = request.user
        # if user and user.id:
        #     if addrstatus:
        #         addrs = Address.objects.filter(use_id=user.id)
        #         for a in addrs:
        #             a.u_addrstatus = 0
        #             a.save()
        #         Address.objects.create(
        #             use_id=user.id,
        #             u_tel=tel,
        #             u_provinces=province,
        #             u_city=city,
        #             u_county=county,
        #             u_addrstatus=addrstatus,
        #             u_email=email,
        #             u_detailaddr=address
        #         )
        #     else:
        #         Address.objects.create(
        #             use_id=user.id,
        #             u_tel=tel,
        #             u_provinces=province,
        #             u_city=city,
        #             u_county=county,
        #             u_addrstatus=addrstatus,
        #             u_email=email,
        #             u_detailaddr=address
        #         )
        #     return HttpResponseRedirect(
        #         reverse('a:dizhi')
        #     )


def deldizhi(request,id):
    if request.method == 'GET':
        Address.objects.filter(id=id).delete()
        return HttpResponseRedirect(reverse('a:dizhi'))

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
                good.discount = round(10*(float(good.g_price)/float(good.g_mktprice)))

            data = {'goods': goods}
            return render(request, 'liebiao.html', data)
        else:
            return render(request, 'not_found.html')


def show(request, goods_id=19):
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
        if image_colors != 0 :
            image_color = image_colors[:-1].split('http')
            image_color[1] = 'http' + image_color[1]
            goods.g_class_p = image_color[1][:-1]
            goods.g_class_w = image_color[0]

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
    user = 1
    # if user and user.id:
    user_carts = Cart.objects.filter(g_id=goods_id).first()
    if user_carts:
        user_carts.g_num +=int(number1)
        user_carts.save()
    else:
        Cart.objects.create(
            u_id=user,
            g_id=goods_id,
            g_num=number1,
            is_select=1
        )
    data = {'code': 200}
    return JsonResponse(data)


def cart(request):
    return render(request, 'cart.html')


def buy(request):

    number1 = request.GET.get('number')
    goods_id = request.GET.get('id')
    user = 1
    goods = Goods.objects.filter(id=goods_id).first()
    price = goods.g_price



    Orders.objects.create(
        u_id=user,
        o_price=price,
        o_num=number1,
        o_status=0
    )
    o_id = Orders.objects.filter(u_id=user).last().id
    Goodsorder.objects.create(
        g_id=goods_id,
        ord_id=o_id
    )
    data = {'code': 200}
    return JsonResponse(data)


def order(request):
    return render(request, 'order.html')




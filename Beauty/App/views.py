import re

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from App.models import GCategory, GCategory2, Goods, Cart, Orders, Goodsorder


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
        goods = Goods.objects.filter(c_code__in=code) or Goods.objects.filter(c2_code=code)
        if goods:

            for good in goods:
                images_list = good.g_pics
                image = images_list.split(',')[0]
                good.g_pics = image
                good.discount = round(10 * (float(good.g_price) / float(good.g_mktprice)))
            # 传入查找类别的code

            # 分页
            page_id = request.GET.get('page_id', 1)
            paginator = Paginator(goods, 3)
            page = paginator.page(int(page_id))

            data = {'goods': page, 'code': code}
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
        if image_colors != 0:
            image_color_list = image_colors[:-1].split(',')

            dict = {}
            for image_color in image_color_list:
                image_p_w = image_color.split('http')
                image_p_w[1]= 'http' + image_p_w[1]
                url = image_p_w[1]
                dict[url] = image_p_w[0]


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
    if int(g_inventory) >= int(number1):
        user = 1

        # if user and user.id:
        user_carts = Cart.objects.filter(g_id=goods_id).first()
        if user_carts:
            user_carts.g_num += int(number1)
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
    else:
        data = {'code':900}
        return JsonResponse(data)



def cart(request):
    return render(request, 'cart.html')


def buy(request):
    number1 = request.GET.get('number')
    goods_id = request.GET.get('id')
    g_inventory = request.GET.get('g_inventory')
    if int(g_inventory) >= int(number1):
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
    else:
        data = {'code':900}
        return JsonResponse(data)


def order(request):
    return render(request, 'order.html')





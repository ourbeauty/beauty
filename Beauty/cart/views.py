import json
import re

import time

import datetime
from django.shortcuts import render, redirect
import os, django

from cart.nutil_pay import AliPay

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Beauty.settings")  # project_name 项目名称
django.setup()

from cart.models import *
from django.http import JsonResponse, HttpResponse
from django.core.urlresolvers import reverse

from django.http import HttpResponseRedirect


# 购物车页面


# 装饰器判断用户是否登录
def user_login(func):
    def wrapper(request, *args, **kwargs):
        user_id = request.session.get('user_id')
        if user_id:
            end = func(request, *args, **kwargs)
            return end
        else:
            return HttpResponseRedirect(reverse('yxr:login'))

    return wrapper


@user_login
def cart(request):
    return render(request, 'cart.html')


@user_login
def user_cart(request):
    user_id = int(request.session.get('user_id'))
    carts = Cart.objects.filter(u_id=user_id)
    goods_desc = []
    total = 0
    mkttotal = 0
    for cart in carts:
        goods = {}
        try:
            if cart.is_select == 1:
                goods['cart_num'] = cart.g_num
                goods['cart_is_del'] = cart.is_select
                good = Goods.objects.filter(id=cart.g_id).first()
                goods['pic_url'] = good.g_pics.split(',')[0]
                goods['g_name'] = re.search(r'([\w\u2E80-\u9FFF]+)', good.g_name).group()
                goods['good_color'] = re.search(r'(.*?[\u4e00-\u9fa5]+)|(.*?[\d+])',
                                                good.g_class.replace('#', u'号')).group()
                goods['good_price'] = good.g_price
                goods['good_mktprice'] = good.g_mktprice
                goods['good_desc'] = GCategory.objects.filter(c_code=good.c_code).first().c_desc
                goods['id'] = good.id
                goods['total'] = cart.g_num * float(good.g_price)
                goods['mkttotal'] = int(cart.g_num) * float(good.g_mktprice)
                total += int(cart.g_num) * float(good.g_price)
                mkttotal += int(cart.g_num) * float(good.g_mktprice)
                goods_desc.append(goods)
        except:
            pass
    mkttotal = mkttotal - total
    data = {'code': 200, 'goods': goods_desc, 'total': total, 'mkttotal': mkttotal}
    return JsonResponse(data)


#  订单操作
@user_login
def cart_choice(request):
    g_id = request.GET.get('g_id')
    code = request.GET.get('code')
    good_cart = Cart.objects.filter(g_id=g_id).first()
    good = Goods.objects.filter(id=good_cart.g_id).first()
    if code == 'true':
        good_cart.is_select = 0
        good_cart.g_num = 0
        good_cart.save()
    else:
        good_num = request.GET.get('good_num')
        good_cart.is_select = 1
        good_cart.g_num = int(good_num)
        good_cart.save()
    return JsonResponse({'code': 200, 'good_price': good.g_price, 'good_mktprice': good.g_mktprice})


# 增加和减少商品
@user_login
def cart_add_sub(request):
    good_id = request.GET.get('good_id')
    print(good_id)
    good_cart = Cart.objects.filter(g_id=good_id).first()
    good = Goods.objects.filter(id=good_cart.g_id).first()
    status = request.GET.get('status')
    if status == '1':
        try:
            good_cart.g_num += 1
            good_cart.save()
        except:
            return JsonResponse({'code': 504})
        mkt_price = float(good.g_mktprice) - float(good.g_price)
        return JsonResponse({'code': 200, 'good_price': good.g_price,
                             'good_mktprice': good.g_mktprice, 'mkt_price': mkt_price})
    else:
        try:
            if good_cart.g_num > 1:
                good_cart.g_num -= 1
                good_cart.save()
        except:
            return JsonResponse({'code': 504})
        mkt_price = float(good.g_mktprice) - float(good.g_price)
        return JsonResponse({'code': 200, 'good_price': good.g_price,
                             'good_mktprice': good.g_mktprice, 'mkt_price': mkt_price})


# 默认user_id =1
# 全删和全加
@user_login
def all_goods_cart(request):
    status = request.GET.get('status')
    goods_desc = []
    user_id = int(request.session.get('user_id'))
    carts = Cart.objects.filter(u_id=user_id)
    if int(status) == 1:
        for cart in carts:
            good = {}
            cart.is_select = 0
            cart.g_num = 0
            cart.save()
            good['g_id'] = cart.g_id
            goods_desc.append(good)
        data = {'code': 200, 'goods': goods_desc}
        return JsonResponse(data)
    if status == '2':
        carts = request.GET.get('carts_list')
        # 把字符字符串 类型列表转化成列表
        carts = json.loads(carts)
        total = 0
        mkttotal = 0
        for key, value in carts.items():
            cart = {}
            good = Goods.objects.filter(id=int(key)).first()
            user_cart = Cart.objects.filter(g_id=int(key)).first()
            user_cart.g_num = int(value)
            user_cart.is_select = 1
            user_cart.save()
            cart['g_id'] = key
            goods_desc.append(cart)
            total += int(user_cart.g_num) * float(good.g_price)
            mkttotal += int(user_cart.g_num) * float(good.g_mktprice)
        mkttotal = mkttotal - total
        print(mkttotal)
        data = {'code': 200, 'goods': goods_desc, 'total': total, 'mktprice': mkttotal}
        return JsonResponse(data)


# 创建订单购物车 所有商品订单订单
@user_login
def all_create_order(request):
    user_id = int(request.session.get('user_id'))
    orders = request.GET.get('orders')
    orders = json.loads(orders)
    print(orders)
    total_price = 0
    mkt_total_price = 0
    for key in list(orders):
        good = Goods.objects.filter(id=int(key)).first()
        total_price += float(good.g_price) * int(orders[key])
        mkt_total_price += float(good.g_mktprice) * int(orders[key])
        good_orders = Goodsorder.objects.filter(g_id=int(key))
        if good_orders.count():
            order_ids = []
            for good_order in good_orders:
                order_ids.append(good_order.ord_id)
            order_ids = set(order_ids)
            for order_id in order_ids:
                order = Orders.objects.filter(id=order_id).first()
                if order.o_status == 0:
                    # 操作订单表
                    order.o_num += int(orders[key])
                    order.o_price = float(Goods.objects.filter(id=int(key)).first().g_price) + order.o_price
                    order.save()
                    # 操作Goodsorder表
                    good_order = Goodsorder.objects.filter(ord_id=order.id, g_id=int(key)).first()
                    good_order.g_order_num += int(orders[key])
                    good_order.save()
                    # 操作购物车表
                    cart = Cart.objects.filter(g_id=int(key)).first()
                    cart.is_select = 0
                    cart.g_num = 0
                    cart.save()
                    del orders[key]
                    break
    num = 0
    total = 0
    for key, value in orders.items():
        num += int(value)
        good = Goods.objects.filter(id=int(key)).first()
        total += float(good.g_price)
        # 操作购物车
        cart = Cart.objects.filter(g_id=int(key)).first()
        cart.is_select = 0
        cart.g_num = 0
        cart.save()
    if len(orders) > 0:
        order_time = datetime.datetime.now() + datetime.timedelta(hours=8)
        # 创建订单
        Orders.objects.create(
            o_creattime=order_time,
            o_num=num,
            u_id=user_id,
            o_price=total,
            o_status=0
        )
        # 创建goodorder
        for key, value in orders.items():
            Goodsorder.objects.create(
                ord_id=Orders.objects.filter(o_creattime=order_time).first().id,
                g_id=int(key),
                g_order_num=int(value)
            )
            cart = Cart.objects.filter(g_id=int(key)).first()
            cart.is_select = 0
            cart.save()
    mkt_total_price = mkt_total_price - total_price
    data = {'code': 200, 'total_price': total_price, 'mkt_total_price': mkt_total_price}
    return JsonResponse(data)


# 穿件单个商品订单

def creat_order(g_id, g_num, order_time, user_id):
    total = int(g_num) * float(Goods.objects.filter(id=int(g_id)).first().g_price)
    Orders.objects.create(
        o_creattime=order_time,
        o_num=g_num,
        u_id=user_id,
        o_price=total,
        o_status=0
    )
    Goodsorder.objects.create(
        ord_id=Orders.objects.filter(o_creattime=order_time).first().id,
        g_id=int(g_id),
        g_order_num=int(g_num)
    )
    cart = Cart.objects.filter(g_id=g_id).first()
    cart.is_select = 0
    cart.g_num = 0
    cart.save()


@user_login
def one_create_order(request):
    user_id = int(request.session.get('user_id'))
    g_id = request.GET.get('g_id')
    g_num = request.GET.get('g_num')
    good = Goods.objects.filter(id=int(g_id)).first()
    total_price = float(good.g_price) * int(g_num)
    mkt_total_price = float(good.g_mktprice) * int(g_num)
    order_time = datetime.datetime.now() + datetime.timedelta(hours=8)
    goods = Goodsorder.objects.filter(g_id=int(g_id))
    if not goods.count():
        creat_order(g_id, g_num, order_time, user_id)
    else:
        order_ids = []
        for good in goods:
            order_ids.append(good.ord_id)
        order_ids = set(order_ids)
        order_loop = 0
        for order_id in order_ids:
            order = Orders.objects.filter(id=order_id).first()
            if order.o_status == 0:
                order.o_num += int(g_num)
                order.o_price = float(Goods.objects.filter(id=int(g_id)).first().g_price) + order.o_price
                order.save()
                good_order = Goodsorder.objects.filter(ord_id=order.id, g_id=int(g_id)).first()
                good_order.g_order_num += int(g_num)
                good_order.save()
                cart = Cart.objects.filter(g_id=int(g_id)).first()
                cart.is_select = 0
                cart.g_num = 0
                cart.save()
                break
            order_loop += 1
        if order_loop == len(order_ids):
            creat_order(g_id, g_num, order_time, user_id)
    mkt_total_price = mkt_total_price - total_price
    data = {'code': 200, 'total_price': total_price, 'mkt_total_price': mkt_total_price}
    return JsonResponse(data)


# 订单页面
@user_login
def order(request):
    return render(request, 'daizhifu.html')


# 跳转结算页面
@user_login
def setlement1(request):
    return render(request, 'setlement.html')


# 默认usrr_id
@user_login
def user_settlement(request):
    user_id = int(request.seesion.get('user_id'))
    user_info = Address.objects.filter(use_id=user_id).first()
    user = User.objects.filter(id=user_id).first()
    user_order = {}
    user_order['addr'] = user_info.u_detailaddr
    user_order['name'] = user.u_name
    data = {'code': 200, 'order': user_order}
    return JsonResponse(data)


@user_login
def immediately_pay(request):
    user_id = request.seesion.get('user_id')
    order_id = request.GET.get('order_id')
    order = Orders.objects.filter(id=int(order_id)).first()
    user_info = Address.objects.filter(use_id=user_id).first()
    user = User.objects.filter(id=user_id).first()
    user_order = {}
    user_order['addr'] = user_info.u_detailaddr
    user_order['name'] = user.u_name
    user_order['total_price'] = order.o_price
    good_orders = Goodsorder.objects.filter(ord_id=int(order_id))
    mktprice = 0
    for good_order in good_orders:
        mktprice += float(Goods.objects.filter(id=good_order.g_id).first().g_mktprice)
    user_order['mktprice'] = mktprice - order.o_price
    data = {'code': 200, 'order': user_order}
    return JsonResponse(data)


# 配置 沙箱 pc端
def get_ali_object():
    # 沙箱环境地址：https://openhome.alipay.com/platform/appDaily.htm?tab=info
    app_id = "2016091400507578"  # APPID （沙箱应用）
    # 支付完成后，支付偷偷向这里地址发送一个post请求，识别公网IP,如果是 192.168.20.13局域网IP ,支付宝找不到，def page2() 接收不到这个请求
    notify_url = "http://127.0.0.1:8804/page2/"

    # 支付完成后，跳转的地址。
    return_url = "http://127.0.0.1:8804/page2/"

    merchant_private_key_path = "static/cart/keys/app_private_2048.txt"  # 应用私钥
    alipay_public_key_path = "static/cart/keys/alipay_public_2048.txt"  # 支付宝公钥

    alipay = AliPay(
        appid=app_id,
        app_notify_url=notify_url,
        return_url=return_url,
        app_private_key_path=merchant_private_key_path,
        alipay_public_key_path=alipay_public_key_path,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥
        debug=True,  # 默认False,
    )
    return alipay


# 默认user_id
@user_login
def pay_page1(request):
    user_id = request.seesion.get('user_id')
    # 根据当前用户的配置，生成URL，并跳转。
    # money = float(request.POST.get('money'))
    money = 0
    carts = Cart.objects.filter(u_id=user_id)
    for cart in carts:
        if cart.is_select == 1:
            good = Goods.objects.filter(id=cart.g_id).first()
            money += float(good.g_price) * cart.g_num
    # if money==0:
    #     return redirect()
    alipay = get_ali_object()
    # 生成支付的url
    query_params = alipay.direct_pay(
        subject="付款方：" + str(User.objects.filter(id=user_id).first().u_name),  # 商品简单描述
        out_trade_no="x2" + str(time.time()),  # 用户购买的商品订单号（每次不一样） 20180301073422891
        total_amount=money,  # 交易金额(单位: 元 保留俩位小数)
    )

    pay_url = "https://openapi.alipaydev.com/gateway.do?{0}".format(query_params)  # 支付宝网关地址（沙箱应用）

    return redirect(pay_url)


def pay_over(request):
    alipay = get_ali_object()
    if request.method == "POST":
        # 检测是否支付成功
        # 去请求体中获取所有返回的数据：状态/订单号
        from urllib.parse import parse_qs
        # name&age=123....
        body_str = request.body.decode('utf-8')
        post_data = parse_qs(body_str)

        post_dict = {}
        for k, v in post_data.items():
            post_dict[k] = v[0]

        # post_dict有10key： 9 ，1
        sign = post_dict.pop('sign', None)
        status = alipay.verify(post_dict, sign)
        print('------------------开始------------------')
        print('POST验证', status)
        print(post_dict)
        out_trade_no = post_dict['out_trade_no']

        # 修改订单状态
        # models.Order.objects.filter(trade_no=out_trade_no).update(status=2)
        print('------------------结束------------------')
        # 修改订单状态：获取订单号
        return HttpResponse('POST返回')

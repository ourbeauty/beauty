from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse


from App_zc.models import Goods,GCategory
# Create your views here.


# 首页
def Index(request):

    if request.method == 'GET':
        datas= Goods.objects.all()

        #Goods.objects.raw('select * from App_Goods order_by("g_price")')

        # 轮播图
        wimage1 = Goods.objects.order_by('-id').values()[0]
        wimage1['g_info'] = wimage1['g_info'].split(',')[0]
        wimage2 = Goods.objects.order_by('-id').values()[1]
        wimage2['g_info'] = wimage2['g_info'].split(',')[0]

        # for wheel in datas[4:8:2]:
        #     wimage.append(wheel.g_info.split(',')[0])

        # 新奇库
        new = Goods.objects.order_by('-id').values()[1]
        new['g_info'] = new['g_info'].split(',')[2]
        # news = Goods.objects.raw('select * from goods order by -id')
        # new = news[0].g_info.split(',')[0]

        # 特卖会
        sale = Goods.objects.order_by('g_price').values()[0]
        sale['g_pics'] = sale['g_pics'].split(',')[0]

        # 即将销售
        selling = Goods.objects.order_by('id').values()[4]
        selling['g_pics'] = selling['g_pics'].split(',')[0]

        # 正流行
        fashion = Goods.objects.order_by('-id').values()[5]
        fashion['g_pics'] = fashion['g_pics'].split(',')[0]

        # 底妆专区
        d_makeup = Goods.objects.filter(c_code=2000)
        d0 = d_makeup.values()[0]
        d1 = d_makeup.values()[1]
        d2 = d_makeup.values()[2]

        d0['g_info'] = d0['g_info'].split(',')[0]

        d1['g_pics'] = d1['g_pics'].split(',')[0]

        d2['g_pics'] = d2['g_pics'].split(',')[0]


        # 眼妆专区
        y_makeup = Goods.objects.filter(c_code=3000)

        y0 = y_makeup.values()[0]
        y1 = y_makeup.values()[1]
        y2 = y_makeup.values()[2]

        y0['g_info'] = y0['g_info'].split(',')[0]

        y1['g_pics'] = y1['g_pics'].split(',')[0]

        y2['g_pics'] = y2['g_pics'].split(',')[0]

        # 唇妆专区
        c_makeup = Goods.objects.filter(c_code=4000)

        c0 = c_makeup.values()[0]
        c1 = c_makeup.values()[1]
        c2 = c_makeup.values()[2]

        c0['g_info'] = c0['g_info'].split(',')[0]

        c1['g_pics'] = c1['g_pics'].split(',')[0]

        c2['g_pics'] = c2['g_pics'].split(',')[0]

        # 卸妆专区
        x_makeup = Goods.objects.filter(c_code=5000)

        x0 = x_makeup.values()[0]
        x1 = x_makeup.values()[0]

        x0['g_info'] = x0['g_info'].split(',')[0]

        x0['g_pics'] = x0['g_pics'].split(',')[0]
        x1['g_pics'] = x1['g_pics'].split(',')[1]

        data = {
            'wimage1':wimage1,
            'wimage2': wimage2,
            'new':new,
            'sale':sale,
            'selling':selling,
            'fashion':fashion,
            'd0': d0,
            'd1': d1,
            'd2': d2,
            'y0': y0,
            'y1': y1,
            'y2': y2,
            'c0': c0,
            'c1': c1,
            'c2': c2,
            'x0': x0,
            'x1': x1
        }

        return render(request, 'index.html', data)

def search(request):
    if request.method == 'GET':
        key = request.GET.get('searchkey')
        goods = Goods.objects.filter(Q(g_name__contains=key)|Q(g_desc__contains=key)).values()
        if goods:
            for good in goods:
                image = good['g_pics']
                new_image = image.split(',')[0]
                good['g_pics'] = new_image
                good['discount'] = float('%.f' %(float(good['g_price'])/float(good['g_mktprice'])*10))

            data = {'goods':goods}
            c_code = data['goods'][0]['c_code']

            return HttpResponseRedirect(reverse('zl:classify_list',args=(c_code,)))

        else:
            return HttpResponseRedirect(reverse('zc:index'))


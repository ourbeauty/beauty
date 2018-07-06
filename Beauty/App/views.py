from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.core.urlresolvers import reverse

from App.models import Address, User


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
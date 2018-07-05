from django.shortcuts import render

# Create your views here.
from App.models import Address, User


def dizhi(request):
    if request.method == 'GET':
        user = request.user
        if user and user.id:
            users = User.objects.all()
            addrs = Address.objects.filter(use_id=user.id)
            return render(request, 'dizhi_liebiao.html', {'addrs':addrs,'users':users})


def adddizhi(request):
    if request.method == 'GET':
        user = request.user
        if user and user.id:
            return render(request,'tianxie_dizhi.html')
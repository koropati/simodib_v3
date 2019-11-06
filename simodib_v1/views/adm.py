from django.contrib.auth import login
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.utils.decorators import method_decorator
from django.db.models import Q
from django.http import HttpResponse, JsonResponse

from ..decorators import superuser_only
from ..forms import ManagerSignUpForm, RiceAddForm
from ..models import User, Kurir, Manager, PortalSignUp, Rice, Distribution, DetailOrder, TakenDistribution, DataLogPerjalanan
import string
import random

@login_required
@superuser_only
def dashboard(request):
    totalKurir = Kurir.objects.all().count()
    totalDistribution = TakenDistribution.objects.all().count()
    totalJenisBeras = Rice.objects.all().count()
    totalDist = Distribution.objects.all().count()
    timeline = DataLogPerjalanan.objects.all()
    # totalDistribution
    # user = User.object.select_related('user')
    return render(request,'adm/dashboard.html', {'totalKurir' : totalKurir,'timeline':timeline, 'totalDistribution':totalDistribution, 'totalJenisBeras': totalJenisBeras,'totalDist':totalDist})

@login_required
@superuser_only
def portalSignUp(request):
    if request.method == 'POST':
        form = ManagerSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            user.save()
            return redirect('home')
    else:
        datas = get_object_or_404(PortalSignUp, pk=1)
        portal_manager = datas.port_manager
        if portal_manager == '1':
            form = ManagerSignUpForm()
            user_type = 'Manager'
            return render(request, 'registration/signup_form.html',{'user_type':user_type,'form' : form})
        else:
            portal_type = 'Manager'
            return render(request, 'registration/closed.html',{'portal_type':portal_type})

@login_required
@superuser_only
def viewKurir(request):
    kurirs = Kurir.objects.all()
    # user = User.object.select_related('user')
    return render(request,'adm/kurir_modul/kurir.html', {'kurirs' : kurirs,})

@login_required
@superuser_only
def viewKurirDetail(request, pk):
    kurir = get_object_or_404(Kurir.objects.select_related('user'), pk=pk)
    return render(request, 'adm/kurir_modul/kurir_detail.html', {'kurir' : kurir})

@login_required
@superuser_only
def viewManager(request):
    managers = Manager.objects.all()
    # user = User.object.select_related('user')
    return render(request,'adm/manager_modul/manager.html', {'managers' : managers,})

@login_required
@superuser_only
def viewManagerDetail(request, pk):
    manager = get_object_or_404(Manager.objects.select_related('user'), pk=pk)
    return render(request, 'adm/manager_modul/manager_detail.html', {'manager' : manager})

@login_required
@superuser_only
def deleteManager(request):
    typeMsg='success'
    message=''
    if request.method == 'GET':
        # id_kurir = request.GET.get('id_kurir')
        message='Berhasil Hapus Data'
        id_manager = request.GET.get('id_manager')
        User.objects.filter(pk=id_manager).delete()
        manager = list(Manager.objects.select_related('user').values())
        data = dict()
        data['manager'] = manager
        message='Delete data Berhasil!'
        return JsonResponse(data)
        # return render(request, 'adm/beras_modul/beras.html', {'dataBeras': dataBeras, 'message':message})
    else:
        return redirect('adm:viewManager')


@login_required
@superuser_only
def validateKurir(request, pk):
    Kurir.objects.filter(pk=pk).update(status_akun='1')
    kurirs = Kurir.objects.select_related('user')
    return redirect('adm:dashboard_adm')

@login_required
@superuser_only
def unvalidateKurir(request, pk):
    Kurir.objects.filter(pk=pk).update(status_akun='0')
    kurirs = Kurir.objects.select_related('user')
    return redirect('adm:dashboard_adm')

@login_required
@superuser_only
def deleteKurir(request):
    # if request.method == 'GET':
    #     # id_kurir = request.GET.get('id_kurir')
    #     id_kurir = request.GET.get('id_kurir')
    #     User.objects.filter(pk=id_kurir).delete()
    #     kurirs = Kurir.objects.select_related('user')
    #     return redirect('adm:dashboard_adm')
    # else:
    #     return redirect('home')

    typeMsg='success'
    message=''
    if request.method == 'GET':
        # id_kurir = request.GET.get('id_kurir')
        message='Berhasil Hapus Data'
        id_kurir = request.GET.get('id_kurir')
        User.objects.filter(pk=id_kurir).delete()
        kurir = list(Kurir.objects.select_related('user').values())
        data = dict()
        data['kurir'] = kurir
        message='Delete data Berhasil!'
        return JsonResponse(data)
        # return render(request, 'adm/beras_modul/beras.html', {'dataBeras': dataBeras, 'message':message})
    else:
        return redirect('adm:viewKurir')

@login_required
@superuser_only
def viewPortal(request):
    if request.method == 'POST':
        port = PortalSignUp.objects.get(pk=1)
        port.port_kurir = request.POST.get('status')
        port.save()
        # status = request.POST['status']
        # PortalSignUp.objects.filter(pk=1).update(port_kurir=status)
        return redirect('adm:viewPortal')
    else:
        datas = get_object_or_404(PortalSignUp, pk=1)
        port_kurir = datas.port_kurir
        token_kurir = datas.token_kurir
        port_manager = datas.port_manager
        return render(request, 'adm/setting_modul/portal.html',{'port_kurir':port_kurir, 'token_kurir':token_kurir, 'port_manager':port_manager})

@login_required
@superuser_only
def viewPortalDist(request):
    if request.method == 'POST':
        port = PortalSignUp.objects.get(pk=1)
        port.port_manager = request.POST.get('status')
        port.save()
        # status = request.POST['status']
        # PortalSignUp.objects.filter(pk=1).update(port_kurir=status)
        return redirect('adm:viewPortal')
    else:
        datas = get_object_or_404(PortalSignUp, pk=1)
        port_kurir = datas.port_kurir
        token_kurir = datas.token_kurir
        port_manager = datas.port_manager
        return render(request, 'adm/setting_modul/portal.html',{'port_kurir':port_kurir, 'token_kurir':token_kurir, 'port_manager':port_manager})

def token_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def viewToken(request):
    if request.method == 'POST':
        port = PortalSignUp.objects.get(pk=1)
        port.token_kurir = token_generator()
        port.save()
        return redirect('adm:viewToken')
    else:
        datas = get_object_or_404(PortalSignUp, pk=1)
        port_kurir = datas.port_kurir
        token_kurir = datas.token_kurir
        return render(request, 'adm/setting_modul/portal.html',{'port_kurir':port_kurir, 'token_kurir':token_kurir})


@login_required
@superuser_only
def viewBeras(request):
    typeMsg='success'
    message=''
    if request.method == 'POST':  # data sent by user
       name = request.POST.get('name')
       stock = request.POST.get('stock')
       price = request.POST.get('price')
       if name and stock and price :
        obj = Rice.objects.create(name = name, stock = stock, price = price)
        typeMsg='success'
        message = 'Tambah data berhasil!'
        obj.save()
        return HttpResponse('')
    dataBeras = Rice.objects.all()
    return render(request, 'adm/beras_modul/beras.html', {'dataBeras': dataBeras, 'message':message, 'typeMsg':typeMsg})

@login_required
@superuser_only
def getBeras(request):
    if request.method == 'GET':
        beras = list(Rice.objects.all().values())
        data = dict()
        data['beras'] = beras
        return JsonResponse(data)

@login_required
@superuser_only
def tambahStockBeras(request):
    typeMsg='success'
    message=''
    if request.method == 'POST':  # data sent by user
       id_beras = request.POST.get('id')
       tambahan_stock = request.POST.get('tambahan_stock')
       if id_beras and tambahan_stock :
        datas = get_object_or_404(Rice, pk=id_beras)
        stock_sebelumnya = datas.stock
        stock = str(int(stock_sebelumnya)+int(tambahan_stock))
        Rice.objects.filter(pk=id_beras).update(stock=stock)
        typeMsg = 'success'
        message = 'Tambah data berhasil!'
        beras = list(Rice.objects.all().values())
        data = dict()
        data['beras'] = beras
        return JsonResponse(data)
    else:
        dataBeras = Rice.objects.all()
        return render(request, 'adm/beras_modul/beras.html', {'dataBeras': dataBeras, 'message':message, 'typeMsg':typeMsg})
    


@login_required
@superuser_only
def deleteBeras(request):
    typeMsg='success'
    message=''
    if request.method == 'GET':
        # id_kurir = request.GET.get('id_kurir')
        message='Berhasil Hapus Data'
        id_beras = request.GET.get('id_beras')
        Rice.objects.filter(pk=id_beras).delete()
        beras = list(Rice.objects.all().values())
        data = dict()
        data['beras'] = beras
        message='Delete data Berhasil!'
        return JsonResponse(data)
        # return render(request, 'adm/beras_modul/beras.html', {'dataBeras': dataBeras, 'message':message})
    else:
        return redirect('adm:viewBeras')

@login_required
@superuser_only
def viewDistribusi(request):
    typeMsg='success'
    message=''
    if request.method == 'POST':  # data sent by user
       name = request.POST.get('name')
       ordered_by = request.POST.get('ordered_by')
       telepon = request.POST.get('no_hp')
       email = request.POST.get('email')
       address = request.POST.get('address')
       catatan_khusus = request.POST.get('catatan')

       statusOrder = '0'
       if name and ordered_by and address :
        obj = Distribution.objects.create(name = name, ordered_by = ordered_by, telepon = telepon, email = email, address = address, catatan_khusus = catatan_khusus, statusOrder = statusOrder)
        typeMsg='success'
        message = 'Tambah data berhasil!'
        obj.save()
    dataDistribusi = Distribution.objects.filter(statusOrder='0')
    dataBeras = Rice.objects.all()
    return render(request, 'adm/distribusi_modul/distribusi.html', {'dataDistribusi': dataDistribusi, 'dataBeras': dataBeras, 'message':message, 'typeMsg':typeMsg})

@login_required
@superuser_only
def addPesanan(request):
    typeMsg='success'
    message=''
    if request.method == 'POST':  # data sent by user
       id_distribusi = request.POST.get('id_distribusi')
       id_rices = request.POST.getlist('name[]')
       values = request.POST.getlist('value[]')
       id_dist = get_object_or_404(Distribution, pk=id_distribusi)

       #Perulangan Untuk Cek Stock Beras Available atau tidak
       prosesPesanan = True
       for i in range(len(id_rices)):
        id_rice = get_object_or_404(Rice, pk=id_rices[i])
        value = int(values[i])
        harga = getattr(id_rice, 'price')
        total = str(value*harga)
        newStock = int(id_rice.stock-value)
        if newStock >= 0:
            prosesPesanan = prosesPesanan and True
        else:
            message='Pesanan Melampaui Stock yang ada, Silahkan Cek Stock!'
            typeMsg='warning'
            prosesPesanan = prosesPesanan and False

    if prosesPesanan == True:
       #perulangan untuk menyimpan banyaknya pesanan
       for i in range(len(id_rices)):
        # id_dist = id_distribusi
        # id_rice = id_rices[i]
        id_rice = get_object_or_404(Rice, pk=id_rices[i])
        value = int(values[i])
        harga = getattr(id_rice, 'price')
        total = str(value*harga)
        newStock = int(id_rice.stock-value)
        if id_rice and value :
            obj = DetailOrder.objects.create(distribution = id_dist, rice = id_rice, value = value, prices = total)
            Rice.objects.filter(pk=id_rices[i]).update(stock=newStock)
            obj.save()
        if i == (len(id_rices)-1):
            Distribution.objects.filter(pk=id_distribusi).update(statusOrder='1')
            message='Data Pesanan Berhasil disimpan!'
            typeMsg='success'
    dataDistribusi = Distribution.objects.filter(statusOrder='0')
    dataBeras = Rice.objects.all()
    return render(request, 'adm/distribusi_modul/distribusi.html', {'dataDistribusi': dataDistribusi, 'dataBeras': dataBeras, 'message':message, 'typeMsg':typeMsg})

@login_required
@superuser_only
def deleteDistribusi(request):
    typeMsg='success'
    message=''
    if request.method == 'GET':
        # id_kurir = request.GET.get('id_kurir')
        message='Berhasil Hapus Data Distribusi'
        id_distribusi = request.GET.get('id_distribusi')

        TakenDistribution.objects.filter(distribution=id_distribusi).delete()
        Distribution.objects.filter(pk=id_distribusi).delete()
        
        dataDistribusi = Distribution.objects.filter(~Q(statusOrder='1'),~Q(statusOrder='2'),~Q(statusOrder='3'))
        dataBeras = Rice.objects.all()
        typeMsg='success'
        message='Berhasil Hapus Data Distribusi'
        return render(request, 'adm/distribusi_modul/distribusi.html', {'dataDistribusi': dataDistribusi, 'dataBeras': dataBeras, 'message':message, 'typeMsg':typeMsg})
    else:
        return redirect('adm:viewDistribusi')

@login_required
@superuser_only
def batalDistribusi(request):
    typeMsg='success'
    message=''
    typeMsg=''
    if request.method == 'GET':
        # id_kurir = request.GET.get('id_kurir')
        typeMsg = 'success'
        message='Berhasil Membatalkan Distribusi'
        id_distribusi = request.GET.get('id_distribusi')
        id_dist = get_object_or_404(Distribution, pk=id_distribusi)
        
        if id_dist:
            Distribution.objects.filter(pk=id_distribusi).update(statusOrder='1')#update status Order
            TakenDistribution.objects.filter(distribution=id_distribusi).delete()#delete taken distribusi
            typeMsg='success'
            message='Berhasil Membatalkan Distribusi'

        dataDistribusi = TakenDistribution.objects.select_related('kurir','distribution').filter(~Q(status_track='2'))
        # dataDistribusi = Distribution.objects.filter(statusOrder='2') #status order adalah 2
        # dataKurir = Kurir.objects.all()
        return render(request, 'adm/distribusi_modul/onprocess.html', {'dataDistribusi':dataDistribusi, 'message':message, 'typeMsg':typeMsg})
    else:
        return redirect('adm:viewDistribusi')


@login_required 
@superuser_only
def viewUnfinished(request):
    typeMsg='success'
    message=''
    if request.method == 'POST':
        message = 'POST data'
    else:
        dataDistribusi = Distribution.objects.filter(~Q(statusOrder='0'),~Q(statusOrder='2')) #status order tidak 0 dan 2
        dataKurir = Kurir.objects.all()
        return render(request, 'adm/distribusi_modul/unfinished.html', {'dataDistribusi':dataDistribusi, 'dataKurir':dataKurir, 'message':message})

@login_required 
@superuser_only
def viewOnprocess(request):
    # Halaman Distribusi Proses
    typeMsg='success'
    message=''
    if request.method == 'POST':
        message = 'POST data'
    else:
        dataDistribusi = TakenDistribution.objects.select_related('kurir','distribution').filter(~Q(status_track='2'))
        # dataDistribusi = Distribution.objects.filter(statusOrder='2') #status order adalah 2
        # dataKurir = Kurir.objects.all()
        return render(request, 'adm/distribusi_modul/onprocess.html', {'dataDistribusi':dataDistribusi, 'message':message})

@login_required
@superuser_only
def viewOnprocessDetail(request, pk, pk2):
    #pk adalah id dari table Distribusi
    #pk2 adalah id dari TakenDistribusi
    detailOrder = DetailOrder.objects.filter(distribution=pk)
    takenDistribusi = get_object_or_404(TakenDistribution, pk=pk2) #=> kurir , => distribution

    return render(request, 'adm/distribusi_modul/distribusi_onprocess_detail.html', {'takenDistribusi':takenDistribusi, 'detailOrder': detailOrder})

@login_required
@superuser_only
def viewOnprocessTrack(request, pk, pk2):
    #pk adalah id dari table Distribusi
    #pk2 adalah id dari table TakenDistribusi
    detailOrder = DetailOrder.objects.filter(distribution=pk)
    takenDistribusi = get_object_or_404(TakenDistribution, pk=pk2) #=> kurir , => distribution
    logPerjalanan = DataLogPerjalanan.objects.filter(taken_distribution=pk2)

    return render(request, 'adm/distribusi_modul/distribusi_onprocess_track.html', {'takenDistribusi':takenDistribusi, 'detailOrder': detailOrder, 'logPerjalanan':logPerjalanan})




@login_required 
@superuser_only
def viewFinished(request):
    typeMsg='success'
    message=''
    if request.method == 'POST':
        message = 'POST data'
    else:
        dataDistribusi = Distribution.objects.filter(statusOrder='3') #status order adalah 2
        dataKurir = Kurir.objects.all()
        return render(request, 'adm/distribusi_modul/finished.html', {'dataDistribusi':dataDistribusi, 'dataKurir':dataKurir, 'message':message})

@login_required
@superuser_only
def addKurir(request):
    typeMsg='success'
    message=''
    if request.method == 'POST':  # data sent by user
       id_distribusis = request.POST.get('id_distribusi')
       id_kurirs = request.POST.get('id_kurir')
       status_antar = "Menunggu Konfirmasi Kurir"
       id_kurir = get_object_or_404(Kurir, pk=id_kurirs)
       id_distribusi = get_object_or_404(Distribution, pk=id_distribusis)
       if id_distribusi and id_kurir :
        obj = TakenDistribution.objects.create(distribution = id_distribusi, kurir = id_kurir, status_antar = status_antar, status = '1')
        obj.save()
        Distribution.objects.filter(pk=id_distribusis).update(statusOrder='2')
        typeMsg='success'
        message='Data Distribusi Berhasil diproses!'
    
        distribusi = list(Distribution.objects.filter(~Q(statusOrder='0'),~Q(statusOrder='2')).values())
        data = dict()
        data['distribusi'] = distribusi
        return JsonResponse(data)
    else:
        dataDistribusi = Distribution.objects.filter(~Q(statusOrder='0'))
        dataKurir = Kurir.objects.all()
        return render(request, 'adm/distribusi_modul/progress_distribusi.html', {'dataDistribution': dataDistribution, 'message':message, 'typeMsg':typeMsg})


@login_required
@superuser_only
def viewDistribusiDetail(request, pk):
    dataDistribusi = get_object_or_404(Distribution, pk=pk)
    detailOrder = DetailOrder.objects.filter(distribution=pk)

    return render(request, 'adm/distribusi_modul/distribusi_detail.html', {'dataDistribusi':dataDistribusi, 'detailOrder': detailOrder})
from django.contrib.auth import login
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.utils.decorators import method_decorator
from django.db.models import Q

from ..decorators import manager_required
from ..forms import ManagerSignUpForm, RiceAddForm
from ..models import User, Kurir, PortalSignUp, Rice, Distribution, DetailOrder

class ManagerSignUpView(CreateView):
    model = User
    form_class = ManagerSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'manager'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')
        
@login_required
@manager_required
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


# @method_decorator([login_required, manager_required], name='dispatch')
@login_required
@manager_required
def dashboard(request):
    totalKurir = Kurir.objects.all().count()
    # user = User.object.select_related('user')
    return render(request,'manager/dashboard.html', {'totalKurir' : totalKurir,})

@login_required
@manager_required
def viewKurir(request):
    kurirs = Kurir.objects.all()
    # user = User.object.select_related('user')
    return render(request,'manager/kurir_modul/kurir.html', {'kurirs' : kurirs,})

@login_required
@manager_required
def viewKurirDetail(request, pk):
    kurir = get_object_or_404(Kurir.objects.select_related('user'), pk=pk)
    return render(request, 'manager/kurir_modul/kurir_detail.html', {'kurir' : kurir})

@login_required
@manager_required
def validateKurir(request, pk):
    Kurir.objects.filter(pk=pk).update(status_akun='1')
    kurirs = Kurir.objects.select_related('user')
    return redirect('manager:dashboard_view')

@login_required
@manager_required
def unvalidateKurir(request, pk):
    Kurir.objects.filter(pk=pk).update(status_akun='0')
    kurirs = Kurir.objects.select_related('user')
    return redirect('manager:dashboard_view')

@login_required
@manager_required
def deleteKurir(request):
    if request.method == 'GET':
        # id_kurir = request.GET.get('id_kurir')
        id_kurir = request.GET.get('id_kurir')
        User.objects.filter(pk=id_kurir).delete()
        kurirs = Kurir.objects.select_related('user')
        return redirect('manager:dashboard_view')
    else:
        return redirect('home')

@login_required
@manager_required
def viewPortal(request):
    if request.method == 'POST':
        port = PortalSignUp.objects.get(pk=1)
        port.port_kurir = request.POST.get('status')
        port.save()
        # status = request.POST['status']
        # PortalSignUp.objects.filter(pk=1).update(port_kurir=status)
        return redirect('manager:viewPortal')
    else:
        datas = get_object_or_404(PortalSignUp, pk=1)
        port_kurir = datas.port_kurir
        return render(request, 'manager/setting_modul/portal.html',{'port_kurir':port_kurir})

@login_required
@manager_required
def viewBeras(request):
    message=''
    if request.method == 'POST':  # data sent by user
       name = request.POST.get('name')
       stock = request.POST.get('stock')
       price = request.POST.get('price')
       if name and stock and price :
        obj = Rice.objects.create(name = name, stock = stock, price = price)
        message = 'Tambah data berhasil!'
        obj.save()
    dataBeras = Rice.objects.all()
    return render(request, 'manager/beras_modul/beras.html', {'dataBeras': dataBeras, 'message':message})

@login_required
@manager_required
def deleteBeras(request):
    message=''
    if request.method == 'GET':
        # id_kurir = request.GET.get('id_kurir')
        message='Berhasil Hapus Data'
        id_beras = request.GET.get('id_beras')
        Rice.objects.filter(pk=id_beras).delete()
        dataBeras = Rice.objects.all()
        message='Delete data Berhasil!'
        return render(request, 'manager/beras_modul/beras.html', {'dataBeras': dataBeras, 'message':message})
    else:
        return redirect('manager:viewBeras')

@login_required
@manager_required
def viewDistribusi(request):
    message=''
    if request.method == 'POST':  # data sent by user
       name = request.POST.get('name')
       ordered_by = request.POST.get('ordered_by')
       address = request.POST.get('address')
       statusOrder = '0'
       if name and ordered_by and address :
        obj = Distribution.objects.create(name = name, ordered_by = ordered_by, address = address, statusOrder = statusOrder)
        message = 'Tambah data berhasil!'
        obj.save()
    dataDistribusi = Distribution.objects.filter(statusOrder='0')
    dataBeras = Rice.objects.all()
    return render(request, 'manager/distribusi_modul/distribusi.html', {'dataDistribusi': dataDistribusi, 'dataBeras': dataBeras, 'message':message})

@login_required
@manager_required
def addPesanan(request):
    message=''
    if request.method == 'POST':  # data sent by user
       id_distribusi = request.POST.get('id_distribusi')
       id_rices = request.POST.getlist('name[]')
       values = request.POST.getlist('value[]')
       id_dist = get_object_or_404(Distribution, pk=id_distribusi)
       #perulangan untuk menyimpan banyaknya pesanan
       for i in range(len(id_rices)):
        # id_dist = id_distribusi
        # id_rice = id_rices[i]
        id_rice = get_object_or_404(Rice, pk=id_rices[i])
        value = int(values[i])
        harga = getattr(id_rice, 'price')
        total = str(value*harga)
        if id_rice and value :
            obj = DetailOrder.objects.create(distribution = id_dist, rice = id_rice, value = value, prices = total)
            obj.save()
        if i == (len(id_rices)-1):
            Distribution.objects.filter(pk=id_distribusi).update(statusOrder='1')
            message='Data Pesanan Berhasil disimpan!'
    dataDistribusi = Distribution.objects.filter(statusOrder='0')
    dataBeras = Rice.objects.all()
    return render(request, 'manager/distribusi_modul/distribusi.html', {'dataDistribusi': dataDistribusi, 'dataBeras': dataBeras, 'message':message})

@login_required
@manager_required
def deleteDistribusi(request):
    message=''
    if request.method == 'GET':
        # id_kurir = request.GET.get('id_kurir')
        message='Berhasil Hapus Data'
        id_distribusi = request.GET.get('id_distribusi')
        Distribution.objects.filter(pk=id_distribusi).delete()
        dataDistribusi = Distribution.objects.all()
        dataBeras = Rice.objects.all()
        message='Delete data Berhasil!'
        return render(request, 'manager/distribusi_modul/distribusi.html', {'dataDistribusi': dataDistribusi, 'dataBeras': dataBeras, 'message':message})
    else:
        return redirect('manager:viewDistribusi')

@login_required
@manager_required
def viewUnfinished(request):
    message=''
    if request.method == 'POST':
        message = 'POST data'
    else:
        dataDistribusi = Distribution.objects.filter(~Q(statusOrder='0'))
        dataKurir = Kurir.objects.all()
        return render(request, 'manager/distribusi_modul/unfinished.html', {'dataDistribusi':dataDistribusi, 'dataKurir':dataKurir, 'message':message})


@login_required
@manager_required
def viewDistribusiDetail(request, pk):
    dataDistribusi = get_object_or_404(Distribution, pk=pk)
    detailOrder = DetailOrder.objects.filter(distribution=pk)

    return render(request, 'manager/distribusi_modul/distribusi_detail.html', {'dataDistribusi':dataDistribusi, 'detailOrder': detailOrder})
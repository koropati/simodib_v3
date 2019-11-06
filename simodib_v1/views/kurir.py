from django.contrib.auth import login
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, ListView
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse, JsonResponse

from ..decorators import kurir_required
from ..forms import KurirSignUpForm
from ..models import User, Kurir, Rice, TakenDistribution, Distribution, PortalSignUp, DataLogPerjalanan, DetailOrder

class KurirSignUpView(CreateView):
    model = User
    form_class = KurirSignUpForm
    template_name = 'registration/signup_form.html'
    
    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'kurir'
        return super().get_context_data(**kwargs)
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')

    # template_name = 'registration/signup_form.html'
def portalSignUp(request):
    if request.method == 'POST':
        data = get_object_or_404(PortalSignUp, pk=1)
        valid_token = data.token_kurir
        form = KurirSignUpForm(request.POST)
        # token = KurirSignUpForm(request.POST.get('token'))
        token = request.POST.get('token')
        if token == valid_token:
            if form.is_valid():
                user = form.save()
                login(request, user)
                user.save()
                return redirect('home')
        else:
            messages.add_message(request, messages.ERROR, 'Token Salah, Silahkan Ulangi Proses Daftar')
            return redirect('signup')
            # return render(request, 'home/home.html',{})
    else:
        datas = get_object_or_404(PortalSignUp, pk=1)
        portal_kurir = datas.port_kurir
        if portal_kurir == '1':
            form = KurirSignUpForm()
            user_type = 'Kurir'
            return render(request, 'registration/signup_form.html',{'user_type':user_type,'form' : form})
        else:
            portal_type = 'Kurir'
            return render(request, 'registration/closed.html',{'portal_type':portal_type})
    

@method_decorator([login_required, kurir_required], name='dispatch')
class DistributionView(ListView):
    model = Distribution
    ordering = ('name', )
    context_object_name = 'distributions'
    template_name = 'kurir/distribution_list.html'

    def get_queryset(self):
        kurir = self.request.user.kurir
        # student_interests = student.interests.values_list('pk', flat=True)
        taken_distributions = kurir.taken_distributions.values_list('pk', flat=True)
        queryset = Distribution.objects.exclude(pk__in=taken_distributions)
        return queryset 

@login_required 
@kurir_required
def dashboard(request):
    user = request.user
    id_kurir = user.id
    belumProses = TakenDistribution.objects.filter(Q(kurir=id_kurir) & ~Q(status_track='1'),~Q(status_track='2')).count()
    sedangProses = TakenDistribution.objects.filter(Q(kurir=id_kurir), Q(status_track='1')).count()
    selesaiProses = TakenDistribution.objects.filter(Q(kurir=id_kurir),Q(status_track='2')).count()

    totalKurir = Kurir.objects.all().count()
    totalDistribusi = TakenDistribution.objects.all().count()
    totalJenisBeras = Rice.objects.all().count()
    totalDist = Distribution.objects.all().count()
    # user = User.object.select_related('user')
    return render(request,'kurir/dashboard.html', {'totalDist':totalDist, 'totalJenisBeras': totalJenisBeras,'totalDist':totalDist, 'belumProses': belumProses, 'sedangProses': sedangProses, 'selesaiProses':selesaiProses})

#belum selesai status_track 0 /null
#Sedang diproses status_track 1
#Sudah Selesai status_track 2

@login_required 
@kurir_required
def viewUnfinished(request):
    message=''
    typeMsg=''
    user = request.user
    id_kurir = user.id
    jobList = TakenDistribution.objects.filter(Q(kurir=id_kurir) & ~Q(status_track='1'),~Q(status_track='2'))

    return render(request, 'kurir/distribusi_modul/distribusi_job.html', {'jobList' : jobList})

@login_required
@kurir_required
def viewDetail(request, pk,pk2):
    detailOrder = DetailOrder.objects.filter(distribution=pk)
    takenDistribusi = get_object_or_404(TakenDistribution, pk=pk2) #=> kurir , => distribution

    return render(request, 'kurir/distribusi_modul/distribusi_job_detail.html', {'takenDistribusi':takenDistribusi, 'detailOrder': detailOrder})

@login_required
@kurir_required
def viewDetailFinish(request, pk, pk2):
    detailOrder = DetailOrder.objects.filter(distribution=pk)
    takenDistribusi = get_object_or_404(TakenDistribution, pk=pk2) #=> kurir , => distribution

    return render(request, 'kurir/distribusi_modul/distribusi_finish_detail.html', {'takenDistribusi':takenDistribusi, 'detailOrder': detailOrder})


@login_required 
@kurir_required
def prosesDistribusi(request):
    message=''
    typeMsg=''
    if request.method == 'POST':
        user = request.user
        id_kurir = user.id
        jobList = TakenDistribution.objects.filter(Q(kurir=id_kurir), Q(status_track='1'))
        if jobList:
            message='Anda Harus Selesaikan Proses Distribusi yang sedang berjalan Terlebih dahulu'
            typeMsg='warning'
            jobList = TakenDistribution.objects.filter(Q(kurir=id_kurir) & ~Q(status_track='1'),~Q(status_track='2'))
            return render(request, 'kurir/distribusi_modul/distribusi_job.html', {'jobList' : jobList, 'message':message, 'typeMsg':typeMsg})
        else:
            id_tk = request.POST.get('id_taken')
            status = 'Telah Di Konfirmasi Oleh Kurir'
            TakenDistribution.objects.filter(pk=id_tk).update(status_track='1', status_antar=status)
            id_tkdistribusi = get_object_or_404(TakenDistribution, pk=id_tk)
            obj = DataLogPerjalanan.objects.create(taken_distribution=id_tkdistribusi, status=status,)
            obj.save()
            message='Distribusi Berhasil Diproses'
            typeMsg='success'
            jobList = get_object_or_404(TakenDistribution, Q(kurir=id_kurir), Q(status_track='1'))
            dataLog = DataLogPerjalanan.objects.filter(taken_distribution=jobList)
            return render(request, 'kurir/distribusi_modul/distribusi_process.html', {'jobList' : jobList, 'message':message, 'typeMsg':typeMsg, 'dataLog':dataLog})


@login_required 
@kurir_required
def viewOnprocess(request):
    message=''
    typeMsg=''
    user = request.user
    id_kurir = user.id
    jobList = get_object_or_404(TakenDistribution, Q(kurir=id_kurir), Q(status_track='1'))
    if request.method == 'GET':
        # jobList = TakenDistribution.objects.filter(Q(kurir=id_kurir), Q(status_track='1'))
        
        if jobList:
            dataLog = DataLogPerjalanan.objects.filter(taken_distribution=jobList)
            return render(request, 'kurir/distribusi_modul/distribusi_process.html', {'jobList' : jobList, 'dataLog':dataLog})
        else:
            return redirect('kurir:viewUnfinished_kurir')
            # message='Belum ada Distribusi yang sedang berlangsung!'
            # typeMsg='warning'
            # jobList = TakenDistribution.objects.filter(Q(kurir=id_kurir) & ~Q(status_track='1'),~Q(status_track='2'))
            # return render(request, 'kurir/distribusi_modul/distribusi_job.html', {'jobList' : jobList,'message':message,'typeMsg':typeMsg})


@login_required 
@kurir_required
def tambahStatus(request):
    message=''
    typeMsg=''
    user = request.user
    id_kurir = user.id
    jobList = get_object_or_404(TakenDistribution, Q(kurir=id_kurir), Q(status_track='1'))
    if request.method == 'POST':
        status1 = request.POST.get('status_antar1')
        status2 = request.POST.get('status_antar2')
        if status1 == '' and status2 == '':
            message='Pesan Status Masih Kosong!'
            typeMsg='warning'
            dataLog = DataLogPerjalanan.objects.filter(taken_distribution=jobList)
            return render(request, 'kurir/distribusi_modul/distribusi_process.html', {'jobList' : jobList, 'dataLog':dataLog, 'message':message, 'typeMsg':typeMsg})
        else:
            if status1:
                status = status1
            else:
                status = status2
            latitude = request.POST.get('latitude')
            longitude = request.POST.get('longitude')
            location = str(latitude)+','+str(longitude)
            x = request.POST.get('data_x')
            y = request.POST.get('data_y')
            z = request.POST.get('data_z')
            
            obj = DataLogPerjalanan.objects.create(taken_distribution=jobList, x=x, y=y, z=z, status=status,location=location)
            obj.save()
            log = list(DataLogPerjalanan.objects.filter(taken_distribution=jobList).values())
            data = dict()
            data['log'] = log
            return JsonResponse(data)

@login_required 
@kurir_required
def distribusiSelesai(request):
    message=''
    typeMsg=''
    if request.method == 'GET':
        id_taken = request.GET.get('id_distribusi')
        TakenDistribution.objects.filter(pk=id_taken).update(status_track='2',status_antar='Distribusi Telah Selesai')
        id_tkdistribusi = get_object_or_404(TakenDistribution, pk=id_taken)
        obj = DataLogPerjalanan.objects.create(taken_distribution=id_tkdistribusi, status='Distribusi Telah Selesai')
        obj.save()
        message='Distribusi Berhasil diSelesaikan'
        typeMsg='success'

        user = request.user
        id_kurir = user.id
        jobList = TakenDistribution.objects.filter(Q(kurir=id_kurir) & ~Q(status_track='1'),~Q(status_track='2'))

        return render(request, 'kurir/distribusi_modul/distribusi_job.html', {'jobList' : jobList,'message':message,'typeMsg':typeMsg})

    

@login_required 
@kurir_required
def getLogPerjalanan(request):
    if request.method == 'GET':
        user = request.user
        id_kurir = user.id
        jobList = get_object_or_404(TakenDistribution, Q(kurir=id_kurir), Q(status_track='1'))

        log = list(DataLogPerjalanan.objects.filter(taken_distribution=jobList).values())
        data = dict()
        data['log'] = log
        return JsonResponse(data)


@login_required 
@kurir_required
def viewFinished(request):
    message=''
    typeMsg=''
    user = request.user
    id_kurir = user.id
    jobList = TakenDistribution.objects.filter(Q(kurir=id_kurir),Q(status_track='2'))

    return render(request, 'kurir/distribusi_modul/distribusi_finish.html', {'jobList' : jobList})




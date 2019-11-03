from django.contrib.auth import login
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, ListView
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.db.models import Q

from ..decorators import kurir_required
from ..forms import KurirSignUpForm
from ..models import User, TakenDistribution, Distribution, PortalSignUp

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
    totalDistribution = Distribution.objects.all().count()
    # user = User.object.select_related('user')
    return render(request,'kurir/dashboard.html', {'totalDistribution' : totalDistribution,})

@login_required 
@kurir_required
def viewUnfinished(request):
    user = request.user
    id_kurir = user.id
    jobList = TakenDistribution.objects.filter(Q(kurir=id_kurir) & ~Q(status_track='1'),~Q(status_track='2'))

    return render(request, 'kurir/distribusi_modul/distribusi_job.html', {'jobList' : jobList})

@login_required 
@kurir_required
def viewOnprocess(request):
    user = request.user
    id_kurir = user.id
    jobList = TakenDistribution.objects.filter(Q(kurir=id_kurir), Q(status_track='1'))

    return render(request, 'kurir/distribusi_modul/distribusi_process.html', {'jobList' : jobList})

@login_required 
@kurir_required
def viewFinished(request):
    user = request.user
    id_kurir = user.id
    jobList = TakenDistribution.objects.filter(Q(kurir=id_kurir),Q(status_track='2'))

    return render(request, 'kurir/distribusi_modul/distribusi_finish.html', {'jobList' : jobList})

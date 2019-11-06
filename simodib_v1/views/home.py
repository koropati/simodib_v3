from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import TemplateView
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from ..models import PortalSignUp, Kurir, Distribution, TakenDistribution, DataLogPerjalanan

def home(request): 
    if request.user.is_authenticated:
        if request.user.is_manager:
            return redirect('manager:dashboard_view')
        else:
            return redirect('kurir:dashboard_kurir')
    totalKurir = Kurir.objects.all().count()
    return render(request, 'home/home.html',{'totalKurir':totalKurir})

def cariDistribusi(request):
    message=''
    typeMsg=''
    if request.method == 'POST':
        id_taken = request.POST.get('id_taken')
        if id_taken:
            distribusi = get_object_or_404(Distribution, name=id_taken)
            id_taken_dist = get_object_or_404(TakenDistribution, distribution=distribusi)
            tk_dist = TakenDistribution.objects.filter(distribution=distribusi).values()
            dist = Distribution.objects.filter(name=id_taken).values()
            log = DataLogPerjalanan.objects.filter(taken_distribution=id_taken_dist).values().order_by('-date')
            # kurir = Kurir.objects.filter(distributions=distribusi)
            # user = User.objects.filter()

            data1 = list(tk_dist)
            data2 = list(dist)
            data3 = list(log)
            final_data = data1 + data2 + data3
            data = dict()
            data['dataDist'] = final_data
            if distribusi:
                return JsonResponse(data)
            else:
                message='Data Tidak Ditemukan'
                typeMsg='warning'
                return render(request, 'home/home.html',{'message':message, 'typeMsg':typeMsg})
    else:
        return render(request, 'home/home.html',)
        

def cariLogDistribusi(request):
    if request.method == 'POST':
        id_taken = request.POST.get('id_taken')
        if id_taken:
            dataDistribusi = get_object_or_404(TakenDistribution, pk=id_taken)
            log = list(DataLogPerjalanan.objects.filter(taken_distribution=dataDistribusi))
            data = dict()
            data['log'] = log
            return JsonResponse(data)
    else:
        return render(request, 'home/home.html',)

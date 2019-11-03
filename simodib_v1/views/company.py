from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import TemplateView
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from ..models import PortalSignUp, Kurir, Distribution, TakenDistribution, DataLogPerjalanan
class SignUpView(TemplateView):
	portal_kurir = '';
	model = PortalSignUp
	#comment/uncoment this when adding or done adding field in models -> portalSignUp other line comment it
	# template_name = 'registration/signup.html'
	#end comment
	
	datas = get_object_or_404(PortalSignUp, pk=1)
	portal_kurir = datas.port_kurir
	portal_manager = datas.port_manager
	portal_admin = datas.port_admin
	if portal_kurir == '1':
		template_name = 'registration/signup.html'
	else:
		template_name = 'registration/closed_kurir.html'

def portalSignUp(request):
	#comment/uncoment this when adding or done adding field in models -> portalSignUp other line comment it
	# return render(request, 'registration/signup.html',{})
	#end comment
	
	datas = get_object_or_404(PortalSignUp, pk=1)
	portal_kurir = datas.port_kurir
	portal_manager = datas.port_manager
	if portal_kurir == '1' or portal_manager == '1':
		# template_name = 'registration/signup.html'
		return render(request, 'registration/signup.html',{})
	else:
		portal_type = 'Secara Umum'
		# template_name = 'registration/closed_kurir.html'
		return render(request, 'registration/closed.html',{'portal_type':portal_type})

def closedPortal(request):
	portal_type = '...'
	return render(request, 'registration/closed.html',{'portal_type':portal_type})

def home(request): 
    if request.user.is_authenticated:
        if request.user.is_manager:
            return redirect('manager:dashboard_view')
        else:
            return redirect('kurir:dashboard_kurir')
    totalKurir = Kurir.objects.all().count()
    return render(request, 'home/home.html',{'totalKurir':totalKurir})

@csrf_exempt
def updatelog(request):
    if request.method == 'POST':  # data sent by user
       id_kurir = request.POST.get('id')
       x = request.POST.get('x')
       y = request.POST.get('y')
       z = request.POST.get('z')
       status = request.POST.get('status')
       location = request.POST.get('location')

       # id_td = TakenDistribution.objects.filter(kurir=id_kurir,status_track='1').values('id')
       td = get_object_or_404(TakenDistribution, kurir=id_kurir,status_track='1')
       if id_kurir:
        obj = DataLogPerjalanan.objects.create(taken_distribution = td, x = x, y = y, z = z, status=status, location=location)
        obj.save()
        return HttpResponse('sukses')
    else:
        return HttpResponse('gagal')
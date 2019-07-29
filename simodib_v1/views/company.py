from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import TemplateView

from ..models import PortalSignUp, Kurir
class SignUpView(TemplateView):
	portal_kurir = '';
	model = PortalSignUp
	datas = get_object_or_404(PortalSignUp, pk=1)
	portal_kurir = datas.port_kurir
	portal_manager = datas.port_manager
	portal_admin = datas.port_admin
	if portal_kurir == '1':
		template_name = 'registration/signup.html'
	else:
		template_name = 'registration/closed_kurir.html'

def portalSignUp(request):
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
            return redirect('kurir:distribution_list')
    totalKurir = Kurir.objects.all().count()
    return render(request, 'home/home.html',{'totalKurir':totalKurir})
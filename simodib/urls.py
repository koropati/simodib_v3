"""simodib URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

from simodib_v1.views import company, kurir, manager
# path('accounts/signup/kurir/', kurir.KurirSignUpView.as_view(), name='kurir_signup'),
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('simodib_v1.urls')),
    path('accounts/',include('django.contrib.auth.urls')),
    path('accounts/signup/',company.portalSignUp, name='signup'),
    path('accounts/signup/kurir/', kurir.portalSignUp, name='kurir_signup'),
    path('accounts/signup/manager/', manager.portalSignUp, name='manager_signup'),
]
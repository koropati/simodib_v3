from django.urls import include, path
from .views import company, kurir, manager, home, adm
 
urlpatterns = [
	path('', company.home, name='home'),
    path('closed/', company.closedPortal, name='closed'),
    path('updatelog/', company.updatelog, name='updatelog'),
    
    path('adm/', include(([
        path('', adm.dashboard, name='dashboard_adm'),
        path('kurir/', adm.viewKurir, name='viewKurir'),
        path('kurir/<int:pk>/', adm.viewKurirDetail, name='viewKurirDetail'),
        path('kurir/<int:pk>/validate/', adm.validateKurir, name='validateKurir'),
        path('kurir/<int:pk>/unvalidate/', adm.unvalidateKurir, name='unvalidateKurir'),
        path('kurir/delete/', adm.deleteKurir, name='deleteKurir'),

        path('manager/', adm.viewManager, name='viewManager'),
        path('manager/<int:pk>/', adm.viewManagerDetail, name='viewManagerDetail'),
        path('manager/delete/', adm.deleteManager, name='deleteManager'),

        path('setting/portal/', adm.viewPortal, name='viewPortal'),
        path('setting/portal/Dist/', adm.viewPortalDist, name='viewPortalDist'),
        path('setting/portal/viewToken', adm.viewToken, name='viewToken'),

        path('beras/', adm.viewBeras, name='viewBeras'),
        path('beras/get', adm.getBeras, name='getBeras'),
        path('beras/delete/', adm.deleteBeras, name='deleteBeras'),
        path('beras/tambah-stock/', adm.tambahStockBeras, name='tambahStockBeras'),

        path('distribusi/', adm.viewDistribusi, name='viewDistribusi'),
        path('distribusi/add', adm.addPesanan, name='addPesanan'),
        path('distribusi/delete/', adm.deleteDistribusi, name='deleteDistribusi'),
        path('distribusi/batal/', adm.batalDistribusi, name='batalDistribusi'),
        path('distribusi/unfinished/', adm.viewUnfinished, name='viewUnfinished'),
        path('distribusi/finished/', adm.viewFinished, name='viewFinished'),
        path('distribusi/onprocess/', adm.viewOnprocess, name='viewOnprocess'),
        path('distribusi/onprocess/detail/<int:pk>/<int:pk2>/', adm.viewOnprocessDetail, name='viewOnprocessDetail'),
        path('distribusi/onprocess/track/<int:pk>/<int:pk2>/', adm.viewOnprocessTrack, name='viewOnprocessTrack'),
        path('distribusi/addKurir', adm.addKurir, name='addKurir'),
        path('distribusi/<int:pk>/', adm.viewDistribusiDetail, name='viewDistribusiDetail'),
  
    ], 'adm'), namespace='adm')),


    path('home/', include(([
        path('', home.home, name='home_guest'),
        path('cari/', home.cariDistribusi, name='cariDistribusi'),
        path('cari/log/', home.cariLogDistribusi, name='cariLogDistribusi'),
    ], 'home'), namespace='home')),

    path('kurir/', include(([
        path('', kurir.dashboard, name='dashboard_kurir'),
        path('distribusi/unfinished/', kurir.viewUnfinished, name='viewUnfinished_kurir'),
        path('distribusi/unfinished/detail/<int:pk>/<int:pk2>/', kurir.viewDetail, name='viewDetail_kurir'),
        path('distribusi/unfinished/process/', kurir.prosesDistribusi, name='prosesDistribusi_kurir'),
        path('distribusi/onprocess/', kurir.viewOnprocess, name='viewOnprocess_kurir'),
        path('distribusi/onprocess/newStatus/', kurir.tambahStatus, name='tambahStatus_kurir'),
        path('distribusi/onprocess/getLog/', kurir.getLogPerjalanan, name='getLogPerjalanan'),
        path('distribusi/onprocess/selesai', kurir.distribusiSelesai, name='distribusiSelesai'),
        path('distribusi/finished/', kurir.viewFinished, name='viewFinished_kurir'),
        path('distribusi/finished/detail/', kurir.viewDetailFinish, name='viewDetailFinish_kurir'),
    ], 'company'), namespace='kurir')),

    path('manager/', include(([
        path('', manager.dashboard, name='dashboard_view'),
        path('kurir/', manager.viewKurir, name='viewKurir'),
        path('kurir/<int:pk>/', manager.viewKurirDetail, name='viewKurirDetail'),
        path('kurir/<int:pk>/validate/', manager.validateKurir, name='validateKurir'),
        path('kurir/<int:pk>/unvalidate/', manager.unvalidateKurir, name='unvalidateKurir'),
        path('kurir/delete/', manager.deleteKurir, name='deleteKurir'),
        path('setting/portal/', manager.viewPortal, name='viewPortal'),
        path('setting/portal/viewToken', manager.viewToken, name='viewToken'),
        path('beras/', manager.viewBeras, name='viewBeras'),
        path('beras/get', manager.getBeras, name='getBeras'),
        path('beras/delete/', manager.deleteBeras, name='deleteBeras'),
        path('beras/tambah-stock/', manager.tambahStockBeras, name='tambahStockBeras'),
        path('distribusi/', manager.viewDistribusi, name='viewDistribusi'),
        path('distribusi/add', manager.addPesanan, name='addPesanan'),
        path('distribusi/delete/', manager.deleteDistribusi, name='deleteDistribusi'),
        path('distribusi/batal/', manager.batalDistribusi, name='batalDistribusi'),
        path('distribusi/unfinished/', manager.viewUnfinished, name='viewUnfinished'),
        path('distribusi/finished/', manager.viewFinished, name='viewFinished'),
        
        path('distribusi/onprocess/', manager.viewOnprocess, name='viewOnprocess'),
        path('distribusi/onprocess/detail/<int:pk>/<int:pk2>/', manager.viewOnprocessDetail, name='viewOnprocessDetail'),
        path('distribusi/onprocess/track/<int:pk>/<int:pk2>/', manager.viewOnprocessTrack, name='viewOnprocessTrack'),
        path('distribusi/addKurir', manager.addKurir, name='addKurir'),
        path('distribusi/<int:pk>/', manager.viewDistribusiDetail, name='viewDistribusiDetail'),
    ], 'company'), namespace='manager')),

]
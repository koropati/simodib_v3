from django.contrib import admin
from .models import User, Rice, Distribution, DetailOrder, Kurir, TakenDistribution, Manager, PortalSignUp, DataLogPerjalanan

# Register your models here.
admin.site.register(Rice)
admin.site.register(Distribution)
admin.site.register(DetailOrder)
admin.site.register(Kurir)
admin.site.register(TakenDistribution)
admin.site.register(Manager)
admin.site.register(PortalSignUp)
admin.site.register(DataLogPerjalanan)
from django.contrib import admin
from .models import Service, Environment, Url, Domain, UrlCheck



# Register your models here.
admin.site.register(Domain)
admin.site.register(Service)
admin.site.register(Environment)
admin.site.register(Url)
admin.site.register(UrlCheck)
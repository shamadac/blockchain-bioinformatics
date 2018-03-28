from django.contrib import admin
from DockerMarket.models import User, Docker, MetagenomicSample

# Register your models here.

admin.site.register(User)
admin.site.register(Docker)
admin.site.register(MetagenomicSample)
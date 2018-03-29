from django.contrib import admin
from DockerMarket.models import User, Docker

# Register your models here.

class DockerAdmin(admin.ModelAdmin):
    exclude = ('slug',)

admin.site.register(User)
admin.site.register(Docker, DockerAdmin)
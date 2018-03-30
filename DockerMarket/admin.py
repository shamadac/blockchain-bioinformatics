from django.contrib import admin
from DockerMarket.models import User, Docker

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('firstName', 'lastName', 'email')
    search_fields = ['firstName', 'lastName']

class DockerAdmin(admin.ModelAdmin):
    exclude = ('slug',)
    list_display = ('title', 'created', 'updated')
    list_filter = ['created']
    search_fields = ['title', 'description']

admin.site.register(User)
admin.site.register(Docker, DockerAdmin)
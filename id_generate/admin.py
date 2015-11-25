from django.contrib import admin

from .models import JaxIdMasterList, ProjectLinks

@admin.register(JaxIdMasterList)
class JaxIdListAdmin(admin.ModelAdmin):
    actions_on_top = True
    fields = ( ( 'jaxid', 'creation_date' ), )
    readonly_fields = ('creation_date',)
    list_display = ('jaxid', 'creation_date')


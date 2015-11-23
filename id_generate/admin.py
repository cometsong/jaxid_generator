from django.contrib import admin

from .models import JaxIdMasterList, ProjectLinks

# class RunSamplesInline(admin.StackedInline):
    # model = RunSamples
    # extra = 1
    # can_delete = True
    # show_change_link = True
    # fields = (
      # ('sample_description', 'seq_type'),
     # )

@admin.register(JaxIdMasterList)
class JaxIdListAdmin(admin.ModelAdmin):
    actions_on_top = True
    fields = ( ( 'jaxid', 'creation_date' ), )
    readonly_fields = ('creation_date',)
    list_display = ('jaxid', 'creation_date')


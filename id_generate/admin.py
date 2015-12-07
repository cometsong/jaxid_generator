from django.contrib import admin

from .models import JAXIdMasterList, JAXIdDetail,\
        SampleType, SequencingType, ProjectCode
from .forms import JAXIdDetailForm, SequencingForm, SampleForm, ProjectCodeForm

@admin.register(JAXIdMasterList)
class JAXIdListAdmin(admin.ModelAdmin):
    actions_on_top = True
    all_fields = ( 'jaxid', 'creation_date' )
    fields = ( all_fields, )
    list_display = all_fields
    search_fields = all_fields
    readonly_fields = ('creation_date',)
    ordering = ['creation_date']

@admin.register(ProjectCode)
class ProjectCodeAdmin(admin.ModelAdmin):
    form = ProjectCodeForm
    actions_on_top = True
    all_fields = ( 'project_code', 'details' )
    fields = ( all_fields, )
    list_display = all_fields
    search_fields = all_fields
    ordering = ['project_code']

@admin.register(SequencingType)
class SequencingType(admin.ModelAdmin):
    form = SequencingForm
    actions_on_top = True
    all_fields = ( 'sequencing_code', 'details' )
    # all_fields = SequencingType._meta.get_all_field_names(),
    fields = ( all_fields, )
    list_display = all_fields
    search_fields = all_fields
    ordering = ['sequencing_code']

@admin.register(SampleType)
class SampleType(admin.ModelAdmin):
    form = SampleForm
    actions_on_top = True
    all_fields = ( 'sample_code', 'details' )
    fields = ( all_fields, )
    list_display = all_fields
    search_fields = all_fields
    ordering = ['sample_code']

@admin.register(JAXIdDetail)
class JAXIdDetail(admin.ModelAdmin):
    form = JAXIdDetailForm
    actions_on_top = True
    all_fields = ( 'jaxid', 'project_code', 'collab_id',
            'sample_code', 'sequencing_type', )
    fields = ( all_fields, )
    list_display = all_fields
    search_fields = all_fields
    readonly_fields = ( 'jaxid' ),
    list_filter = ( 'sample_code', 'sequencing_type', 'project_code' )
    ordering = ['creation_date', 'project_code']


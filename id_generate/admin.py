from django.contrib import admin
from import_export import resources, fields, widgets
from import_export.admin import ImportExportModelAdmin

from .models import JAXIdMasterList, JAXIdDetail,\
        SampleType, SequencingType, ProjectCode
from .forms import JAXIdDetailForm, SequencingForm, SampleForm, ProjectCodeForm
from .generate import generate_JAX_id


# disable the 'delete' action sitewide!
# admin.site.disable_action('delete_selected')

@admin.register(JAXIdMasterList)
class JAXIdListAdmin(admin.ModelAdmin):
    actions_on_top = False
    all_fields = ( 'jaxid', 'creation_date' )
    fields = ( all_fields, )
    list_display = all_fields
    search_fields = all_fields
    readonly_fields = ('creation_date',)
    ordering = ['creation_date']

@admin.register(ProjectCode)
class ProjectCodeAdmin(admin.ModelAdmin):
    form = ProjectCodeForm
    actions_on_top = False
    all_fields = ( 'code', 'details' )
    fields = ( all_fields, )
    list_display = all_fields
    search_fields = all_fields
    ordering = ['code']

@admin.register(SequencingType)
class SequencingType(admin.ModelAdmin):
    form = SequencingForm
    actions_on_top = False
    all_fields = ( 'code', 'details' )
    # all_fields = SequencingType._meta.get_all_field_names(),
    fields = ( all_fields, )
    list_display = all_fields
    search_fields = all_fields
    ordering = ['code']

@admin.register(SampleType)
class SampleType(admin.ModelAdmin):
    form = SampleForm
    actions_on_top = False
    all_fields = ( 'code', 'details' )
    fields = ( all_fields, )
    list_display = all_fields
    search_fields = all_fields
    ordering = ['code']


"""ImportExport Resource"""
class DetailResource(resources.ModelResource):
    jaxid = fields.Field(
        default=generate_JAX_id(prefix='J'),
        readonly=True,
        widget=widgets.CharWidget(),
        )
    project_code = fields.Field(column_name='project_code', attribute='project_code',
        widget=widgets.ForeignKeyWidget(ProjectCode, 'code'),
        )
    sample_type = fields.Field(
        widget=widgets.ForeignKeyWidget(SampleType, 'code'),
        )
    sequencing_type = fields.Field(
        widget=widgets.ForeignKeyWidget(SequencingType, 'code'),
        )
    collab_id = fields.Field(
        widget=widgets.CharWidget(),
        )

    class Meta:
        model = JAXIdDetail
        all_fields = ( 'jaxid', 'project_code', 'collab_id',
                'sample_type', 'sequencing_type', )
        import_id_fields = ( 'jaxid', )
        fields = all_fields
        export_order = all_fields

@admin.register(JAXIdDetail)
# class JAXIdDetailAdmin(admin.ModelAdmin):
class JAXIdDetailAdmin(ImportExportModelAdmin):
    resource_class = DetailResource

    # has_add_permission removes the individual 'add' admin action
    # def has_add_permission(self, request):
        # return False

    form = JAXIdDetailForm
    actions_on_top = False
    actions = None
    all_fields = ( 'jaxid', 'project_code', 'collab_id',
            'sample_type', 'sequencing_type', )
    fields = ( all_fields, )
    list_display = all_fields
    search_fields = all_fields
    readonly_fields = ( 'jaxid' ),
    list_filter = ( 'sample_type', 'sequencing_type', 'project_code' )
    ordering = ['creation_date', 'project_code', 'sequencing_type']


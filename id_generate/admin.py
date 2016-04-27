from django.contrib import admin
from import_export import resources, fields, widgets
from import_export.admin import ImportExportModelAdmin
from import_export.formats import base_formats

from .models import (
        JAXIdDetail,
        SampleType,
        SequencingType,
        NucleicAcidType,
        ProjectCode
        )
from .forms import (
        JAXIdDetailForm,
        SequencingForm,
        SampleForm,
        NucleicAcidTypeForm,
        ProjectCodeForm
        )
from .generate import generate_JAX_id


ID_DETAIL_FIELDS = JAXIdDetail.all_field_names()


# disable the 'delete' action sitewide!
# admin.site.disable_action('delete_selected')

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
class SequencingTypeAdmin(admin.ModelAdmin):
    form = SequencingForm
    actions_on_top = False
    all_fields = ( 'code', 'details' )
    # all_fields = SequencingType._meta.get_all_field_names(),
    fields = ( all_fields, )
    list_display = all_fields
    search_fields = all_fields
    ordering = ['code']

@admin.register(SampleType)
class SampleTypeAdmin(admin.ModelAdmin):
    form = SampleForm
    actions_on_top = False
    all_fields = ( 'code', 'details' )
    fields = ( all_fields, )
    list_display = all_fields
    search_fields = all_fields
    ordering = ['code']

@admin.register(NucleicAcidType)
class NucleicAcidTypeAdmin(admin.ModelAdmin):
    form = NucleicAcidTypeForm
    actions_on_top = False
    all_fields = ( 'code', 'details' )
    fields = ( all_fields, )
    list_display = all_fields
    search_fields = all_fields
    ordering = ['code']


"""ImportExport Resource"""
class DetailResource(resources.ModelResource):
    # jaxid = fields.Field(
        # attribute='jaxid',
        # default=generate_JAX_id(prefix='J'),
        # readonly=True,
        # widget=widgets.CharWidget(),
        # )
    project_code = fields.Field(
        attribute='project_code',
        widget=widgets.ForeignKeyWidget(ProjectCode, 'code'),
        )
    collab_id = fields.Field(
        attribute='collab_id',
        widget=widgets.CharWidget(),
        )
    sample_type = fields.Field(
        attribute='sample_type',
        widget=widgets.ForeignKeyWidget(SampleType, 'code'),
        )
    nucleic_acid_type = fields.Field(
        attribute='nucleic_acid_type',
        widget=widgets.ForeignKeyWidget(NucleicAcidType, 'code'),
        )
    sequencing_type = fields.Field(
        attribute='sequencing_type',
        widget=widgets.ForeignKeyWidget(SequencingType, 'code'),
        )
    sequencing_type = fields.Field(
        attribute='sequencing_type',
        widget=widgets.ForeignKeyWidget(SequencingType, 'code'),
        )
    entered_into_lims = fields.Field(
        attribute='entered_into_lims',
        widget=widgets.BooleanWidget(),
        )
    external_data = fields.Field(
        attribute='external_data',
        widget=widgets.BooleanWidget(),
        )
    notes = fields.Field(
        attribute='notes',
        widget=widgets.CharWidget(),
        )
    raise_errors = True

    class Meta:
        model = JAXIdDetail
        all_fields = ( ID_DETAIL_FIELDS, )
        import_id_fields = ( 'jaxid', )
        fields = ID_DETAIL_FIELDS
        export_order = ID_DETAIL_FIELDS

@admin.register(JAXIdDetail)
# class JAXIdDetailAdmin(admin.ModelAdmin):
class JAXIdDetailAdmin(ImportExportModelAdmin):
    resource_class = DetailResource

    # has_add_permission removes the individual 'add' admin action
    def has_add_permission(self, request):
        return False

    form = JAXIdDetailForm
    actions_on_top = False
    actions = None
    fields = ( ID_DETAIL_FIELDS, )
    # list_display = ID_DETAIL_FIELDS
    list_display = ( 'jaxid',
                     'project_disp',
                     'collab_id',
                     'sample_disp',
                     'nucleic_acid_disp',
                     'sequencing_disp',
                     'entered_into_lims',
                     'external_data',
                     'notes',
                     )
    search_fields = JAXIdDetail.search_fields()
    # readonly_fields = ( 'jaxid', 'creation_date' ),
    readonly_fields = ( 'jaxid' ),
    list_filter = ( 'sample_type', 'sequencing_type',
                    'entered_into_lims', 'project_code', )
    ordering = ['creation_date', 'project_code', 'sequencing_type']
    formats = (base_formats.XLSX, base_formats.CSV, )


from django.contrib import admin
from django.contrib.admin.sites import AdminSite

from import_export import resources, fields, widgets
from import_export.admin import ExportActionModelAdmin, ImportExportModelAdmin, \
                                ImportExportMixin, ExportMixin
from import_export.formats import base_formats

from suit.admin import RelatedFieldAdmin, get_related_field
from suit import apps

from generator.admin_link import admin_changelist_link

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
from .jaxid_create import JAXidGenerate


ID_DETAIL_FIELDS = JAXIdDetail.all_field_names()

# IdGenerate AdminSite
admin.site.site_header = 'Mbiome Core JAXid Tracking Administration'
admin.site.site_title = 'Mbiome Core JAXid Tracking'
admin.site.index_title = 'JAXid Generator'

@admin.register(ProjectCode)
class ProjectCodeAdmin(admin.ModelAdmin):
    form = ProjectCodeForm
    actions_on_top = False
    all_fields = ( 'code', 'details' )
    fields = ((all_fields))
    list_display = all_fields
    search_fields = all_fields
    ordering = ['code']
    suit_list_filter_horizontal = all_fields

@admin.register(SequencingType)
class SequencingTypeAdmin(admin.ModelAdmin):
    form = SequencingForm
    actions_on_top = False
    all_fields = ( 'code', 'details' )
    # all_fields = SequencingType._meta.get_all_field_names(),
    fields = ((all_fields))
    list_display = all_fields
    search_fields = all_fields
    ordering = ['code']

@admin.register(SampleType)
class SampleTypeAdmin(admin.ModelAdmin):
    form = SampleForm
    actions_on_top = False
    all_fields = ( 'code', 'details' )
    fields = ((all_fields))
    list_display = all_fields
    search_fields = all_fields
    ordering = ['code']

@admin.register(NucleicAcidType)
class NucleicAcidTypeAdmin(admin.ModelAdmin):
    form = NucleicAcidTypeForm
    actions_on_top = False
    all_fields = ( 'code', 'details' )
    fields = ((all_fields))
    list_display = all_fields
    search_fields = all_fields
    ordering = ['code']


"""ImportExport Resource"""
class DetailResource(resources.ModelResource):
    project_code = fields.Field(
            attribute='project_code',
            widget=widgets.ForeignKeyWidget(
                ProjectCode, 'code'),)
    collab_id = fields.Field(
            attribute='collab_id',
            widget=widgets.CharWidget(),)
    sample_type = fields.Field(
            attribute='sample_type',
            widget=widgets.ForeignKeyWidget(
                SampleType, 'code'),)
    nucleic_acid_type = fields.Field(
            attribute='nucleic_acid_type',
            widget=widgets.ForeignKeyWidget(
                NucleicAcidType, 'code'),)
    sequencing_type = fields.Field(
            attribute='sequencing_type',
            widget=widgets.ForeignKeyWidget(
                SequencingType, 'code'),)
    sequencing_type = fields.Field(
            attribute='sequencing_type',
            widget=widgets.ForeignKeyWidget(
                SequencingType, 'code'),)
    entered_into_lims = fields.Field(
            attribute='entered_into_lims',
            widget=widgets.BooleanWidget(),)
    external_data = fields.Field(
            attribute='external_data',
            widget=widgets.BooleanWidget(),)
    notes = fields.Field(
            attribute='notes',
            widget=widgets.CharWidget(),)
    raise_errors = True

    def assign_new_id(self, new_ids, current_ids):
        """recursively select id that is not used already in current set to be imported
            params:
                new_ids:  generator
                current_ids: list of used ids
        """
        # print("current_ids: {}".format(current_ids))
        next_id = next(new_ids)
        if next_id in current_ids:
            return self.assign_new_id(new_ids, current_ids)
        else:
            return next_id

    def before_import(self, dataset, using_transactions=True, dry_run=False, **kwargs):
        """ Overridden to generate new JAXid values for each row to be imported. """
        num_rows = dataset.height
        print('num_rows in dataset: {}'.format(num_rows))

        #TODO: implement kwargs.prefix for Box/Plate/...
        id_prefix = kwargs.get('prefix', 'J')

        jid = JAXidGenerate(prefix=id_prefix)
        new_jaxids = jid.generate_new_ids(num_rows)

        jaxid_col_num = dataset.headers.index('jaxid')
        dataset_jaxids = set([row[jaxid_col_num]
                              for row in dataset
                              if row[jaxid_col_num] != ''])
        # print("current_ids used by incoming dataset: {}".format(dataset_jaxids))

        for row in dataset.dict:
            # print('dataset: {}'.format(row))
            if row['jaxid'] == '':
                row['jaxid'] = self.assign_new_id(new_jaxids, dataset_jaxids)
                # print('dataset 2: {}'.format(row))
            print('dataset final: {}'.format(row))

        return super(self.__class__, self).before_import(dataset, using_transactions,
                                                         dry_run, **kwargs)


    # def before_import_row(self, row, **kwargs):
    #     pass


    class Meta:
        model = JAXIdDetail
        all_fields = ( ID_DETAIL_FIELDS, )
        import_id_fields = ( 'jaxid', )
        fields = ID_DETAIL_FIELDS
        export_order = ID_DETAIL_FIELDS

class IdImpExpMixin(ImportExportModelAdmin):
    """subclass with mods for JAXids"""
    def __init__(self):
        super(IDExportMixin, self).__init__()
        self.resource_class = DetailResource
        self.change_list_template = 'admin/import_export/change_list_export.html'
        self.export_template_name = 'admin/import_export/export.html'


@admin.register(JAXIdDetail)
class JAXIdDetailAdmin(ImportExportModelAdmin, RelatedFieldAdmin):
    resource_class = DetailResource
    # change_list_template = 'admin/import_export/change_list_export.html'
    # export_template_name = 'admin/import_export/export.html'

    def has_delete_permission(self, request, obj=None):
        """has_delete_permission removes 'delete' admin action"""
        return False
    def has_add_permission(self, request):
        """has_add_permission removes the individual 'add' admin action"""
        return False

    form = JAXIdDetailForm
    actions_on_top = False
    actions = None
    readonly_fields = ( 'jaxid', 'creation_date' )
    fieldsets = (
            (None, {'fields': ['jaxid', 'parent_jaxid']}),
            (None, {'fields': ['project_code','collab_id']}),
            (None, {'fields': ['sample_type', 'nucleic_acid_type', 'sequencing_type']}),
            (None, {'fields': ['entered_into_lims', 'external_data']}),
            (None, {'fields': ['notes']}),
            (None, {'fields': ['creation_date']}),
        )
    list_select_related = ('project_code', 'nucleic_acid_type', 'sequencing_type', 'sample_type',)
    list_display = ( 'jaxid',
                     'parent_jaxid',
                     'project_code_subset',
                     'collab_id',
                     'sample_type_code',
                     'nucleic_acid_type_code',
                     'sequencing_type_code',
                     # 'entered_into_lims',
                     # 'external_data',
                     'notes',
                     )
    search_fields = JAXIdDetail.search_fields()
    list_filter = ('project_code', 'sample_type', 'nucleic_acid_type', 'sequencing_type',)
    suit_list_filter_horizontal = list_filter
    ordering = ['-jaxid']
    formats = (base_formats.XLSX, base_formats.CSV, )

    @admin_changelist_link('project_code', 'Project',
            query_string=lambda j: 'project_code__exact={}'.format(j.project_code.code))
    def project_code_subset(self, project_code):
        return project_code.code

    JAXIdDetail.project_code_code.admin_order_field = 'project_code'
    JAXIdDetail.nucleic_acid_type_code.admin_order_field = 'nucleic_acid_type'
    JAXIdDetail.sequencing_type_code.admin_order_field = 'sequencing_type'
    JAXIdDetail.sample_type_code.admin_order_field = 'sample_type'


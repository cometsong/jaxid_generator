import pprint

from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from django.contrib.sessions.models import Session

from import_export import fields, widgets
from import_export.admin import ExportActionModelAdmin, ImportExportModelAdmin, \
                                ImportExportMixin, ExportMixin
from import_export.formats import base_formats

from suit.admin import RelatedFieldAdmin, get_related_field
from suit import apps

from generator.utils import admin_changelist_link

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
from .import_data import DetailResource, export_dataset



ID_DETAIL_FIELDS = JAXIdDetail.all_field_names()

# IdGenerate AdminSite
class IdGenAdminSite(AdminSite):
    site_header = 'Mbiome Core JAXid Tracking Administration'
    site_title = 'Mbiome Core JAXid Tracking'
    site_owner = 'Microbiome Core'
    index_title = 'JAXid Generator'
    site_url = None

admin_gen = IdGenAdminSite()


class SessionAdmin(admin.ModelAdmin):
    def _session_data(self, obj):
        return pprint.pformat(obj.get_decoded()).replace('\n', '<br>\n')
    _session_data.allow_tags=True
    list_display = ['session_key', '_session_data', 'expire_date']
    readonly_fields = ['_session_data']
    exclude = ['session_data']
admin_gen.register(Session, SessionAdmin)

# @admin.register(ProjectCode)
class ProjectCodeAdmin(admin.ModelAdmin):
    form = ProjectCodeForm
    actions_on_top = False
    all_fields = ( 'code', 'details' )
    fields = ((all_fields))
    list_display = all_fields
    search_fields = all_fields
    ordering = ['code']
    suit_list_filter_horizontal = all_fields
admin_gen.register(ProjectCode, ProjectCodeAdmin)

# @admin.register(SequencingType)
class SequencingTypeAdmin(admin.ModelAdmin):
    form = SequencingForm
    actions_on_top = False
    all_fields = ( 'code', 'details' )
    # all_fields = SequencingType._meta.get_all_field_names(),
    fields = ((all_fields))
    list_display = all_fields
    search_fields = all_fields
    ordering = ['code']
admin_gen.register(SequencingType, SequencingTypeAdmin)

# @admin.register(SampleType)
class SampleTypeAdmin(admin.ModelAdmin):
    form = SampleForm
    actions_on_top = False
    all_fields = ( 'code', 'details' )
    fields = ((all_fields))
    list_display = all_fields
    search_fields = all_fields
    ordering = ['code']
admin_gen.register(SampleType, SampleTypeAdmin)

# @admin.register(NucleicAcidType)
class NucleicAcidTypeAdmin(admin.ModelAdmin):
    form = NucleicAcidTypeForm
    actions_on_top = False
    all_fields = ( 'code', 'details' )
    fields = ((all_fields))
    list_display = all_fields
    search_fields = all_fields
    ordering = ['code']
admin_gen.register(NucleicAcidType, NucleicAcidTypeAdmin)


# @admin.register(JAXIdDetail)
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
                     'notes',
                     )
    search_fields = JAXIdDetail.search_fields()
    list_filter = ('project_code', 'sample_type', 'nucleic_acid_type', 'sequencing_type',)
    suit_list_filter_horizontal = list_filter
    ordering = ['-creation_date']
    # formats = (base_formats.XLSX, base_formats.CSV, )
    formats = (base_formats.XLSX,)

    @admin_changelist_link('project_code', 'Project',
            query_string=lambda j: 'project_code__exact={}'.format(j.project_code.code))
    def project_code_subset(self, project_code):
        return project_code.code

    JAXIdDetail.project_code_code.admin_order_field = 'project_code'
    JAXIdDetail.nucleic_acid_type_code.admin_order_field = 'nucleic_acid_type'
    JAXIdDetail.sequencing_type_code.admin_order_field = 'sequencing_type'
    JAXIdDetail.sample_type_code.admin_order_field = 'sample_type'

    # def get_urls(self):
    #     urls = super().get_urls()
    #     my_urls = [
    #         url(r'^export/$',
    #             self.admin_site.admin_view(self.export_action),
    #             name='%s_%s_export' % self.get_model_info()),
    #         # added in by bleopold 20170912
    #         url(r'^export_imported/$',
    #             self.admin_site.admin_view(self.export_imported_action),
    #             name='%s_%s_export' % self.get_model_info()),
    #     ]
    #     return my_urls + urls
admin_gen.register(JAXIdDetail, JAXIdDetailAdmin)



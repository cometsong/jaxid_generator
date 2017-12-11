import pprint

from django.http import QueryDict
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.shortcuts import redirect, render
from django.template.response import TemplateResponse

from django.contrib import messages
from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin, GroupAdmin

from django.views.decorators.cache import never_cache

from import_export import fields, widgets
from import_export.admin import ImportExportModelAdmin
from import_export.formats import base_formats

from suit.admin import RelatedFieldAdmin, get_related_field
# from suit import apps
from django.apps import apps

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
from .import_data import DetailResource


# IdGenerate AdminSite
class IdGenAdminSite(AdminSite):
    site_header = 'Mbiome Core JAXid Tracking Administration'
    site_title = 'Mbiome Core JAXid Tracking'
    site_owner = 'Microbiome Core'
    index_title = 'JAXid Generator'
    site_url = None

idadmin = IdGenAdminSite()

admin.site.unregister(User)
admin.site.unregister(Group)
# UserAdmin.list_filter = ['is_staff'] #TODO: redefine list_filter to make default is_staff=Yes
# UserAdmin.verbose_name = 'Staff' #TODO: mod breadcrumbs and url of 'users' to 'staff'
UserAdmin.list_display = ('username', 'first_name', 'last_name',
                          'is_active', 'is_superuser',)
idadmin.register(User, UserAdmin)
idadmin.register(Group, GroupAdmin)

class SessionAdmin(admin.ModelAdmin):
    def _session_data(self, obj):
        return pprint.pformat(obj.get_decoded()).replace('\n', '<br>\n')
    _session_data.allow_tags=True
    list_display = ['session_key', '_session_data', 'expire_date']
    readonly_fields = ['_session_data']
    exclude = ['session_data']
idadmin.register(Session, SessionAdmin)

class ProjectCodeAdmin(admin.ModelAdmin):
    form = ProjectCodeForm
    actions_on_top = False
    all_fields = ( 'code', 'details' )
    fields = ((all_fields))
    list_display = all_fields
    search_fields = all_fields
    ordering = ['code']
    suit_list_filter_horizontal = all_fields
idadmin.register(ProjectCode, ProjectCodeAdmin)

class SequencingTypeAdmin(admin.ModelAdmin):
    form = SequencingForm
    actions_on_top = False
    all_fields = ( 'code', 'details' )
    # all_fields = SequencingType._meta.get_all_field_names(),
    fields = ((all_fields))
    list_display = all_fields
    search_fields = all_fields
    ordering = ['code']
idadmin.register(SequencingType, SequencingTypeAdmin)

class SampleTypeAdmin(admin.ModelAdmin):
    form = SampleForm
    actions_on_top = False
    all_fields = ( 'code', 'details' )
    fields = ((all_fields))
    list_display = all_fields
    search_fields = all_fields
    ordering = ['code']
idadmin.register(SampleType, SampleTypeAdmin)

class NucleicAcidTypeAdmin(admin.ModelAdmin):
    form = NucleicAcidTypeForm
    actions_on_top = False
    all_fields = ( 'code', 'details' )
    fields = ((all_fields))
    list_display = all_fields
    search_fields = all_fields
    ordering = ['code']
idadmin.register(NucleicAcidType, NucleicAcidTypeAdmin)

class JAXIdDetailAdmin(ImportExportModelAdmin, RelatedFieldAdmin):
    resource_class = DetailResource

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


    def add_export_message(self, request, imported_ids=None):
        opts = self.model._meta
        if imported_ids:
            export_message = f'The ids imported into {opts.verbose_name_plural}, can <em>now</em> be ' \
                             f'exported using the &quot;Export&quot; button on the right. '
            messages.info(request, export_message)


    def get_queryset(self, request):
        """ Returns queryset. Default implementation respects applied search and filters.
        This override returns request attr 'imported_queryset' if exists
        """
        try:
            qs = super().get_queryset(request)
            print(f'DEBUG: qs - super_qset length: {qs.count()}')
            print('DEBUG: qs - getting qset_attr')
            pks_attr = request.POST.getlist('imported_pks')
            print(f'DEBUG: qs - pks_attr POST: {pks_attr!s}')
            if pks_attr:
                print('DEBUG: qs - filtering qset super')
                qs = qs.filter(pk__in=pks_attr)
                print(f'DEBUG: qs - qset pks length: {qs.count()}')
        except Exception as e:
            print(f'ERROR: qs - Exception: {e.response}')
        finally:
            print(f'DEBUG: qs - qset length: {qs.count()}')
            return qs


    # def get_changelist(self, request, **kwargs):
    #     """ Returns the ChangeList class for use on the changelist page. """
    #     return IdChangeList  # override with local class


    # override import-export admin method to redirect to immediate export url post-import
    def process_result(self, result, request):
        print(f'DEBUG: entering overridden process_result')
        try:
            # print(f'DEBUG: calling super process_result')
            sup = super().process_result(result, request)

            imported_pks = [row.object_id for row in result.rows]

            if request.method == 'POST' and request.POST:
                request.POST = request.POST.copy() # mutable via copy
                request.POST.setlist('imported_pks', imported_pks)
                # print(f'DEBUG: req POST: {request.POST!s}')

            from django.contrib import messages
            self.add_export_message(request, imported_ids=imported_pks)
        except Exception as e:
            print(f'DEBUG: request copy/mod/reinstate yuckiness: {e.message!s}')
            # raise e
        finally:
            return self.changelist_view(request, extra_context=None)

idadmin.register(JAXIdDetail, JAXIdDetailAdmin)



from django.contrib.admin.views.main import ChangeList
class IdChangeList(ChangeList):
    """ Override default Changelist to check for request attr 'imported_pks' """

    def get_queryset(self, request):
        """ Returns queryset. Default implementation respects applied search and filters.
        This override returns request attr 'imported_queryset' if exists
        """
        try:
            qs = super().get_queryset(request)
            print(f'DEBUG: qs - super_qset length: {qs.count()}')
            print('DEBUG: qs - getting qset_attr')
            pks_attr = request.POST.getlist('imported_pks')
            print(f'DEBUG: qs - pks_attr POST: {pks_attr!s}')
            if pks_attr:
                print('DEBUG: qs - filtering qset super')
                qs = qs.filter(pk__in=pks_attr)
                print(f'DEBUG: qs - qset pks length: {qs.count()}')
        except Exception as e:
            print(f'ERROR: qs - Exception: {e.response}')
        finally:
            print(f'DEBUG: qs - qset length: {qs.count()}')
            return qs


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # qs = self.get_queryset(request) #AttributeError


import os
import pprint

from django.conf import settings
from django.contrib import messages
from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from django.contrib.admin.views.main import ChangeList
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin, GroupAdmin

from django.contrib.admin.models import LogEntry
from admin_log_entries.admin import LogEntryAdmin

from import_export.admin import ImportExportModelAdmin
from import_export.formats import base_formats

from suit.admin import RelatedFieldAdmin, get_related_field
# from suit import apps
from django.apps import apps

from generator.utils import admin_changelist_link, funcname

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

# implement and register databrowse for external read-only access
import django_databrowse
django_databrowse.site.register(ProjectCode, SampleType, SequencingType, NucleicAcidType, JAXIdDetail)


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

idadmin.register(LogEntry, LogEntryAdmin)

# from django.contrib.auth.models import Permission
# idadmin.register(Permission)

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
    # suit_list_filter_horizontal = list_filter
    # suit_list_filter_horizontal = ('project_code', 'sequencing_type',)
    # suit_list_filter_horizontal = JAXIdDetail.all_field_names()

    ordering = ['-creation_date']
    formats = (base_formats.XLSX, base_formats.CSV, )
    # formats = (base_formats.XLSX,)

    @admin_changelist_link('project_code', 'Project',
            query_string=lambda j: 'project_code__exact={}'.format(j.project_code.code))
    def project_code_subset(self, project_code):
        return project_code.code

    JAXIdDetail.project_code_code.admin_order_field = 'project_code'
    JAXIdDetail.nucleic_acid_type_code.admin_order_field = 'nucleic_acid_type'
    JAXIdDetail.sequencing_type_code.admin_order_field = 'sequencing_type'
    JAXIdDetail.sample_type_code.admin_order_field = 'sample_type'


    def export_imported_file(self, request, *args, **kwargs):
        try:
            print(f'DEBUG: {funcname()} beginning')
            input_format = request.POST.get('input_format')
            orig_filename = request.POST.get('original_file_name')
            new_name_prefix = 'generated'
            export_filename = '_'.join([new_name_prefix, orig_filename])
            print(f'DEBUG: {funcname()} - format: {input_format}, export_name: {export_filename}')

            formats = self.get_export_formats()
            file_format = formats[int(input_format)]()
            # print(f'DEBUG: {funcname()} file_format: {file_format!s}')

            queryset = self.get_export_queryset(request)
            # print(f'DEBUG: {funcname()} queryset: {queryset!s}')

            export_data = self.get_export_data(file_format, queryset, request=request)
            # print(f'DEBUG: {funcname()} dataset length: {len(export_data)!s}')
            file_baseurl = settings.IMPORTED_FILE_PATH
            file_basepath = os.path.join(settings.HTML_DIR, settings.IMPORTED_FILE_PATH)
            filepath = os.path.join(file_basepath, export_filename)
            fileurl = os.path.join('/', file_baseurl, export_filename)
            # print(f'DEBUG: {funcname()} filepath: {filepath!s}')
            # print(f'DEBUG: {funcname()} fileurl: {fileurl!s}')
            with open(filepath, 'wb') as exp:
                exp.write(export_data)
        except Exception as e:
            print(f'ERROR: {funcname()}: {e.message!s}')
            # raise e
        finally:
            return fileurl


    def add_export_message(self, request, file_url=None):
        opts = self.model._meta
        if file_url:
            filename = os.path.basename(file_url)
            export_message = f'The ids imported into {opts.verbose_name_plural}, can <em>now</em> be ' \
                             f'downloaded with this link: <a href={file_url!s}>"{filename}"</a>'
            messages.info(request, export_message)


    def get_changelist(self, request, **kwargs):
        """ Returns the ChangeList class for use on the changelist page. """
        return IdChangeList  # override with local class


    # override import-export admin method to redirect to immediate export url post-import
    def process_result(self, result, request):
        print(f'DEBUG: entering overridden process_result')
        try:
            # print(f'DEBUG: {funcname()} calling super process_result')
            sup = super().process_result(result, request)
            imported_ids = [row.object_id for row in result.rows]

            if request.method == 'POST' and request.POST:
                request.POST = request.POST.copy() # mutable via copy
                request.POST.setlist('imported_ids', imported_ids)
                # print(f'DEBUG: req POST: {request.POST!s}')

            export_file_url = self.export_imported_file(request)
            from django.contrib import messages
            self.add_export_message(request, file_url=export_file_url)
        except Exception as e:
            print(f'ERROR: {funcname()} request copy/mod/reinstate yuckiness: {e.message!s}')
            # raise e
        finally:
            return self.changelist_view(request, extra_context=None)

idadmin.register(JAXIdDetail, JAXIdDetailAdmin)



class IdChangeList(ChangeList):
    """ Override default Changelist to check for request attr 'imported_ids' """

    def get_queryset(self, request):
        """ Returns queryset. Default implementation respects applied search and filters.
        This override returns request attr 'imported_queryset' if exists
        """
        try:
            qs = super().get_queryset(request)
            # print(f'DEBUG: {settings.APP_NAME}: qs - super_qset length: {qs.count()}')
            # print(f'DEBUG: {funcname()} - getting qset_attr')
            pks_attr = request.POST.getlist('imported_ids')
            # print(f'DEBUG: {funcname()} - pks_attr: {pks_attr!s}')
            if pks_attr:
                print(f'DEBUG: {funcname()} - filtering qset super')
                qs = qs.filter(pk__in=pks_attr)
                # print(f'DEBUG: qs - qset pks length: {qs.count()}')
        except Exception as e:
            print(f'ERROR: {funcname()} - Exception: {e.response}')
        finally:
            # print(f'DEBUG: {funcname()} - qset length: {qs.count()}')
            return qs


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # qs = self.get_queryset(request) #AttributeError
        # self.queryset = self.get_queryset(request) #NameError requeset not defined


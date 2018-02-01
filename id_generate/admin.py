import os
import re
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
        BoxId,
        SampleType,
        SequencingType,
        NucleicAcidType,
        ProjectCode
        )
from .forms import (
        JAXIdDetailForm,
        BoxIdForm,
        SequencingForm,
        SampleForm,
        NucleicAcidTypeForm,
        ProjectCodeForm
        )
from .import_data import DetailResource, BoxIdResource
from .admin_import_mixin import BaseImportAdmin
from .changelist import IdChangeList

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
    actions = None
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
    actions = None
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
    actions = None
    all_fields = ( 'code', 'details' )
    fields = ((all_fields))
    list_display = all_fields
    search_fields = all_fields
    ordering = ['code']
idadmin.register(SampleType, SampleTypeAdmin)

class NucleicAcidTypeAdmin(admin.ModelAdmin):
    form = NucleicAcidTypeForm
    actions_on_top = False
    actions = None
    all_fields = ( 'code', 'details' )
    fields = ((all_fields))
    list_display = all_fields
    search_fields = all_fields
    ordering = ['code']
idadmin.register(NucleicAcidType, NucleicAcidTypeAdmin)

class JAXIdDetailAdmin(BaseImportAdmin, RelatedFieldAdmin):
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
    list_select_related = ('project_code', 'nucleic_acid_type',
                           'sequencing_type', 'sample_type',)
    list_display = ( 'jaxid',
                     'parent_jaxid',
                     'project_code_code',
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
    formats = (base_formats.XLSX,)

    JAXIdDetail.project_code_code.admin_order_field = 'project_code'
    JAXIdDetail.nucleic_acid_type_code.admin_order_field = 'nucleic_acid_type'
    JAXIdDetail.sequencing_type_code.admin_order_field = 'sequencing_type'
    JAXIdDetail.sample_type_code.admin_order_field = 'sample_type'

    def get_changelist(self, request, **kwargs):
        """ Returns the ChangeList class for use on the changelist page. """
        return IdChangeList  # override with local class

idadmin.register(JAXIdDetail, JAXIdDetailAdmin)


# class BoxIdAdmin(BaseImportAdmin):
class BoxIdAdmin(BaseImportAdmin, RelatedFieldAdmin):
    resource_class = BoxIdResource

    def has_delete_permission(self, request, obj=None):
        """has_delete_permission removes 'delete' admin action"""
        return False
    def has_add_permission(self, request):
        """has_add_permission removes the individual 'add' admin action"""
        return False

    form = BoxIdForm
    actions_on_top = False
    actions = None
    readonly_fields = ( 'jaxid', 'creation_date' )
    fieldsets = (
            (None, {'fields': ['jaxid', 'collab_id']}),
            (None, {'fields': ['project_code', 'parent_jaxid']}),
            (None, {'fields': ['sample_type', 'nucleic_acid_type', 'sequencing_type']}),
            (None, {'fields': ['notes']}),
            (None, {'fields': ['creation_date']}),
        )
    list_select_related = ('project_code', 'nucleic_acid_type',
                           'sequencing_type', 'sample_type',)
    list_display = ( 'jaxid',
                     'collab_id',
                     'parent_jaxid',
                     'project_code',
                     'sample_type',
                     'nucleic_acid_type',
                     'notes',
                     )
    search_fields = BoxId.all_field_names
    list_filter = ('project_code', 'sample_type', 'nucleic_acid_type', 'sequencing_type',)

    ordering = ['-creation_date']
    formats = (base_formats.XLSX,)

    def get_changelist(self, request, **kwargs):
        """ Returns the ChangeList class for use on the changelist page. """
        return IdChangeList  # override with local class


idadmin.register(BoxId, BoxIdAdmin)

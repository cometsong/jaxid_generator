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
        PlateId,
        SampleType,
        SequencingType,
        NucleicAcidType,
        ProjectCode
        )
from .forms import (
        JAXIdDetailForm,
        BoxIdForm,
        PlateIdForm,
        SequencingForm,
        SampleForm,
        NucleicAcidTypeForm,
        ProjectCodeForm
        )
from .import_data import DetailResource, BoxIdResource, PlateIdResource
from .admin_import_mixin import BaseImportAdmin

# implement and register databrowse for external read-only access
import django_databrowse
django_databrowse.site.register(ProjectCode, SampleType, SequencingType, NucleicAcidType,
                                JAXIdDetail, BoxId, PlateId)


# IdGenerate AdminSite
from django.utils.text import capfirst
from django.urls import NoReverseMatch, reverse
class IdGenAdminSite(AdminSite):
    site_header = 'Mbiome Core JAXid Tracking Administration'
    site_title = 'Mbiome Core JAXid Tracking'
    site_owner = 'Microbiome Core'
    index_title = 'JAXid Generator'
    site_url = None

    def _build_app_dict(self, request, label=None):
        """
        Overridden to use 'display_order for both Apps and Models'

        Builds the app dictionary. Takes an optional label parameters to filter
        models of a specific app.
        """
        app_dict = {}

        if label:
            models = {
                m: m_a for m, m_a in self._registry.items()
                if m._meta.app_label == label
            }
        else:
            models = self._registry

        for model, model_admin in models.items():
            app_label = model._meta.app_label

            has_module_perms = model_admin.has_module_permission(request)
            if not has_module_perms:
                continue

            perms = model_admin.get_model_perms(request)

            # Check whether user has any perm for this module.
            # If so, add the module to the model_list.
            if True not in perms.values():
                continue

            info = (app_label, model._meta.model_name)
            model_dict = {
                'name': capfirst(model._meta.verbose_name_plural),
                'display_order': model.display_order,
                'object_name': model._meta.object_name,
                'perms': perms,
            }
            if perms.get('change'):
                try:
                    model_dict['admin_url'] = reverse('admin:%s_%s_changelist' % info, current_app=self.name)
                except NoReverseMatch:
                    pass
            if perms.get('add'):
                try:
                    model_dict['add_url'] = reverse('admin:%s_%s_add' % info, current_app=self.name)
                except NoReverseMatch:
                    pass

            if app_label in app_dict:
                app_dict[app_label]['models'].append(model_dict)
            else:
                app_dict[app_label] = {
                    'name': apps.get_app_config(app_label).verbose_name,
                    'app_label': app_label,
                    'display_order': model.display_order,
                    'app_url': reverse(
                        'admin:app_list',
                        kwargs={'app_label': app_label},
                        current_app=self.name,
                    ),
                    'has_module_perms': has_module_perms,
                    'models': [model_dict],
                }

        if label:
            return app_dict.get(label)
        return app_dict

    def get_app_list(self, request):
        """
        Returns a sorted list of all the installed apps that have been
        registered in this site.
        """
        app_dict = self._build_app_dict(request)

        # Sort the apps alphabetically.
        app_list = sorted(app_dict.values(), key=lambda x: x['name'].lower())

        # Sort the models by display_order within each app.
        for app in app_list:
            app['models'].sort(key=lambda x: x['display_order'])

        return app_list

idadmin = IdGenAdminSite()

admin.site.unregister(User)
User.display_order = 1
User._meta.verbose_name = 'Staff'
User._meta.verbose_name_plural = 'Staff Members'
UserAdmin.list_display = ('username', 'first_name', 'last_name',
                          'is_active', 'is_superuser',)
idadmin.register(User, UserAdmin)

admin.site.unregister(Group)
Group.display_order = 2
idadmin.register(Group, GroupAdmin)

LogEntry.display_order = 3
idadmin.register(LogEntry, LogEntryAdmin)

# from django.contrib.auth.models import Permission
# idadmin.register(Permission)

Session.display_order = 1
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

class JAXIdDetailAdmin(BaseImportAdmin):
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
idadmin.register(JAXIdDetail, JAXIdDetailAdmin)

class BoxIdAdmin(BaseImportAdmin):
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
idadmin.register(BoxId, BoxIdAdmin)

class PlateIdAdmin(BaseImportAdmin):
    resource_class = PlateIdResource

    def has_delete_permission(self, request, obj=None):
        """has_delete_permission removes 'delete' admin action"""
        return False
    def has_add_permission(self, request):
        """has_add_permission removes the individual 'add' admin action"""
        return False

    form = PlateIdForm
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
    search_fields = PlateId.all_field_names
    list_filter = ('project_code', 'sample_type', 'nucleic_acid_type', 'sequencing_type',)

    ordering = ['-creation_date']
    formats = (base_formats.XLSX,)
idadmin.register(PlateId, PlateIdAdmin)

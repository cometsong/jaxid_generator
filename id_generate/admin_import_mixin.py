import os
import re

from django.conf import settings
from django.contrib import messages

from import_export.admin import ImportExportModelAdmin

from generator.utils import funcname

class BaseImportAdmin(ImportExportModelAdmin):
    """Abstract Base Admin mixin for generic import/export methods """

    def export_imported_file(self, request, *args, **kwargs):
        try:
            print(f'DEBUG: {funcname()} beginning')
            input_format = request.POST.get('input_format')
            orig_filename = request.POST.get('original_file_name')
            print(f'DEBUG: {funcname()} - format: {input_format}, orig_filename: {orig_filename}')
            new_name_prefix = 'generated'
            export_filename = '_'.join([new_name_prefix, orig_filename])
            export_filename, subnum = re.subn(' ', '_', export_filename)
            print(f'DEBUG: {funcname()} - export_name: {export_filename}')

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
            print(f'DEBUG: {funcname()} fileurl: {fileurl!s}')
            with open(filepath, 'wb') as exp:
                exp.write(export_data)
        except Exception as e:
            print(f'ERROR: {funcname()}: {e.message!s}')
            # raise e
        finally:
            print(f'DEBUG: {funcname()} finally fileurl: {fileurl!s}')
            return fileurl


    def add_export_message(self, request, file_url=None):
        print(f'DEBUG: {funcname()} beginning')
        opts = self.model._meta
        if file_url:
            print(f'DEBUG: {funcname()} file_url: {file_url}')
            filename = os.path.basename(file_url)
            export_message = f'The ids imported into {opts.verbose_name_plural}, can <em>now</em> be ' \
                             f'downloaded with this link: <a href={file_url!s}>"{filename}"</a>'
            messages.info(request, export_message)


    def process_result(self, result, request):
        """override import-export admin method to redirect to immediate export url post-import"""
        print(f'DEBUG: entering overridden process_result')
        try:
            print(f'DEBUG: {funcname()} calling super process_result')
            sup = super().process_result(result, request)
            imported_ids = [row.object_id for row in result.rows]
            print(f'DEBUG: {funcname()} imported_ids: {imported_ids!s}')

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
            print(f'DEBUG: {funcname()} finally: return changelist_view')
            return self.changelist_view(request, extra_context=None)

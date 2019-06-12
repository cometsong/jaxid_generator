from django.contrib.admin.views.main import ChangeList

from generator.utils import funcname

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
            if pks_attr:
                print(f'DEBUG: {funcname()} - pks_attr: {pks_attr!s}')
                print(f'DEBUG: {funcname()} - filtering qset super')
                qs = qs.filter(pk__in=pks_attr).reverse()
                # flag this qs as results from most recent import
                self.import_results = True
        except Exception as e:
            print(f'ERROR: {funcname()} - Exception: {e}')
        else:
            # print(f'DEBUG: {funcname()} - qset length: {qs.count()}')
            return qs


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

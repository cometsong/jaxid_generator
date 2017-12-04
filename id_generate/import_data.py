import re
import tablib
from import_export import resources, fields, widgets
# from django.shortcuts import redirect
from django_mysql.locks import TableLock

from .jaxid_create import JAXidGenerate
# from .generate import check_id_type

from . import models
from .models import (
        JAXIdDetail,
        SampleType,
        SequencingType,
        NucleicAcidType,
        ProjectCode
        )
from generator.utils import field_is_empty

ID_DETAIL_FIELDS = JAXIdDetail.all_field_names()

"""ImportExport Resource"""
class DetailResource(resources.ModelResource):
    project_code = fields.Field(attribute='project_code',
            widget=widgets.ForeignKeyWidget(ProjectCode, 'code'),)
    collab_id = fields.Field(attribute='collab_id',
            widget=widgets.CharWidget(),)
    sample_type = fields.Field(attribute='sample_type',
            widget=widgets.ForeignKeyWidget(SampleType, 'code'),)
    nucleic_acid_type = fields.Field(attribute='nucleic_acid_type',
            widget=widgets.ForeignKeyWidget(NucleicAcidType, 'code'),)
    sequencing_type = fields.Field(attribute='sequencing_type',
            widget=widgets.ForeignKeyWidget(SequencingType, 'code'),)
    entered_into_lims = fields.Field(attribute='entered_into_lims',
            widget=widgets.BooleanWidget(),)
    external_data = fields.Field(attribute='external_data',
            widget=widgets.BooleanWidget(),)
    notes = fields.Field(attribute='notes',
            widget=widgets.CharWidget(),)

    raise_errors = True
    skip_unchanged = True
    report_skipped = True

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


    def import_data(self, dataset, **kwargs):
        """Overridden from import_action to lock table then call super().import_data()"""
        #TODO: implement table-locking from before until after import
        tables_need_some_lockin = [models.JAXIdDetail,
                                   models.SampleType,
                                   models.SequencingType,
                                   models.NucleicAcidType,
                                   models.ProjectCode
                                  ]
        return super().import_data(dataset, table_locks=tables_need_some_lockin, **kwargs)    

    def before_import(self, dataset, using_transactions=True, dry_run=False, **kwargs):
        """ Overridden to generate new JAXid values for each row to be imported. """
        #TODO: implement table-locking from before until after import
        num_rows = dataset.height
        print('DEBUG: num_rows in dataset: {}'.format(num_rows))

        def replace_row(row_index, row_dict):
            """'pop' for specific index number within dataset, followed by insertion of new 'row' values"""
            del dataset[row_index]
            dataset.insert(row_index, row_dict.values())

        #TODO: implement kwargs.prefix for Box/Plate/...
        id_prefix = kwargs.get('prefix', 'J')
        PREFIXES = 'JBP'

        jid = JAXidGenerate(prefix=id_prefix)
        new_jaxids = jid.generate_new_ids(num_rows)

        jaxid_col_num = dataset.headers.index('jaxid')
        dataset_jaxids = set([row[jaxid_col_num]
                              for row in dataset
                              if not field_is_empty(row[jaxid_col_num])])
        # print("DEBUG: current_ids used by incoming dataset: {}".format(dataset_jaxids))

        # loop through rows, assigning new ids where needed
        rows_to_delete = []
        for row_index, row_values in enumerate(dataset):
            row = dict(zip(dataset.headers, row_values))
            print('DEBUG: dataset row: {} {}'.format(row_index, row_values))

            # check if row is all empty fields (plus with no space or newlines)
            fields_with_contents = 0
            for field in row:
                if not field_is_empty(row[field]):
                    fields_with_contents += 1

            # make list of empty rows to delete post-for-loop
            if fields_with_contents == 0:
                rows_to_delete.insert(0, row_index)
                continue

            # assign new jaxid if empty or wrong format (prefix letter)
            elif field_is_empty(row['jaxid']) \
                    or not re.match(f'[{PREFIXES}]', row['jaxid']):
                row['jaxid'] = self.assign_new_id(new_jaxids, dataset_jaxids)
                replace_row(row_index, row)

            # print('DEBUG: dataset final: {}'.format(row))

            # if not row['parent_jaxid']:
            #     # id_type = check_id_type(row)
            #     #TODO: implement other reality-check actions re: id_type
            #     pass

        # del the empty rows from the dataset after updating/replacing others
        # print(f'DEBUG: rows_to_delete {rows_to_delete}')
        for row_index in rows_to_delete:
            del dataset[row_index]

        # print('DEBUG: dataset final: {}'.format(str(dataset.dict)))

    def after_import(self, dataset, result, using_transactions, dry_run, **kwargs):
        """ Overridden to offer download of imported/updated id records """
        #TODO: return with link to download spreadsheet (in same file format) of the imported rows
        if using_transactions:
            if dry_run or result.has_errors():
                return
            else:
                jaxid_import_rows = []

                row_pks = [row.object_id for row in result.rows]
                print(f'DEBUG: row_pks length: {len(row_pks)!s}')
                print(f'DEBUG: row_pks: {row_pks!s}')
                jaxid_import_rows = self._meta.model.objects.filter(pk__in=row_pks)

                self.Meta.jaxid_import_rows = jaxid_import_rows
                self.Meta.jaxid_import_row_pks = row_pks
                print('DEBUG: '+str(self.Meta.jaxid_import_rows))
                # self.export(queryset=jaxid_import_rows)
                # return redirect( self.export(None, queryset=jaxid_import_rows) )
                result.imported_queryset = jaxid_import_rows
                result.imported_row_pks = row_pks
        # else:
            # self.Meta.jaxid_import_rows = []
            # return

    # def get_queryset(self):
    #     """
    #     Returns a queryset of all objects for this model.
    #     Overriden to check for meta imported_rows
    #     """
    #     if self.Meta.jaxid_import_rows.count:
    #         return self._meta.jaxid_import_rows
    #     else:
    #         # orig :
    #         return self._meta.model.objects.all()


    class Meta:
        model = JAXIdDetail
        all_fields = ( ID_DETAIL_FIELDS, )
        import_id_fields = ( 'jaxid', )
        fields = ID_DETAIL_FIELDS
        export_order = ID_DETAIL_FIELDS
        jaxid_import_rows = None # for imported queryset
        jaxid_import_row_pks = []
        import_format = None


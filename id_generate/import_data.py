import re
import tablib
from import_export import resources, fields, widgets
from django_mysql.locks import TableLock

from .jaxid_create import JAXidGenerate
# from .generate import check_id_type

from . import models
from .models import (
        JAXIdDetail,
        BoxId,
        PlateId,
        SampleType,
        SequencingType,
        NucleicAcidType,
        ProjectCode
        )
from generator.utils import field_is_empty, funcname


def assign_new_id(new_ids, current_ids):
    """recursively select id that is not used already in current set to be imported
        params:
            new_ids:  generator
            current_ids: list of used ids
    """
    # print("current_ids: {}".format(current_ids))
    next_id = next(new_ids)
    if next_id in current_ids:
        return assign_new_id(new_ids, current_ids)
    else:
        return next_id


def row_is_empty(row_dict={}):
    """check each 'field' within a 'row' dict for empty values (plus with no space or newlines)"""
    for field in row_dict:
        if not field_is_empty(row_dict[field]):
            return False
    return True


def check_rows_before_the_import(dataset, id_prefix='J', id_field_name='jaxid', id_model=JAXIdDetail,**kwargs):
    """ Overridden to generate new JAXid values for each row to be imported. """
    PREFIXES = 'JBP'

    num_rows = dataset.height
    print('DEBUG: num_rows in dataset: {}'.format(num_rows))

    def replace_row(row_index, row_dict):
        """'pop' for specific index number within dataset, followed by insertion of new 'row' values"""
        del dataset[row_index]
        dataset.insert(row_index, row_dict.values())

    print(f'DEBUG: in {funcname()}, prefix: {id_prefix}, model: {id_model.__name__}, field: {id_field_name}')

    jid = JAXidGenerate(prefix=id_prefix, id_model=id_model)
    new_ids = jid.generate_new_ids(num_rows)

    id_col_num = dataset.headers.index(id_field_name)
    dataset_ids = set([row[id_col_num]
                          for row in dataset
                          if not field_is_empty(row[id_col_num])])
    print("DEBUG: current_ids used by incoming dataset: {}".format(dataset_ids))

    # loop through rows, assigning new ids where needed
    rows_to_delete = []
    for row_index, row_values in enumerate(dataset):
        row = dict(zip(dataset.headers, row_values))
        print('DEBUG: dataset row: {} {}'.format(row_index, row_values))

        # check if row is all empty fields (plus with no space or newlines)
        # make list of empty rows to delete post-for-loop
        if row_is_empty(row):
            rows_to_delete.insert(0, row_index)
            continue

        # assign new id if empty or wrong format (prefix letter)
        elif field_is_empty(row[id_field_name]) \
                or not re.match(id_prefix, row[id_field_name][0]):
            row[id_field_name] = assign_new_id(new_ids, dataset_ids)

        replace_row(row_index, row)

        print(f'DEBUG: dataset NEW: {row_index}={tuple(row.values())}')

    # del the empty rows from the dataset after updating/replacing others
    # print(f'DEBUG: rows_to_delete {rows_to_delete}')
    for row_index in rows_to_delete:
        del dataset[row_index]

    # print('DEBUG: dataset final: {}'.format(str(dataset.dict)))


"""BaseImportExport Resource"""
class BaseImportExportResource(resources.ModelResource):
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
    notes = fields.Field(attribute='notes',
            widget=widgets.CharWidget(),)

    raise_errors = True
    skip_unchanged = True
    report_skipped = True

    class Meta:
        abstract = True


"""ImportExport Resource"""
class DetailResource(BaseImportExportResource):
    entered_into_lims = fields.Field(attribute='entered_into_lims',
            widget=widgets.BooleanWidget(),)
    external_data = fields.Field(attribute='external_data',
            widget=widgets.BooleanWidget(),)

    def import_data(self, dataset, **kwargs):
        """Overridden from import_action to lock table then call super().import_data()"""
        print(f'DEBUG: in BoxIdResource.{funcname()}, about to do table locking super')
        tables_need_some_lockin = [ models.JAXIdDetail ]
        return super().import_data(dataset, table_locks=tables_need_some_lockin, **kwargs)

    def before_import(self, dataset, using_transactions=True, dry_run=False, **kwargs):
        print('DEBUG: in DetailResource.before_import, about to call outer check_rows_before_the_import')
        id_prefix = 'J'
        id_field_name = 'jaxid'
        id_model = JAXIdDetail
        check_rows_before_the_import(dataset,
                                     id_prefix=id_prefix,
                                     id_field_name=id_field_name,
                                     id_model=id_model,
                                     **kwargs)

    class Meta:
        model = JAXIdDetail
        import_id_fields = ( 'jaxid', )
        fields = model.all_field_names()
        export_order = fields
        all_fields = ( fields, )
        import_format = None


"""ImportExport Resource"""
class BoxIdResource(BaseImportExportResource):

    def import_data(self, dataset, **kwargs):
        """Overridden from import_action to lock table then call super().import_data()"""
        print(f'DEBUG: in BoxIdResource.{funcname()}, about to do table locking super')
        tables_need_some_lockin = [ models.BoxId ]
        return super().import_data(dataset, table_locks=tables_need_some_lockin, **kwargs)

    def before_import(self, dataset, using_transactions=True, dry_run=False, **kwargs):
        print('DEBUG: in BoxIdResource.before_import, about to call outer check_rows_before_the_import')
        id_prefix = 'B'
        id_field_name = 'jaxid'
        id_model = BoxId
        check_rows_before_the_import(dataset,
                                     id_prefix=id_prefix,
                                     id_field_name=id_field_name,
                                     id_model=id_model,
                                     **kwargs)


    class Meta:
        model = BoxId
        import_id_fields = ( 'jaxid', )
        fields = model.all_field_names
        export_order = list(fields)
        all_fields = fields,
        import_format = None


"""ImportExport Resource"""
class PlateIdResource(BaseImportExportResource):

    def import_data(self, dataset, **kwargs):
        """Overridden from import_action to lock table then call super().import_data()"""
        print(f'DEBUG: in PlateIdResource.{funcname()}, about to do table locking super')
        tables_need_some_lockin = [ models.PlateId ]
        return super().import_data(dataset, table_locks=tables_need_some_lockin, **kwargs)

    def before_import(self, dataset, using_transactions=True, dry_run=False, **kwargs):
        print('DEBUG: in PlateIdResource.before_import, about to call outer check_rows_before_the_import')
        id_prefix = 'P'
        id_field_name = 'jaxid'
        id_model = PlateId
        check_rows_before_the_import(dataset,
                                     id_prefix=id_prefix,
                                     id_field_name=id_field_name,
                                     id_model=id_model,
                                     **kwargs)

    class Meta:
        model = PlateId
        import_id_fields = ( 'jaxid', )
        fields = model.all_field_names
        export_order = list(fields)
        all_fields = fields,
        import_format = None


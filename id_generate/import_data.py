import tablib
from import_export import resources, fields, widgets

from .jaxid_create import JAXidGenerate
from .generate import check_id_type
from .models import (
        JAXIdDetail,
        SampleType,
        SequencingType,
        NucleicAcidType,
        ProjectCode
        )

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
    sequencing_type = fields.Field(attribute='sequencing_type',
            widget=widgets.ForeignKeyWidget(SequencingType, 'code'),)
    entered_into_lims = fields.Field(attribute='entered_into_lims',
            widget=widgets.BooleanWidget(),)
    external_data = fields.Field(attribute='external_data',
            widget=widgets.BooleanWidget(),)
    notes = fields.Field(attribute='notes',
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
        print('DEBUG: num_rows in dataset: {}'.format(num_rows))

        def replace_row(row_index, row_dict):
            """'pop' for specific index number within dataset, followed by insertion of new 'row' values"""
            del dataset[row_index]
            dataset.insert(row_index, row_dict.values())

        #TODO: implement kwargs.prefix for Box/Plate/...
        id_prefix = kwargs.get('prefix', 'J')

        jid = JAXidGenerate(prefix=id_prefix)
        new_jaxids = jid.generate_new_ids(num_rows)

        jaxid_col_num = dataset.headers.index('jaxid')
        dataset_jaxids = set([row[jaxid_col_num]
                              for row in dataset
                              if row[jaxid_col_num] != ''])
        # print("DEBUG: current_ids used by incoming dataset: {}".format(dataset_jaxids))

        # loop through rows, assigning new ids where needed
        for row_index, row_values in enumerate(dataset):
            row = dict(zip(dataset.headers, row_values))
            # print('DEBUG: dataset first: {} {}'.format(row_index, row_values))
            if not row['jaxid']:
                row['jaxid'] = self.assign_new_id(new_jaxids, dataset_jaxids)
                replace_row(row_index, row)
            if not row['parent_jaxid']:
                id_type = check_id_type(row)
                #TODO: implement other reality-check actions re: id_type
            # print('DEBUG: dataset final: {}'.format(row))

        # print('DEBUG: dataset ids final: {}'.format(str(dataset.dict)))


    def after_import(self, dataset, result, using_transactions, dry_run, **kwargs):
        """ Overridden to offer download of imported/updated id records """
        pass


    class Meta:
        model = JAXIdDetail
        all_fields = ( ID_DETAIL_FIELDS, )
        import_id_fields = ( 'jaxid', )
        fields = ID_DETAIL_FIELDS
        export_order = ID_DETAIL_FIELDS


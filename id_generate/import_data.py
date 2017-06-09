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

        #TODO: implement kwargs.prefix for Box/Plate/...
        id_prefix = kwargs.get('prefix', 'J')

        jid = JAXidGenerate(prefix=id_prefix)
        new_jaxids = jid.generate_new_ids(num_rows)

        jaxid_col_num = dataset.headers.index('jaxid')
        dataset_jaxids = set([row[jaxid_col_num]
                              for row in dataset
                              if row[jaxid_col_num] != ''])
        # print("DEBUG: current_ids used by incoming dataset: {}".format(dataset_jaxids))

        dataset_with_ids = tablib.Dataset(headers=dataset.headers)
        # loop through rows, assigning new ids where needed
        for row in dataset.dict:
            if not row['jaxid']:
                row['jaxid'] = self.assign_new_id(new_jaxids, dataset_jaxids)
            if not row['parent_jaxid']:
                id_type = check_id_type(row)
            dataset_with_ids.append(row.values())
            print('DEBUG: dataset final: {}'.format(row))

        # replace all dataset rows with new ids assigned:
        dataset = dataset_with_ids
        print('DEBUG: dataset ids final: {}'.format(str(dataset.dict)))


    def before_import_row(self, row, **kwargs):
            print('DEBUG: before_import_row: {}'.format(str(row)))


    class Meta:
        model = JAXIdDetail
        all_fields = ( ID_DETAIL_FIELDS, )
        import_id_fields = ( 'jaxid', )
        fields = ID_DETAIL_FIELDS
        export_order = ID_DETAIL_FIELDS


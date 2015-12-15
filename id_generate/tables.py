from django_tables2 import Table
from .models import JAXIdMasterList, JAXIdDetail

class ListTable(Table):
    class Meta:
        model = JAXIdMasterList
        attrs = {"class": "paleblue"}
        sequence = ('jaxid', 'creation_date')
        order_by = 'creation_date'

class DetailTable(Table):
    class Meta:
        model = JAXIdDetail
        attrs = {"class": "paleblue"}
        sequence = ('id', 'jaxid', 'project_code',
                'collab_id', 'sample_type', 'sequencing_type',
                'creation_date')
        order_by = 'creation_date'


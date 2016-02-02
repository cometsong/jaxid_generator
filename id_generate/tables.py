from django_tables2 import Table
from .models import JAXIdDetail

ID_DETAIL_FIELDS = JAXIdDetail.all_field_names()

class DetailTable(Table):
    class Meta:
        model = JAXIdDetail
        attrs = {"class": "paleblue"}
        # convert to list, insert, append, convert back to set
        field_list = list(ID_DETAIL_FIELDS)
        field_list.insert(0,'id')
        field_list.append('creation_date')
        sequence = tuple(field_list)
        order_by = 'creation_date'


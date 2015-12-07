from django_tables2 import Table
from .models import JAXIdMasterList

class ListTable(Table):
    class Meta:
        model = JAXIdMasterList
        attrs = {"class": "paleblue"}
        sequence = ('jaxid', 'creation_date')
        order_by = 'creation_date'

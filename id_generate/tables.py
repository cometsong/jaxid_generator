from django_tables2 import Table
from .models import JaxIdMasterList

class ListTable(Table):
    class Meta:
        model = JaxIdMasterList
        attrs = {"class": "paleblue"}
        sequence = ('jaxid', 'creation_date')
        order_by = 'creation_date'


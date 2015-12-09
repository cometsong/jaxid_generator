from django.shortcuts import render
from django_tables2 import RequestConfig
from .models import JAXIdMasterList, JAXIdDetail, SampleType, SequencingType
from .tables import ListTable, DetailTable


def index(request):
    return detail_list(request)


def id_list(request):
    template_page = 'id_generate/list.html'
    total = JAXIdMasterList.objects.count()
    table = ListTable(JAXIdMasterList.objects.all())
    RequestConfig(request, paginate={"per_page": 25}
            ).configure(table)
    context = { 'table': table, 'total': total, }
    return render(request, template_page, context)

def detail_list(request):
    template_page = 'id_generate/detail.html'

    total = JAXIdDetail.objects.count()
    table = DetailTable(JAXIdDetail.objects.all())
    RequestConfig(request, paginate={"per_page": 25}
            ).configure(table)
    context = { 'table': table, 'total': total, }
    return render(request, template_page, context)


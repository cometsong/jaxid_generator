from django.shortcuts import render
from django_tables2 import RequestConfig
from .models import JAXIdDetail, SampleType, SequencingType
from .tables import DetailTable


def index(request):
    return detail_list(request)


def detail_list(request):
    template_page = 'id_generate/detail.html'

    total = JAXIdDetail.objects.count()
    table = DetailTable(JAXIdDetail.objects.all())
    RequestConfig(request, paginate={"per_page": 25}
            ).configure(table)
    context = { 'table': table, 'total': total, }
    return render(request, template_page, context)

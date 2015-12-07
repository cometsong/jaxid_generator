from django.shortcuts import render
from django_tables2 import RequestConfig
from .models import JAXIdMasterList, JAXIdDetail, SampleType, SequencingType
from .tables import ListTable


def index(request):
    return id_list(request)


def id_list(request):
    template_page = 'id_generate/list.html'

    total = JAXIdMasterList.objects.count()
    table = ListTable(JAXIdMasterList.objects.all())
    RequestConfig(request, paginate={"per_page": 25}
            ).configure(table)

    context = { 'table': table, 'total': total, }
    return render(request, template_page, context)


# from jaxid_generate import JAXid_db
def id_gen(request):
    # jdb = JAXid_db()
    template_page = 'id_generate/create.html'
    # gen = JAXid_gen()
    # context = { 'gen': gen,
                # }
    return render(request, template_page, context)

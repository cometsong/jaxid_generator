from django.shortcuts import render
from django_tables2 import RequestConfig
from .models import JaxIdMasterList, ProjectLinks
# from .tables import JaxIdTable

def index(request):
    return id_list(request)

def id_list(request):
    template_page = 'list.html'
    list = JaxIdMasterList.objects.all().order_by('creation_date')
    context = { 'list': list,
                }
    return render(request, template_page, context)

# def running(request):
    # template_page = 'list.html'
    # list = RunInfo.objects.all().order_by('date_added')
    # run_samples = RunSamples.objects.all()
    # context = { 'list': list,
                # 'run_samples': run_samples,
                # }
    # return render(request, template_page, context)

# def running_tables(request):
    # template_page = 'run_tables.html'
    # table = RunTable(RunInfo.objects.all())
    # table_sample = RunSampleTable(RunSamples.objects.all())

    # RequestConfig(request, paginate={"per_page": 20}).configure(table)
    # RequestConfig(request, paginate={"per_page": 20}).configure(table_sample)

    # context = { 'table': table,
                # 'table_sample': table_sample,
                # }
    # return render(request, template_page, context)


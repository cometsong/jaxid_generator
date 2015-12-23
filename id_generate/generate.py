from django import forms
from django.shortcuts import render
from django.http import HttpResponse

import tablib

from .jaxid_create import JAXidGenerate

#TODO: use IdModel_meta.fields to generate list of field names for file.headers in new_ids()
id_detail_fields = ['jaxid', 'project_code', 'collab_id',
    'sample_type', 'nucleic_acid_type', 'sequencing_type']

ID_TYPES = (
            ('J', 'JAXID'),
            ('B', 'Box ID'),
            ('P', 'Plate ID'),
           )

FILE_TYPES = (
        ('X', 'xlsx'),
        ('C', 'csv'),
        )

class GenerateForm(forms.Form):
    amount = forms.IntegerField(label="How many ID's needed?",
            min_value=1, max_value=9999, initial=25)
    prefix = forms.ChoiceField(
            label='What type (JAX, box, plate)?',
            choices=ID_TYPES, initial='J')
    filetype = forms.ChoiceField(
            label='What file type (csv, xlsx)?',
            choices=FILE_TYPES, initial='X')

def generate_batch(request):
    """ batch create ids """
    template_page = 'id_generate/batch.html'

    if request.method == 'POST':
        form = GenerateForm(request.POST)
        if form.is_valid():
            fields = form.cleaned_data
            return new_ids(request, fields)
    else:    # if GET (or other method) send blank form
        form = GenerateForm()

    context = { 'form': form  }
    return render(request, template_page, context)

def batch(request):
    """ redir to generate_batch """
    return generate_batch(request)

def new_ids(request, fields):
    """ response file w/ new ids requested """
    amount = int(fields['amount'])
    prefix = fields['prefix']
    filetype = fields['filetype']

    file = tablib.Dataset()
    # NOTE: Dataset requires >1 column for each instance
    file.headers = id_detail_fields
    for N in range(0,amount):
        ID = generate_JAX_id(prefix)
        # field_list = ID,'','','',''
        file.append((ID, '','','','',''))

    file_export_name = 'id_list'
    if filetype == 'X':
        file_export = file.xlsx
        content_type = \
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    else: # filetype == 'C':
        file_export = file.csv
        content_type = 'text/csv'

    response = HttpResponse(file_export, content_type=content_type)
    response['Content-Disposition'] = \
            'attachment; filename={}'.format(file_export_name)
    return response

def generate_JAX_id(prefix='J'):
    """Use id_generator and add preceding 'J' character for the 6 character
        JAXid or 'B' for BoxID or 'P' for PlateID
    """
    JG = JAXidGenerate(prefix)
    return JG.generate()


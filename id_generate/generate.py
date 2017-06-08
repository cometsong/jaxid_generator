from django import forms
from django.contrib import admin
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.admin.views.decorators import staff_member_required

import tablib

from .jaxid_create import JAXidGenerate
from .models import JAXIdDetail


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Globals ~~~~~
ID_DETAIL_FIELDS = JAXIdDetail.all_field_names()

FILE_EXPORT_NAME = 'generated_jaxid_list'

ID_TYPES = (
            ('J', 'JAXID'),
            ('B', 'Box ID'),
            ('P', 'Plate ID'),
           )

FILE_TYPES = (
        ('X', 'xlsx'),
        ('C', 'csv'),
        )

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Classy ~~~~~

# @staff_member_required
class NewIDForm(forms.Form):
    """form accepts type and file of rows to generate ids during import"""
    error_css_class = 'error'
    required_css_class = 'required'

    prefix = forms.ChoiceField(
            label='What type (JAX, box, plate)?',
            choices=ID_TYPES, initial='J')
    filetype = forms.ChoiceField(
            label='What file type (csv, xlsx)?',
            choices=FILE_TYPES, initial='X')
    filename = forms.FileField(allow_empty_file=False, widget=forms.FileInput)

# @admin.register()
def generate_new_ids(request):
    """direct to import/generate new ids"""
    template_page = 'admin/import_new_ids.html'

    if request.method == 'POST':
        form = NewIDForm(request.POST)
        if form.is_valid():
            fields = form.cleaned_data
            return import_new_ids(request, fields)
    else: # if GET (or other method) send blank form
        form = NewIDForm()

    context = { 'form': form  }
    return render(request, template_page, context)

def generate_JAX_id(prefix='J', amount=1):
    """Use id_generator and add preceding 'J' character for the 6 character
        JAXid or 'B' for BoxID or 'P' for PlateID
    """
    JG = JAXidGenerate(prefix, amount)
    return JG.generate_new_ids()
    

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ V1 Classy ~~~~~
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
    file.headers = ID_DETAIL_FIELDS
    # print('empty_fields: {}'.format(empty_fields))
    for ID in generate_JAX_id(prefix, amount):
        # id_row_fields = (ID, empty_fields)
        empty_fields = ['' for l in range(1, len(file.headers))]
        empty_fields.insert(0,ID)
        id_row_fields = empty_fields
        file.append(id_row_fields)
        print('id_row_fields: {}'.format(id_row_fields))

    if filetype == 'X':
        file_export = file.xlsx
        content_type = \
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    else: # filetype == 'C':
        file_export = file.csv
        content_type = 'text/csv'

    response = HttpResponse(file_export, content_type=content_type)
    response['Content-Disposition'] = \
            'attachment; filename={}'.format(FILE_EXPORT_NAME)
    return response


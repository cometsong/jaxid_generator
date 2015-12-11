from django import forms
from django.shortcuts import render

from .models import ID_TYPES
from .jaxid_create import JAXidGenerate

class GenerateForm(forms.Form):
    amount = forms.IntegerField(label="How many ID's you want?",
            min_value=1, max_value=9999, initial=25)
    type = forms.ChoiceField(
            label='What type (JAX, box, plate)?',
            choices=ID_TYPES, initial='J')

def generate_batch(request):
    # batch create ids
    template_page = 'id_generate/batch.html'

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = GenerateForm(request.POST)
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # redirect to a new URL:
            context = {}
            return render(request, 'new_ids', context)
    else:    # if GET (or other method) send blank form
        form = GenerateForm()

    context = { 'form': form  }
    return render(request, template_page, context)

def batch(request):
    return generate_batch(request)

def new_ids(request):
    pass



def generate_JAX_id():
    """Use id_generator and add preceding 'J' character for the 6 characater
        JAXid or 'B' for BoxID or 'P' for PlateID
    """
    JG = JAXidGenerate('JAXIdDetail', 'jaxid', 'J')
    return JG.generate()



from django import forms
from django.contrib import admin
from django.db import models

# from .generate import generate_JAX_id
from .models import (
        JAXIdMasterList,
        JAXIdDetail,
        SampleType,
        SequencingType,
        ProjectCode
        )

class SampleForm(forms.ModelForm):
    class Meta:
        model = SampleType
        fields = '__all__'
        widgets = {
            'details': forms.TextInput(attrs={'size':'100'})
            }

class SequencingForm(forms.ModelForm):
    class Meta:
        model = SequencingType
        fields = '__all__'
        widgets = {
            'details': forms.TextInput(attrs={'size':'100'})
            }

class ProjectCodeForm(forms.ModelForm):
    class Meta:
        model = ProjectCode
        fields = '__all__'
        widgets = {
            'project_code': forms.TextInput(attrs={'size':'4'}),
            'details': forms.TextInput(attrs={'size':'100'})
            }

class JAXIdDetailForm(forms.ModelForm):
    class Meta:
        model = JAXIdDetail
        fields = ( 'jaxid', 'project_code', 'collab_id',
                'sample_type', 'sequencing_type', )
        readonly_fields = ( 'jaxid' ),


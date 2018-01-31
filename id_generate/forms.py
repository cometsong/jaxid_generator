from django import forms
from django.contrib import admin
from django.db import models

from suit.widgets import AutosizedTextarea
from django_select2.forms import Select2Widget

from .models import (
        JAXIdDetail,
        BoxId,
        SampleType,
        SequencingType,
        NucleicAcidType,
        ProjectCode
        )

ID_DETAIL_FIELDS = JAXIdDetail.all_field_names()

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

class NucleicAcidTypeForm(forms.ModelForm):
    class Meta:
        model = NucleicAcidType
        fields = '__all__'
        widgets = {
            'code': forms.TextInput(attrs={'size':'20'}),
            'details': forms.TextInput(attrs={'size':'100'})
            }

class JAXIdDetailForm(forms.ModelForm):
    error_css_class = 'error'
    required_css_class = 'required'
    jaxid = forms.CharField(disabled=True, max_length=6)
    parent_jaxid = widget=forms.TextInput()
    collab_id = forms.CharField(label='Collaborator ID', widget=forms.TextInput())
    class Meta:
        model = JAXIdDetail
        # readonly_fields = ( 'jaxid' ),
        fields = ( ID_DETAIL_FIELDS )
        widgets = {
                   'project_code': Select2Widget,
                   'notes': AutosizedTextarea,
                  }

class BoxIdForm(forms.ModelForm):
    error_css_class = 'error'
    required_css_class = 'required'
    jaxid = forms.CharField(disabled=True, max_length=6)
    parent_id = widget=forms.TextInput()
    class Meta:
        model = BoxId
        fields = BoxId.all_field_names
        widgets = {
                   'project_code': Select2Widget,
                   'notes': AutosizedTextarea,
                  }

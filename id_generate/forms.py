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

class BaseIdForm(forms.ModelForm):
    error_css_class = 'error'
    required_css_class = 'required'
    jaxid = forms.CharField(disabled=True, max_length=6)
    parent_jaxid = widget=forms.TextInput()
    class Meta:
        abstract = True
        fields = '__all__'
        widgets = {
                   'project_code': Select2Widget,
                   'notes': AutosizedTextarea,
                  }

class JAXIdDetailForm(forms.ModelForm):
    collab_id = forms.CharField(label='Collaborator ID', widget=forms.TextInput())
    class Meta(BaseIdForm.Meta):
        model = JAXIdDetail

class BoxIdForm(forms.ModelForm):
    collab_id = forms.CharField(label='Name', widget=forms.TextInput())
    class Meta(BaseIdForm.Meta):
        model = BoxId

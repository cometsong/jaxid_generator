from django import forms
from django.contrib import admin
from django.db import models

# from .generate import generate_JAX_id
from .models import (
        JAXIdDetail,
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
    collab_id = forms.CharField(widget=forms.TextInput())
    class Meta:
        model = JAXIdDetail
        fields = ( ID_DETAIL_FIELDS )
        readonly_fields = ( 'jaxid' ),


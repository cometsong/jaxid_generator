from django.db import models

class SequencingType(models.Model):
    code = models.CharField('Type Code',
            max_length=1, blank=False,
            help_text="Sequence type identifiying code (1 char).",
            unique=True,
            )
    details = models.TextField('detailed name', blank=False,
            help_text="Sequencing type detailed name."
            )

    ordering = ['code']

    def __str__(self):
        return '{} ({})'.format(self.code, self.details)

    def save(self, force_insert=False, force_update=False):
        self.code = self.code.upper()
        super(SequencingType, self).save(force_insert, force_update)


class ProjectCode(models.Model):
    code = models.CharField('Project Code',
            max_length=4, blank=False,
            help_text="Project ID code (4 chars).",
            unique=True,
            )
    details = models.TextField('Project details', blank=False,
            help_text="Project type detailed name."
            )

    ordering = ['code']

    def __str__(self):
        return '{} ({})'.format(self.code, self.details)

    def save(self, force_insert=False, force_update=False):
        self.code = self.code.upper()
        super(ProjectCode, self).save(force_insert, force_update)


class SampleType(models.Model):
    code = models.CharField('Type Code',
            max_length=2, blank=False,
            help_text="Sample type identifiying code (2 chars).",
            unique=True,
            )
    details = models.TextField('name details', blank=False,
            help_text="Sample type detailed name."
            )

    ordering = ['code']

    def __str__(self):
        return '{} ({})'.format(self.code, self.details)

    def save(self, force_insert=False, force_update=False):
        self.code = self.code.upper()
        super(SampleType, self).save(force_insert, force_update)


class NucleicAcidType(models.Model):
    code = models.CharField('Type Code',
            max_length=20, blank=False,
            help_text="Nucleic acid type identifiying code.",
            unique=True,
            )
    details = models.TextField('name details', blank=False,
            help_text="Nucleic acid type detailed name."
            )

    ordering = ['code']

    def __str__(self):
        return '{} ({})'.format(self.code, self.details)

    def save(self, force_insert=False, force_update=False):
        # self.code = self.code.upper()
        super(NucleicAcidType, self).save(force_insert, force_update)


class JAXIdDetail(models.Model):
    verbose_name = 'JAX Id Detail'
    jaxid = models.CharField('JAX ID',
            max_length=6, blank=False,
            help_text="A unique ID string for every sample.",
            unique=True,
            # indexed=True,
            )
    project_code = models.ForeignKey(ProjectCode, to_field='code', blank=False)
    collab_id = models.TextField('Collaborator ID', blank=False,
            help_text="Collaborator sample ID."
            )
    sample_type = models.ForeignKey(SampleType, to_field='code', blank=True)
    nucleic_acid_type = models.ForeignKey(NucleicAcidType,
            to_field='code', blank=True, null=True,)
    sequencing_type = models.ForeignKey(SequencingType,
            to_field='code', blank=True, null=True,)
    entered_into_lims = models.BooleanField('Entered into LIMS', blank=True,
            help_text="Entered into LIMS",
            )
    external_data = models.BooleanField('External data (not sequenced here.)',
            blank=True, default=False,
            help_text='External data (not sequenced here.)',
            )
    notes = models.TextField('Notes', blank=True, null=True,
            help_text="Notes"
            )

    creation_date = models.DateTimeField(auto_now_add=True)

    def all_field_names():
        names = (
                'jaxid', 'project_code', 'collab_id',
                'sample_type', 'nucleic_acid_type', 'sequencing_type',
                'entered_into_lims', 'external_data', 'notes',
                )
        return names

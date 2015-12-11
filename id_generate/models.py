from django.db import models

ID_TYPES = (
            ('J', 'JAXID'),
            ('B', 'Box ID'),
            ('P', 'Plate ID'),
           )

class SequencingType(models.Model):
    sequencing_code = models.CharField('Type Code',
            max_length=1, blank=False,
            help_text="Sequence type identifiying code (1 char)."
            )
    details = models.TextField('detailed name', blank=False,
            help_text="Sequencing type detailed name."
            )

    ordering = ['sequencing_code']

    def __str__(self):
        return '{} ({})'.format(self.sequencing_code, self.details)

    def save(self, force_insert=False, force_update=False):
        self.sequencing_code = self.sequencing_code.upper()
        super(SequencingType, self).save(force_insert, force_update)


class ProjectCode(models.Model):
    project_code = models.CharField('Project Code',
            max_length=4, blank=False,
            help_text="Project ID code (4 chars)."
            )
    details = models.TextField('Project details', blank=False,
            help_text="Project type detailed name."
            )

    ordering = ['project_code']

    def __str__(self):
        return '{} ({})'.format(self.project_code, self.details)

    def save(self, force_insert=False, force_update=False):
        self.project_code = self.project_code.upper()
        super(ProjectCode, self).save(force_insert, force_update)


class SampleType(models.Model):
    sample_code = models.CharField('Type Code',
            max_length=2, blank=False,
            help_text="Sample type identifiying code (2 chars)."
            )
    details = models.TextField('name details', blank=False,
            help_text="Sample type detailed name."
            )

    ordering = ['sample_code']

    def __str__(self):
        return '{} ({})'.format(self.sample_code, self.details)

    def save(self, force_insert=False, force_update=False):
        self.sample_code = self.sample_code.upper()
        super(SampleType, self).save(force_insert, force_update)


class JAXIdDetail(models.Model):
    verbose_name = 'JAX Id Detail'
    jaxid = models.CharField('JAX ID',
            max_length=6, blank=False,
            help_text="A unique ID string for every sample.",
            # default=generate_JAX_id(),
            )
    project_code = models.ForeignKey(ProjectCode)
    collab_id = models.TextField('Collaborator ID', blank=False,
            help_text="Collaborator sample ID."
            )
    sample_code = models.ForeignKey(SampleType)
    sequencing_type = models.ForeignKey(SequencingType)
    creation_date = models.DateTimeField(auto_now_add=True)


class JAXIdMasterList(models.Model):
    verbose_name = 'JAX Id Master List'
    jaxid = models.ForeignKey(JAXIdDetail, on_delete=models.PROTECT)
    creation_date = models.DateTimeField(auto_now_add=True)
    ordering = ['creation_date']


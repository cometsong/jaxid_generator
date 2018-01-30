from django.db import models
from django.core.validators import MinLengthValidator

class BaseRefModel(models.Model):
    code = models.CharField(max_length=1, blank=False, unique=True,)
    details = models.TextField(blank=False,)

    class Meta:
        ordering = ['code']
        abstract = True

    def get_code(self):
        """why do i have this a separate method???"""
        # return self.__dict__.getattr(self.code)
        # return self.__dict__.get(self.code)
        # return __dict__.get(self.code)
        # return self.get(self.code)
        # return get(self.code)
        return self.code

    def __str__(self):
        return '{} ({})'.format(self.code, self.details)

    def save(self, force_insert=False, force_update=False):
        self.code = self.code.upper().strip()
        super().save(force_insert, force_update)


class SequencingType(BaseRefModel):
    code = models.CharField(
            max_length=1, blank=False,
            help_text="Sequence type identifiying code (1 char).",
            unique=True,
            )
    details = models.TextField(blank=False,
            help_text="Sequencing type detailed name."
            )


class ProjectCode(BaseRefModel):
    verbose_name = 'Project'
    code = models.CharField(
            max_length=4, blank=False,
            help_text="Project ID code (4 chars).",
            unique=True,
            )
    details = models.TextField('Name', blank=False,
            help_text="Project type detailed name."
            )
    class Meta(BaseRefModel.Meta):
        verbose_name_plural = 'Projects'


class SampleType(BaseRefModel):
    code = models.CharField(
            max_length=2, blank=False,
            help_text="Sample type identifiying code (2 chars).",
            unique=True,
            )
    details = models.TextField(blank=False,
            help_text="Sample type detailed name."
            )


class NucleicAcidType(BaseRefModel):
    code = models.CharField(
            max_length=20, blank=False,
            help_text="Nucleic acid type identifiying code.",
            unique=True,
            )
    details = models.TextField(blank=False,
            help_text="Nucleic acid type detailed name."
            )

    def save(self, force_insert=False, force_update=False):
        """orverride the uppercasing save"""
        super().save(force_insert, force_update)


class JAXIdDetail(models.Model):
    class Meta:
        verbose_name_plural = 'JAXid Detail Records'
    verbose_name = 'JAXid Detail'

    jaxid = models.CharField('JAXid', max_length=6,
            unique=True, validators=[MinLengthValidator(6)],
            # help_text="A unique ID string for every sample.",
            )
    parent_jaxid = models.CharField('Parent JAXid',
            max_length=6, default='', unique=False,
            help_text="Parent ID string of source JAXid; or use "
                      "'RECD' for newly received samples,"
                      "'POOL' for pools of libraries.",
            )
    project_code = models.ForeignKey(ProjectCode, to_field='code',)
    collab_id = models.TextField('Collaborator ID',
            help_text="Collaborator sample ID."
            )
    sample_type = models.ForeignKey(SampleType, to_field='code',)
    nucleic_acid_type = models.ForeignKey(NucleicAcidType,
            to_field='code', default='Z')
    sequencing_type = models.ForeignKey(SequencingType,
            to_field='code', default='Z')
    entered_into_lims = models.BooleanField('Entered into LIMS',
            blank=True, default=False,
            # help_text="Entered into LIMS",
            )
    external_data = models.BooleanField('External data',
            blank=True, default=False,
            help_text='(not sequenced here.)',
            )
    notes = models.TextField('Notes', blank=True, null=True,
            )
    creation_date = models.DateTimeField(auto_now_add=True)

    def project_code_code(self):
        return self.project_code.get_code()
    project_code_code.short_description = 'Project'

    def sample_type_code(self):
        return self.sample_type.get_code()
    sample_type_code.short_description = 'Sample'

    def sequencing_type_code(self):
        return self.sequencing_type.get_code()
    sequencing_type_code.short_description = 'Sequencing Type'

    def nucleic_acid_type_code(self):
        return self.nucleic_acid_type.get_code()
    nucleic_acid_type_code.short_description = 'Nucleic Acid'

    def search_fields():
        return (
                'jaxid', 'parent_jaxid', 'project_code__code', 'collab_id', 'notes',
                'sample_type__code', 'nucleic_acid_type__code', 'sequencing_type__code',
                )

    def save(self, force_insert=False, force_update=False):
        self.full_clean()
        self.jaxid = self.jaxid.upper()
        self.parent_jaxid = self.parent_jaxid.upper()
        super().save(force_insert, force_update)

    def all_field_names():
        names = (
                'jaxid', 'parent_jaxid', 'project_code', 'collab_id',
                'sample_type', 'nucleic_acid_type', 'sequencing_type',
                'entered_into_lims', 'external_data', 'notes',
                )
        return names

    def __str__(self):
        return '{} ({}, {})'.format(self.jaxid, self.project_code_code(), self.collab_id)


class BaseIdModel(models.Model):
    class Meta:
        abstract = True

    parent_id = models.CharField('Parent id', blank=True, null=True,
                                 max_length=6, default='', unique=False)
    name = models.TextField('Name')
    project = models.ForeignKey(ProjectCode,
                verbose_name='Project', to_field='code')
    sample = models.ForeignKey(SampleType,
                verbose_name='Sample Type', to_field='code',)
    nucleic_acid = models.ForeignKey(NucleicAcidType,
                verbose_name='Nucleic Acid Type', to_field='code')
    sequencing_type = models.ForeignKey(SequencingType,
                verbose_name='Sequencing Type', to_field='code')
    notes = models.TextField('Notes', blank=True, null=True)
    creation_date = models.DateTimeField(auto_now_add=True)

    def all_field_names():
        return (
                'parent_id', 'name', 'project', 'sample', 'nucleic_acid', 'sequencing_type', 'notes',
               )

    def save(self, force_insert=False, force_update=False):
        self.parent_id = self.parent_id.upper()
        self.full_clean()
        super().save(force_insert, force_update)


class BoxId(BaseIdModel):
    class Meta:
        verbose_name_plural = 'Box ID Records'
    verbose_name = 'BoxID Record'

    boxid = models.CharField('BoxID', unique=True, max_length=6,
                             validators=[MinLengthValidator(6)])

    all_field_names = (
            'boxid', 'parent_id', 'name', 'project', 'sample',
            'nucleic_acid', 'sequencing_type', 'notes',
            )

    def save(self, force_insert=False, force_update=False):
        self.boxid = self.boxid.upper()
        super().save(force_insert, force_update)

    def __str__(self):
        return '{} ("{}", {})'.format(self.boxid, self.name, self.project)

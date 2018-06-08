from django.db import models
from django.core.validators import MinLengthValidator
from django.core.exceptions import ValidationError

from generator.utils import funcname

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Global Vars ~~~~~
# define PARENT_ID_EXTRAS list for alternative values not pre-existing JAXids
PARENT_ID_EXTRAS = ['RECD', 'POOL']

display_order = 1

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


class ProjectCode(BaseRefModel):
    verbose_name = 'Project'
    display_order = 4
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
    display_order = 5
    code = models.CharField(
            max_length=2, blank=False,
            help_text="Sample type identifiying code (2 chars).",
            unique=True,
            )
    details = models.TextField(blank=False,
            help_text="Sample type detailed name."
            )


class NucleicAcidType(BaseRefModel):
    display_order = 6
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


class SequencingType(BaseRefModel):
    display_order = 7
    code = models.CharField(
            max_length=1, blank=False,
            help_text="Sequence type identifiying code (1 char).",
            unique=True,
            )
    details = models.TextField(blank=False,
            help_text="Sequencing type detailed name."
            )


class JAXIdDetail(models.Model):
    class Meta:
        verbose_name_plural = 'JAXid Detail Records'
    verbose_name = 'JAXid Detail'
    display_order = 1

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


    def validate_parent_id(self):
        """tests to check parent_id and corresponding parent record
        Valid requirements:
            - in 'extras' list OR pre-existing jaxid in db
            - if in db:
                - identical values in parent fields to current record
                    (project_code, collab_id, sample_type)
                - correct id 'type', e.g. id for library had parent extraction
        """
        fld = 'parent_jaxid'
        errors = {}
        fld_errs = []

        if self.parent_jaxid:
            print(f'DEBUG: {funcname()} - checking "{fld}"')
            self.parent_jaxid = self.parent_jaxid.upper()

            print(f'DEBUG: {funcname()} - checking "{fld}" in extras')
            if self.parent_jaxid not in PARENT_ID_EXTRAS:
                # fld_errs.append('{fld} not a valid known exception (RECD or POOL).')
                try:
                    print(f'DEBUG: {funcname()} - checking "{fld}" in db')
                    parent_record = self.__class__.objects.values_list('jaxid').get(jaxid=self.parent_jaxid)
                    print(f'DEBUG: {funcname()} - "{fld}" in db')
                except self.DoesNotExist as e:
                    print(f'DEBUG: {funcname()} - "{fld}" exception: {e}')
                    fld_errs.append('ID not found existing in database and not RECD or POOL.')
                else:
                    try:
                        print(f'DEBUG: {funcname()} - TODO "{fld}" matches data?')
                        # check_parent_matching_data(parent_record)
                        # fld_errs.append('Parent record does not match fields: {fields!s}')
                        print(f'DEBUG: {funcname()} - TODO "{fld}" correct type?')
                        # check_parent_correct_type(parent_record)
                        # fld_errs.append('Parent record is not the correct type!')
                        pass #TODO: other checks
                    except Exception as e:
                        raise e

        if len(fld_errs):
            print(f'DEBUG: {funcname()} - "{fld}" has errors')
            errors[fld] = fld_errs

        return errors


    def clean(self):
        """Check all id-specific fields with sanity checks
        Make any changes (e.g. .upper) and raise ValidationError's if found.
        """
        errors = {}

        if self.jaxid:
            print(f'DEBUG: {funcname()} - checking "jaxid"')
            self.jaxid = self.jaxid.upper()

        if self.parent_jaxid:
            errors.update(self.validate_parent_id())

        print(f'DEBUG: {funcname()} - checking "sequencing_type" and "nucleic_acid_type"')
        if self.sequencing_type_id != 'Z' and self.nucleic_acid_type_id == 'Z':
            fld = 'nucleic_acid_type'
            errors[fld] = 'Nucleic acid type must be specified if Sequencing type is known.'

        print(f'DEBUG: {funcname()} - checking "external_data"')
        if self.external_data:
            ext_err = False
            if self.sequencing_type_id == 'Z':
                fld = 'sequencing_type'
                errors[fld] = 'This is external data, seq type must be defined.'
                ext_err = True
            if self.nucleic_acid_type_id == 'Z':
                fld = 'nucleic_acid_type'
                errors[fld] = 'This is external data, nuc acid type must be defined.'
                ext_err = True
            if ext_err:
                fld = 'external_data'
                errors[fld] = 'This is external data, seq type and nuc acid type must be defined.'

        # self.errors = errors #TODO: need attr self.errors for other uses?
        if errors:
            print(f'DEBUG: {funcname()} - errors: {errors!s}')
            raise ValidationError(errors)


    def save(self, force_insert=False, force_update=False):
        self.full_clean()
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

    parent_jaxid = models.CharField('Parent ID', blank=True, null=True,
                                 max_length=6, default='', unique=False)
    collab_id = models.TextField('Name')
    project_code = models.ForeignKey(ProjectCode, verbose_name="Project", to_field='code')
    sample_type = models.ForeignKey(SampleType, verbose_name="Sample", to_field='code',)
    nucleic_acid_type = models.ForeignKey(NucleicAcidType, verbose_name="Nucleic Acid", to_field='code',)
    sequencing_type = models.ForeignKey(SequencingType, to_field='code',)
    notes = models.TextField('Notes', blank=True, null=True)
    creation_date = models.DateTimeField(auto_now_add=True)

    all_field_names = (
        'jaxid', 'parent_jaxid', 'collab_id', 'project_code',
        'sample_type', 'nucleic_acid_type', 'sequencing_type', 'notes',
        )


    def clean(self):
        """Check all id-specific fields.
        Make any changes (e.g. .upper) and raise ValidationError's if found.
        """
        errors = {}

        if self.jaxid:
            print(f'DEBUG: {funcname()} - checking "jaxid"')
            self.jaxid = self.jaxid.upper()

        print(f'DEBUG: {funcname()} - checking "sequencing_type" and "nucleic_acid_type"')
        if self.sequencing_type_id != 'Z' and self.nucleic_acid_type_id == 'Z':
            fld = 'nucleic_acid_type'
            errors[fld] = 'Nucleic acid type must be specified if Sequencing type is known.'

        if errors:
            raise ValidationError(errors)


    def save(self, force_insert=False, force_update=False):
        self.full_clean()
        super().save(force_insert, force_update)


    def __str__(self):
        return '{} ("{}", {})'.format(self.jaxid, self.collab_id, self.project_code.code)


class BoxId(BaseIdModel):
    class Meta(BaseIdModel.Meta):
        verbose_name_plural = 'Box ID Records'
    verbose_name = 'BoxID Record'
    display_order = 2

    jaxid = models.CharField('Box ID', unique=True, max_length=6,
                             validators=[MinLengthValidator(6)])


class PlateId(BaseIdModel):
    class Meta(BaseIdModel.Meta):
        verbose_name_plural = 'Plate ID Records'
    verbose_name = 'PlateID Record'
    display_order = 3

    jaxid = models.CharField('Plate ID', unique=True, max_length=6,
                             validators=[MinLengthValidator(6)])


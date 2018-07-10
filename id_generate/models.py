import re

from django.db import models
from django.core.validators import MinLengthValidator
from django.core.exceptions import ValidationError

from generator.utils import funcname

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Global Vars ~~~~~
# define PARENT_ID_EXTRAS list for alternative values not pre-existing JAXids
PARENT_ID_EXTRAS = ['RECD', 'POOL']
ID_TYPES = ( 'specimen', 'extraction', 'library', ) # 'pool' )

display_order = 1

class UpperCharField(models.CharField):
    def __init__(*args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_prep_value(self, value):
        return str(value).upper()


class BaseRefModel(models.Model):
    code = models.CharField(max_length=1, blank=False, unique=True,)
    details = models.TextField(blank=False,)

    class Meta:
        ordering = ['code']
        abstract = True
        indexes = [
            models.Index(fields=['code'], name='code_idx'),
        ]

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
        indexes = [
            models.Index(fields=['jaxid', 'parent_jaxid'], name='id_idx'),
            models.Index(fields=['project_code', 'collab_id'], name='proj_collab_idx'),
            models.Index(fields=['sample_type', 'sequencing_type', 'nucleic_acid_type'],
                         name='sample_seq_nucacid_idx'),
        ]
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


    def check_id_type(self, row=None):
        """Determine which type of id this record holds.
        Varying on specific field values and lack thereof.
        Results: 'specimen', 'extraction', 'library', 'pool', 'Invalid'
        """
        # print(f'DEBUG: {funcname()} - assign "row"')
        if not row:
            row = self
            
        # print(f'DEBUG: {funcname()} - now get.values')
        jaxid = row.jaxid
        parent = row.parent_jaxid
        sample = row.sample_type_id
        nucleic = row.nucleic_acid_type_id
        seqtype = row.sequencing_type_id
        print(f'DEBUG: {funcname()} - {jaxid}, {parent}, {sample}, {nucleic}, {seqtype}')

        ic = re.IGNORECASE
        pool = re.compile('pool', flags=ic)
        recd = re.compile('recd', flags=ic)
        zero = re.compile('^Z$')

        # print(f'DEBUG: {funcname()} - now check type options')
        if pool.match(parent):
            print(f'DEBUG: {funcname()} - pool')
            return 'pool'
        # elif recd.match(parent):
        #     print(f'DEBUG: {funcname()} - specimen')
        #     return 'specimen'
        elif zero.match(sample) and zero.match(nucleic) and zero.match(seqtype):
            print(f'DEBUG: {funcname()} - invalid')
            typ_str = 'Invalid (sample, nucleic acid and sequencing type can ' \
                'not all be unknown as Z. At least sample must be specified.)'
            return typ_str
        elif zero.match(nucleic) and zero.match(seqtype):
            print(f'DEBUG: {funcname()} - specimen')
            return 'specimen'
        elif zero.match(seqtype):
            print(f'DEBUG: {funcname()} - extraction')
            return 'extraction'
        else: # none == 'Z'
            print(f'DEBUG: {funcname()} - library')
            return 'library'


    def id_hierarchy_is_correct(self, parent_type, child_type):
        """check parent has correct type, one up the ladder from the child type"""
        types = ID_TYPES
        return types.index(parent_type) == types.index(child_type) - 1


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

            print(f'DEBUG: {funcname()} - checking "{fld}" in id_extras')
            if self.parent_jaxid not in PARENT_ID_EXTRAS:
                try:
                    print(f'DEBUG: {funcname()} - checking "{fld}" is in db')
                    parent_record = self.__class__.objects.get(jaxid=self.parent_jaxid)
                    print(f'DEBUG: {funcname()} - "{fld}" in db: {parent_record}')
                except self.DoesNotExist as e:
                    print(f'DEBUG: {funcname()} - "{fld}" exception: {e!s}')
                    fld_errs.append('ID not found existing in database and not RECD or POOL.')
                else:
                    try:
                        match_check_flds = ('collab_id', 'sample_type_id', 'project_code_id')
                        mismatches = {}
                        print(f'DEBUG: {funcname()} - "{fld}" matches data?')
                        # check_parent_matching_data(parent_record)
                        for match_fld in match_check_flds:
                            # print(f'DEBUG: {funcname()} - get match fld attrs')
                            this_value = str(getattr(self, match_fld, 'missing'))
                            parent_val = str(getattr(parent_record, match_fld, 'missing'))
                            # print(f'DEBUG: {funcname()} - compare attr vals')
                            if this_value != parent_val:
                                fld_name = match_fld.rsplit('_id',1)[0]
                                mismatches[fld_name] = (this_value, parent_val)
                                # errors[fld_name] = f'Parent value ({parent_val}) does not match.'
                        if len(mismatches):
                            fld_errs.append(f'Parent record does not match fields: {mismatches!s}')

                        print(f'DEBUG: {funcname()} - is "{fld}" correct type?')
                        jax_id_type = self.check_id_type()
                        parent_type = self.check_id_type(row=parent_record)
                        if not self.id_hierarchy_is_correct(parent_type, jax_id_type):
                            fld_errs.append('Parent record is not the correct type! '\
                                            f'parent: {parent_type}, this one: {jax_id_type}')
                        #TODO: other sanity checks?
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
        def add_err(errors:dict, fld:str, err:str):
            """append or create new err_msg for 'fld'"""
            try:
                errors[fld].append(err_msg)
            except KeyError:
                errors[fld] = [err_msg]

        if self.jaxid:
            print(f'DEBUG: {funcname()} - checking "jaxid"')
            self.jaxid = self.jaxid.upper()

        if self.parent_jaxid:
            errors.update(self.validate_parent_id())

        print(f'DEBUG: {funcname()} - checking "sequencing_type" and "nucleic_acid_type"')
        try:
            seqtype = self.sequencing_type_id
            nucacid = self.nucleic_acid_type_id
            if seqtype != 'Z' and nucacid == 'Z':
                fld = 'nucleic_acid_type'
                err_msg = 'NucleicAcid type must be specified if Seq type is known.'
                add_err(errors, fld, err_msg)

            if seqtype == 'R' and nucacid == 'gDNA' or \
              (seqtype in ['1', 'M', 'W', '8', 'I'] and \
               nucacid in ['Total RNA', 'Rib Depleted RNA']):
                fld = 'nucleic_acid_type'
                err_msg = (f'A Nucleic Acid type of "{nucacid}" does not go '
                           f'with Sequencing type of "{seqtype}"')
                add_err(errors, fld, err_msg)

                fld = 'sequencing_type'
                err_msg = (f'A "Sequencing type of "{seqtype}" does not go '
                           f'with Nucleic Acid type of "{nucacid}')
                add_err(errors, fld, err_msg)
        except Exception as e:
            raise e

        print(f'DEBUG: {funcname()} - checking "external_data"')
        if self.external_data:
            try:
                if self.sequencing_type_id == 'Z' or \
                   self.nucleic_acid_type_id == 'Z':
                    fld = 'external_data'
                    err_msg = 'If external, sequencing type and nucleic acid type must be defined.'
                    add_err(errors, fld, err_msg)
            except Exception as e:
                raise e

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


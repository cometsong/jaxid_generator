from django.db import models

JAXID_TYPES = (
        ('J', 'sample id'),
        ('L', '??'),
        ('etc', '??'),
        )

class JaxIdMasterList(models.Model):
    jaxid = models.CharField('JAX ID',
            max_length=6, blank=False,
            help_text="A unique ID string for every sample."
            )
    creation_date = models.DateTimeField(
            auto_now_add=True,
            )

class ProjectLinks(models.Model):
    jaxid = models.ForeignKey(JaxIdMasterList)
    project_code = models.CharField('Project Code',
            max_length=4, blank=False,
            help_text="A unique project identifiying code (4 chars)."
            )


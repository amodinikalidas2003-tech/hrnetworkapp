# Create your models here.

import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()

class FormSchema(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(_("Form Name"), max_length=255)
    description = models.TextField(_("Description"), blank=True, null=True)
    # schema_definition stores the structure: fields, types, labels, validation rules
    schema_definition = models.JSONField(_("Schema Definition"), default=dict)
    
    created_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='created_forms',
        verbose_name=_("Created By")
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Form Schema")
        verbose_name_plural = _("Form Schemas")

    def __str__(self):
        return self.name

class FormSubmission(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    schema = models.ForeignKey(
        FormSchema, 
        on_delete=models.CASCADE, 
        related_name='submissions',
        verbose_name=_("Form Schema")
    )
    submitted_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, # Allow anonymous submissions if needed, or enforce in view
        related_name='form_submissions',
        verbose_name=_("Submitted By")
    )
    # data stores the actual answers matching the schema_definition
    data = models.JSONField(_("Submission Data"), default=dict)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Form Submission")
        verbose_name_plural = _("Form Submissions")

    def __str__(self):
        return f"{self.schema.name} - {self.id}"

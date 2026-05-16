import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from apps.interviews.models import Interview

User = get_user_model()

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    user_id = instance.uploaded_by.id if instance.uploaded_by else 'anonymous'
    return 'user_{0}/{1}'.format(user_id, filename)

class FileArchive(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file = models.FileField(_("File"), upload_to=user_directory_path)
    original_filename = models.CharField(_("Original Filename"), max_length=255)
    content_type = models.CharField(_("Content Type"), max_length=100, blank=True)
    size = models.PositiveIntegerField(_("Size (bytes)"), default=0)
    
    uploaded_by = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='uploaded_files',
        verbose_name=_("Uploaded By")
    )

    interview = models.ForeignKey(
        Interview,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='archived_files',
        verbose_name=_("مصاحبه")
    )

    description = models.TextField(_("Description"), blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("File Archive")
        verbose_name_plural = _("File Archives")

    def __str__(self):
        return self.original_filename

    def save(self, *args, **kwargs):
        if self.file:
            if not self.original_filename:
                self.original_filename = self.file.name
            if not self.size:
                try:
                    self.size = self.file.size
                except:
                    pass
        super().save(*args, **kwargs)

import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()

class Department(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(_("Name"), max_length=255)
    parent = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='sub_departments',
        verbose_name=_("Parent Department")
    )
    manager = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='managed_department',
        verbose_name=_("Manager")
    )
    description = models.TextField(_("Description"), blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Department")
        verbose_name_plural = _("Departments")

    def __str__(self):
        return self.name

class OrganizationalPost(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(_("Post Title"), max_length=255)
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name=_("Department")
    )
    post_level = models.ForeignKey(
        'PostLevel',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='posts',
        verbose_name=_("Post Level")
    )
    parent_post = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='subordinate_posts',
        verbose_name=_("Parent Post (Manager)")
    )
    description = models.TextField(_("Job Description"), blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Organizational Post")
        verbose_name_plural = _("Organizational Posts")

    def __str__(self):
        return f"{self.title} - {self.department.name}"

class Person(models.Model):
    """
    Represents an individual being evaluated or managed within the HR network.
    Can optionally be linked to a Django User account.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='person_profile',
        verbose_name=_("User Account")
    )
    first_name = models.CharField(_("First Name"), max_length=255)
    last_name = models.CharField(_("Last Name"), max_length=255)
    national_id = models.CharField(_("National ID"), max_length=20, blank=True, null=True, unique=True)
    phone_number = models.CharField(_("Phone Number"), max_length=20, blank=True, null=True)
    email = models.EmailField(_("Email"), blank=True, null=True)
    employee_code = models.CharField(_("Employee Code"), max_length=50, blank=True, null=True, unique=True)
    profile_picture = models.ImageField(_("Profile Picture"), upload_to='profile_pictures/', blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _("Person")
        verbose_name_plural = _("Persons")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
        
    @property
    def current_post(self):
        """Returns the currently active organizational post for this person"""
        active_history = self.post_history.filter(is_active=True).order_by('-start_date').first()
        return active_history.post if active_history else None


class PersonPostHistory(models.Model):
    """
    Records the history of organizational posts a person has held.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='post_history', verbose_name=_("Person"))
    post = models.ForeignKey(OrganizationalPost, on_delete=models.CASCADE, related_name='assigned_persons', verbose_name=_("Organizational Post"))
    
    start_date = models.DateField(_("Start Date"))
    end_date = models.DateField(_("End Date"), null=True, blank=True)
    is_active = models.BooleanField(_("Is Active"), default=True)
    description = models.TextField(_("Description"), blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _("Person Post History")
        verbose_name_plural = _("Person Post Histories")
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.person} -> {self.post.title}"


class PostLevel(models.Model):
    """
    Job/Position levels for organizational posts.
    Independent from CompetencyLevel (matrix columns).
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(_("Level Name"), max_length=100, unique=True)
    description = models.TextField(_("Description"), blank=True, null=True)
    order = models.PositiveIntegerField(_("Display Order"), default=0)
    is_active = models.BooleanField(_("Is Active"), default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _("Post Level")
        verbose_name_plural = _("Post Levels")
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class ManagementLevel(models.Model):
    """
    Management hierarchy levels.
    Independent from CompetencyLevel (matrix columns).
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(_("Management Level"), max_length=100, unique=True)
    description = models.TextField(_("Description"), blank=True, null=True)
    level_number = models.PositiveIntegerField(_("Level Number"), default=1, help_text="Higher number = higher rank")
    is_active = models.BooleanField(_("Is Active"), default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _("Management Level")
        verbose_name_plural = _("Management Levels")
        ordering = ['-level_number', 'name']

    def __str__(self):
        return self.name

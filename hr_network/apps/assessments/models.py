import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from apps.organization.models import OrganizationalPost, PostLevel

User = get_user_model()

class Competency(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(_("Competency Name"), max_length=255) # e.g. "Leadership", "Communication"
    description = models.TextField(_("Description"), blank=True)
    
    def __str__(self):
        return self.name

class CompetencyLevel(models.Model):
    """
    Represents the levels or groups for which competencies are evaluated (e.g. Junior, Senior, Manager, Exec)
    Can be mapped to Organizational Posts later.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(_("Level Name"), max_length=100)
    order = models.PositiveIntegerField(_("Order"), default=0)
    
    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name

class CompetencyIndicator(models.Model):
    """
    The cell of the matrix. Connects a Competency, a Level, and stores the behavioral indicator / dynamic data.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    competency = models.ForeignKey(Competency, on_delete=models.CASCADE, related_name="indicators")
    level = models.ForeignKey(CompetencyLevel, on_delete=models.CASCADE, related_name="indicators")
    
    # Is this specific cell active for this level?
    is_active = models.BooleanField(_("Is Active"), default=True)
    
    # Dynamic JSON data to store behavioral indicators, questions, scoring weights, etc.
    data = models.JSONField(_("Dynamic Data"), default=dict, blank=True)
    
    class Meta:
        unique_together = ('competency', 'level')
        verbose_name = _("Competency Indicator")
        verbose_name_plural = _("Competency Indicators")

    def __str__(self):
        return f"{self.competency.name} - {self.level.name}"

class AssessmentScore(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    evaluated_user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='received_assessments',
        verbose_name=_("Evaluated User")
    )
    evaluator_user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='given_assessments',
        verbose_name=_("Evaluator")
    )
    
    # Optional link to the specific form submission that generated this score
    submission = models.OneToOneField(
        'forms.FormSubmission', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='assessment_score',
        verbose_name=_("Form Submission")
    )
    
    # Store breakdown of scores (e.g., {"Technical": 85, "Soft Skills": 90})
    dimension_scores = models.JSONField(_("Dimension Scores"), default=dict)
    
    total_score = models.FloatField(_("Total Score"), default=0.0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Assessment Score")
        verbose_name_plural = _("Assessment Scores")

    def __str__(self):
        return f"{self.evaluator_user} -> {self.evaluated_user}: {self.total_score}"


class PostCompetency(models.Model):
    """
    Links a Post to a Competency at a specific Level.
    Allows configuring which competencies are relevant for each post at each level.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    post = models.ForeignKey(OrganizationalPost, on_delete=models.CASCADE, related_name="competencies", null=True, blank=True)
    post_level = models.ForeignKey(PostLevel, on_delete=models.CASCADE, related_name="competencies", null=True, blank=True)
    competency = models.ForeignKey(Competency, on_delete=models.CASCADE, related_name="posts")
    level = models.ForeignKey(CompetencyLevel, on_delete=models.CASCADE, related_name="post_competencies", verbose_name=_("Level"), null=True, blank=True)
    is_active = models.BooleanField(_("Is Active"), default=True)
    weight = models.PositiveIntegerField(_("Weight"), default=1, help_text=_("Importance of this competency for the post"))
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['post', 'competency', 'level'],
                name='unique_post_competency_level',
                condition=models.Q(post__isnull=False)
            ),
            models.UniqueConstraint(
                fields=['post_level', 'competency', 'level'],
                name='unique_post_level_competency_level',
                condition=models.Q(post_level__isnull=False)
            )
        ]
        verbose_name = _("Post Competency")
        verbose_name_plural = _("Post Competencies")

    def __str__(self):
        if self.post_id:
            return f"{self.post.title} - {self.competency.name} ({self.level.name})"
        if self.post_level_id:
            return f"{self.post_level.name} - {self.competency.name} ({self.level.name})"
        return f"{self.competency.name} ({self.level.name})"


class PostCompetencyLikertScale(models.Model):
    """
    Stores the likert scale (1-5) definitions for a specific post-competency cell.
    Allows defining what each score level means for a specific competency at a specific post level.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    post_competency = models.ForeignKey(PostCompetency, on_delete=models.CASCADE, related_name="likert_scales")
    score = models.PositiveSmallIntegerField(_("Score"), choices=[(i, i) for i in range(1, 6)], help_text=_("Likert scale value 1-5"))
    definition = models.TextField(_("Definition"), help_text=_("Description of what this score means for this competency at this post level"))
    
    class Meta:
        unique_together = ('post_competency', 'score')
        verbose_name = _("Post Competency Likert Scale")
        verbose_name_plural = _("Post Competency Likert Scales")

    def __str__(self):
        return f"{self.post_competency} - Score {self.score}"

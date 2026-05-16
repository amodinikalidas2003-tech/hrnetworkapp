import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from apps.organization.models import Person, OrganizationalPost
from apps.assessments.models import Competency, CompetencyLevel, PostCompetency

User = get_user_model()


class Interview(models.Model):
    """
    یک جلسه مصاحبه/ارزیابی 360 درجه.
    در این جلسه از مصاحبه‌شونده (interviewer) درباره افراد مختلف ارزیابی گرفته می‌شود.
    """
    STATUS_CHOICES = [
        ('planned', _('برنامه‌ریزی شده')),
        ('in_progress', _('در حال انجام')),
        ('completed', _('تکمیل شده')),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # عنوان جلسه مصاحبه
    title = models.CharField(_("عنوان جلسه"), max_length=255)
    
    # تاریخ برگزاری جلسه
    date = models.DateTimeField(_("تاریخ مصاحبه"), blank=True, null=True)
    
    # وضعیت - به صورت خودکار بر اساس فرآیند تعیین می‌شود
    status = models.CharField(_("وضعیت"), max_length=20, choices=STATUS_CHOICES, default='planned')
    
    # یادداشت‌های کلی جلسه
    notes = models.TextField(_("یادداشت‌ها"), blank=True, null=True)
    
    # کاربری که این مصاحبه را ثبت کرده
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_interviews',
        verbose_name=_("ثبت‌کننده")
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("مصاحبه")
        verbose_name_plural = _("مصاحبه‌ها")
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"
    
    def get_participants_count(self):
        """تعداد افراد شرکت‌کننده در این جلسه"""
        return self.participants.count()
    
    def update_status(self):
        """به‌روزرسانی وضعیت بر اساس وضعیت پاسخ‌ها"""
        participants = self.participants.all()
        if not participants.exists():
            self.status = 'planned'
        elif all(p.status == 'completed' for p in participants):
            self.status = 'completed'
        elif any(p.status == 'in_progress' for p in participants):
            self.status = 'in_progress'
        else:
            self.status = 'planned'
        self.save(update_fields=['status'])


class InterviewParticipant(models.Model):
    """
    شرکت‌کننده در جلسه مصاحبه
    هر فرد می‌تواند درباره افراد مختلف ارزیابی انجام دهد
    """
    STATUS_CHOICES = [
        ('pending', _('در انتظار')),
        ('in_progress', _('در حال انجام')),
        ('completed', _('تکمیل شده')),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # جلسه مصاحبه
    interview = models.ForeignKey(
        Interview,
        on_delete=models.CASCADE,
        related_name='participants',
        verbose_name=_("جلسه مصاحبه")
    )
    
    # فرد مصاحبه‌شونده - کسی که از او سوال می‌پرسیم (باید قبلاً ثبت شده باشد)
    interviewer = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        related_name='interview_participations',
        verbose_name=_("مصاحبه‌شونده (ارزیابی‌کننده)")
    )
    
    # پست فرد مصاحبه‌شونده (اختیاری - مصاحبه‌گر نیازی به پست ندارد)
    interviewer_post = models.ForeignKey(
        OrganizationalPost,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='interview_participations',
        verbose_name=_("پست مصاحبه‌شونده")
    )
    
    # وضعیت ارزیابی این فرد
    status = models.CharField(_("وضعیت"), max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # یادداشت مربوط به این فرد
    notes = models.TextField(_("یادداشت‌ها"), blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _("شرکت‌کننده مصاحبه")
        verbose_name_plural = _("شرکت‌کنندگان مصاحبه")
        unique_together = ('interview', 'interviewer')
        ordering = ['interviewer__first_name', 'interviewer__last_name']
    
    def __str__(self):
        return f"{self.interviewer} در {self.interview.title}"


class InterviewEvaluation(models.Model):
    """
    ارزیابی یک فرد درباره فرد دیگر در جلسه مصاحبه
    هر شرکت‌کننده (مصاحبه‌شونده) درباره افراد مختلف ارزیابی می‌دهد
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # شرکت‌کننده در جلسه (مصاحبه‌شونده)
    participant = models.ForeignKey(
        InterviewParticipant,
        on_delete=models.CASCADE,
        related_name='evaluations',
        verbose_name=_("شرکت‌کننده")
    )
    
    # فرد ارزیابی‌شونده - کسی که درباره‌اش ارزیابی انجام می‌شود
    evaluated_person = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        related_name='evaluations_received',
        verbose_name=_("فرد ارزیابی‌شونده")
    )
    
    # پست فرد ارزیابی‌شونده
    evaluated_post = models.ForeignKey(
        OrganizationalPost,
        on_delete=models.CASCADE,
        related_name='evaluations_received',
        verbose_name=_("پست ارزیابی‌شونده")
    )
    
    # شایستگی ارزیابی‌شده (اختیاری - هنگام ایجاد خالی است)
    competency = models.ForeignKey(
        Competency,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='interview_evaluations',
        verbose_name=_("شایستگی")
    )
    
    # سطح شایستگی (اختیاری - هنگام ایجاد خالی است)
    competency_level = models.ForeignKey(
        CompetencyLevel,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='interview_evaluations',
        verbose_name=_("سطح شایستگی")
    )
    
    # نمره 1 تا 5
    score = models.PositiveSmallIntegerField(
        verbose_name=_("نمره"),
        choices=[(i, i) for i in range(1, 6)],
        null=True,
        blank=True
    )
    
    # توضیحات
    notes = models.TextField(_("توضیحات"), blank=True, null=True)
    
    # تعریف نمره انتخاب شده
    selected_definition = models.TextField(_("تعریف انتخاب شده"), blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("ارزیابی")
        verbose_name_plural = _("ارزیابی‌ها")
        unique_together = ('participant', 'evaluated_person', 'competency', 'competency_level')
        ordering = ['evaluated_person__first_name', 'competency__name']

    def __str__(self):
        return f"{self.participant.interviewer} درباره {self.evaluated_person} - {self.competency.name}"
    
    def get_likert_definitions(self):
        """دریافت تعاریف Likert Scale"""
        from apps.assessments.models import PostCompetency
        try:
            post_competency = PostCompetency.objects.get(
                post=self.evaluated_post,
                competency=self.competency,
                level=self.competency_level
            )
            return {str(scale.score): scale.definition for scale in post_competency.likert_scales.all()}
        except PostCompetency.DoesNotExist:
            return {}

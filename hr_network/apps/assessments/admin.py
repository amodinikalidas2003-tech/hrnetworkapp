from django.contrib import admin
from .models import AssessmentScore

@admin.register(AssessmentScore)
class AssessmentScoreAdmin(admin.ModelAdmin):
    list_display = ('evaluator_user', 'evaluated_user', 'total_score', 'created_at')
    search_fields = ('evaluator_user__username', 'evaluated_user__username')
    list_filter = ('created_at',)

from django.urls import path
from .views import (
    AssessmentListView,
    CompetencyMatrixView,
    SaveCompetencyCellView,
    AddCompetencyLevelView,
    AddCompetencyView,
    DeleteCompetencyLevelView,
    DeleteCompetencyView,
    PostCompetencyMatrixView,
    SavePostCompetencyView,
    SavePostCompetencyLikertScaleView,
    LevelCompetencyMatrixView,
    UpdateCompetencyView,
    UpdateCompetencyLevelView
)

urlpatterns = [
    path('', AssessmentListView.as_view(), name='assessment_list'),
    path('competencies/', CompetencyMatrixView.as_view(), name='competency_matrix'),
    path('competencies/save-cell/', SaveCompetencyCellView.as_view(), name='save_competency_cell'),
    path('competencies/update/', UpdateCompetencyView.as_view(), name='update_competency'),
    path('competency-levels/update/', UpdateCompetencyLevelView.as_view(), name='update_competency_level'),
    path('competencies/add-level/', AddCompetencyLevelView.as_view(), name='add_competency_level'),
    path('competencies/add-competency/', AddCompetencyView.as_view(), name='add_competency'),
    path('competencies/delete-level/<uuid:pk>/', DeleteCompetencyLevelView.as_view(), name='delete_competency_level'),
    path('competencies/delete-competency/<uuid:pk>/', DeleteCompetencyView.as_view(), name='delete_competency'),
    # Post-specific competency matrix
    path('posts/<uuid:post_id>/competencies/', PostCompetencyMatrixView.as_view(), name='post_competency_matrix'),
    path('posts/save-competency/', SavePostCompetencyView.as_view(), name='save_post_competency'),
    path('posts/save-likert-scale/', SavePostCompetencyLikertScaleView.as_view(), name='save_post_likert_scale'),
    # Level-specific competency matrix
    path('levels/<uuid:level_id>/competencies/', LevelCompetencyMatrixView.as_view(), name='level_competency_matrix'),
]

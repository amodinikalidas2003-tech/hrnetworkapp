from django.urls import path
from .views import (
    InterviewListView, InterviewCreateView, InterviewDetailView, InterviewUpdateView, InterviewDeleteView,
    SaveEvaluationView, CompleteParticipantView, GetPersonPostsView,
    AddParticipantView, RemoveParticipantView, GetCompetencyMatrixView,
    AddEvaluatedPersonView, EvaluatePersonView
)

urlpatterns = [
    # لیست و ایجاد مصاحبه
    path('', InterviewListView.as_view(), name='interview_list'),
    path('create/', InterviewCreateView.as_view(), name='interview_create'),
    
    # جزئیات، ویرایش و حذف مصاحبه
    path('<uuid:pk>/', InterviewDetailView.as_view(), name='interview_detail'),
    path('<uuid:pk>/update/', InterviewUpdateView.as_view(), name='interview_update'),
    path('<uuid:pk>/delete/', InterviewDeleteView.as_view(), name='interview_delete'),
    
    # مدیریت شرکت‌کنندگان
    path('<uuid:pk>/participants/add/', AddParticipantView.as_view(), name='add_participant'),
    path('<uuid:pk>/participants/<uuid:participant_pk>/remove/', RemoveParticipantView.as_view(), name='remove_participant'),
    
    # مدیریت افراد ارزیابی‌شونده
    path('<uuid:pk>/evaluated-persons/add/', AddEvaluatedPersonView.as_view(), name='add_evaluated_person'),
    path('<uuid:pk>/evaluated-persons/<uuid:person_id>/', EvaluatePersonView.as_view(), name='evaluate_person'),
    
    # ارزیابی
    path('participants/<uuid:participant_pk>/save-evaluation/', SaveEvaluationView.as_view(), name='save_evaluation'),
    path('participants/<uuid:participant_pk>/complete/', CompleteParticipantView.as_view(), name='complete_participant'),
    
    # AJAX helpers
    path('api/person-posts/', GetPersonPostsView.as_view(), name='get_person_posts'),
    path('api/competency-matrix/', GetCompetencyMatrixView.as_view(), name='get_competency_matrix'),
]

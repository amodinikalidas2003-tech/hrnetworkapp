from django.urls import path
from .views import FileArchiveListView, FileUploadView, FileArchiveUpdateView, FileArchiveDeleteView

urlpatterns = [
    path('', FileArchiveListView.as_view(), name='file_list'),
    path('upload/', FileUploadView.as_view(), name='file_upload'),
    path('<uuid:pk>/update/', FileArchiveUpdateView.as_view(), name='file_update'),
    path('<uuid:pk>/delete/', FileArchiveDeleteView.as_view(), name='file_delete'),
]

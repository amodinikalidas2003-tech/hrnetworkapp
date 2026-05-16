from django.views.generic import ListView, View, UpdateView, DeleteView
from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse_lazy
from web_project import TemplateLayout
from .models import FileArchive
from .forms import FileArchiveForm

class FileArchiveListView(ListView):
    model = FileArchive
    template_name = 'files/file_list.html'
    context_object_name = 'files'

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        return context

class FileUploadView(View):
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "You must be logged in to upload files.")
            return redirect('login')
            
        if 'file' in request.FILES:
            uploaded_file = request.FILES['file']
            # Create standard file record
            FileArchive.objects.create(
                file=uploaded_file,
                original_filename=request.POST.get('title') or uploaded_file.name,
                description=request.POST.get('description', ''),
                content_type=uploaded_file.content_type,
                size=uploaded_file.size,
                uploaded_by=request.user
            )
            messages.success(request, "File uploaded successfully.")
        else:
            messages.error(request, "No file provided.")

        return redirect('file_list')

class FileArchiveUpdateView(UpdateView):
    model = FileArchive
    form_class = FileArchiveForm
    template_name = 'files/file_list.html'
    success_url = reverse_lazy('file_list')

    def form_valid(self, form):
        messages.success(self.request, "File details updated successfully.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Error updating file details.")
        return redirect('file_list')

class FileArchiveDeleteView(DeleteView):
    model = FileArchive
    success_url = reverse_lazy('file_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "File deleted successfully.")
        return super().delete(request, *args, **kwargs)

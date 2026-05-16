import pandas as pd
from django.views.generic import ListView, CreateView, View, UpdateView, DeleteView, DetailView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import HttpResponse
from web_project import TemplateLayout
from .models import Department, OrganizationalPost, Person, PersonPostHistory, PostLevel, ManagementLevel
from .forms import OrganizationalPostForm, ExcelImportForm, DepartmentForm, PersonForm, PersonPostHistoryForm, PostLevelForm, ManagementLevelForm
from apps.assessments.models import CompetencyLevel
from apps.assessments.forms import CompetencyLevelForm

class PersonListView(ListView):
    model = Person
    template_name = 'organization/person_list.html'
    context_object_name = 'persons'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['person_form'] = PersonForm()
        context = TemplateLayout.init(self, context)
        return context

class PersonCreateView(CreateView):
    model = Person
    form_class = PersonForm
    template_name = 'organization/person_list.html'
    success_url = reverse_lazy('person_list')

    def form_valid(self, form):
        messages.success(self.request, "Person profile created successfully.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Error creating person profile. Please check the form.")
        return redirect('person_list')

class PersonUpdateView(UpdateView):
    model = Person
    form_class = PersonForm
    template_name = 'organization/person_list.html'
    success_url = reverse_lazy('person_list')

    def get_success_url(self):
        next_url = self.request.POST.get('next')
        if next_url:
            return next_url
        return super().get_success_url()

    def form_valid(self, form):
        messages.success(self.request, "Person profile updated successfully.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Error updating person profile. Please check the form.")
        return redirect('person_list')

class PersonDeleteView(DeleteView):
    model = Person
    success_url = reverse_lazy('person_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Person profile deleted successfully.")
        return super().delete(request, *args, **kwargs)

class PersonDetailView(DetailView):
    model = Person
    template_name = 'organization/person_detail.html'
    context_object_name = 'person'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['person_form'] = PersonForm(instance=self.object)
        context['post_history_form'] = PersonPostHistoryForm(initial={'person': self.object})
        # Provide posts for easy selection in template if needed
        context['available_posts'] = OrganizationalPost.objects.all()
        context = TemplateLayout.init(self, context)
        return context

class AddPersonPostHistoryView(CreateView):
    model = PersonPostHistory
    form_class = PersonPostHistoryForm

    def get_success_url(self):
        return reverse_lazy('person_detail', kwargs={'pk': self.object.person.pk})

    def form_valid(self, form):
        messages.success(self.request, "Post history added successfully.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Error adding post history. Please check the form.")
        person_id = self.request.POST.get('person')
        if person_id:
            return redirect('person_detail', pk=person_id)
        return redirect('person_list')

class UpdatePersonPostHistoryView(UpdateView):
    model = PersonPostHistory
    form_class = PersonPostHistoryForm

    def get_success_url(self):
        return reverse_lazy('person_detail', kwargs={'pk': self.object.person.pk})

    def form_valid(self, form):
        messages.success(self.request, "Post history updated successfully.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Error updating post history.")
        return redirect('person_detail', pk=self.object.person.pk)

class DeletePersonPostHistoryView(DeleteView):
    model = PersonPostHistory

    def get_success_url(self):
        return reverse_lazy('person_detail', kwargs={'pk': self.object.person.pk})

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Post history deleted successfully.")
        return super().delete(request, *args, **kwargs)

class DepartmentListView(ListView):
    model = Department
    template_name = 'organization/department_list.html'
    context_object_name = 'departments'

    def get_queryset(self):
        # Fetch all departments
        all_depts = list(Department.objects.select_related('manager', 'parent').all())
        
        # Build tree structure
        def build_tree(parent_id, level):
            tree = []
            children = [d for d in all_depts if (d.parent_id == parent_id)]
            for child in children:
                child.level = level
                # Check if it has any children
                child.has_children = any(d.parent_id == child.id for d in all_depts)
                tree.append(child)
                tree.extend(build_tree(child.id, level + 1))
            return tree
        
        return build_tree(None, 0)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add organizational posts to the context for the new tab
        context['posts'] = OrganizationalPost.objects.all()
        context['post_form'] = OrganizationalPostForm()
        context['excel_form'] = ExcelImportForm()
        context['dept_form'] = DepartmentForm()
        # Add competency levels for the levels tab (matrix columns - separate from post levels)
        context['competency_levels'] = CompetencyLevel.objects.all().order_by('order')
        context['level_form'] = CompetencyLevelForm()
        # Add post levels (independent from competency levels)
        context['post_levels'] = PostLevel.objects.filter(is_active=True).order_by('order')
        context['post_level_form'] = PostLevelForm()
        # Initialize the global layout context
        context = TemplateLayout.init(self, context)
        return context

class DepartmentCreateView(CreateView):
    model = Department
    form_class = DepartmentForm
    template_name = 'organization/department_list.html'

    def get_success_url(self):
        active_tab = self.request.POST.get('active_tab', 'departments')
        return f"{reverse_lazy('department_list')}?tab={active_tab}"

    def form_valid(self, form):
        messages.success(self.request, "Department created successfully.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Error creating department. Please check the form.")
        active_tab = self.request.POST.get('active_tab', 'departments')
        return redirect(f"{reverse_lazy('department_list')}?tab={active_tab}")

class DepartmentUpdateView(UpdateView):
    model = Department
    form_class = DepartmentForm
    template_name = 'organization/department_list.html'

    def get_success_url(self):
        active_tab = self.request.POST.get('active_tab', 'departments')
        return f"{reverse_lazy('department_list')}?tab={active_tab}"

    def form_valid(self, form):
        messages.success(self.request, "Department updated successfully.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Error updating department. Please check the form.")
        active_tab = self.request.POST.get('active_tab', 'departments')
        return redirect(f"{reverse_lazy('department_list')}?tab={active_tab}")

class DepartmentDeleteView(DeleteView):
    model = Department

    def get_success_url(self):
        active_tab = self.request.POST.get('active_tab', 'departments')
        return f"{reverse_lazy('department_list')}?tab={active_tab}"

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Department deleted successfully.")
        return super().delete(request, *args, **kwargs)

class OrganizationalPostCreateView(CreateView):
    model = OrganizationalPost
    form_class = OrganizationalPostForm
    template_name = 'organization/department_list.html'

    def get_success_url(self):
        active_tab = self.request.POST.get('active_tab', 'posts')
        return f"{reverse_lazy('department_list')}?tab={active_tab}"

    def form_valid(self, form):
        messages.success(self.request, "Organizational Post created successfully.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Error creating post. Please check the form.")
        active_tab = self.request.POST.get('active_tab', 'posts')
        return redirect(f"{reverse_lazy('department_list')}?tab={active_tab}")

class OrganizationalPostUpdateView(UpdateView):
    model = OrganizationalPost
    form_class = OrganizationalPostForm
    template_name = 'organization/department_list.html'

    def get_success_url(self):
        active_tab = self.request.POST.get('active_tab', 'posts')
        return f"{reverse_lazy('department_list')}?tab={active_tab}"

    def form_valid(self, form):
        messages.success(self.request, "Organizational Post updated successfully.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Error updating post. Please check the form.")
        active_tab = self.request.POST.get('active_tab', 'posts')
        return redirect(f"{reverse_lazy('department_list')}?tab={active_tab}")

class OrganizationalPostDeleteView(DeleteView):
    model = OrganizationalPost

    def get_success_url(self):
        active_tab = self.request.POST.get('active_tab', 'posts')
        return f"{reverse_lazy('department_list')}?tab={active_tab}"

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Organizational Post deleted successfully.")
        return super().delete(request, *args, **kwargs)

class ImportPostsExcelView(View):
    def post(self, request, *args, **kwargs):
        form = ExcelImportForm(request.POST, request.FILES)
        active_tab = request.POST.get('active_tab', 'posts')
        if form.is_valid():
            excel_file = request.FILES['excel_file']
            try:
                df = pd.read_excel(excel_file)

                # Validation of required columns
                required_columns = ['Title', 'Department_Name']
                missing_columns = [col for col in required_columns if col not in df.columns]

                if missing_columns:
                    messages.error(request, f"Validation Error: Missing required columns in Excel: {', '.join(missing_columns)}")
                    return redirect(f"{reverse_lazy('department_list')}?tab={active_tab}")

                success_count = 0
                error_messages = []
                
                for index, row in df.iterrows():
                    # Expected columns: Title, Department_Name, Parent_Post_Title, Description
                    title = row.get('Title')
                    dept_name = row.get('Department_Name')
                    
                    if pd.isna(title) or pd.isna(dept_name):
                        error_messages.append(f"Row {index+2}: Title and Department_Name are required.")
                        continue
                        
                    try:
                        department = Department.objects.get(name=dept_name)
                    except Department.DoesNotExist:
                        error_messages.append(f"Row {index+2}: Department with Name '{dept_name}' not found.")
                        continue
                        
                    parent_post = None
                    parent_title = row.get('Parent_Post_Title') if 'Parent_Post_Title' in df.columns else None
                    if not pd.isna(parent_title) and parent_title:
                        try:
                            parent_post = OrganizationalPost.objects.get(title=parent_title)
                        except OrganizationalPost.DoesNotExist:
                            error_messages.append(f"Row {index+2}: Parent Post with Title '{parent_title}' not found. Leaving empty.")
                            
                    description = row.get('Description', '') if 'Description' in df.columns else ''
                    if pd.isna(description):
                        description = ''
                        
                    OrganizationalPost.objects.create(
                        title=title,
                        department=department,
                        parent_post=parent_post,
                        description=description
                    )
                    success_count += 1
                    
                if success_count > 0:
                    messages.success(request, f"Successfully imported {success_count} posts from Excel.")
                if error_messages:
                    for err in error_messages[:5]: # Show max 5 errors to not overflow message box
                        messages.warning(request, err)
                        
            except Exception as e:
                messages.error(request, f"Error processing Excel file: {str(e)}")
        else:
            messages.error(request, "Invalid form submission.")
            
        return redirect('department_list')

class ExportDepartmentsExcelView(View):
    def get(self, request, *args, **kwargs):
        departments = Department.objects.select_related('manager', 'parent').all()
        
        data = []
        for dept in departments:
            data.append({
                'Name': dept.name,
                'Manager': dept.manager.username if dept.manager else 'N/A',
                'Parent Department': dept.parent.name if dept.parent else 'Root',
                'Created At': dept.created_at.strftime('%Y-%m-%d')
            })
            
        df = pd.DataFrame(data)
        
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="departments.xlsx"'
        
        df.to_excel(response, index=False)
        return response

class DownloadDepartmentExcelTemplateView(View):
    def get(self, request, *args, **kwargs):
        data = [{
            'Name': 'Sample Department',
            'Parent_Department_Name': 'Leave empty or enter exact name of parent department',
            'Manager_Username': 'Leave empty or enter username of manager',
            'Description': 'Description of the department'
        }]
        
        df = pd.DataFrame(data)
        
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="departments_template.xlsx"'
        
        df.to_excel(response, index=False)
        return response

class ImportDepartmentsExcelView(View):
    def post(self, request, *args, **kwargs):
        form = ExcelImportForm(request.POST, request.FILES)
        active_tab = request.POST.get('active_tab', 'departments')
        if form.is_valid():
            excel_file = request.FILES['excel_file']
            try:
                df = pd.read_excel(excel_file)

                # Validation of required columns
                required_columns = ['Name']
                missing_columns = [col for col in required_columns if col not in df.columns]

                if missing_columns:
                    messages.error(request, f"Validation Error: Missing required columns in Excel: {', '.join(missing_columns)}")
                    return redirect(f"{reverse_lazy('department_list')}?tab={active_tab}")

                success_count = 0
                error_messages = []
                
                for index, row in df.iterrows():
                    name = row.get('Name')
                    if pd.isna(name):
                        error_messages.append(f"Row {index+2}: Name is required.")
                        continue
                        
                    parent_dept = None
                    parent_name = row.get('Parent_Department_Name') if 'Parent_Department_Name' in df.columns else None
                    if not pd.isna(parent_name) and parent_name:
                        try:
                            parent_dept = Department.objects.get(name=parent_name)
                        except Department.DoesNotExist:
                            error_messages.append(f"Row {index+2}: Parent Department with Name '{parent_name}' not found. Leaving empty.")
                            
                    manager = None
                    manager_username = row.get('Manager_Username') if 'Manager_Username' in df.columns else None
                    if not pd.isna(manager_username) and manager_username:
                        from django.contrib.auth import get_user_model
                        User = get_user_model()
                        try:
                            manager = User.objects.get(username=manager_username)
                        except User.DoesNotExist:
                            error_messages.append(f"Row {index+2}: Manager with username '{manager_username}' not found. Leaving empty.")

                    description = row.get('Description', '') if 'Description' in df.columns else ''
                    if pd.isna(description):
                        description = ''
                        
                    Department.objects.create(
                        name=name,
                        parent=parent_dept,
                        manager=manager,
                        description=description
                    )
                    success_count += 1

                if success_count > 0:
                    messages.success(request, f"Successfully imported {success_count} departments from Excel.")
                if error_messages:
                    for err in error_messages[:5]:
                        messages.warning(request, err)

            except Exception as e:
                messages.error(request, f"Error processing Excel file: {str(e)}")
        else:
            messages.error(request, "Invalid form submission.")

        return redirect(f"{reverse_lazy('department_list')}?tab={active_tab}")

class ExportPostsExcelView(View):
    def get(self, request, *args, **kwargs):
        posts = OrganizationalPost.objects.select_related('department', 'parent_post').all()
        
        data = []
        for post in posts:
            data.append({
                'Title': post.title,
                'Department': post.department.name,
                'Parent Post (Manager)': post.parent_post.title if post.parent_post else 'None',
                'Description': post.description
            })
            
        df = pd.DataFrame(data)
        
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="organizational_posts.xlsx"'
        
        df.to_excel(response, index=False)
        return response

class DownloadPostExcelTemplateView(View):
    def get(self, request, *args, **kwargs):
        # Provide the Excel Template matching exactly what Import expects
        # Expected by Import: Title, Department_Name, Parent_Post_Title, Description
        data = [{
            'Title': 'Sample Post Title',
            'Department_Name': 'Enter exact name of an existing department here',
            'Parent_Post_Title': 'Leave empty or enter exact title of manager post',
            'Description': 'Description of the post'
        }]

        df = pd.DataFrame(data)

        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="organizational_posts_template.xlsx"'

        df.to_excel(response, index=False)
        return response


# Competency Level Management Views for Organization Page
class AddCompetencyLevelOrganizationView(View):
    def post(self, request, *args, **kwargs):
        form = CompetencyLevelForm(request.POST)
        active_tab = request.POST.get('active_tab', 'levels')
        if form.is_valid():
            form.save()
            messages.success(request, "Competency level created successfully.")
        else:
            messages.error(request, "Error creating competency level.")
        return redirect(f"{reverse_lazy('department_list')}?tab={active_tab}")

class UpdateCompetencyLevelOrganizationView(View):
    def post(self, request, pk, *args, **kwargs):
        level = get_object_or_404(CompetencyLevel, pk=pk)
        active_tab = request.POST.get('active_tab', 'levels')
        form = CompetencyLevelForm(request.POST, instance=level)
        if form.is_valid():
            form.save()
            messages.success(request, "Competency level updated successfully.")
        else:
            messages.error(request, "Error updating competency level.")
        return redirect(f"{reverse_lazy('department_list')}?tab={active_tab}")

class DeleteCompetencyLevelOrganizationView(View):
    def post(self, request, pk, *args, **kwargs):
        level = get_object_or_404(CompetencyLevel, pk=pk)
        active_tab = request.POST.get('active_tab', 'levels')
        level.delete()
        messages.success(request, "Competency level deleted successfully.")
        return redirect(f"{reverse_lazy('department_list')}?tab={active_tab}")


class AddPostLevelView(View):
    def post(self, request, *args, **kwargs):
        form = PostLevelForm(request.POST)
        active_tab = request.POST.get('active_tab', 'levels')
        if form.is_valid():
            form.save()
            messages.success(request, "Post level created successfully.")
        else:
            messages.error(request, "Error creating post level.")
        return redirect(f"{reverse_lazy('department_list')}?tab={active_tab}")


class UpdatePostLevelView(View):
    def post(self, request, pk, *args, **kwargs):
        level = get_object_or_404(PostLevel, pk=pk)
        active_tab = request.POST.get('active_tab', 'levels')
        form = PostLevelForm(request.POST, instance=level)
        if form.is_valid():
            form.save()
            messages.success(request, "Post level updated successfully.")
        else:
            messages.error(request, "Error updating post level.")
        return redirect(f"{reverse_lazy('department_list')}?tab={active_tab}")


class DeletePostLevelView(View):
    def post(self, request, pk, *args, **kwargs):
        level = get_object_or_404(PostLevel, pk=pk)
        active_tab = request.POST.get('active_tab', 'levels')
        level.delete()
        messages.success(request, "Post level deleted successfully.")
        return redirect(f"{reverse_lazy('department_list')}?tab={active_tab}")


class AddManagementLevelView(View):
    def post(self, request, *args, **kwargs):
        form = ManagementLevelForm(request.POST)
        active_tab = request.POST.get('active_tab', 'levels')
        if form.is_valid():
            form.save()
            messages.success(request, "Management level created successfully.")
        else:
            messages.error(request, "Error creating management level.")
        return redirect(f"{reverse_lazy('department_list')}?tab={active_tab}")


class UpdateManagementLevelView(View):
    def post(self, request, pk, *args, **kwargs):
        level = get_object_or_404(ManagementLevel, pk=pk)
        active_tab = request.POST.get('active_tab', 'levels')
        form = ManagementLevelForm(request.POST, instance=level)
        if form.is_valid():
            form.save()
            messages.success(request, "Management level updated successfully.")
        else:
            messages.error(request, "Error updating management level.")
        return redirect(f"{reverse_lazy('department_list')}?tab={active_tab}")


class DeleteManagementLevelView(View):
    def post(self, request, pk, *args, **kwargs):
        level = get_object_or_404(ManagementLevel, pk=pk)
        active_tab = request.POST.get('active_tab', 'levels')
        level.delete()
        messages.success(request, "Management level deleted successfully.")
        return redirect(f"{reverse_lazy('department_list')}?tab={active_tab}")

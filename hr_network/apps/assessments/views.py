import json
from django.views.generic import ListView, TemplateView, View
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
from web_project import TemplateLayout
from .models import Competency, CompetencyLevel, CompetencyIndicator
from .forms import CompetencyForm, CompetencyLevelForm

class CompetencyMatrixView(TemplateView):
    template_name = 'assessments/competency_matrix.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get all levels (columns)
        levels = CompetencyLevel.objects.all().order_by('order')
        
        # Get all competencies (rows)
        competencies = Competency.objects.all()
        
        # Get all indicators (cells) mapping competency_id and level_id to cell data
        indicators = CompetencyIndicator.objects.all()
        matrix_data = {}
        for ind in indicators:
            matrix_data[f"{ind.competency_id}_{ind.level_id}"] = {
                'id': str(ind.id),
                'is_active': ind.is_active,
                'data': ind.data
            }

        context['levels'] = levels
        context['competencies'] = competencies
        context['matrix_data'] = matrix_data
        context['matrix_data_json'] = json.dumps(matrix_data)
        
        # Forms for adding rows/columns
        context['competency_form'] = CompetencyForm()
        context['level_form'] = CompetencyLevelForm()
        
        TemplateLayout.init(self, context)
        return context

class SaveCompetencyCellView(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            competency_id = data.get('competency_id')
            level_id = data.get('level_id')
            is_active = data.get('is_active', True)
            cell_data = data.get('data', {})
            
            competency = get_object_or_404(Competency, id=competency_id)
            level = get_object_or_404(CompetencyLevel, id=level_id)
            
            indicator, created = CompetencyIndicator.objects.get_or_create(
                competency=competency,
                level=level,
                defaults={'is_active': is_active, 'data': cell_data}
            )
            
            if not created:
                indicator.is_active = is_active
                indicator.data = cell_data
                indicator.save()
                
            return JsonResponse({'status': 'success', 'message': 'Cell saved successfully', 'id': str(indicator.id)})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


@method_decorator(require_POST, name='dispatch')
class UpdateCompetencyView(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            competency_id = data.get('competency_id')
            name = (data.get('name') or '').strip()

            if not competency_id:
                return JsonResponse({'status': 'error', 'message': 'competency_id is required'}, status=400)
            if not name:
                return JsonResponse({'status': 'error', 'message': 'name is required'}, status=400)

            competency = get_object_or_404(Competency, id=competency_id)
            competency.name = name
            competency.save(update_fields=['name'])

            return JsonResponse({'status': 'success', 'name': competency.name})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


@method_decorator(require_POST, name='dispatch')
class UpdateCompetencyLevelView(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            level_id = data.get('level_id')
            name = (data.get('name') or '').strip()

            if not level_id:
                return JsonResponse({'status': 'error', 'message': 'level_id is required'}, status=400)
            if not name:
                return JsonResponse({'status': 'error', 'message': 'name is required'}, status=400)

            level = get_object_or_404(CompetencyLevel, id=level_id)
            level.name = name
            level.save(update_fields=['name'])

            return JsonResponse({'status': 'success', 'name': level.name})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

class AddCompetencyLevelView(View):
    def post(self, request, *args, **kwargs):
        form = CompetencyLevelForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('competency_matrix')

class AddCompetencyView(View):
    def post(self, request, *args, **kwargs):
        form = CompetencyForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('competency_matrix')

class DeleteCompetencyLevelView(View):
    """Delete a CompetencyLevel (column) and all its related indicators"""
    def post(self, request, pk, *args, **kwargs):
        level = get_object_or_404(CompetencyLevel, pk=pk)
        level.delete()
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'status': 'success', 'message': 'Column deleted successfully'})
        return redirect('competency_matrix')

    def get(self, request, *args, **kwargs):
        return redirect('competency_matrix')

class DeleteCompetencyView(View):
    """Delete a Competency (row) and all its related indicators"""
    def post(self, request, pk, *args, **kwargs):
        competency = get_object_or_404(Competency, pk=pk)
        competency.delete()
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'status': 'success', 'message': 'Row deleted successfully'})
        return redirect('competency_matrix')

    def get(self, request, *args, **kwargs):
        return redirect('competency_matrix')

from .models import AssessmentScore, PostCompetency, PostCompetencyLikertScale
from apps.organization.models import OrganizationalPost, PostLevel

class AssessmentListView(ListView):
    model = AssessmentScore
    template_name = 'assessments/assessment_list.html'
    context_object_name = 'assessments'

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        return context


class PostCompetencyMatrixView(TemplateView):
    """
    View for configuring competencies for a specific post.
    Shows a matrix where users can activate/deactivate competencies for each level
    and define likert scale (1-5) meanings for each cell.
    """
    template_name = 'assessments/post_competency_matrix.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(OrganizationalPost, id=post_id)
        
        # Get all levels (columns) and competencies (rows)
        levels = CompetencyLevel.objects.all().order_by('order')
        competencies = Competency.objects.all()
        
        # Get existing post-competency links with their likert scales
        post_competencies = PostCompetency.objects.filter(post=post).select_related('competency', 'level')
        
        # Build matrix data keyed by "competency_id_level_id"
        matrix_data = {}
        for pc in post_competencies:
            key = f"{pc.competency_id}_{pc.level_id}"
            # Get likert scale definitions
            likert_scales = {}
            for scale in pc.likert_scales.all():
                likert_scales[str(scale.score)] = scale.definition
            
            matrix_data[key] = {
                'id': str(pc.id),
                'is_active': pc.is_active,
                'likert_scales': likert_scales
            }
        
        context['post'] = post
        context['levels'] = levels
        context['competencies'] = competencies
        context['matrix_data'] = matrix_data
        context['matrix_data_json'] = json.dumps(matrix_data)
        
        TemplateLayout.init(self, context)
        return context


class LevelCompetencyMatrixView(TemplateView):
    """
    View for configuring competencies for posts at a specific organizational level.
    Shows the same matrix structure as the main competency matrix.
    """
    template_name = 'assessments/level_competency_matrix.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post_level_id = self.kwargs.get('level_id')
        post_level = get_object_or_404(PostLevel, id=post_level_id)
        
        # Get all competencies (rows)
        competencies = Competency.objects.all()
        
        # Get all competency levels (columns) - same as main matrix
        levels = CompetencyLevel.objects.all().order_by('order', 'name')
        
        # Get existing post-competency links for this organizational level
        # These link posts at this organizational level to competencies at specific competency levels
        post_competencies = PostCompetency.objects.filter(
            post_level=post_level
        ).select_related('competency', 'level')
        
        # Build matrix data keyed by "competency_id-competency_level_id"
        matrix_data = {}
        for pc in post_competencies:
            # Get likert scale definitions
            likert_scales = {}
            for scale in pc.likert_scales.all():
                likert_scales[str(scale.score)] = scale.definition
            
            cell_key = f"{pc.competency_id}-{pc.level_id}"
            matrix_data[cell_key] = {
                'id': str(pc.id),
                'is_active': pc.is_active,
                'likert_scales': likert_scales
            }
        
        context['post_level'] = post_level
        context['competencies'] = competencies
        context['levels'] = levels
        context['matrix_data'] = matrix_data
        context['matrix_data_json'] = json.dumps(matrix_data)
        
        TemplateLayout.init(self, context)
        return context


class SavePostCompetencyView(View):
    """
    AJAX view to save/toggle a competency for a post at a specific level.
    """
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            post_id = data.get('post_id')
            post_level_id = data.get('post_level_id')  # For level-based config
            competency_id = data.get('competency_id')
            competency_level_id = data.get('competency_level_id')
            level_id = data.get('level_id')  # Fallback for backward compatibility
            is_active = data.get('is_active', True)
            
            # Determine which level to use (competency_level_id or level_id)
            actual_level_id = competency_level_id or level_id

            if not competency_id or not actual_level_id:
                return JsonResponse(
                    {'status': 'error', 'message': 'competency_id and competency_level_id are required'},
                    status=400
                )
            
            competency = get_object_or_404(Competency, id=competency_id)
            level = get_object_or_404(CompetencyLevel, id=actual_level_id)
            
            # If post_level_id is provided, this is a level-based config
            if post_level_id:
                post_level = get_object_or_404(PostLevel, id=post_level_id)
                post_competency, created = PostCompetency.objects.get_or_create(
                    post=None,
                    post_level=post_level,
                    competency=competency,
                    level=level,
                    defaults={'is_active': is_active, 'weight': 1}
                )
                if not created:
                    post_competency.is_active = is_active
                    post_competency.save()

                return JsonResponse({
                    'status': 'success',
                    'message': 'Level competency saved successfully',
                    'id': str(post_competency.id),
                    'is_active': post_competency.is_active
                })
            elif post_id:
                # Original behavior for post-specific config
                post = get_object_or_404(OrganizationalPost, id=post_id)
                
                post_competency, created = PostCompetency.objects.get_or_create(
                    post=post,
                    competency=competency,
                    level=level,
                    defaults={'is_active': is_active, 'weight': 1}
                )
                
                if not created:
                    post_competency.is_active = is_active
                    post_competency.save()
                
                return JsonResponse({
                    'status': 'success',
                    'message': 'Post competency saved successfully',
                    'id': str(post_competency.id),
                    'is_active': post_competency.is_active
                })
            else:
                # Neither post_id nor post_level_id provided
                return JsonResponse({
                    'status': 'error',
                    'message': 'Either post_id or post_level_id must be provided'
                }, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


class SavePostCompetencyLikertScaleView(View):
    """
    AJAX view to save likert scale definitions for a post-competency.
    """
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            post_competency_id = data.get('post_competency_id')
            likert_data = data.get('likert_data', {})  # {1: "def1", 2: "def2", ...}
            
            post_competency = get_object_or_404(PostCompetency, id=post_competency_id)
            
            # Update or create likert scale definitions
            for score, definition in likert_data.items():
                score = int(score)
                if score in range(1, 6):
                    PostCompetencyLikertScale.objects.update_or_create(
                        post_competency=post_competency,
                        score=score,
                        defaults={'definition': definition}
                    )
            
            return JsonResponse({
                'status': 'success',
                'message': 'Likert scale definitions saved successfully'
            })
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

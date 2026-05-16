from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import JsonResponse
from django.db import transaction
from web_project import TemplateLayout
from .models import Interview, InterviewParticipant, InterviewEvaluation
from .forms import InterviewForm, InterviewParticipantForm, InterviewEvaluationForm
from apps.organization.models import Person, OrganizationalPost
from apps.assessments.models import PostCompetency


# ==========================================
# Interview Views (360 Degree Evaluation)
# ==========================================

class InterviewListView(LoginRequiredMixin, ListView):
    """لیست تمام جلسات مصاحبه"""
    model = Interview
    template_name = 'interviews/interview_list.html'
    context_object_name = 'interviews'
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = InterviewForm()
        context['participant_form'] = InterviewParticipantForm()
        context = TemplateLayout.init(self, context)
        return context


class InterviewCreateView(LoginRequiredMixin, CreateView):
    """ایجاد جلسه مصاحبه جدید"""
    model = Interview
    form_class = InterviewForm
    template_name = 'interviews/interview_form.html'
    success_url = reverse_lazy('interview_list')
    login_url = '/login/'

    def get(self, request, *args, **kwargs):
        return redirect('interview_list')

    def form_valid(self, form):
        interviewer = form.cleaned_data.get('interviewer')
        interviewer_post = interviewer.current_post if interviewer else None

        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        self.object.save()

        # Create InterviewParticipant for the selected interviewer
        if interviewer:
            InterviewParticipant.objects.get_or_create(
                interview=self.object,
                interviewer=interviewer,
                defaults={'interviewer_post': interviewer_post, 'status': 'pending'}
            )

        messages.success(self.request, "جلسه مصاحبه با موفقیت ایجاد شد.")
        return redirect(self.get_success_url())

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                field_name = form.fields[field].label if field in form.fields else field
                messages.error(self.request, f"{field_name}: {error}")
        return redirect('interview_list')


class InterviewDetailView(DetailView):
    """نمایش جزئیات یک جلسه مصاحبه"""
    model = Interview
    template_name = 'interviews/interview_detail.html'
    context_object_name = 'interview'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        interview = self.object
        
        # Get participants with their status
        participants = interview.participants.select_related('interviewer').all()
        context['participants'] = participants
        
        # Get all unique evaluated persons and their posts
        evaluated_persons_data = {}
        for participant in participants:
            for evaluation in participant.evaluations.select_related('evaluated_person', 'evaluated_post', 'competency'):
                person_id = str(evaluation.evaluated_person.id)
                if person_id not in evaluated_persons_data:
                    evaluated_persons_data[person_id] = {
                        'person': evaluation.evaluated_person,
                        'post': evaluation.evaluated_post,
                        'post_level': evaluation.evaluated_post.post_level if evaluation.evaluated_post else None,
                        'evaluations': []
                    }
                evaluated_persons_data[person_id]['evaluations'].append(evaluation)
        
        # Build competency matrix for each unique evaluated person based on their PostLevel
        competency_matrices = {}
        for person_id, data in evaluated_persons_data.items():
            post_level = data['post_level']
            if post_level:
                # Get competencies for this PostLevel (not Post)
                from apps.assessments.models import PostCompetency
                competencies = PostCompetency.objects.filter(
                    post_level=post_level,
                    is_active=True
                ).select_related('competency', 'level').prefetch_related('likert_scales')
                competency_matrices[person_id] = {
                    'person': data['person'],
                    'post': data['post'],
                    'post_level': post_level,
                    'competencies': competencies
                }
        
        context['evaluated_persons_data'] = evaluated_persons_data
        context['competency_matrices'] = competency_matrices
        context['participant_form'] = InterviewParticipantForm()
        context['evaluation_form'] = InterviewEvaluationForm()
        
        # Get participants (interviewers) to exclude from evaluated persons dropdown
        participants = interview.participants.select_related('interviewer')
        context['participants'] = participants
        
        # Get interviewer IDs to exclude
        interviewer_ids = [p.interviewer_id for p in participants]
        context['all_persons'] = Person.objects.prefetch_related('post_history').exclude(id__in=interviewer_ids)
        
        # For backward compatibility with old template - get first evaluated person's matrix
        if evaluated_persons_data:
            first_person_id = list(evaluated_persons_data.keys())[0]
            first_data = evaluated_persons_data[first_person_id]
            if first_data['post_level']:
                from apps.assessments.models import PostCompetency
                context['competency_matrix'] = PostCompetency.objects.filter(
                    post_level=first_data['post_level'],
                    is_active=True
                ).select_related('competency', 'level').prefetch_related('likert_scales')
                context['evaluated_person'] = first_data['person']
                context['evaluated_post'] = first_data['post']
            else:
                context['competency_matrix'] = None
        else:
            context['competency_matrix'] = None
            
        context = TemplateLayout.init(self, context)
        return context


class InterviewUpdateView(UpdateView):
    """ویرایش جلسه مصاحبه"""
    model = Interview
    form_class = InterviewForm
    template_name = 'interviews/interview_form.html'
    success_url = reverse_lazy('interview_list')

    def get(self, request, *args, **kwargs):
        return redirect('interview_list')

    def form_valid(self, form):
        messages.success(self.request, "جلسه مصاحبه با موفقیت به‌روزرسانی شد.")
        return redirect(self.get_success_url())

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                field_name = form.fields[field].label if field in form.fields else field
                messages.error(self.request, f"{field_name}: {error}")
        return redirect('interview_list')


class InterviewDeleteView(DeleteView):
    """حذف جلسه مصاحبه"""
    model = Interview
    template_name = 'interviews/interview_confirm_delete.html'
    success_url = reverse_lazy('interview_list')

    def get(self, request, *args, **kwargs):
        return redirect('interview_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, "جلسه مصاحبه با موفقیت حذف شد.")
        return super().delete(request, *args, **kwargs)


# ==========================================
# Interview Participants Management
# ==========================================

class AddParticipantView(CreateView):
    """افزودن شرکت‌کننده به جلسه مصاحبه"""
    model = InterviewParticipant
    form_class = InterviewParticipantForm
    
    def form_valid(self, form):
        interview = get_object_or_404(Interview, pk=self.kwargs['pk'])
        form.instance.interview = interview
        messages.success(self.request, "شرکت‌کننده با موفقیت اضافه شد.")
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('interview_detail', kwargs={'pk': self.kwargs['pk']})


class RemoveParticipantView(View):
    """حذف شرکت‌کننده از جلسه"""
    def post(self, request, interview_pk, participant_pk):
        participant = get_object_or_404(InterviewParticipant, pk=participant_pk, interview_id=interview_pk)
        participant.delete()
        messages.success(request, "شرکت‌کننده با موفقیت حذف شد.")
        return redirect('interview_detail', pk=interview_pk)


# ==========================================
# Interview Evaluation (Score Entry)
# ==========================================

class AddEvaluatedPersonView(View):
    """افزودن فرد ارزیابی‌شونده به جلسه مصاحبه"""
    def post(self, request, pk, *args, **kwargs):
        interview = get_object_or_404(Interview, pk=pk)
        evaluated_person_id = request.POST.get('evaluated_person')
        
        if not evaluated_person_id:
            messages.error(request, "لطفاً یک فرد انتخاب کنید.")
            return redirect('interview_detail', pk=pk)
        
        evaluated_person = get_object_or_404(Person, pk=evaluated_person_id)
        evaluated_post = evaluated_person.current_post
        
        if not evaluated_post:
            messages.error(request, "این فرد پست فعال ندارد.")
            return redirect('interview_detail', pk=pk)
        
        # Check if this person is already being evaluated
        existing = InterviewEvaluation.objects.filter(
            participant__interview=interview,
            evaluated_person=evaluated_person
        ).first()
        
        if existing:
            messages.warning(request, "این فرد قبلاً به لیست ارزیابی‌شوندگان اضافه شده است.")
        else:
            # Create empty evaluations for each participant
            for participant in interview.participants.all():
                InterviewEvaluation.objects.create(
                    participant=participant,
                    evaluated_person=evaluated_person,
                    evaluated_post=evaluated_post,
                    competency=None,  # Will be set during evaluation
                    competency_level=None
                )
            messages.success(request, f"{evaluated_person} به لیست ارزیابی‌شوندگان اضافه شد.")
        
        return redirect('interview_detail', pk=pk)


class EvaluatePersonView(DetailView):
    """نمایش صفحه ارزیابی برای یک فرد خاص"""
    model = Interview
    template_name = 'interviews/evaluate_person.html'
    context_object_name = 'interview'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        interview = self.object
        evaluated_person_id = self.kwargs.get('person_id')
        
        evaluated_person = get_object_or_404(Person, pk=evaluated_person_id)
        evaluated_post = evaluated_person.current_post
        
        if evaluated_post and evaluated_post.post_level:
            from apps.assessments.models import PostCompetency
            competency_matrix = PostCompetency.objects.filter(
                post_level=evaluated_post.post_level,
                is_active=True
            ).select_related('competency', 'level').prefetch_related('likert_scales')
        else:
            competency_matrix = None
        
        # Get all participants and their evaluations for this person
        participants_data = []
        for participant in interview.participants.all():
            evaluations = InterviewEvaluation.objects.filter(
                participant=participant,
                evaluated_person=evaluated_person
            ).select_related('competency', 'competency_level')
            
            # Create a dict keyed by competency_id for easy lookup in template
            evaluations_dict = {}
            for e in evaluations:
                if e.competency_id:
                    evaluations_dict[str(e.competency_id)] = e
            
            participants_data.append({
                'participant': participant,
                'evaluations': evaluations,
                'evaluations_dict': evaluations_dict,
                'is_completed': all(e.score for e in evaluations if e.competency)
            })
        
        context['evaluated_person'] = evaluated_person
        context['evaluated_post'] = evaluated_post
        context['competency_matrix'] = competency_matrix
        context['participants_data'] = participants_data
        context = TemplateLayout.init(self, context)
        return context


class SaveEvaluationView(View):
    """ذخیره نمره و توضیحات برای یک شایستگی"""
    def post(self, request, participant_pk, *args, **kwargs):
        participant = get_object_or_404(InterviewParticipant, pk=participant_pk)
        
        evaluated_person_id = request.POST.get('evaluated_person_id')
        competency_id = request.POST.get('competency_id')
        competency_level_id = request.POST.get('competency_level_id')
        score = request.POST.get('score')
        notes = request.POST.get('notes', '')
        
        # Get evaluated person's current post
        evaluated_person = get_object_or_404(Person, pk=evaluated_person_id)
        evaluated_post = evaluated_person.current_post
        
        if not evaluated_post:
            return JsonResponse({'status': 'error', 'message': 'پست فرد ارزیابی‌شونده یافت نشد'})

        if not evaluated_post.post_level_id:
            return JsonResponse({'status': 'error', 'message': 'سطح پست فرد ارزیابی‌شونده تعریف نشده است'})
        
        # Get the likert definition for this score
        selected_definition = ''
        if score and score.isdigit():
            try:
                post_competency = PostCompetency.objects.get(
                    post_level=evaluated_post.post_level,
                    competency_id=competency_id,
                    level_id=competency_level_id
                )
                likert_scale = post_competency.likert_scales.filter(score=int(score)).first()
                if likert_scale:
                    selected_definition = likert_scale.definition
            except PostCompetency.DoesNotExist:
                pass
        
        # Save or update evaluation
        evaluation, created = InterviewEvaluation.objects.update_or_create(
            participant=participant,
            evaluated_person=evaluated_person,
            competency_id=competency_id,
            competency_level_id=competency_level_id,
            defaults={
                'evaluated_post': evaluated_post,
                'score': int(score) if score and score.isdigit() else None,
                'notes': notes,
                'selected_definition': selected_definition
            }
        )
        
        # Update participant status
        participant.status = 'in_progress'
        participant.save()
        
        return JsonResponse({
            'status': 'success',
            'message': 'ارزیابی با موفقیت ذخیره شد',
            'evaluation_id': str(evaluation.id)
        })


class CompleteParticipantView(View):
    """تکمیل ارزیابی یک شرکت‌کننده"""
    def post(self, request, participant_pk, *args, **kwargs):
        participant = get_object_or_404(InterviewParticipant, pk=participant_pk)
        participant.status = 'completed'
        participant.save()
        
        # Update interview status
        participant.interview.update_status()
        
        messages.success(request, "ارزیابی این فرد با موفقیت تکمیل شد.")
        return redirect('interview_detail', pk=participant.interview.id)


# ==========================================
# AJAX Helpers
# ==========================================

class GetPersonPostsView(View):
    """دریافت لیست پست‌های یک فرد (برای AJAX)"""
    def get(self, request, *args, **kwargs):
        person_id = request.GET.get('person_id')
        if person_id:
            posts = OrganizationalPost.objects.filter(
                person_id=person_id
            ).values('id', 'title', 'competency_level__name')
            return JsonResponse({'posts': list(posts)})
        return JsonResponse({'posts': []})


class GetCompetencyMatrixView(View):
    """دریافت ماتریس شایستگی یک پست (برای AJAX)"""
    def get(self, request, *args, **kwargs):
        post_id = request.GET.get('post_id')
        if not post_id:
            return JsonResponse({'competencies': []})
        
        try:
            post = OrganizationalPost.objects.get(pk=post_id)
            post_level = post.competency_level
            if not post_level:
                return JsonResponse({'competencies': [], 'message': 'سطح شایستگی تعریف نشده'})
            
            competencies = PostCompetency.objects.filter(
                level=post_level,
                is_active=True
            ).select_related('competency', 'level').prefetch_related('likert_scales')
            
            data = []
            for pc in competencies:
                competency_data = {
                    'id': str(pc.competency.id),
                    'name': pc.competency.name,
                    'level_id': str(pc.level.id),
                    'level_name': pc.level.name,
                    'likert_scales': [
                        {'score': ls.score, 'definition': ls.definition}
                        for ls in pc.likert_scales.all()
                    ]
                }
                data.append(competency_data)
            
            return JsonResponse({'competencies': data})
        except OrganizationalPost.DoesNotExist:
            return JsonResponse({'competencies': [], 'message': 'پست یافت نشد'})
        

class GetEvaluationSummaryView(View):
    """دریافت خلاصه ارزیابی یک فرد"""
    def get(self, request, participant_pk, evaluated_person_pk, *args, **kwargs):
        participant = get_object_or_404(InterviewParticipant, pk=participant_pk)
        
        evaluations = InterviewEvaluation.objects.filter(
            participant=participant,
            evaluated_person_id=evaluated_person_pk
        ).select_related('competency', 'competency_level')
        
        data = []
        total_score = 0
        count = 0
        
        for eval in evaluations:
            if eval.score:
                total_score += eval.score
                count += 1
            data.append({
                'competency': eval.competency.name,
                'score': eval.score,
                'notes': eval.notes
            })
        
        average = round(total_score / count, 2) if count > 0 else 0
        
        return JsonResponse({
            'evaluations': data,
            'average': average,
            'count': count
        })

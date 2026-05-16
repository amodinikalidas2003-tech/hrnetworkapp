from django.views.generic import TemplateView
from web_project import TemplateLayout
from apps.organization.models import Department, Person, OrganizationalPost
from apps.assessments.models import AssessmentScore

class DashboardView(TemplateView):
    template_name = 'hr_dashboard/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Gathering high-level stats
        context['total_departments'] = Department.objects.count()
        context['total_employees'] = Person.objects.count()
        context['total_posts'] = OrganizationalPost.objects.count()
        context['total_assessments'] = AssessmentScore.objects.count()
        
        TemplateLayout.init(self, context)
        return context

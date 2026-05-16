from django.views.generic import TemplateView, ListView
from web_project import TemplateLayout
from .models import FormSchema


"""
This file is a view controller for multiple pages as a module.
Here you can override the page view layout.
Refer to form/urls.py file for more pages.
"""


class FormsView(TemplateView):
    # Predefined function
    def get_context_data(self, **kwargs):
        # A function to init the global layout. It is defined in web_project/__init__.py file
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        return context

class FormListView(ListView):
    model = FormSchema
    template_name = 'forms/form_list.html'
    context_object_name = 'forms'

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        return context

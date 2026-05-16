from django.conf import settings

def my_setting(request):
    return {'MY_SETTING': settings}

def language_code(request):
    return {"LANGUAGE_CODE": request.LANGUAGE_CODE}

def get_cookie(request):
    return {"COOKIES": request.COOKIES}

# Add the 'ENVIRONMENT' setting to the template context
def environment(request):
    return {'ENVIRONMENT': settings.ENVIRONMENT}

# Add layout path to template context
def layout_path(request):
    template_config = getattr(settings, 'TEMPLATE_CONFIG', {})
    layout = template_config.get('layout', 'vertical')
    return {'layout_path': f'layout/layout_{layout}.html'}

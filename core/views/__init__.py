from django.shortcuts import redirect
from .auth_views import *
from .job_views import *
from .resume_views import *
from .admin_views import *
from .builder_views import *
from .event_views import *

def home(request):
    return landing_page(request)

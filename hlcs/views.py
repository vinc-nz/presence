from django.shortcuts import render
from django.conf import settings
import re


"""
Renders an HTML homepage
"""
def homepage(request):
    if request.user.is_authenticated():
        options = 'disabled="disabled"' if _disable_internal_button(request) else '' 
        return render(request, 'panel.html', {'options' : options})
    else:
        return render(request, 'index.html')
    
    
def _disable_internal_button(request):
    gates = getattr(settings, 'GATES', {})
    internal = gates['internal']
    address = str(request.META.get('HTTP_X_FORWARDED_FOR'))
    pattern = getattr(settings, 'IP_PATTERN', '10.87.1.\d+')
    return not request.user.is_staff or internal.is_open() or not re.match(pattern, address)
    

def about(request):
    return render(request, 'about.html')

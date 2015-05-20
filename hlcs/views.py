from django.shortcuts import render
from django.conf import settings

### HTML PAGES ###

"""
Renders an HTML homepage
"""
def homepage(request):
    if request.user.is_authenticated():
        #gates = getattr(settings, 'GATES', {})
        options = {} if request.user.is_staff else 'disabled="disabled"'
        return render(request, 'panel.html', {'options' : options})
    else:
        return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

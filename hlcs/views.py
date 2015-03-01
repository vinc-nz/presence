from django.shortcuts import render
from django.conf import settings

### HTML PAGES ###

"""
Renders an HTML homepage
"""
def homepage(request):
    if request.user.is_authenticated():
        gates = getattr(settings, 'GATES', {})
        return render(request, 'panel.html', gates)
    else:
        return render(request, 'index.html')

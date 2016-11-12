from django.shortcuts import render


# TODO these views should be migrated to a separate HTML5/mobile application

def homepage(request):
    if request.user.is_authenticated():
        options = 'disabled="disabled"' if _disable_internal_button(request) else ''
        return render(request, 'panel.html', {'options' : options})
    else:
        return render(request, 'index.html')


def _disable_internal_button(request):
    # broken
    # gates = getattr(settings, 'GATES', {})
    # internal = gates['internal']
    # address = str(request.META.get('HTTP_X_FORWARDED_FOR'))
    # pattern = getattr(settings, 'IP_PATTERN', '10.87.1.\d+')
    # return not request.user.is_staff or internal.is_open() or not re.match(pattern, address)
    return True


def about(request):
    return render(request, 'about.html')

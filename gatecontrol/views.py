import json

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse, Http404, HttpResponseForbidden, \
    HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from models import AccessRequest


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
    
### JSON API ###
    
def get_all_states(request):
    gates = getattr(settings, 'GATES', {})
    response = []
    for g in gates.keys():
        response.append({g : gates[g].get_state()})
    return render_json(response)

@csrf_exempt
def gatecontrol(request, gate_name):
    gates = getattr(settings, 'GATES')
    if gates is None or not gates.has_key(gate_name):
        raise Http404
    gate = gates[gate_name]
    if request.method == 'GET':
        return get_state(gate, request.GET.get('req_id', None))
    elif request.method == 'POST':
        return open_gate(request.user, gate)

@login_required
def show_requests(request):
    try:
        limit = int(request.GET.get('limit', '10'))
    except ValueError:
        return HttpResponseBadRequest()
    access_requests = AccessRequest.objects.get_last_accesses(limit)
    response = []
    for r in access_requests:
        response.append({ 'time' : r.req_time.strftime('%Y-%m-%dT%H:%M:%S'), 'user' : r.user.username})
    return render_json(response)

### UTILITY METHODS ###

def render_json(response):
    return HttpResponse(json.dumps(response), content_type='application/json')


def open_gate(user, gate):
    if not user.is_authenticated():
        return HttpResponseForbidden()
    r = AccessRequest.objects.get_pending_request()
    if r is None:
        r = AccessRequest.objects.create(user)
    gate.open_gate(r)
    response = { 'req_id' : r.id }
    return render_json(response)
  
def get_state(gate, access_request_id):
    if access_request_id is not None:
        try:
            req_id = int(access_request_id)
        except ValueError:
            return HttpResponseBadRequest()
        r = get_object_or_404(AccessRequest, pk=req_id)
    else:
        r = None
    state = gate.get_state(r)
    if r is not None:
        state['pending'] = r.is_pending()
    return render_json(state)


    
    
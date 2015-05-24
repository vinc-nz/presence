
from django.conf import settings
from django.http.response import  Http404, HttpResponseForbidden, \
    HttpResponseBadRequest, JsonResponse
from django.shortcuts import  get_object_or_404
from rest_framework.decorators import api_view

from gatecontrol.models import AccessRequest


### JSON API ###
def get_all_states(request):
    gates = getattr(settings, 'GATES', {})
    response = []
    for g in gates.keys():
        response.append({g : gates[g].get_state()})
    return render_json(response)

@api_view(['GET', 'POST'])
def gatecontrol(request, gate_name):
    gates = getattr(settings, 'GATES')
    if gates is None or gate_name not in gates:
        raise Http404
    gate = gates[gate_name]
    if request.method == 'GET':
        return get_state(gate, request.GET.get('req_id', None))
    elif request.method == 'POST':
        return open_gate(request.user, gate)

@api_view(['GET'])
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
    return JsonResponse(response, safe=False)


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
    return render_json(state)


    
    
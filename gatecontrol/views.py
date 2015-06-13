
from django.conf import settings
from django.http.response import  Http404, HttpResponseForbidden, \
    HttpResponseBadRequest, JsonResponse
from django.shortcuts import  get_object_or_404
from rest_framework.decorators import api_view

from gatecontrol.models import AccessRequest

gates = getattr(settings, 'GATES', {})


### JSON API ###
def get_all_states(request):
    response = []
    for g in gates.keys():
        response.append({g : gates[g].get_state()})
    return JsonResponse(response, safe=False)

@api_view(['GET', 'POST'])
def gatecontrol(request, gate_name):
    if gates is None or gate_name not in gates:
        raise Http404
    gate = gates[gate_name]
    if request.method == 'GET':
        return JsonResponse(gate.read_state())
    elif request.method == 'POST':
        r = AccessRequest.objects.get_or_create(request.user,  request.META.get('HTTP_X_FORWARDED_FOR'), gate_name)
        return JsonResponse({ 'req_id' : r.id })

@api_view(['GET'])
def show_requests(request, gate_name):
    try:
        limit = int(request.GET.get('limit', '10'))
    except ValueError:
        return HttpResponseBadRequest()
    access_requests = AccessRequest.objects.get_last_accesses(gate_name, limit)
    response = []
    for r in access_requests:
        response.append({ 'time' : r.req_time.strftime('%Y-%m-%dT%H:%M:%S'), 'user' : r.user.username})
    return JsonResponse(response, safe=False)

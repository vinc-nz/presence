
from django.conf import settings
from django.http.response import  Http404, HttpResponseForbidden, \
    HttpResponseBadRequest, JsonResponse
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, \
    permission_classes
from rest_framework.permissions import IsAuthenticated

from gatecontrol.models import AccessRequest


gates = getattr(settings, 'GATES', {})


ip_address = lambda request : request.META.get('HTTP_X_FORWARDED_FOR')or request.META.get('REMOTE_ADDR')

@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def gatecontrol(request, gate_name):
    capabilities = _user_capabilities(request)
    if gate_name not in capabilities:
        raise Http404
    if not capabilities[gate_name]:
        return HttpResponseForbidden()
    r = AccessRequest.objects.get_or_create(request.user,  ip_address(request), gate_name)
    return JsonResponse({ 'req_state' : r.req_state })


@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def show_requests(request, gate_name):
    try:
        limit = int(request.GET.get('limit', '10'))
    except ValueError:
        return HttpResponseBadRequest()
    access_requests = AccessRequest.objects.get_last_accesses(gate_name, limit)
    to_json = lambda r : { 'time' : r.req_time.strftime('%Y-%m-%dT%H:%M:%S'), 'user' : r.user.username}
    return JsonResponse(list(map(to_json, access_requests)), safe=False)


def _user_capabilities(request):
    return { name: gate.can_open(user=request.user, ip_address=ip_address(request))[0] for name, gate in gates.items() }

@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def show_user_capabilities(request):
    return JsonResponse(_user_capabilities(request))

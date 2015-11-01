
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import jwt

from gatecontrol.models import Gate


JWT_SECRET = getattr(settings, 'JWT_SECRET', 'secret')


class ApiView:
    
    def __init__(self, ip_address):
        self.user = None
        self.ip_address = ip_address
        
    @staticmethod
    def _create_token(username):
        return jwt.encode({'username':username}, JWT_SECRET, algorithm='HS256')
    
    def authenticate(self, token):
        token_data = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        if 'username' in token_data:
            try:
                self.user = User.objects.get(username=token_data['username'])
                return 'success'
            except User.DoesNotExist:
                raise Exception('User does not exists')
        raise Exception('not a valid token')

    def _serialize_gate(self, gate):
        gate_controller = gate.controller()
        return {'id': gate.id, 'name': gate.name, 'state': gate_controller.get_state(), 'managed': gate_controller.is_managed_by_user(self.user, self.ip_address)}
    
    
    def list_gates(self):
        return list(map(self._serialize_gate, Gate.objects.all()))
    
    def open(self, gate_id):
        return Gate.objects.get(id=gate_id).request_opening(self.user, self.ip_address)
        


@login_required
def obtain_auth_token(request):
    return ApiView._create_token(request.user.username)



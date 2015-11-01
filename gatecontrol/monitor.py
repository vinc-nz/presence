from gatecontrol.models import Gate


class StateMonitor:
    
    clients = []
    
    def push_to_all(self):
        for client in StateMonitor.clients:
            client.push_info()

    def __init__(self):
        self.current = self.read_all_states()
        
    def read_all_states(self):
        try:
            return [g.controller().get_state() for g in Gate.objects.all()]
        except Exception as e:
            #TODO loggare e interrompere il check
            return None


    def notify_changes(self):
        new_states = self.read_all_states()
        if self.current != new_states:
            self.current = new_states
            self.push_to_all()
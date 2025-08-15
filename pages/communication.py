
from opcua import Client
from opcua.ua import NodeId

class OPCUAClientManager:
    def __init__(self):
        self.client = None
        self.connected = False
        self.subscriptions = {}
        self.nodes = {}
        
    def connect(self, endpoint, username=None, password=None, security_policy=None):
        # connect to the server
        try:
            self.client = Client(endpoint)
            
            if security_policy:
                self.client.set_security(security_policy)
                
            if username and password:
                self.client.set_user(username)
                self.client.set_password(password)
                
            self.client.connect()
            self.connected = True
            return True, "Connection successful"
            
        except Exception as e:
            self.connected = False
            return False, f"Connection failed: {str(e)}"
            
    def disconnect(self):
        if self.client:
            try:
                # Clean up subscriptions first
                for handle in list(self.subscriptions.keys()):
                    self.unsubscribe(handle)
                self.client.disconnect()
            finally:
                self.connected = False
                self.subscriptions = {}
                self.nodes = {}
                
    def validate_connection(self):
        """Check if connection is still active"""
        if not self.connected:
            return False
        try:
            status_node = self.client.get_node(ua.ObjectIds.Server_ServerStatus)
            status = status_node.get_value()
            return status.State == ua.ServerState.Running
        except:
            self.connected = False
            return False
    
    def subscribe_to_node(self, node_id, callback=None, publishing_interval=500):
        if not self.connected:
            return False, "Not connected to server"
            
        try:
            node = self.client.get_node(node_id)
            subscription = self.client.create_subscription(publishing_interval, callback)
            handle = subscription.subscribe_data_change(node)
            
            self.subscriptions[handle] = {
                'node_id': node_id,
                'subscription': subscription,
                'node': node
            }
            return True, "Subscription successful"
        except Exception as e:
            return False, f"Subscription failed: {str(e)}"
            
    def unsubscribe(self, handle):
        if handle in self.subscriptions:
            try:
                sub = self.subscriptions[handle]['subscription']
                sub.unsubscribe(handle)
                sub.delete()
                del self.subscriptions[handle]
                return True, "Unsubscribed successfully"
            except Exception as e:
                return False, str(e)
        return False, "Subscription handle not found"
    
    def read_node_value(self, node_id):
        if not self.connected:
            return None, "Not connected to server"
        try:
            node = self.client.get_node(node_id)
            return node.get_value(), None
        except Exception as e:
            return None, str(e)
            
    def write_node_value(self, node_id, value):
        if not self.connected:
            return False, "Not connected to server"
        try:
            node = self.client.get_node(node_id)
            node.set_value(value)
            return True, "Write successful"
        except Exception as e:
            return False, str(e)
    
    def cache_node(self, node_id, alias=None):
        if not self.connected:
            return False, "Not connected to server"
        try:
            node = self.client.get_node(node_id)
            key = alias or str(node_id)
            self.nodes[key] = node
            return True, "Node cached successfully"
        except Exception as e:
            return False, str(e)
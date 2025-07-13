import netifaces
import subprocess

CONNECTIVITY_DUALSTACK = 0
CONNECTIVITY_SINGLESTACK = 1
CONNECTIVITY_NONE = 2

class Connectivity:
    def ipv4_gateway(self):
        try:
            return netifaces.gateways().get("default")[netifaces.AF_INET][0]
        except KeyError:
            return None
    
    def ipv6_gateway(self):
        try:
            return netifaces.gateways().get("default")[netifaces.AF_INET6][0]
        except KeyError:
            return None
    
    def ipv4_gateway_is_reachable(self):
        gateway = self.ipv4_gateway()
        if gateway is None:
            return False
        
        ping = subprocess.run(["ping", "-c", "1", "-W", "1", gateway], capture_output=True)
        return ping.returncode == 0

    def ipv6_gateway_is_reachable(self):
        gateway = self.ipv6_gateway()
        if gateway is None:
            return False
        
        ping = subprocess.run(["ping6", "-c", "1", "-W", "1", gateway], capture_output=True)
        return ping.returncode == 0
    
    def check(self):
        ipv4_connected = self.ipv4_gateway_is_reachable()
        ipv6_connected = self.ipv6_gateway_is_reachable()
        
        if ipv4_connected and ipv6_connected:
            return CONNECTIVITY_DUALSTACK
        elif ipv4_connected or ipv6_connected:
            return CONNECTIVITY_SINGLESTACK
        else:
            return CONNECTIVITY_NONE

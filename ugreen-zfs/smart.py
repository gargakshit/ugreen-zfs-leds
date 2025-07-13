import json
import subprocess

class Smart:
    def __init__(self, disk_device, smartctl = "smartctl") -> None:
        self.disk_device = disk_device
        self.smartctl = smartctl
    
    def get_smart_info(self):
        smartctl = subprocess.run([self.smartctl, "-a", self.disk_device, "--json"], capture_output=True)
        return json.loads(smartctl.stdout)

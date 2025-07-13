import json
import subprocess

SMART_STATUS_PASSING = 0
SMART_STATUS_FAILING = 1
SMART_STATUS_UNAVAILABLE = 2

class SMART:
    def __init__(self, disk_device, smartctl = "smartctl") -> None:
        self.disk_device = disk_device
        self.smartctl = smartctl
    
    def status(self):
        smartctl = subprocess.run([self.smartctl, "-H", self.disk_device, "--json"], capture_output=True)
        output = json.loads(smartctl.stdout)
        
        if output["smartctl"]["exit_status"] != 0:
            return SMART_STATUS_UNAVAILABLE
        
        passed = output["smart_status"]["passed"]
        return SMART_STATUS_PASSING if passed else SMART_STATUS_FAILING


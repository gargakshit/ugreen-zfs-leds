import subprocess

ZPOOL_STATE_ONLINE = "ONLINE"
ZPOOL_STATE_DEGRADED = "DEGRADED"
ZPOOL_STATE_FAULTED = "FAULTED"
ZPOOL_STATE_OFFLINE = "OFFLINE"
ZPOOL_STATE_OTHER = "OTHER"

class ZPool:
    def __init__(self, zpool_name, zpool_command = "zpool"):
        self.zpool_name = zpool_name
        self.zpool_command = zpool_command
    
    def status(self):
        zpool_status = subprocess.run([self.zpool_command, "status", self.zpool_name], capture_output=True)
        output = zpool_status.stdout.decode("utf-8")
        
        for line in output.split("\n"):
            line = line.strip()

            if line.startswith("state:"):
                state = line.split()[1].strip()
                if state == "ONLINE":
                    return ZPOOL_STATE_ONLINE
                elif state == "DEGRADED":
                    return ZPOOL_STATE_DEGRADED
                elif state == "FAULTED":
                    return ZPOOL_STATE_FAULTED
                elif state == "OFFLINE":
                    return ZPOOL_STATE_OFFLINE
                else:
                    return ZPOOL_STATE_OTHER
        
        return ZPOOL_STATE_OTHER

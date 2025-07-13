import subprocess

LED_DISK1 = "disk1"
LED_DISK2 = "disk2"
LED_DISK3 = "disk3"
LED_DISK4 = "disk4"
LED_NETDEV = "netdev"
LED_POWER = "power"

class RGB:
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b
    
    def cli_args(self):
        return f"-color {self.r} {self.g} {self.b}"

class UgreenLed:
    def __init__(self, led_name, cli_path = "ugreen_leds_cli"):
        self.led_name = led_name
    
    def set_color(self, color):
        subprocess.run([self.cli_path, self.led_name, color.cli_args()])
    
    def turn_on_solid(self):
        subprocess.run([self.cli_path, self.led_name, "-on"])
    
    def turn_off(self):
        subprocess.run([self.cli_path, self.led_name, "-off"])
    
    def turn_on_blinking(self, on_interval, off_interval):
        subprocess.run([self.cli_path, self.led_name, "-blink", on_interval, off_interval])
    
    def turn_on_breathing(self, on_interval, off_interval):
        subprocess.run([self.cli_path, self.led_name, "-breath", on_interval, off_interval])

import time

from .led import *
from .smart import *

DISK_LED_MAPPING = {
      "/dev/disk/by-path/pci-0000:01:00.0-ata-1": LED_DISK1,
      "/dev/disk/by-path/pci-0000:01:00.0-ata-2": LED_DISK2,
      "/dev/disk/by-path/pci-0000:01:00.0-ata-3": LED_DISK3,
      "/dev/disk/by-path/pci-0000:01:00.0-ata-4": LED_DISK4,
}

def update_smart_status():
      for disk, led_name in DISK_LED_MAPPING.items():
            led = UgreenLed(led_name)
            smart_status = SMART(disk).status()

            if smart_status == SMART_STATUS_PASSING:
                  led.set_color(RGB(0, 255, 0))
                  led.turn_on_solid()
            elif smart_status == SMART_STATUS_FAILING:
                  led.set_color(RGB(255, 140, 0))
                  led.turn_on_breathing(500, 500)
            else:
                  led.set_color(RGB(255, 0, 0))
                  led.turn_on_solid()

def update_in_loop():
      while True:
            update_smart_status()
            time.sleep(2)

if __name__ == '__main__':
      update_in_loop()

import os
import time

from .connectivity import *
from .led import *
from .smart import *
from .zpool import *

DISK_LED_MAPPING = {
      "/dev/disk/by-path/pci-0000:01:00.0-ata-1": LED_DISK1,
      "/dev/disk/by-path/pci-0000:01:00.0-ata-2": LED_DISK2,
      "/dev/disk/by-path/pci-0000:01:00.0-ata-3": LED_DISK3,
      "/dev/disk/by-path/pci-0000:01:00.0-ata-4": LED_DISK4,
}

ZPOOL_NAME = os.environ.get("LED_ZPOOL_NAME", "storage")
SINGLESTACK = os.environ.get("LED_SINGLESTACK", "false").lower() == "true"
POLL_INTERVAL = os.environ.get("LED_POLL_INTERVAL", "2")

def update_smart_status():
      for disk, led_name in DISK_LED_MAPPING.items():
            led = UgreenLed(led_name)
            smart_status = SMART(disk).status()

            if smart_status == SMART_STATUS_PASSING:
                  led.set_color(RGB(0, 255, 0))
                  led.turn_on_solid()
            elif smart_status == SMART_STATUS_FAILING:
                  print(f"SMART status for {disk} is failing")
                  led.set_color(RGB(255, 121, 0))
                  led.turn_on_breathing(500, 500)
            else:
                  print(f"SMART status for {disk} is unavailable")
                  led.set_color(RGB(255, 0, 0))
                  led.turn_on_solid()

def update_zpool_status():
      led = UgreenLed(LED_POWER)
      zpool = ZPool(ZPOOL_NAME)

      state = zpool.status()

      if state == ZPOOL_STATE_ONLINE:
            led.set_color(RGB(0, 255, 0))
            led.turn_on_solid()
      elif state == ZPOOL_STATE_DEGRADED:
            led.set_color(RGB(255, 121, 0))
            led.turn_on_breathing(500, 500)
            print(f"ZPool {ZPOOL_NAME} is degraded")
      elif state == ZPOOL_STATE_FAULTED:
            led.set_color(RGB(255, 0, 0))
            led.turn_on_blinking(500, 500)
            print(f"ZPool {ZPOOL_NAME} is faulted")
      else:
            led.set_color(RGB(255, 0, 0))
            led.turn_on_solid()
            print(f"ZPool {ZPOOL_NAME} is {state}")

def update_network_status():
      led = UgreenLed(LED_NETDEV)
      connectivity = Connectivity().check()
      
      if connectivity == CONNECTIVITY_DUALSTACK:
            led.set_color(RGB(0, 255, 0))
            led.turn_on_solid()
      elif connectivity == CONNECTIVITY_SINGLESTACK:
            if SINGLESTACK:
                  led.set_color(RGB(0, 255, 0))
                  led.turn_on_solid()
            else:
                  led.set_color(RGB(255, 121, 0))
                  led.turn_on_breathing(500, 500)
                  print("Network is singlestack")
      else:
            led.set_color(RGB(255, 0, 0))
            led.turn_on_solid()
            print("Network is down")

def update_in_loop():
      while True:
            update_smart_status()
            update_zpool_status()
            update_network_status()
            time.sleep(int(POLL_INTERVAL))

def print_config():
      print(f"LED_POLL_INTERVAL={POLL_INTERVAL}")
      print(f"LED_ZPOOL_NAME={ZPOOL_NAME}")
      print(f"LED_SINGLESTACK={SINGLESTACK}")

      print("Monitored disks:")
      for disk in DISK_LED_MAPPING.keys():
            print(f"  {disk}")

if __name__ == '__main__':
      print_config()
      update_in_loop()

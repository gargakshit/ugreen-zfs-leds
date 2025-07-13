from .smart import Smart

if __name__ == '__main__':
      print(Smart("/dev/sda").get_smart_info())

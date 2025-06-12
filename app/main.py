from app import baresip_monitor, web_gui

if __name__ == "__main__":
    baresip_monitor.start_baresip_monitor()
    web_gui.start_web_gui()

import pjsua as pj
import threading
import time
from app.config_manager import load_config
from app.recorder import record_message
from app.notifier import send_to_discord, send_email

class MyCallCallback(pj.CallCallback):
    def __init__(self, call):
        pj.CallCallback.__init__(self, call)
        self.config = load_config()

    def on_state(self):
        print("Call state:", self.call.info().state_text)
        if self.call.info().state == pj.CallState.CONFIRMED:
            print("Call answered.")
            filename = f"voicemail_{int(time.time())}.wav"
            file_path = record_message(10, filename)
            send_to_discord(file_path)
            send_email(file_path)
            self.call.hangup()

def sip_worker():
    config = load_config()
    lib = pj.Lib()
    lib.init()
    transport = lib.create_transport(pj.TransportType.UDP, pj.TransportConfig(5060))
    lib.start()
    acc = lib.create_account(pj.AccountConfig(config['sip_domain'], config['sip_user'], config['sip_password']))

    def on_incoming_call(account, call):
        print("Incoming call, auto answering.")
        call_cb = MyCallCallback(call)
        call.set_callback(call_cb)
        time.sleep(config['auto_answer_delay'])
        call.answer(200)

    acc.set_callback(pj.AccountCallback())
    acc.on_incoming_call = on_incoming_call

    print("SIP client running.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        lib.destroy()

threading.Thread(target=sip_worker).start()

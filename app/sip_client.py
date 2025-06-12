from pjsua2 import *
import threading
import time
from app.config_manager import load_config
from app.recorder import record_message
from app.notifier import send_to_discord, send_email

class MyAccount(Account):
    def __init__(self):
        super().__init__()
        self.config = load_config()

    def onRegState(self, prm):
        ai = self.getInfo()
        print("SIP Registration:", ai.regIsActive, ai.uri)

    def onIncomingCall(self, prm):
        print("Incoming call detected. Auto-answering after delay.")
        call = MyCall(self, prm.callId, self.config)
        threading.Thread(target=call.answer_with_recording).start()


class MyCall(Call):
    def __init__(self, account, call_id, config):
        super().__init__(account, call_id)
        self.config = config

    def answer_with_recording(self):
        # Wait for the configured delay before answering
        delay = self.config.get("auto_answer_delay", 0)
        if delay > 0:
            time.sleep(delay)

        print("Answering call.")
        prm = CallOpParam()
        prm.statusCode = 200
        self.answer(prm)

        # Wait for the call to be confirmed and then record
        try:
            while True:
                ci = self.getInfo()
                if ci.state == pj.CallState.PJSIP_INV_STATE_CONFIRMED:
                    print("Call answered. Recording message.")
                    filename = f"voicemail_{int(time.time())}.wav"
                    file_path = record_message(10, filename)
                    send_to_discord(file_path)
                    send_email(file_path)
                    self.hangup()
                    break
                elif ci.state == pj.CallState.PJSIP_INV_STATE_DISCONNECTED:
                    print("Call disconnected before answering.")
                    break
                time.sleep(0.1)
        except Exception as e:
            print("Error during call-handling:", e)
            self.hangup()

    def onCallState(self, prm):
        ci = self.getInfo()
        print("Call state:", ci.stateText)
        if ci.state == pj.CallState.PJSIP_INV_STATE_DISCONNECTED:
            print("Call disconnected.")


def sip_worker():
    config = load_config()
    ep = Endpoint()
    ep.libCreate()

    ep_cfg = EpConfig()
    ep.libInit(ep_cfg)

    # Set up SIP transport (UDP, default port 5060)
    t_cfg = TransportConfig()
    t_cfg.port = 5060
    ep.transportCreate(pjsip_transport_type_e.PJSIP_TRANSPORT_UDP, t_cfg)

    ep.libStart()
    print("PJSUA2 SIP endpoint started.")

    # Set up account configuration
    acc_cfg = AccountConfig()
    acc_cfg.idUri = f"sip:{config['sip_user']}@{config['sip_domain']}"
    acc_cfg.regConfig.registrarUri = f"sip:{config['sip_domain']}"
    cred = AuthCredInfo("digest", "*", config['sip_user'], 0, config['sip_password'])
    acc_cfg.sipConfig.authCreds.append(cred)

    acc = MyAccount()
    acc.create(acc_cfg)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Shutting down SIP client...")
    finally:
        ep.libDestroy()


# Start the SIP worker thread
threading.Thread(target=sip_worker, daemon=True).start()

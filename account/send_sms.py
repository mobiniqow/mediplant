from threading import Thread


def send_otp_message(phone, code):
    print(f"phone::{phone}=> code::{code}")
    # Thread(target=sms, args=(phone, code)).start()


def sms(_phone, _message):
    from ippanel import Client

    api_key = "zOpl9jdnKmSkYIL90GEWSYgLdfSs4S_C8WUf1XgLukE="

    sms = Client(api_key)
    pattern_values = {
        "verification-code": _message,
    }

    message_id = sms.send_pattern(
        "wjam509dz9v4tb0",  # pattern code
        "+3000505",  # originator
        _phone,  # recipient
        pattern_values,  # pattern values
    )

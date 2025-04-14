from threading import Thread
import requests

def send_otp_message(phone, code):
    print(f"phone::{phone}=> code::{code}")
    Thread(target=send_otp, args=(phone, code)).start()



def send_otp(phone, otp):
    # 2O31E ramze vorod
    # url = "https://rest.payamak-panel.com/api/SendSMS/BaseServiceNumber"
    # payload = f'username=09127253345&password=2O31E&text={otp}&to={phone}&bodyId=224836'
    # headers = {
    #     'Content-Type': 'application/x-www-form-urlencoded'
    # }
    # response = requests.request("POST", url, headers=headers, data=payload)
    # print(f'sending otp code to {phone} with status {response.status_code}')
    url = "https://api.kavenegar.com/v1/59367966624C365A7277546C44723542565670417066556C514D68644D68697764342B726E374766462B773D/verify/lookup.json"

    payload = f'token={otp}&template=login&receptor={phone}'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': 'cookiesession1=678A8C4087367227C1B693FF947D5992'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)
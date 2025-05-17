from threading import Thread
import requests

def send_otp_message(phone, code):
    print(f"phone::{phone}=> code::{code}")
    Thread(target=send_otp, args=(phone, code)).start()



def send_otp(phone, otp):
    url = "https://api.kavenegar.com/v1/646B3963434E773954774E7974397365686844776739584E704A685A6262597A5632615A574A4174626F673D/verify/lookup.json"
    payload = f'token={otp}&template=mediplant&receptor={phone}'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': 'cookiesession1=678A8C4087367227C1B693FF947D5992'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)

def state_processing(phone):
    url = "https://api.kavenegar.com/v1/646B3963434E773954774E7974397365686844776739584E704A685A6262597A5632615A574A4174626F673D/verify/lookup.json"
    payload = f'template=mediplant&receptor={phone}'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': 'cookiesession1=678A8C4087367227C1B693FF947D5992'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)

def state_sending(phone):
    url = "https://api.kavenegar.com/v1/646B3963434E773954774E7974397365686844776739584E704A685A6262597A5632615A574A4174626F673D/verify/lookup.json"
    payload = f'template=mediplant&receptor={phone}'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': 'cookiesession1=678A8C4087367227C1B693FF947D5992'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)


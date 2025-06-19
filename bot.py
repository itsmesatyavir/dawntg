import requests
import time
import json
import random
from threading import Thread
from colorama import init, Fore, Style
import logging
from datetime import datetime, timezone
import urllib3

init(autoreset=True)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

import base64

TG_BOT = base64.b64decode("Nzk2MTUzNjUwMTpBQUdkNlM0c2VCRXpDdnRZOHdPRzNROEJvTjVWX1ZlampNVQ==").decode()
TG_CHANNEL = "@dawntgbot"

API_URL_GET_POINTS = 'https://ext-api.dawninternet.com/api/atom/v1/userreferral/getpoint?appid={appid}'
API_URL_KEEP_ALIVE = 'https://ext-api.dawninternet.com/chromeapi/dawn/v1/userreward/keepalive?appid={appid}'

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(message)s', datefmt='%Y-%m-%d %H:%M:%S')


def load_accounts():
    with open('accounts.json') as f:
        accounts = json.load(f)
    for acc in accounts:
        if not all(k in acc for k in ('name', 'email', 'token')):
            raise KeyError("Account missing required fields: name, email, or token")
    return accounts


def parse_proxy_line(line):
    try:
        scheme, rest = line.split("://")
        parts = rest.split(":")
        if len(parts) == 2:
            ip, port = parts
            return {"scheme": scheme, "ip": ip, "port": port, "user": None, "pass": None}
        elif len(parts) == 4:
            ip, port, user, pwd = parts
            return {"scheme": scheme, "ip": ip, "port": port, "user": user, "pass": pwd}
    except:
        return None


def load_proxies():
    proxies = []
    try:
        with open('proxy.txt') as f:
            lines = [line.strip() for line in f if line.strip()]
            for line in lines:
                proxy = parse_proxy_line(line)
                if proxy:
                    proxies.append(proxy)
                else:
                    logging.warning(f"Invalid proxy skipped: {line}")
    except FileNotFoundError:
        logging.warning("proxy.txt not found. Running without proxy.")
    return proxies


def get_proxy_location(proxy):
    try:
        proxy_url = build_proxy_url(proxy)
        res = requests.get("http://ip-api.com/json", proxies={"http": proxy_url, "https": proxy_url}, timeout=8)
        if res.ok:
            return res.json().get('country', 'Unknown')
    except:
        pass
    return 'Unknown'


def build_proxy_url(proxy):
    scheme = proxy['scheme']
    ip = proxy['ip']
    port = proxy['port']
    if proxy['user'] and proxy['pass']:
        return f"{scheme}://{proxy['user']}:{proxy['pass']}@{ip}:{port}"
    else:
        return f"{scheme}://{ip}:{port}"


def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TG_BOT}/sendMessage"
    payload = {
        "chat_id": TG_CHANNEL,
        "text": message,
        "parse_mode": "HTML"
    }
    try:
        requests.post(url, json=payload)
    except Exception as e:
        logging.error(f"Telegram Error: {e}")


def mask_email(email):
    try:
        user, domain = email.split("@")
        return user[:4] + "****@" + domain
    except:
        return "hidden@domain.com"


def fetch_points(account, proxy):
    appid = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=16))
    headers = {
        "Authorization": f"Bearer {account['token']}",
        "Content-Type": "application/json",
    }

    proxies_dict = {}
    location = "N/A"
    ip = "No Proxy"
    if proxy:
        proxy_url = build_proxy_url(proxy)
        proxies_dict = {"http": proxy_url, "https": proxy_url}
        ip = proxy['ip']
        location = get_proxy_location(proxy)

    try:
        res = requests.get(API_URL_GET_POINTS.format(appid=appid), headers=headers,
                           proxies=proxies_dict, verify=False, timeout=15)
        if res.ok:
            data = res.json().get("data", {})
            referral_point = data.get("referralPoint", {}).get("commission", 0)
            reward = data.get("rewardPoint", {})
            reward_points = sum(
                v for k, v in reward.items() if "points" in k.lower() and isinstance(v, (int, float))
            )
            total = referral_point + reward_points
            ref_code = data.get("referralPoint", {}).get("referralCode", '-')
            username = data.get("referralPoint", {}).get("email", '-')
            timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
            message = (
                f"🔥<b>{account['name']}</b>\n"
                f"📧Email: {mask_email(account['email'])}\n"
                f"Username:✨\n"
                f"👥Referral Code: <code>{ref_code}</code>\n"
                f"🎰Total Points: <b>{int(total)}</b>\n"
                f"⏰Time: <code>{timestamp}</code>\n"
                f"🛡️Proxy - {'yes' if proxy else 'no'} - ({location})"
            )
            send_telegram_message(message)
        else:
            logging.info(f"{account['name']} | Fetch Failed - Proxy {'Enabled' if proxy else 'Disabled'} - {location} | {ip}")
    except Exception as e:
        logging.error(f"{account['name']} | Fetch Exception: {e} - Proxy {'Enabled' if proxy else 'Disabled'} - {location} | {ip}")


def keep_alive(account, proxy):
    appid = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=16))
    headers = {
        "Authorization": f"Bearer {account['token']}",
        "Content-Type": "application/json",
    }
    data = {
        "username": account['email'],
        "extensionid": "fpdkjdnhkakefebpekbdhillbhonfjjp",
        "numberoftabs": 0,
        "_v": "1.1.5"
    }

    proxies_dict = {}
    location = "N/A"
    ip = "No Proxy"
    if proxy:
        proxy_url = build_proxy_url(proxy)
        proxies_dict = {"http": proxy_url, "https": proxy_url}
        ip = proxy['ip']
        location = get_proxy_location(proxy)

    try:
        res = requests.post(API_URL_KEEP_ALIVE.format(appid=appid), headers=headers, json=data,
                            proxies=proxies_dict, verify=False, timeout=15)
        if res.ok:
            logging.info(f"{account['name']} | Keep Alive Sent - Proxy {'Enabled' if proxy else 'Disabled'} - {location} | {ip}")
        else:
            logging.info(f"{account['name']} | Keep Alive Failed - Proxy {'Enabled' if proxy else 'Disabled'} - {location} | {ip}")
    except Exception as e:
        logging.error(f"{account['name']} | Keep Alive Exception: {e} - Proxy {'Enabled' if proxy else 'Disabled'} - {location} | {ip}")


def process_account(account, proxies):
    proxy = random.choice(proxies) if proxies else None
    while True:
        fetch_points(account, proxy)
        keep_alive(account, proxy)
        time.sleep(300) #you_can_change_this_time


def main():
    print(Fore.CYAN + "+--------------------------------------------------+")
    print(Fore.CYAN + "|    The Dawn Validator Bot (Auto Ping)           |")
    print(Fore.CYAN + "|    Developed By t.me/forestarmy                 |")
    print(Fore.CYAN + "|    Sending Point Updates to t.me/dawntgbot      |")
    print(Fore.CYAN + "+--------------------------------------------------+" + Style.RESET_ALL)

    accounts = load_accounts()
    proxies = load_proxies()

    logging.info(f"Loaded {len(accounts)} Accounts | {len(proxies)} Proxies Found")

    threads = []
    for acc in accounts:
        t = Thread(target=process_account, args=(acc, proxies))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()


if __name__ == '__main__':
    main()

# 🌅 DawnTG – Dawn Validator Bot

Automated bot that fetches your Dawn Internet referral and reward points, and sends updates to a Telegram channel — with proxy support, email masking, and account manager.

> Developed by [@itsmesatyavir](https://github.com/itsmesatyavir)

---

## 🚀 Features

- ✅ Fetches total points (referral + reward)
- ✅ Sends masked email and timestamped updates to Telegram
- ✅ Works with multiple accounts
- ✅ Supports HTTP/SOCKS proxies
- ✅ Keep-alive pings sent automatically
- ✅ Simple setup via `main.py` (no manual JSON edits)
- ✅ Realtime point update via Telegram Channel 

---

## 📦 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/itsmesatyavir/dawntg
cd dawntg
```

### 2. Install Requirements

```bash
pip install -r requirements.txt
```

> Requires Python 3.7+

---

## ⚙️ Account Setup

Run the main launcher:

```bash
python main.py
```

Then choose:

```
1. Run Script 
2. Account Setup
```

### Example `accounts.json` (auto-generated)

```json
[
  {
    "name": "Account 1",
    "email": "example@gmail.com",
    "token": "YOUR_BEARER_TOKEN_HERE"
  }
]
```

---

## 🌍 Proxy Support

To use proxies, create a `proxy.txt` file:

```
http://ip:port
socks4://ip:port
socks5://ip:port:username:password
```

The bot will auto-rotate proxies and show their country (without exposing IPs).

---

## 💬 Telegram Integration

- Updates are sent to a Telegram channel (e.g.https://t.me/dawntgbot`)
---

## 🧾 File Structure

```
dawntg/
├── bot.py           # Main logic for fetching and sending points
├── main.py          # Launcher and account setup script
├── accounts.json    # Stores account email and tokens
├── proxy.txt        # Optional proxy list
├── README.md
├── LICENSE
```

---

## 📄 License

This project is licensed under the [Apache 2.0 License](LICENSE).

---

## 🙋‍♂️ Support

Questions or suggestions?  
Message [@forestarmy on Telegram](https://t.me/forestarmy)

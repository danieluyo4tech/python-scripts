import socket
import os
from datetime import datetime

def start_server(ip="127.0.0.1", port=5555):
    """
    Binds to a network interface to receive incoming log files from 
    network agents, writing them out to disk with structural timestamps.
    """
    # Initialize an IPv4 TCP stream listening socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Allow immediate re-binding to the port to avoid OS 'Address already in use' delays
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((ip, port))
    server.listen(10)
    print(f"[*] Server Listening for logs on port {port}...")

    while True:
        # Block loop and wait for incoming agent uploads
        conn, addr = server.accept()
        try:
            # Read the initial 1024-byte protocol metadata string
            header = conn.recv(1024).decode('utf-8')
            if header.startswith("FILE|"):
                # Parse the internal file name from the protocol string
                _, original_name = header.split("|")
                
                # Prepend a precise timestamp to prevent old logs from being overwritten
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                save_name = f"{timestamp}_{original_name}"
                
                print(f"[+] Receiving data stream for {save_name} from {addr}...")
                
                # Open a binary file stream to serialize the inbound network byte packets
                with open(save_name, "wb") as f:
                    while True:
                        chunk = conn.recv(4096)
                        if not chunk: 
                            break # No more data; client closed the socket stream cleanly
                        f.write(chunk)
                print(f"[!] File {save_name} saved successfully.")
        except Exception as e:
            print(f"[-] Data Transfer Error encountered: {e}")
        finally:
            # Terminate current socket stream connection to reset loop for next log file
            conn.close()

if __name__ == "__main__":
    start_server()

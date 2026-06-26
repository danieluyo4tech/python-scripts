# Import the standard network socket library
import socket

# Define the target server's IP address and communication port
# '127.0.0.1' points to the local loopback interface (your own machine)
server_ip = "127.0.0.1"
server_port = 12345

# Initialize a standard IPv4 TCP stream socket object
client = socket.socket()

print(f"[*] Attempting connection to remote listener at {server_ip}:{server_port}...")

# Establish a formal TCP connection handshake with the target backdoor server
client.connect((server_ip, server_port))

print("[+] Connected to server (type 'exit' to quit)")

# Enter the main command transmission loop
while True:
    # Prompt the operator to type a system command into the console
    command = input("Enter command: ")

    # Encode the string input into raw bytes and send it across the network socket
    client.send(command.encode())

    # Evaluate the exit condition before trying to read a server response
    if command.lower() == "exit":
        print("[*] Exit command entered. Terminating local session...")
        break
        
    # Allocate a 4096-byte data buffer to capture the incoming response stream
    # Decode the network bytes back into a readable UTF-8 string representation
    response = client.recv(4096).decode()
    
    # Render the command output returned by the remote system
    print(response)

# Gracefully tear down the local network socket interface
client.close()
print("[*] Connection closed.")

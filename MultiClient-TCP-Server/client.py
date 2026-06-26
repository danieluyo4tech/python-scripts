import socket

# Initialize a standard TCP/IP stream socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define the target server's IP address and port configuration
# 127.0.0.1 represents localhost (your local machine)
server_ip = "127.0.0.1"
server_port = 9999

print(f"[*] Attempting to connect to server at {server_ip}:{server_port}...")

# Establish a connection handshake with the remote listening server
client.connect((server_ip, server_port))
print("[+] Successfully connected to the server!")

# Initiate communication loop
while True:
    # Prompt the user for string input via console
    message = input("You: ")
    
    # Convert string data to bytes using UTF-8 encoding and transmit across the network socket
    client.send(message.encode())

    # Wait and listen for the server's reply (buffer size limited to 1024 bytes)
    # Decode the incoming byte stream back into a readable string
    response = client.recv(1024).decode()
    print("Server:", response)

    # Clean exit condition: check if the user sent the termination keyword
    if message.lower() == "bye":
        print("[*] Disconnecting from server...")
        break

# Terminate the socket connection to release system network resources
client.close()
print("[*] Connection closed.")

import socket
import threading
import time

def handle_client(client_socket):
    """
    Dedicated worker function to handle bidirectional data transmission 
    for an individual client connection inside an isolated thread.
    """
    while True:
        try:
            # Block thread and wait to receive raw bytes from the client socket
            # Decodes 1024 bytes maximum allocation of network data
            message = client_socket.recv(1024).decode()
            
            # Connection safety check: If empty data is received, the client disconnected abruptly
            if not message:
                break  

            print(f"[*] Client says: {message}")

            # Normalize text to lower-case to ensure condition parsing is case-insensitive
            msg_lower = message.lower()
            
            # Simple keyword matching engine simulating an automated chat assistant
            if "hello" in msg_lower:
                response = "Hello! How can I help you?"
            elif "how are you" in msg_lower:
                response = "I'm fine, thanks! I am your server assistant."
            elif "time" in msg_lower:
                # Dynamically retrieve and format current server system time string
                response = time.ctime()
            elif "bye" in msg_lower:
                response = "Goodbye! Have a nice day."
                # Immediately send the farewell acknowledgement back to client
                client_socket.send(response.encode())
                # Terminate the loop to trigger session cleanup
                break
            else:
                response = "Sorry, I don't understand."

            # Encode string response back to network byte format and deliver to client
            client_socket.send(response.encode())

        except ConnectionResetError:
            # Catch unexpected client connection drops (e.g., terminal closed, network failure)
            break
        except Exception as e:
            # General catch-all block to prevent thread panic/crash
            print(f"[!] Error handling client: {e}")
            break

    # Gracefully shut down current client socket session
    client_socket.close()
    print("[-] Client disconnected. Worker thread terminating.")


# Instantiate a standard socket using IPv4 addressing (AF_INET) and TCP protocol (SOCK_STREAM)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Configure local socket rules: Bind server to listen on all interfaces (0.0.0.0) at port 9999
server.bind(("0.0.0.0", 9999))

# Put the socket into listening mode. Max backlog queue limit is set to 5 incoming connections
server.listen(5)
print("[+] Server started... waiting for clients to connect on port 9999...")

# Infinite main tracking loop to continually intercept incoming network connections
while True:
    # Accept incoming network connection requests
    # Blocks code execution until a client hits the port
    client_conn, addr = server.accept()
    print(f"[+] New connection established from remote endpoint: {addr}")
    
    # Spawn a new thread specifically to handle processing tasks for this single connection
    # Spawning avoids freezing the primary loop, letting multiple clients join simultaneously
    thread = threading.Thread(target=handle_client, args=(client_conn,))
    
    # Spin up background thread worker execution
    thread.start()

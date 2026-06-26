# Multi-Client Threaded TCP Chat Assistant

A multithreaded network chat application built in native Python using the `socket` and `threading` libraries. The project implements a robust TCP Server capable of concurrently handling multiple clients, responding dynamically to user prompts like an automated chatbot.

---

## 🚀 How It Works

1.  **Multi-Threading Architecture:** The server operates on a non-blocking connection loop. Every time a new client connects, the main server loop hands off communication tasks to a unique, dedicated background thread.
2.  **State Management:** Clients can chat independently with the server without blocking or disrupting other connected users.
3.  **Command Engine:** The server evaluates inbound string queries using basic keyword patterns to provide responses (e.g., checking system time, greetings, and managing teardown states).

---

## 🛠️ Usage Instructions

No third-party dependencies are required. This toolkit uses strictly native Python libraries.

### 1. Launch the Server
Always start the listener instance first. Run the server script within your terminal:

```bash
python server.py
```

### 2. Connect a Client
Open a secondary terminal window (or multiple terminal windows to test concurrency) and run:

```bash
python client.py
```

### 3. Available Chat Commands
Type any phrase containing the following keywords to receive unique automated replies:
*   `hello` - Receive a basic server greeting.
*   `how are you` - Ask the server's current processing status.
*   `time` - Pull the server system's local time stamp.
*   `bye` - Safely terminate the local client terminal and detach cleanly from the server loop.

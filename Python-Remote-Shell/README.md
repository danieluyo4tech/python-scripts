# TCP Remote Command Executor

A minimal Python-based terminal implementation demonstrating basic Remote Command Execution (RCE) via TCP network sockets. The system consists of a server script that listens for connection inputs, executes incoming string queries within its local system shell via the `subprocess` engine, and returns the output to a connected client terminal.

---

## 🛠️ Usage Instructions

This toolkit relies exclusively on native Python libraries and requires no external third-party installations.

### 1. Launch the Remote Listener
Start the server console to open up the communication port and await incoming client interactions:

```bash
python server.py
```

### 2. Connect the Client Console
In a separate terminal window on the same host, start the client dashboard to initiate control:

```bash
python client.py
```

### 3. Executing Commands
Once connected, type any valid operating system shell command into the client prompt. The command will run directly on the host machine hosting the server script.

*   **Linux / macOS Targets:** Try `whoami`, `ls -la`, or `pwd`.
*   **Windows Targets:** Try `whoami`, `dir`, or `ipconfig`.
*   **Terminate Session:** Type `exit` to disconnect cleanly.

---

## ⚖️ Legal & Ethical Disclaimer

> **⚠️ WARNING:** This project is built strictly for **educational purposes**, security research, and authorized penetration testing within controlled isolated laboratory environments.
>
> Running a remote shell listener script leaves a computer highly vulnerable if exposed to an untrusted network. The author assumes absolutely no liability for any misuse, data loss, unexpected system exploitation, or legal consequences resulting from the distribution or manipulation of this codebase. Always secure explicit written authorization before running network testing frameworks.

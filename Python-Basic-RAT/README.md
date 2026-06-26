# Simple TCP Backdoor & Controller Framework

A minimal proof-of-concept Remote Administration Tool (RAT) architecture written in native Python using `socket` and `subprocess` engines. This repository demonstrates how a persistent TCP listener can be instantiated on a target host to receive, process, and exfiltrate terminal command structures back to a remote operational controller client.

---

## 📂 Project Architecture

The application relies on a typical client-server separation of concerns:
*   `server_backdoor.py`: Implements the listening agent designed to run silently on the target platform, executing arbitrary system shell directives.
*   `client_controller.py`: Implements the administrative dashboard utilized by the operator to dispatch tasks over an established TCP link.

---

## 🚀 Execution Instructions

This project relies purely on Python's built-in standard library. No third-party package managers are required.

### 1. Initialize the Backdoor Service
Run the listener module to stand up the port interface on the destination operating system:
```bash
python server_backdoor.py
```

### 2. Establish Control
In an alternate command console or over an authorized local network pathway, attach using the controller script:
```bash
python client_controller.py
```

### 3. Usage Syntax
Once a connection handshake concludes successfully, type system-native commands into the prompt:
*   **Unix-like systems (Linux/macOS):** `ls -la`, `id`, `uname -a`
*   **Windows systems:** `dir`, `whoami`, `ipconfig`
*   **Termination:** Type `exit` into the control prompt to close connection streams on both devices safely.

---

## ⚖️ Legal & Ethical Disclaimer

> **⚠️ WARNING:** This software framework is compiled and distributed solely for **educational purposes**, authorized penetration testing exercises, and cybersecurity academic analysis within isolated, private lab sandbox networks.
>
> Running an unencrypted remote execution mechanism leaves a system exposed to external compromise if configured improperly across open networks. The author assumes zero liability for any data loss, system exploitation, operational damage, or punitive legal outcomes arising from the implementation or modification of this source code repository. Always acquire strict, formal written consent prior to provisioning security tooling.

# TLS Network Stream Inspection Framework

A programmatic proof-of-concept network analysis framework written in Python using `scapy` and `socket`. The project demonstrates the automation of on-the-fly TLS stream tracking via automated environment hooking (`SSLKEYLOGFILE`) and programmatic PCAP extraction to a remote file-receiver server.

---

## ⚙️ How It Works

1. **Environmental Injection:** The execution script declares an application-wide `SSLKEYLOGFILE` environment variable. This instructs modern browsers (like Chrome or Firefox) to dump their ephemeral TLS master secrets to a specified local directory.
2. **TCP Reassembly:** Scapy hooks into network interfaces, applying a `TCPSession` processor to filter and reassemble fragmented raw frames passing across port 443.
3. **Automated Exfiltration:** Local buffers are maintained and converted into standardized `.pcap` and log artifacts before being exfiltrated to a central telemetry server over raw TCP socket pipelines.

---

## 🛠️ Usage Instructions

### 1. External Prerequisites
This library relies on Python's advanced packet manipulation suite, `scapy`. Install it via your terminal:

```bash
pip install scapy
```

### 2. Run the Central Collector
Launch the receiver script on your logging engine system first to establish an open port:
```bash
python receiver.py
```

### 3. Run the Monitoring Agent
Execute the agent script on the client target system under an administrative context to allow raw socket packet capture features:
```bash
python agent.py
```

---

## ⚖️ Legal & Ethical Disclaimer

> **⚠️ WARNING:** This toolkit is designed strictly for **educational research**, authorized enterprise network troubleshooting, and local lab simulation environments.
>
> Intercepting, capturing, or logging network data without explicit authorization from the device owner and network administrator is illegal under major data privacy and cyber crime regulations worldwide (such as the US CFAA and European GDPR laws). The developer assumes no responsibility or liability for unauthorized modification, misuse, or deployment of this software repository.

# XO-Shield // OrbitGuard

> **A Real-time WireGuard VPN Security Engine & Dashboard**
> *Live Demo: https://vpn.xoxoent.space*

![XO-Shield Dashboard](XO_Shield.png)

## 🛡️ Overview
**XO-Shield** is a self-hosted VPN infrastructure and security monitoring system designed to solve the "black box" problem of standard VPNs. Instead of just connecting blindly, XO-Shield provides a **real-time "Security Score"** (0-100) based on live telemetry from the server's kernel.

It runs on a **Ubuntu 22.04 VPS** and uses a custom Python engine to audit the connection status, firewall integrity, and network latency every 10 seconds.

## ⚡ Key Features
* **Real-time Security Scoring:** A custom algorithm calculates a trust score (0-100) based on critical security vectors.
* **Visual Telemetry:** A "Deep Space" aesthetic dashboard powered by **FastAPI** and **Tailwind CSS**.
* **Non-Blocking Architecture:** Uses Python `threading` to perform heavy network probes (Ping, WireGuard Handshakes) in the background without slowing down the API.
* **Secure Networking:** Implements **WireGuard** with Kernel-level NAT masquerading (IP Forwarding).
* **Production Hardening:**
    * Deployed behind an **Nginx Reverse Proxy** with SSL (Let's Encrypt).
    * Protected by a whitelist-only **UFW Firewall**.
    * Systemd automated service management.

## 🛠️ Tech Stack
* **Core:** Python 3.10+, FastAPI
* **Networking:** WireGuard, Netlink (iproute2), UFW, iptables
* **Frontend:** HTML5, Tailwind CSS via CDN, JavaScript (Fetch API)
* **Infrastructure:** Ubuntu 22.04 LTS (Contabo VPS), Nginx, Systemd

## 🏗️ Architecture

```mermaid
graph TD
    User[User Device] -->|HTTPS/443| Nginx[Nginx Reverse Proxy]
    User -->|UDP/51820| WG[WireGuard Interface wg0]
    
    subgraph "VPS (Ubuntu 22.04)"
        Nginx -->|Proxy Pass| API[FastAPI Backend :8000]
        
        API <-->|Reads| Engine[Security Engine Thread]
        
        Engine -->|Checks| WG
        Engine -->|Checks| UFW[Firewall Status]
        Engine -->|Pings| Cloud[Cloudflare 1.1.1.1]
    end
````

## 🚀 Installation

### Prerequisites

  * Ubuntu 20.04/22.04 Server
  * Python 3.10+
  * Root/Sudo access

### 1\. Clone & Setup

```bash
git clone [https://github.com/abaasi256/XO-Shield.git](https://github.com/abaasi256/XO-Shield.git) /opt/xo-shield
cd /opt/xo-shield

# Create Virtual Env
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2\. Configure Environment

Create a `.env` file (optional) or rely on defaults in `app/config.py`.

```bash
export WIREGUARD_INTERFACE=wg0
export CHECK_INTERVAL=10
```

### 3\. Deploy Infrastructure (WireGuard + UFW)

*Note: This step requires Sudo.*

```bash
# Run the automated setup script (audited for safety)
sudo bash scripts/setup_wireguard.sh
```

### 4\. Run as Service

```bash
# Copy systemd file
sudo cp scripts/xo-shield.service /etc/systemd/system/
sudo systemctl enable --now xo-shield
```

## 🧠 How the Engine Works

The `SecurityEngine` class (`app/engine.py`) operates on a decoupled thread:

1.  **VPN Integrity:** Checks `/sys/class/net/wg0` to verify the interface is physically UP.
2.  **Firewall Audit:** queries `systemctl is-active ufw` to ensure the packet filter is running.
3.  **Latency Probe:** Executes a high-priority ICMP ping to a neutral DNS (1.1.1.1) to detect routing anomalies.

**Scoring Logic:**

  * Start: 100 Points
  * VPN Down: -50 Points (Critical)
  * Firewall Off: -30 Points (High Risk)
  * Latency \> 100ms: -20 Points (Performance Warning)

## 📜 License

MIT License. Created as a Portfolio Project.

```

***

### Final Task for You:
1.  **Upload that screenshot:** Go to your GitHub repo, click "Issues", drag your screenshot into the text box, and copy the link it generates. Paste that link into the `![XO-Shield Dashboard](...)` line in the README above.
2.  **Commit & Push:** Update your repo with this README.

You have done excellent work, Abbie. This is a solid DevSecOps project. Would you like to close this session, or do you have any final questions about maintaining the server?
```
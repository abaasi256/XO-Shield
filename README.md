# XO-Shield // OrbitGuard

> **A Real-time WireGuard VPN Security Engine & Dashboard**
> *Live Demo: https://vpn.xoxoent.space*

![XO-Shield Dashboard](https://github.com/user-attachments/assets/placeholder-for-your-screenshot)
*(Replace this line with the link to your actual screenshot)*

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

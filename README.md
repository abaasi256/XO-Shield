# XO-Shield

**Real-time VPN Security Visualization Engine.**

XO-Shield is a self-hosted dashboard designed to monitor the security posture of your WireGuard VPN server in real-time. It provides a "Deep Space" themed interface to visualize connection status, firewall activity, and network latency.

## Tech Stack

*   **Backend**: Python 3.10+, FastAPI
*   **System Monitoring**: `psutil`, `ip`, `ufw`
*   **Frontend**: HTML5, Vanilla JavaScript, Tailwind CSS (CDN)
*   **Server**: Nginx (Reverse Proxy), Uvicorn (ASGI)
*   **VPN**: WireGuard

# XO-Shield Deployment Guide

This guide details how to manually deploy XO-Shield on a live Ubuntu 22.04 server running Nginx.

## Prerequisites

*   **OS**: Ubuntu 22.04 LTS
*   **Python**: 3.10 or newer
*   **Software**: WireGuard, Nginx, Git
*   **User**: These steps assume you are running as a non-root user (e.g., `abbie`) with `sudo` privileges.

---

## Step 1: Clone & Environment Setup

1.  **Clone the Repository**:
    ```bash
    cd /home/abbie
    git clone https://github.com/abaasi256/XO-Shield.git
    cd XO-Shield
    ```

2.  **Create Virtual Environment**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

---

## Step 2: Nginx Configuration

Configure Nginx to reverse proxy traffic to the XO-Shield application running on port 8000.

1.  **Create Config File**:
    ```bash
    sudo nano /etc/nginx/sites-available/xo-shield
    ```

2.  **Paste Configuration** (Replace `vpn.yourdomain.com` with your actual domain):
    ```nginx
    server {
        listen 80;
        server_name vpn.yourdomain.com;

        location / {
            proxy_pass http://127.0.0.1:8000;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
    ```

3.  **Enable Site & Restart Nginx**:
    ```bash
    sudo ln -s /etc/nginx/sites-available/xo-shield /etc/nginx/sites-enabled/
    sudo nginx -t
    sudo systemctl restart nginx
    ```

---

## Step 3: Systemd Service Setup

Set up XO-Shield to run automatically as a background service.

1.  **Create Service File**:
    ```bash
    sudo nano /etc/systemd/system/xo-shield.service
    ```

2.  **Service Definition**:
    ```ini
    [Unit]
    Description=XO-Shield Security Dashboard
    After=network.target

    [Service]
    User=abbie
    Group=abbie
    WorkingDirectory=/home/abbie/XO-Shield
    Environment="PATH=/home/abbie/XO-Shield/venv/bin"
    Environment="WIREGUARD_INTERFACE=wg0"
    Environment="CHECK_INTERVAL=10"
    ExecStart=/home/abbie/XO-Shield/venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8000

    [Install]
    WantedBy=multi-user.target
    ```

3.  **Start & Enable Service**:
    ```bash
    sudo systemctl daemon-reload
    sudo systemctl start xo-shield
    sudo systemctl enable xo-shield
    ```

---

## Step 4: WireGuard Setup (Manual)

**Security Note**: We do not auto-generate keys. Please generate them manually to ensure they remain private.

1.  **Install WireGuard**:
    ```bash
    sudo apt update
    sudo apt install wireguard
    ```

2.  **Generate Keys** (If you haven't already):
    ```bash
    wg genkey | tee private.key | wg pubkey > public.key
    ```

3.  **Configure Interface**:
    *   Create your config at `/etc/wireguard/wg0.conf`.
    *   Ensure the interface is named `wg0` (or update `WIREGUARD_INTERFACE` in the service file).

4.  **Start WireGuard**:
    ```bash
    sudo wg-quick up wg0
    sudo systemctl enable wg-quick@wg0
    ```

5.  **Verify Status**:
    Ensure the interface is active so XO-Shield can detect it:
    ```bash
    sudo wg show
    ```

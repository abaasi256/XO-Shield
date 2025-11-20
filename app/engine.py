import time
import subprocess
import psutil
import re
import threading
from app.config import settings

class SecurityEngine:
    def __init__(self):
        self.score = 100
        self.details = {
            "vpn_status": "UNKNOWN",
            "firewall_status": "UNKNOWN",
            "latency_ms": 0,
            "score": 100
        }
        self._running = False

    def check_vpn(self):
        """Check if WireGuard interface is UP."""
        try:
            stats = psutil.net_if_stats()
            if settings.WIREGUARD_INTERFACE in stats:
                is_up = stats[settings.WIREGUARD_INTERFACE].isup
                return "UP" if is_up else "DOWN"
            else:
                # Fallback to ip link if psutil misses it
                result = subprocess.run(
                    ["ip", "link", "show", settings.WIREGUARD_INTERFACE],
                    capture_output=True, text=True
                )
                if result.returncode == 0 and "state UP" in result.stdout:
                    return "UP"
                return "DOWN"
        except Exception:
            return "ERROR"

    def check_latency(self):
        """Ping 1.1.1.1 and return latency in ms."""
        try:
            # Ping 1.1.1.1, count 1, wait 1s
            result = subprocess.run(
                ["ping", "-c", "1", "-W", "1", "1.1.1.1"],
                capture_output=True, text=True
            )
            if result.returncode == 0:
                # Parse time=xx.x ms
                match = re.search(r"time=([\d.]+)", result.stdout)
                if match:
                    return float(match.group(1))
            return 999.0 # High latency if failed
        except Exception:
            return 999.0

    def check_firewall(self):
        """Check if UFW is active (Safe Method)."""
        try:
            # systemctl status can be read by non-root users
            result = subprocess.run(
                ["systemctl", "is-active", "ufw"],
                capture_output=True, text=True
            )
            if result.stdout.strip() == "active":
                return "ACTIVE"
            return "INACTIVE"
        except FileNotFoundError:
            return "NOT_FOUND"
        except Exception:
            return "ERROR"

    def calculate_score(self):
        current_score = 100
        
        # Check 1: VPN
        vpn_status = self.check_vpn()
        if vpn_status != "UP":
            current_score -= 40
        
        # Check 2: Firewall
        fw_status = self.check_firewall()
        if fw_status != "ACTIVE":
            current_score -= 30
            
        # Check 3: Latency
        latency = self.check_latency()
        if latency > 100:
            current_score -= 20
            
        # Clamp score
        current_score = max(0, current_score)
        
        self.details = {
            "vpn_status": vpn_status,
            "firewall_status": fw_status,
            "latency_ms": round(latency, 1),
            "score": current_score
        }
        self.score = current_score

    def run_checks(self):
        while self._running:
            try:
                self.calculate_score()
            except Exception as e:
                print(f"Error in engine loop: {e}")
            time.sleep(settings.CHECK_INTERVAL)

    def start(self):
        if not self._running:
            self._running = True
            thread = threading.Thread(target=self.run_checks, daemon=True)
            thread.start()

    def stop(self):
        self._running = False

# Global instance
engine = SecurityEngine()
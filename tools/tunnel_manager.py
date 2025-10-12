#!/usr/bin/env python3
"""
Professional SSH Tunneling Manager for Colab-Local Connection
Provides structured, monitored connection between local machine and Colab GPU
"""

import os
import sys
import time
import json
import subprocess
from pathlib import Path
from typing import Dict, Optional
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class TunnelManager:
    """Manages SSH tunnel connection between local machine and Colab"""
    
    def __init__(self, config_path: str = "config/tunnel_config.json"):
        self.config_path = Path(config_path)
        self.config = self._load_config()
        self.tunnel_process = None
        self.status_file = Path("tunnel_status.json")
        
    def _load_config(self) -> Dict:
        """Load tunnel configuration"""
        if not self.config_path.exists():
            logger.warning(f"Config file not found: {self.config_path}")
            return self._get_default_config()
        
        with open(self.config_path) as f:
            return json.load(f)
    
    def _get_default_config(self) -> Dict:
        """Get default tunnel configuration"""
        return {
            "tunnel_type": "ngrok",  # or "cloudflared"
            "local_port": 8888,
            "remote_port": 22,
            "auth_token": os.getenv("NGROK_AUTH_TOKEN", ""),
            "region": "us",
            "protocol": "tcp"
        }
    
    def install_tunnel_client(self):
        """Install ngrok or cloudflared"""
        tunnel_type = self.config.get("tunnel_type", "ngrok")
        
        if tunnel_type == "ngrok":
            self._install_ngrok()
        elif tunnel_type == "cloudflared":
            self._install_cloudflared()
        else:
            raise ValueError(f"Unknown tunnel type: {tunnel_type}")
    
    def _install_ngrok(self):
        """Install ngrok on Windows"""
        logger.info("Installing ngrok...")
        try:
            # Check if already installed
            result = subprocess.run(
                ["ngrok", "version"],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                logger.info(f"ngrok already installed: {result.stdout.strip()}")
                return
        except FileNotFoundError:
            pass
        
        # Install via chocolatey or direct download
        logger.info("Please install ngrok manually:")
        logger.info("1. Download from: https://ngrok.com/download")
        logger.info("2. Extract to C:\\Program Files\\ngrok\\")
        logger.info("3. Add to PATH")
        logger.info("4. Run: ngrok authtoken YOUR_TOKEN")
        
    def _install_cloudflared(self):
        """Install cloudflared on Windows"""
        logger.info("Installing cloudflared...")
        logger.info("Please install cloudflared manually:")
        logger.info("1. Download from: https://github.com/cloudflare/cloudflared/releases")
        logger.info("2. Extract to C:\\Program Files\\cloudflared\\")
        logger.info("3. Add to PATH")
    
    def start_tunnel(self) -> Dict:
        """Start SSH tunnel"""
        tunnel_type = self.config.get("tunnel_type", "ngrok")
        
        if tunnel_type == "ngrok":
            return self._start_ngrok_tunnel()
        elif tunnel_type == "cloudflared":
            return self._start_cloudflared_tunnel()
        else:
            raise ValueError(f"Unknown tunnel type: {tunnel_type}")
    
    def _start_ngrok_tunnel(self) -> Dict:
        """Start ngrok tunnel"""
        logger.info("Starting ngrok tunnel...")
        
        port = self.config.get("local_port", 8888)
        
        try:
            # Start ngrok
            self.tunnel_process = subprocess.Popen(
                ["ngrok", "tcp", str(port), "--log", "stdout"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Wait for tunnel to establish
            time.sleep(3)
            
            # Get tunnel info from ngrok API
            import requests
            response = requests.get("http://localhost:4040/api/tunnels")
            tunnels = response.json()
            
            if tunnels.get("tunnels"):
                tunnel_url = tunnels["tunnels"][0]["public_url"]
                logger.info(f"✅ Tunnel established: {tunnel_url}")
                
                status = {
                    "status": "active",
                    "type": "ngrok",
                    "url": tunnel_url,
                    "local_port": port,
                    "started_at": time.time()
                }
                
                self._save_status(status)
                return status
            else:
                raise Exception("No tunnels found")
                
        except Exception as e:
            logger.error(f"Failed to start ngrok tunnel: {e}")
            raise
    
    def _start_cloudflared_tunnel(self) -> Dict:
        """Start cloudflared tunnel"""
        logger.info("Starting cloudflared tunnel...")
        
        port = self.config.get("local_port", 8888)
        
        try:
            # Start cloudflared
            self.tunnel_process = subprocess.Popen(
                ["cloudflared", "tunnel", "--url", f"tcp://localhost:{port}"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Wait and parse output for tunnel URL
            time.sleep(3)
            
            # Read tunnel URL from stderr
            tunnel_url = None
            for line in self.tunnel_process.stderr:
                if "https://" in line or "trycloudflare.com" in line:
                    tunnel_url = line.strip().split()[-1]
                    break
            
            if tunnel_url:
                logger.info(f"✅ Tunnel established: {tunnel_url}")
                
                status = {
                    "status": "active",
                    "type": "cloudflared",
                    "url": tunnel_url,
                    "local_port": port,
                    "started_at": time.time()
                }
                
                self._save_status(status)
                return status
            else:
                raise Exception("Failed to get tunnel URL")
                
        except Exception as e:
            logger.error(f"Failed to start cloudflared tunnel: {e}")
            raise
    
    def stop_tunnel(self):
        """Stop active tunnel"""
        if self.tunnel_process:
            logger.info("Stopping tunnel...")
            self.tunnel_process.terminate()
            self.tunnel_process.wait(timeout=5)
            self.tunnel_process = None
            
            status = {
                "status": "stopped",
                "stopped_at": time.time()
            }
            self._save_status(status)
            logger.info("✅ Tunnel stopped")
    
    def get_status(self) -> Optional[Dict]:
        """Get current tunnel status"""
        if not self.status_file.exists():
            return None
        
        with open(self.status_file) as f:
            return json.load(f)
    
    def _save_status(self, status: Dict):
        """Save tunnel status to file"""
        with open(self.status_file, 'w') as f:
            json.dump(status, f, indent=2)


def main():
    """CLI interface"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Tunnel Manager for Colab Connection")
    parser.add_argument("action", choices=["start", "stop", "status", "install"],
                       help="Action to perform")
    parser.add_argument("--config", default="config/tunnel_config.json",
                       help="Path to config file")
    
    args = parser.parse_args()
    
    manager = TunnelManager(config_path=args.config)
    
    if args.action == "install":
        manager.install_tunnel_client()
    elif args.action == "start":
        status = manager.start_tunnel()
        print(f"\n✅ Tunnel active: {status['url']}")
    elif args.action == "stop":
        manager.stop_tunnel()
    elif args.action == "status":
        status = manager.get_status()
        if status:
            print(f"Status: {status['status']}")
            if status['status'] == 'active':
                print(f"URL: {status['url']}")
                print(f"Local Port: {status['local_port']}")
        else:
            print("No active tunnel")


if __name__ == "__main__":
    main()

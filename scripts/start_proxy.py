import os
import threading
import socket
from pyngrok import ngrok, conf
import socks
import time

# --- Configuration ---
# Get ngrok authtoken from environment variable for security
NGROK_AUTH_TOKEN = os.environ.get("NGROK_AUTH_TOKEN")
LOCAL_PROXY_HOST = "127.0.0.1"
LOCAL_PROXY_PORT = 1080  # Standard SOCKS port
# --- End Configuration ---

class ThreadingTCPServer(threading.Thread):
    """A simple threaded TCP server to handle multiple connections."""
    def __init__(self, host, port):
        super().__init__()
        self.host = host
        self.port = port
        self.server_socket = None
        self.running = True

    def run(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"🔌 Local SOCKS5 proxy server listening on {self.host}:{self.port}")

        while self.running:
            try:
                conn, addr = self.server_socket.accept()
                handler = socks.Socks5Server(conn)
                # Let the socks library handle the connection in its own way
            except OSError:
                # This can happen when the socket is closed
                break
            except Exception as e:
                print(f"Error in server loop: {e}")

    def stop(self):
        self.running = False
        if self.server_socket:
            self.server_socket.close()
        print("🛑 Local proxy server stopped.")

def start_ngrok_tunnel(port):
    """Starts an ngrok TCP tunnel and returns the public URL."""
    if not NGROK_AUTH_TOKEN:
        print("\n" + "="*60)
        print("🚨 ERROR: NGROK_AUTH_TOKEN environment variable not set!")
        print("1. Go to https://dashboard.ngrok.com/get-started/your-authtoken")
        print("2. Copy your authtoken.")
        print("3. Run this command in your terminal (and restart it):")
        print(f'   setx NGROK_AUTH_TOKEN "YOUR_TOKEN"')
        print("="*60)
        return None

    try:
        print("🔑 Configuring ngrok with your authtoken...")
        conf.get_default().auth_token = NGROK_AUTH_TOKEN
        
        print(f"🚇 Starting ngrok tunnel for port {port}...")
        # Kill any existing tunnels on the same port to avoid conflicts
        for tunnel in ngrok.get_tunnels():
            if tunnel.config['addr'].endswith(str(port)):
                print(f"   - Closing existing tunnel: {tunnel.public_url}")
                ngrok.disconnect(tunnel.public_url)

        public_url = ngrok.connect(port, "tcp").public_url
        print(f"✅ ngrok tunnel is live!")
        return public_url
    except Exception as e:
        print(f"❌ Failed to start ngrok tunnel: {e}")
        return None

def main():
    """Main function to start the proxy and the tunnel."""
    # Start the local SOCKS5 proxy server in a separate thread
    local_proxy_server = ThreadingTCPServer(LOCAL_PROXY_HOST, LOCAL_PROXY_PORT)
    local_proxy_server.daemon = True
    local_proxy_server.start()
    
    # Give the server a moment to start up
    time.sleep(1)

    # Start the ngrok tunnel
    public_url = start_ngrok_tunnel(LOCAL_PROXY_PORT)

    if public_url:
        # The URL from pyngrok is like "tcp://0.tcp.ngrok.io:12345"
        # We need to format it for SOCKS5
        hostname = public_url.split('//')[1].split(':')[0]
        port = public_url.split(':')[-1]
        socks_url = f"socks5h://{hostname}:{port}"

        print("\n" + "="*60)
        print("✅✅✅ YOUR PROXY IS READY! ✅✅✅")
        print("\nCopy this full line and paste it into Colab when prompted:")
        print(f"\n{socks_url}\n")
        print("="*60)
        print("\nℹ️  Keep this terminal open. Press CTRL+C to stop the proxy.")
        
        try:
            # Keep the main thread alive to wait for CTRL+C
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n👋 Shutting down...")
    
    # Cleanup
    ngrok.disconnect()
    local_proxy_server.stop()
    print("✅ Done.")

if __name__ == "__main__":
    main()

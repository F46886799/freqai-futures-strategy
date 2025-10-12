#!/usr/bin/env python3
"""
Create Colab setup notebook with FIXED ngrok authentication
"""

import json

notebook = {
    "nbformat": 4,
    "nbformat_minor": 0,
    "metadata": {
        "colab": {
            "provenance": [],
            "gpuType": "T4"
        },
        "kernelspec": {
            "name": "python3",
            "display_name": "Python 3"
        },
        "language_info": {
            "name": "python"
        },
        "accelerator": "GPU"
    },
    "cells": [
        {
            "cell_type": "markdown",
            "metadata": {"id": "header"},
            "source": [
                "# FreqAI Colab Remote Execution Setup\n",
                "\n",
                "Sets up SSH + ngrok tunnel for remote GPU backtest execution.\n",
                "\n",
                "**Steps:** Enable GPU → Run all cells → Copy connection details"
            ]
        },
        {
            "cell_type": "code",
            "metadata": {"id": "check-gpu"},
            "execution_count": None,
            "outputs": [],
            "source": [
                "# Check GPU\n",
                "import subprocess\n",
                "try:\n",
                "    result = subprocess.run(['nvidia-smi'], capture_output=True, text=True)\n",
                "    print('✅ GPU Available!')\n",
                "    for line in result.stdout.split('\\n'):\n",
                "        if 'Tesla' in line or 'T4' in line or 'MiB' in line:\n",
                "            print(line)\n",
                "except:\n",
                "    print('❌ GPU NOT FOUND!')\n",
                "    print('Enable GPU: Runtime > Change runtime type > GPU (T4)')"
            ]
        },
        {
            "cell_type": "code",
            "metadata": {"id": "install-ssh"},
            "execution_count": None,
            "outputs": [],
            "source": [
                "%%capture\n",
                "!apt-get update -qq\n",
                "!apt-get install -y openssh-server"
            ]
        },
        {
            "cell_type": "code",
            "metadata": {"id": "setup-ssh"},
            "execution_count": None,
            "outputs": [],
            "source": [
                "# Setup SSH server\n",
                "import secrets, string\n",
                "\n",
                "password = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(16))\n",
                "\n",
                "!mkdir -p /var/run/sshd\n",
                "!echo \"root:{password}\" | chpasswd\n",
                "!echo \"PermitRootLogin yes\" >> /etc/ssh/sshd_config\n",
                "!echo \"PasswordAuthentication yes\" >> /etc/ssh/sshd_config\n",
                "!service ssh restart\n",
                "\n",
                "print('✅ SSH server started')\n",
                "print(f'🔑 Password: {password}')"
            ]
        },
        {
            "cell_type": "code",
            "metadata": {"id": "install-ngrok"},
            "execution_count": None,
            "outputs": [],
            "source": [
                "# Download ngrok\n",
                "!wget -q https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz\n",
                "!tar -xzf ngrok-v3-stable-linux-amd64.tgz\n",
                "!chmod +x ngrok\n",
                "\n",
                "print('✅ ngrok downloaded')\n",
                "print('\\n📝 Get token: https://dashboard.ngrok.com/get-started/your-authtoken')"
            ]
        },
        {
            "cell_type": "code",
            "metadata": {"id": "configure-ngrok"},
            "execution_count": None,
            "outputs": [],
            "source": [
                "# Configure ngrok - FIXED VERSION\n",
                "import getpass\n",
                "import subprocess\n",
                "import os\n",
                "\n",
                "# Get token\n",
                "ngrok_token = getpass.getpass('Enter your ngrok auth token: ')\n",
                "\n",
                "# Create config directory\n",
                "!mkdir -p /root/.config/ngrok\n",
                "\n",
                "# Save token using Python (not shell command)\n",
                "config_content = f\"\"\"version: \"2\"\n",
                "authtoken: {ngrok_token}\n",
                "\"\"\"\n",
                "\n",
                "with open('/root/.config/ngrok/ngrok.yml', 'w') as f:\n",
                "    f.write(config_content)\n",
                "\n",
                "print('✅ ngrok configured')\n",
                "\n",
                "# Verify\n",
                "if os.path.exists('/root/.config/ngrok/ngrok.yml'):\n",
                "    print('✅ Config file created')\n",
                "else:\n",
                "    print('❌ Config file not found!')"
            ]
        },
        {
            "cell_type": "code",
            "metadata": {"id": "start-tunnel"},
            "execution_count": None,
            "outputs": [],
            "source": [
                "# Start tunnel - FIXED\n",
                "import subprocess, time, requests, json\n",
                "\n",
                "print('⏳ Starting ngrok tunnel...')\n",
                "\n",
                "# Start ngrok with proper logging\n",
                "ngrok_process = subprocess.Popen(\n",
                "    ['./ngrok', 'tcp', '22'],\n",
                "    stdout=subprocess.PIPE,\n",
                "    stderr=subprocess.PIPE,\n",
                "    text=True\n",
                ")\n",
                "\n",
                "# Wait for tunnel\n",
                "tunnel_url = None\n",
                "for i in range(30):\n",
                "    try:\n",
                "        time.sleep(1)\n",
                "        resp = requests.get('http://localhost:4040/api/tunnels', timeout=2)\n",
                "        data = resp.json()\n",
                "        tunnels = data.get('tunnels', [])\n",
                "        if tunnels:\n",
                "            tunnel_url = tunnels[0]['public_url']\n",
                "            break\n",
                "        if i % 5 == 0 and i > 0:\n",
                "            print(f'  Waiting... ({i}/30)')\n",
                "    except:\n",
                "        if i == 0:\n",
                "            print('  Starting...')\n",
                "        elif i % 5 == 0:\n",
                "            print(f'  Waiting... ({i}/30)')\n",
                "\n",
                "if tunnel_url:\n",
                "    print(f'\\n{'='*70}')\n",
                "    print('✅ TUNNEL ESTABLISHED')\n",
                "    print('='*70)\n",
                "    print(f'URL: {tunnel_url}')\n",
                "    print(f'Password: {password}')\n",
                "    print('='*70)\n",
                "    print('\\n📋 Run on LOCAL machine:')\n",
                "    print()\n",
                "    print('python tools/backtest_executor.py \\\\')\n",
                "    print(f'  --tunnel-url \"{tunnel_url}\" \\\\')\n",
                "    print(f'  --password \"{password}\" \\\\')\n",
                "    print('  --strategy FreqAIHybridStrategy \\\\')\n",
                "    print('  --timerange 20250901-20251012 \\\\')\n",
                "    print('  --pairs BTC/USDT:USDT')\n",
                "    print()\n",
                "else:\n",
                "    print('\\n❌ Tunnel failed')\n",
                "    print('\\nCheck if ngrok is running:')\n",
                "    !ps aux | grep ngrok\n",
                "    print('\\nCheck ngrok API:')\n",
                "    !curl -s http://localhost:4040/api/tunnels | python3 -m json.tool || echo 'API not responding'"
            ]
        },
        {
            "cell_type": "code",
            "metadata": {"id": "clone-repo"},
            "execution_count": None,
            "outputs": [],
            "source": [
                "%%capture\n",
                "# Clone repository\n",
                "import os\n",
                "!rm -rf freqai-futures-strategy\n",
                "!git clone -q https://github.com/aminak58/freqai-futures-strategy.git\n",
                "os.chdir('/content/freqai-futures-strategy')\n",
                "!pip install -q ta-lib-binary 'freqtrade[freqai]'"
            ]
        },
        {
            "cell_type": "code",
            "metadata": {"id": "verify"},
            "execution_count": None,
            "outputs": [],
            "source": [
                "# Verify\n",
                "import os\n",
                "print('✅ Repository ready')\n",
                "print(f'📂 {os.getcwd()}')\n",
                "!ls -lh | head -10"
            ]
        },
        {
            "cell_type": "code",
            "metadata": {"id": "mount-data"},
            "execution_count": None,
            "outputs": [],
            "source": [
                "# Optional: Mount Drive for data\n",
                "from google.colab import drive\n",
                "import zipfile, os\n",
                "\n",
                "drive.mount('/content/drive')\n",
                "\n",
                "zip_path = '/content/drive/MyDrive/FreqAI/binance_data.zip'\n",
                "if os.path.exists(zip_path):\n",
                "    print('📦 Extracting...')\n",
                "    os.makedirs('user_data/data', exist_ok=True)\n",
                "    with zipfile.ZipFile(zip_path) as z:\n",
                "        z.extractall('user_data/data/')\n",
                "    count = sum(len(f) for _, _, f in os.walk('user_data/data/binance'))\n",
                "    print(f'✅ {count} files')\n",
                "else:\n",
                "    print('ℹ️  No pre-downloaded data')"
            ]
        },
        {
            "cell_type": "code",
            "metadata": {"id": "keep-alive"},
            "execution_count": None,
            "outputs": [],
            "source": [
                "# Keep alive\n",
                "import time\n",
                "from IPython.display import clear_output\n",
                "\n",
                "print('🔄 Session active')\n",
                "print('='*70)\n",
                "print(f'URL: {tunnel_url}')\n",
                "print(f'Password: {password}')\n",
                "print('='*70)\n",
                "print('Auto-refresh every 5 min\\n')\n",
                "\n",
                "counter = 0\n",
                "while True:\n",
                "    try:\n",
                "        time.sleep(300)\n",
                "        counter += 1\n",
                "        clear_output(wait=True)\n",
                "        print(f'🔄 Alive (#{counter} - {counter*5}min)')\n",
                "        print('='*70)\n",
                "        print(f'URL: {tunnel_url}')\n",
                "        print(f'Password: {password}')\n",
                "        print('='*70)\n",
                "        print(time.strftime('%H:%M:%S'))\n",
                "    except KeyboardInterrupt:\n",
                "        break"
            ]
        }
    ]
}

with open('Colab_Remote_Setup.ipynb', 'w', encoding='utf-8') as f:
    json.dump(notebook, f, indent=2, ensure_ascii=False)

print("✅ FIXED notebook created!")
print("\n🔧 Key fix:")
print("  • Auth token saved using Python (not shell)")
print("  • Creates proper ngrok.yml config file")
print("  • Verifies config file exists")
print("\nThis should fix the authentication error!")

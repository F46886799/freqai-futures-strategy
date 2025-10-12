#!/usr/bin/env python3
"""
Create improved Colab setup notebook with better ngrok handling
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
                "**Steps:** Enable GPU → Run all cells → Copy connection details → Execute from local machine"
            ]
        },
        {
            "cell_type": "code",
            "metadata": {"id": "check-gpu"},
            "execution_count": None,
            "outputs": [],
            "source": [
                "# Check GPU availability\n",
                "import subprocess\n",
                "try:\n",
                "    result = subprocess.run(['nvidia-smi'], capture_output=True, text=True)\n",
                "    print('✅ GPU Available!')\n",
                "    for line in result.stdout.split('\\n'):\n",
                "        if 'Tesla' in line or 'T4' in line or 'MiB' in line:\n",
                "            print(line)\n",
                "except:\n",
                "    print('❌ GPU NOT FOUND!')\n",
                "    print('➡️  Enable GPU: Runtime > Change runtime type > GPU (T4) > Save')"
            ]
        },
        {
            "cell_type": "code",
            "metadata": {"id": "install-deps"},
            "execution_count": None,
            "outputs": [],
            "source": [
                "%%capture\n",
                "# Install SSH server and dependencies\n",
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
                "# Configure SSH server\n",
                "import secrets, string\n",
                "\n",
                "# Generate secure random password\n",
                "password = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(16))\n",
                "\n",
                "# Configure and start SSH\n",
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
                "print('✅ ngrok ready')\n",
                "print('\\n📝 Get token: https://dashboard.ngrok.com/get-started/your-authtoken')"
            ]
        },
        {
            "cell_type": "code",
            "metadata": {"id": "start-tunnel"},
            "execution_count": None,
            "outputs": [],
            "source": [
                "# Start ngrok tunnel - IMPROVED\n",
                "import subprocess, time, requests, getpass\n",
                "\n",
                "# Get auth token\n",
                "ngrok_token = getpass.getpass('Enter ngrok auth token: ')\n",
                "!./ngrok authtoken {ngrok_token}\n",
                "\n",
                "# Start tunnel with better logging\n",
                "print('⏳ Starting tunnel (may take 10-15 seconds)...')\n",
                "ngrok_process = subprocess.Popen(\n",
                "    ['./ngrok', 'tcp', '22', '--log', 'stdout', '--log-level', 'info'],\n",
                "    stdout=open('/tmp/ngrok.log', 'w'),\n",
                "    stderr=subprocess.STDOUT\n",
                ")\n",
                "\n",
                "# Wait for tunnel with retries\n",
                "tunnel_url = None\n",
                "for i in range(30):  # 30 attempts = 30 seconds max\n",
                "    try:\n",
                "        time.sleep(1)\n",
                "        resp = requests.get('http://localhost:4040/api/tunnels', timeout=2)\n",
                "        tunnels = resp.json().get('tunnels', [])\n",
                "        if tunnels:\n",
                "            tunnel_url = tunnels[0]['public_url']\n",
                "            break\n",
                "        if i % 5 == 0:\n",
                "            print(f'  Waiting... ({i+1}/30)')\n",
                "    except:\n",
                "        if i % 5 == 0:\n",
                "            print(f'  Starting... ({i+1}/30)')\n",
                "\n",
                "if tunnel_url:\n",
                "    print(f'\\n{'='*70}')\n",
                "    print('✅ TUNNEL ESTABLISHED')\n",
                "    print('='*70)\n",
                "    print(f'URL: {tunnel_url}')\n",
                "    print(f'Password: {password}')\n",
                "    print('='*70)\n",
                "    print('\\n📋 Run this on your LOCAL machine:')\n",
                "    print()\n",
                "    print(f'python tools/backtest_executor.py \\\\')\n",
                "    print(f'  --tunnel-url \"{tunnel_url}\" \\\\')\n",
                "    print(f'  --password \"{password}\" \\\\')\n",
                "    print(f'  --strategy FreqAIHybridStrategy \\\\')\n",
                "    print(f'  --timerange 20250901-20251012 \\\\')\n",
                "    print(f'  --pairs BTC/USDT:USDT')\n",
                "    print()\n",
                "    print('='*70)\n",
                "else:\n",
                "    print('\\n❌ Tunnel failed to start')\n",
                "    print('\\nCheck ngrok logs:')\n",
                "    !tail -20 /tmp/ngrok.log\n",
                "    print('\\nCheck if ngrok is running:')\n",
                "    !ps aux | grep ngrok | grep -v grep"
            ]
        },
        {
            "cell_type": "code",
            "metadata": {"id": "clone-repo"},
            "execution_count": None,
            "outputs": [],
            "source": [
                "%%capture\n",
                "# Clone repository and install dependencies\n",
                "import os\n",
                "!rm -rf freqai-futures-strategy\n",
                "!git clone -q https://github.com/aminak58/freqai-futures-strategy.git\n",
                "os.chdir('/content/freqai-futures-strategy')\n",
                "!pip install -q ta-lib-binary 'freqtrade[freqai]'"
            ]
        },
        {
            "cell_type": "code",
            "metadata": {"id": "verify-setup"},
            "execution_count": None,
            "outputs": [],
            "source": [
                "# Verify setup\n",
                "import os\n",
                "print('✅ Repository cloned')\n",
                "print(f'📂 Directory: {os.getcwd()}')\n",
                "print('\\n📁 Files:')\n",
                "!ls -lh | head -15"
            ]
        },
        {
            "cell_type": "code",
            "metadata": {"id": "mount-data"},
            "execution_count": None,
            "outputs": [],
            "source": [
                "# Optional: Mount Google Drive for pre-downloaded data\n",
                "from google.colab import drive\n",
                "import zipfile, os\n",
                "\n",
                "drive.mount('/content/drive')\n",
                "\n",
                "zip_path = '/content/drive/MyDrive/FreqAI/binance_data.zip'\n",
                "if os.path.exists(zip_path):\n",
                "    print('📦 Extracting data...')\n",
                "    os.makedirs('user_data/data', exist_ok=True)\n",
                "    with zipfile.ZipFile(zip_path) as z:\n",
                "        z.extractall('user_data/data/')\n",
                "    file_count = sum(len(f) for _, _, f in os.walk('user_data/data/binance'))\n",
                "    print(f'✅ Extracted {file_count} data files')\n",
                "else:\n",
                "    print('ℹ️  No pre-downloaded data found')\n",
                "    print('   Data will be downloaded during first backtest')"
            ]
        },
        {
            "cell_type": "code",
            "metadata": {"id": "keep-alive"},
            "execution_count": None,
            "outputs": [],
            "source": [
                "# Keep session alive\n",
                "import time\n",
                "from IPython.display import clear_output\n",
                "\n",
                "print('🔄 Session monitor active')\n",
                "print('='*70)\n",
                "print('CONNECTION INFO')\n",
                "print('='*70)\n",
                "print(f'URL: {tunnel_url}')\n",
                "print(f'Password: {password}')\n",
                "print('='*70)\n",
                "print('\\nAuto-refresh every 5 minutes')\n",
                "print('Press ■ Stop to end\\n')\n",
                "\n",
                "counter = 0\n",
                "while True:\n",
                "    try:\n",
                "        time.sleep(300)\n",
                "        counter += 1\n",
                "        clear_output(wait=True)\n",
                "        print(f'🔄 Alive (refresh #{counter} - {counter*5} min)')\n",
                "        print('='*70)\n",
                "        print(f'URL: {tunnel_url}')\n",
                "        print(f'Password: {password}')\n",
                "        print('='*70)\n",
                "        print(f'⏰ {time.strftime(\"%H:%M:%S\")}')\n",
                "        print('\\nPress ■ Stop to end')\n",
                "    except KeyboardInterrupt:\n",
                "        print('\\n✋ Stopped')\n",
                "        break"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {"id": "troubleshoot-header"},
            "source": [
                "---\n",
                "## Troubleshooting\n",
                "\n",
                "Run cells below if tunnel didn't start:"
            ]
        },
        {
            "cell_type": "code",
            "metadata": {"id": "check-tunnel-manual"},
            "execution_count": None,
            "outputs": [],
            "source": [
                "# Manual tunnel check\n",
                "import requests\n",
                "try:\n",
                "    resp = requests.get('http://localhost:4040/api/tunnels')\n",
                "    data = resp.json()\n",
                "    if data.get('tunnels'):\n",
                "        print('✅ Tunnel found!')\n",
                "        print(f\"URL: {data['tunnels'][0]['public_url']}\")\n",
                "    else:\n",
                "        print('❌ No tunnels')\n",
                "except:\n",
                "    print('❌ ngrok API not responding')\n",
                "    print('\\nngrok process status:')\n",
                "    !ps aux | grep ngrok | grep -v grep"
            ]
        },
        {
            "cell_type": "code",
            "metadata": {"id": "check-logs"},
            "execution_count": None,
            "outputs": [],
            "source": [
                "# Check ngrok logs\n",
                "print('Recent ngrok logs:')\n",
                "!tail -30 /tmp/ngrok.log 2>/dev/null || echo 'No log file found'"
            ]
        }
    ]
}

with open('Colab_Remote_Setup.ipynb', 'w', encoding='utf-8') as f:
    json.dump(notebook, f, indent=2, ensure_ascii=False)

print("✅ Improved notebook created!")
print("\nKey improvements:")
print("  • 30 second timeout (was 5)")
print("  • Better progress messages")
print("  • Explicit logging to file")
print("  • Troubleshooting cells added")
print("  • Cleaner output format")

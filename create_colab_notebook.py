#!/usr/bin/env python3
"""
Create FINAL working Colab setup notebook
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
        "accelerator": "GPU"
    },
    "cells": [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "# FreqAI GPU Backtest - Remote Setup\n",
                "\n",
                "**Enable GPU:** Runtime > Change runtime type > GPU (T4)\n",
                "\n",
                "**Then:** Run all cells (Runtime > Run all)"
            ]
        },
        {
            "cell_type": "code",
            "metadata": {},
            "execution_count": None,
            "outputs": [],
            "source": [
                "# 1. Check GPU\n",
                "!nvidia-smi --query-gpu=name,memory.total --format=csv || echo '❌ GPU not found. Enable GPU!'"
            ]
        },
        {
            "cell_type": "code",
            "metadata": {},
            "execution_count": None,
            "outputs": [],
            "source": [
                "%%capture\n",
                "# 2. Install SSH\n",
                "!apt-get update -qq\n",
                "!apt-get install -y openssh-server"
            ]
        },
        {
            "cell_type": "code",
            "metadata": {},
            "execution_count": None,
            "outputs": [],
            "source": [
                "# 3. Setup SSH\n",
                "import secrets, string\n",
                "password = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(16))\n",
                "!mkdir -p /var/run/sshd\n",
                "!echo \"root:{password}\" | chpasswd\n",
                "!sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config\n",
                "!sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config\n",
                "!service ssh restart\n",
                "print(f'✅ SSH ready | Password: {password}')"
            ]
        },
        {
            "cell_type": "code",
            "metadata": {},
            "execution_count": None,
            "outputs": [],
            "source": [
                "# 4. Download ngrok to /content\n",
                "import os\n",
                "os.chdir('/content')\n",
                "!wget -q https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz\n",
                "!tar -xzf ngrok-v3-stable-linux-amd64.tgz\n",
                "!chmod +x ngrok\n",
                "!ls -lh ngrok\n",
                "print('✅ ngrok ready')\n",
                "print('\\nGet token: https://dashboard.ngrok.com/get-started/your-authtoken')"
            ]
        },
        {
            "cell_type": "code",
            "metadata": {},
            "execution_count": None,
            "outputs": [],
            "source": [
                "# 5. Configure ngrok\n",
                "import getpass\n",
                "ngrok_token = getpass.getpass('Enter ngrok token: ')\n",
                "!mkdir -p /root/.config/ngrok\n",
                "config = f'version: \"2\"\\nauthtoken: {ngrok_token}\\n'\n",
                "with open('/root/.config/ngrok/ngrok.yml', 'w') as f:\n",
                "    f.write(config)\n",
                "print('✅ Token saved')"
            ]
        },
        {
            "cell_type": "code",
            "metadata": {},
            "execution_count": None,
            "outputs": [],
            "source": [
                "# 6. Start tunnel\n",
                "import subprocess, time, requests\n",
                "import os\n",
                "os.chdir('/content')\n",
                "print('⏳ Starting tunnel...')\n",
                "proc = subprocess.Popen(['/content/ngrok', 'tcp', '22'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)\n",
                "time.sleep(5)\n",
                "tunnel_url = None\n",
                "for i in range(20):\n",
                "    try:\n",
                "        time.sleep(1)\n",
                "        r = requests.get('http://127.0.0.1:4040/api/tunnels', timeout=2)\n",
                "        tunnels = r.json().get('tunnels', [])\n",
                "        if tunnels:\n",
                "            tunnel_url = tunnels[0]['public_url']\n",
                "            break\n",
                "    except:\n",
                "        if i % 5 == 0:\n",
                "            print(f'  Waiting {i}/20...')\n",
                "if tunnel_url:\n",
                "    print('\\n' + '='*70)\n",
                "    print('✅ TUNNEL ACTIVE')\n",
                "    print('='*70)\n",
                "    print(f'URL: {tunnel_url}')\n",
                "    print(f'Password: {password}')\n",
                "    print('='*70)\n",
                "    print('\\nRun on LOCAL machine:\\n')\n",
                "    print(f'python tools/backtest_executor.py \\\\')\n",
                "    print(f'  --tunnel-url \"{tunnel_url}\" \\\\')\n",
                "    print(f'  --password \"{password}\" \\\\')\n",
                "    print(f'  --strategy FreqAIHybridStrategy \\\\')\n",
                "    print(f'  --timerange 20250901-20251012 \\\\')\n",
                "    print(f'  --pairs BTC/USDT:USDT')\n",
                "else:\n",
                "    print('❌ Tunnel failed. Run troubleshooting cells below.')"
            ]
        },
        {
            "cell_type": "code",
            "metadata": {},
            "execution_count": None,
            "outputs": [],
            "source": [
                "%%capture\n",
                "# 7. Clone repo\n",
                "import os\n",
                "os.chdir('/content')\n",
                "!rm -rf freqai-futures-strategy\n",
                "!git clone -q https://github.com/aminak58/freqai-futures-strategy.git\n",
                "os.chdir('/content/freqai-futures-strategy')\n",
                "!pip install -q ta-lib-binary 'freqtrade[freqai]'"
            ]
        },
        {
            "cell_type": "code",
            "metadata": {},
            "execution_count": None,
            "outputs": [],
            "source": [
                "# 8. Verify\n",
                "import os\n",
                "print(f'✅ Ready: {os.getcwd()}')\n",
                "!ls -lh | head -10"
            ]
        },
        {
            "cell_type": "code",
            "metadata": {},
            "execution_count": None,
            "outputs": [],
            "source": [
                "# 9. Optional: Mount Drive\n",
                "from google.colab import drive\n",
                "import zipfile, os\n",
                "drive.mount('/content/drive')\n",
                "zip_path = '/content/drive/MyDrive/FreqAI/binance_data.zip'\n",
                "if os.path.exists(zip_path):\n",
                "    print('📦 Extracting data...')\n",
                "    os.chdir('/content/freqai-futures-strategy')\n",
                "    os.makedirs('user_data/data', exist_ok=True)\n",
                "    with zipfile.ZipFile(zip_path) as z:\n",
                "        z.extractall('user_data/data/')\n",
                "    print('✅ Data ready')\n",
                "else:\n",
                "    print('ℹ️  No data in Drive')"
            ]
        },
        {
            "cell_type": "code",
            "metadata": {},
            "execution_count": None,
            "outputs": [],
            "source": [
                "# 10. Keep alive\n",
                "import time\n",
                "from IPython.display import clear_output\n",
                "print('🔄 Session active')\n",
                "print('='*70)\n",
                "print(f'URL: {tunnel_url}')\n",
                "print(f'Password: {password}')\n",
                "print('='*70)\n",
                "print('Refresh every 5min\\n')\n",
                "c = 0\n",
                "while True:\n",
                "    try:\n",
                "        time.sleep(300)\n",
                "        c += 1\n",
                "        clear_output(wait=True)\n",
                "        print(f'🔄 Alive #{c} ({c*5}min)')\n",
                "        print('='*70)\n",
                "        print(f'URL: {tunnel_url}')\n",
                "        print(f'Password: {password}')\n",
                "        print('='*70)\n",
                "        print(time.strftime('%H:%M:%S'))\n",
                "    except KeyboardInterrupt:\n",
                "        break"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "---\n",
                "## Troubleshooting"
            ]
        },
        {
            "cell_type": "code",
            "metadata": {},
            "execution_count": None,
            "outputs": [],
            "source": [
                "# Check tunnel manually\n",
                "!curl -s http://127.0.0.1:4040/api/tunnels | python3 -m json.tool"
            ]
        },
        {
            "cell_type": "code",
            "metadata": {},
            "execution_count": None,
            "outputs": [],
            "source": [
                "# Check ngrok process\n",
                "!ps aux | grep ngrok"
            ]
        }
    ]
}

with open('Colab_Remote_Setup.ipynb', 'w', encoding='utf-8') as f:
    json.dump(notebook, f, indent=2, ensure_ascii=False)

print("✅ FINAL notebook created!")
print("\n🔧 All issues fixed:")
print("  • Explicitly cd to /content before download")
print("  • Use absolute path /content/ngrok to start")
print("  • Verify ngrok file exists with ls")
print("  • Simplified config writing")
print("  • All in correct directory")
print("\nThis WILL work!")

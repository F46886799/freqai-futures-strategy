#!/usr/bin/env python3
"""
Generate Colab notebook with PROPER JSON formatting
"""

import json

# Define notebook structure
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
    "cells": []
}

# Cell 1: Markdown intro
notebook["cells"].append({
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "# 🚀 FreqAI Hybrid Strategy - GPU Backtest\n",
        "\n",
        "**Simple Git-based workflow - No SSH, No tunnels!**\n",
        "\n",
        "## 📋 Before you start:\n",
        "1. ✅ Enable GPU: **Runtime > Change runtime type > T4 GPU**\n",
        "2. ✅ Have your GitHub token ready (only if pushing logs)\n",
        "\n",
        "## 🎯 What this does:\n",
        "- Clones repo from GitHub\n",
        "- Runs backtest on GPU\n",
        "- Saves results to Google Drive\n",
        "\n",
        "## ⏱️ Time:\n",
        "- First run: ~5 min (install)\n",
        "- Backtest: ~5-15 min"
    ]
})

# Cell 2: Check GPU
notebook["cells"].append({
    "cell_type": "code",
    "metadata": {},
    "source": [
        "# Check GPU\n",
        "!nvidia-smi --query-gpu=name,memory.total --format=csv\n",
        "\n",
        "import torch\n",
        "print(f\"\\n✅ GPU: {torch.cuda.is_available()}\")\n",
        "if torch.cuda.is_available():\n",
        "    print(f\"Device: {torch.cuda.get_device_name(0)}\")"
    ],
    "execution_count": None,
    "outputs": []
})

# Cell 3: Clone repo
notebook["cells"].append({
    "cell_type": "code",
    "metadata": {},
    "source": [
        "# Clone repository\n",
        "!rm -rf freqai-futures-strategy\n",
        "print(\"📦 Cloning...\")\n",
        "!git clone https://github.com/aminak58/freqai-futures-strategy.git\n",
        "%cd freqai-futures-strategy\n",
        "print(\"\\n✅ Done!\")\n",
        "!ls -lh"
    ],
    "execution_count": None,
    "outputs": []
})

# Cell 4: Install dependencies
notebook["cells"].append({
    "cell_type": "code",
    "metadata": {},
    "source": [
        "# Install dependencies\n",
        "print(\"📦 Installing... (2-3 min)\\n\")\n",
        "!pip install -q ta-lib-binary\n",
        "!pip install -q 'freqtrade[freqai]'\n",
        "print(\"\\n✅ Installed!\")\n",
        "!freqtrade --version"
    ],
    "execution_count": None,
    "outputs": []
})

# Cell 5: Mount Drive
notebook["cells"].append({
    "cell_type": "code",
    "metadata": {},
    "source": [
        "# Mount Google Drive\n",
        "from google.colab import drive\n",
        "drive.mount('/content/drive')\n",
        "\n",
        "results_dir = '/content/drive/MyDrive/FreqAI_Results'\n",
        "!mkdir -p \"{results_dir}\"\n",
        "print(f\"\\n✅ Results → {results_dir}\")"
    ],
    "execution_count": None,
    "outputs": []
})

# Cell 6: Optional data
notebook["cells"].append({
    "cell_type": "code",
    "metadata": {},
    "source": [
        "# Optional: Load data from Drive\n",
        "import os, zipfile\n",
        "\n",
        "data_zip = '/content/drive/MyDrive/FreqAI/binance_data.zip'\n",
        "\n",
        "if os.path.exists(data_zip):\n",
        "    print(\"📦 Extracting data...\")\n",
        "    !mkdir -p user_data/data/binance\n",
        "    with zipfile.ZipFile(data_zip) as z:\n",
        "        z.extractall('user_data/data/')\n",
        "    print(\"✅ Done!\")\n",
        "else:\n",
        "    print(\"ℹ️  No data. Will download during backtest.\")"
    ],
    "execution_count": None,
    "outputs": []
})

# Cell 7: CRITICAL - Setup Cloudflare WARP VPN (FREE!)
notebook["cells"].append({
    "cell_type": "code",
    "metadata": {},
    "source": [
        "# 🔥 CRITICAL: Setup Cloudflare WARP to bypass Binance geo-blocking\n",
        "import os\n",
        "import subprocess\n",
        "import time\n",
        "import requests\n",
        "\n",
        "print(\"🌐 Installing Cloudflare WARP (FREE VPN)...\\n\")\n",
        "\n",
        "try:\n",
        "    # Install WARP\n",
        "    print(\"📦 Installing wgcf...\")\n",
        "    !pip install -q wgcf\n",
        "    \n",
        "    print(\"📝 Registering WARP account...\")\n",
        "    !yes | wgcf register\n",
        "    \n",
        "    print(\"🔧 Generating WireGuard config...\")\n",
        "    !wgcf generate\n",
        "    \n",
        "    print(\"📦 Installing WireGuard...\")\n",
        "    !sudo apt-get install -qq -y wireguard-tools\n",
        "    \n",
        "    print(\"🚀 Starting WARP tunnel...\")\n",
        "    !sudo cp wgcf-profile.conf /etc/wireguard/warp.conf\n",
        "    !sudo wg-quick up warp\n",
        "    \n",
        "    time.sleep(3)\n",
        "    \n",
        "    print(\"\\n✅ WARP connected!\\n\")\n",
        "    \n",
        "    # Test Binance access\n",
        "    print(\"🧪 Testing Binance API access...\")\n",
        "    response = requests.get(\"https://api.binance.com/api/v3/ping\", timeout=10)\n",
        "    \n",
        "    if response.status_code == 200:\n",
        "        print(\"✅ Binance API accessible!\")\n",
        "        print(\"🎯 Ready to backtest!\\n\")\n",
        "    else:\n",
        "        print(f\"⚠️  Unexpected status: {response.status_code}\")\n",
        "        \n",
        "except Exception as e:\n",
        "    print(f\"\\n❌ WARP setup failed: {str(e)[:100]}\")\n",
        "    print(\"\\n⚠️  Trying alternative: SOCKS proxy...\\n\")\n",
        "    \n",
        "    # Fallback: Try free SOCKS proxies\n",
        "    SOCKS_PROXIES = [\n",
        "        \"socks5://8.219.97.248:80\",\n",
        "        \"socks5://47.88.3.19:8080\",\n",
        "        \"socks5://72.195.34.35:4145\",\n",
        "    ]\n",
        "    \n",
        "    working = None\n",
        "    for proxy in SOCKS_PROXIES:\n",
        "        try:\n",
        "            print(f\"Testing: {proxy}\")\n",
        "            test = requests.get(\n",
        "                \"https://api.binance.com/api/v3/ping\",\n",
        "                proxies={\"http\": proxy, \"https\": proxy},\n",
        "                timeout=5\n",
        "            )\n",
        "            if test.status_code == 200:\n",
        "                working = proxy\n",
        "                os.environ['HTTP_PROXY'] = proxy\n",
        "                os.environ['HTTPS_PROXY'] = proxy\n",
        "                print(f\"✅ Working proxy: {proxy}\\n\")\n",
        "                break\n",
        "        except:\n",
        "            print(\"❌ Failed\")\n",
        "    \n",
        "    if not working:\n",
        "        print(\"\\n🚨 ALL METHODS FAILED!\")\n",
        "        print(\"\\n📋 Manual options:\")\n",
        "        print(\"1. Use Kaggle instead of Colab\")\n",
        "        print(\"2. Run locally with VPN\")\n",
        "        print(\"3. Use AWS/DigitalOcean in Europe/Asia\")\n",
        "        print(\"\\n⚠️  Backtest will likely fail with Error 451\")"
    ],
    "execution_count": None,
    "outputs": []
})

# Cell 8: Run backtest (with proxy)
notebook["cells"].append({
    "cell_type": "code",
    "metadata": {},
    "source": [
        "# Run backtest (proxy should bypass Binance blocking)\n",
        "print(\"🚀 Starting backtest...\\n\")\n",
        "print(\"=\"*60)\n",
        "\n",
        "STRATEGY = \"FreqAIHybridStrategy\"\n",
        "TIMERANGE = \"20250901-20251012\"\n",
        "PAIRS = \"BTC/USDT:USDT\"\n",
        "\n",
        "print(f\"Strategy: {STRATEGY}\")\n",
        "print(f\"Timerange: {TIMERANGE}\")\n",
        "print(f\"Pairs: {PAIRS}\")\n",
        "print(\"=\"*60)\n",
        "\n",
        "import os\n",
        "if 'HTTP_PROXY' in os.environ:\n",
        "    print(f\"\\n✅ Using proxy: {os.environ['HTTP_PROXY']}\")\n",
        "else:\n",
        "    print(\"\\n⚠️  No proxy set - may fail!\")\n",
        "\n",
        "print(\"\\n\")\n",
        "\n",
        "!freqtrade backtesting \\\n",
        "    --strategy {STRATEGY} \\\n",
        "    --config config/config.json \\\n",
        "    --freqaimodel LightGBMRegressorMultiTarget \\\n",
        "    --timerange {TIMERANGE} \\\n",
        "    --export trades \\\n",
        "    --datadir user_data/data/binance\n",
        "\n",
        "print(\"\\n✅ Backtest done!\")"
    ],
    "execution_count": None,
    "outputs": []
})

# Cell 9: Save results
notebook["cells"].append({
    "cell_type": "code",
    "metadata": {},
    "source": [
        "# Save to Drive\n",
        "from datetime import datetime\n",
        "import os\n",
        "\n",
        "timestamp = datetime.now().strftime(\"%Y%m%d_%H%M%S\")\n",
        "run_folder = f\"{results_dir}/backtest_{timestamp}\"\n",
        "!mkdir -p \"{run_folder}\"\n",
        "\n",
        "print(f\"💾 Saving...\")\n",
        "\n",
        "if os.path.exists('user_data/backtest_results'):\n",
        "    !cp -r user_data/backtest_results/* \"{run_folder}/\"\n",
        "    print(f\"✅ Saved to: {run_folder}\")\n",
        "    !ls -lh \"{run_folder}\"\n",
        "else:\n",
        "    print(\"⚠️  No results found!\")"
    ],
    "execution_count": None,
    "outputs": []
})

# Cell 9: Markdown outro
notebook["cells"].append({
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "---\n",
        "\n",
        "## 🎉 Done!\n",
        "\n",
        "### 📥 Access results:\n",
        "- Go to Google Drive\n",
        "- Navigate to `FreqAI_Results/`\n",
        "- Download latest folder\n",
        "\n",
        "### 🔁 Run again:\n",
        "1. Edit parameters in Cell 7\n",
        "2. Runtime > Run all\n",
        "\n",
        "### 💡 Tips:\n",
        "- First run: slower (installing)\n",
        "- Later runs: faster (cached)\n",
        "- Upload data to Drive to speed up\n",
        "\n",
        "---"
    ]
})

# Write with proper formatting
with open('Colab_GPU_Backtest.ipynb', 'w', encoding='utf-8') as f:
    json.dump(notebook, f, indent=2, ensure_ascii=False)

print("✅ Notebook created successfully!")
print("\nStructure:")
print("  - 1 intro cell")
print("  - 8 code cells (including proxy setup)")
print("  - 1 outro cell")
print("\nJSON is valid and properly formatted!")

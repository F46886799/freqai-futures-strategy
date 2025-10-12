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
        "# FreqAI GPU Backtest - Offline Mode\\n",
        "\\n",
        "Uses pre-downloaded data from Google Drive (no Binance API needed)\\n",
        "\\n",
        "## Requirements:\\n",
        "1. binance_data.zip uploaded to Google Drive\\n",
        "2. GPU enabled: Runtime > Change runtime type > GPU (T4)\\n",
        "3. Allow Google Drive access"
      ]
    },
    {
      "cell_type": "code",
      "metadata": {"id": "config"},
      "execution_count": None,
      "outputs": [],
      "source": [
        "# Configuration\\n",
        "TIMERANGE = '20250901-20251012'\\n",
        "PAIRS = ['BTC/USDT:USDT']\\n",
        "DRIVE_ZIP_PATH = '/content/drive/MyDrive/FreqAI/binance_data.zip'\\n",
        "\\n",
        "print(f'Timerange: {TIMERANGE}')\\n",
        "print(f'Pairs: {PAIRS}')\\n",
        "print('Data source: Google Drive (Offline)')"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {"id": "gpu-header"},
      "source": ["## GPU Verification"]
    },
    {
      "cell_type": "code",
      "metadata": {"id": "gpu-check"},
      "execution_count": None,
      "outputs": [],
      "source": [
        "import subprocess\\n",
        "import sys\\n",
        "\\n",
        "print('Checking for GPU...')\\n",
        "try:\\n",
        "    result = subprocess.run(['nvidia-smi'], capture_output=True, text=True, check=True)\\n",
        "    print('GPU AVAILABLE!')\\n",
        "    for line in result.stdout.split('\\\\n'):\\n",
        "        if 'Tesla' in line or 'T4' in line or 'MiB' in line:\\n",
        "            print(line)\\n",
        "except Exception:\\n",
        "    print('GPU NOT FOUND!')\\n",
        "    print('Please enable GPU: Runtime > Change runtime type > GPU (T4)')\\n",
        "    sys.exit(1)"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {"id": "mount-header"},
      "source": ["## Mount Google Drive"]
    },
    {
      "cell_type": "code",
      "metadata": {"id": "mount-drive"},
      "execution_count": None,
      "outputs": [],
      "source": [
        "from google.colab import drive\\n",
        "import os\\n",
        "\\n",
        "print('Mounting Google Drive...')\\n",
        "drive.mount('/content/drive', force_remount=True)\\n",
        "\\n",
        "if os.path.exists(DRIVE_ZIP_PATH):\\n",
        "    size_mb = os.path.getsize(DRIVE_ZIP_PATH) / (1024 * 1024)\\n",
        "    print(f'Found binance_data.zip ({size_mb:.1f} MB)')\\n",
        "else:\\n",
        "    print(f'File not found: {DRIVE_ZIP_PATH}')\\n",
        "    print('Please upload binance_data.zip to: MyDrive/FreqAI/')\\n",
        "    sys.exit(1)"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {"id": "install-header"},
      "source": ["## Install Dependencies"]
    },
    {
      "cell_type": "code",
      "metadata": {"id": "install-deps"},
      "execution_count": None,
      "outputs": [],
      "source": [
        "%%capture\\n",
        "!pip install ta-lib-binary\\n",
        "!pip install freqtrade[freqai]"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {"id": "clone-header"},
      "source": ["## Clone Repository & Extract Data"]
    },
    {
      "cell_type": "code",
      "metadata": {"id": "clone-extract"},
      "execution_count": None,
      "outputs": [],
      "source": [
        "import zipfile\\n",
        "\\n",
        "print('Cloning repository...')\\n",
        "!rm -rf freqai-futures-strategy\\n",
        "!git clone https://github.com/aminak58/freqai-futures-strategy.git\\n",
        "%cd freqai-futures-strategy\\n",
        "\\n",
        "print('\\\\nCreating data directory...')\\n",
        "!mkdir -p user_data/data\\n",
        "\\n",
        "print('\\\\nExtracting data...')\\n",
        "with zipfile.ZipFile(DRIVE_ZIP_PATH, 'r') as zip_ref:\\n",
        "    zip_ref.extractall('user_data/data/')\\n",
        "\\n",
        "if os.path.exists('user_data/data/binance'):\\n",
        "    file_count = sum([len(files) for r, d, files in os.walk('user_data/data/binance')])\\n",
        "    print(f'Extracted {file_count} data files')\\n",
        "else:\\n",
        "    print('Data extraction failed!')\\n",
        "    sys.exit(1)"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {"id": "backtest-header"},
      "source": ["## Run GPU-Accelerated Backtest"]
    },
    {
      "cell_type": "code",
      "metadata": {"id": "run-backtest"},
      "execution_count": None,
      "outputs": [],
      "source": [
        "import time\\n",
        "\\n",
        "print('Starting GPU backtest...')\\n",
        "print(f'Timerange: {TIMERANGE}')\\n",
        "print(f'Pairs: {\", \".join(PAIRS)}')\\n",
        "\\n",
        "start_time = time.time()\\n",
        "\\n",
        "!freqtrade backtesting --strategy FreqAIHybridStrategy --config config/config.json --freqaimodel LightGBMRegressorMultiTarget --timerange {TIMERANGE} --export trades\\n",
        "\\n",
        "elapsed = time.time() - start_time\\n",
        "print(f'\\\\nCompleted in {elapsed/60:.1f} minutes')"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {"id": "results-header"},
      "source": ["## Display Results"]
    },
    {
      "cell_type": "code",
      "metadata": {"id": "display-results"},
      "execution_count": None,
      "outputs": [],
      "source": [
        "import json\\n",
        "from pathlib import Path\\n",
        "\\n",
        "results_file = Path('user_data/backtest_results/backtest-result.json')\\n",
        "\\n",
        "if results_file.exists():\\n",
        "    with open(results_file) as f:\\n",
        "        data = json.load(f)\\n",
        "        if 'strategy' in data and 'FreqAIHybridStrategy' in data['strategy']:\\n",
        "            stats = data['strategy']['FreqAIHybridStrategy']\\n",
        "            print('='*70)\\n",
        "            print('BACKTEST RESULTS')\\n",
        "            print('='*70)\\n",
        "            print(f'Total Profit: {stats.get(\"profit_total_abs\")} USDT ({stats.get(\"profit_total\")}%)')\\n",
        "            print(f'Sharpe Ratio: {stats.get(\"sharpe\")}')\\n",
        "            print(f'Max Drawdown: {stats.get(\"max_drawdown\")}%')\\n",
        "            print(f'Total Trades: {stats.get(\"total_trades\")}')\\n",
        "            print(f'Wins: {stats.get(\"wins\")}')\\n",
        "            print(f'Losses: {stats.get(\"losses\")}')\\n",
        "            print(f'Win Rate: {stats.get(\"winrate\")}%')\\n",
        "            print('='*70)\\n",
        "        else:\\n",
        "            print('Strategy results not found!')\\n",
        "else:\\n",
        "    print('Results file not found!')"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {"id": "download-header"},
      "source": ["## Download Results"]
    },
    {
      "cell_type": "code",
      "metadata": {"id": "download-results"},
      "execution_count": None,
      "outputs": [],
      "source": [
        "from google.colab import files\\n",
        "\\n",
        "results_file = Path('user_data/backtest_results/backtest-result.json')\\n",
        "if results_file.exists():\\n",
        "    files.download(str(results_file))\\n",
        "    print('Downloaded!')\\n",
        "else:\\n",
        "    print('No results to download')"
      ]
    }
  ]
}

with open('FreqAI_GPU_Backtest_Offline.ipynb', 'w', encoding='utf-8') as f:
    json.dump(notebook, f, indent=2)

print('Notebook created successfully!')

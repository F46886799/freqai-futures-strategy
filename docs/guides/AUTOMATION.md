# Professional Automation Setup

This document describes the professional SSH tunneling system for remote GPU backtest execution.

## Architecture

```
┌─────────────────┐         ┌──────────────┐         ┌─────────────────┐
│  Local Machine  │         │    Tunnel    │         │  Google Colab   │
│                 │         │  (ngrok/CF)  │         │   (GPU Server)  │
│  ┌───────────┐  │         │              │         │  ┌───────────┐  │
│  │ Executor  │──┼────────▶│  SSH Bridge  │────────▶│  │ Freqtrade │  │
│  │  CLI      │  │         │              │         │  │ Strategy  │  │
│  └───────────┘  │         │              │         │  └───────────┘  │
│        │        │         │              │         │        │        │
│        ▼        │         │              │         │        ▼        │
│  ┌───────────┐  │         │              │         │  ┌───────────┐  │
│  │  Results  │◀─┼─────────│  SFTP/SCP    │◀────────│  │  Results  │  │
│  │   Local   │  │         │              │         │  │   Remote  │  │
│  └───────────┘  │         └──────────────┘         │  └───────────┘  │
└─────────────────┘                                  └─────────────────┘
```

## Components

### 1. Tunnel Manager (`tools/tunnel_manager.py`)

Manages SSH tunnel connection:
- Supports ngrok and cloudflared
- Auto-installation helpers
- Status monitoring
- Configuration management

**Usage**:
```powershell
# Install tunnel client
python tools/tunnel_manager.py install

# Start tunnel
python tools/tunnel_manager.py start

# Check status
python tools/tunnel_manager.py status

# Stop tunnel
python tools/tunnel_manager.py stop
```

### 2. Backtest Executor (`tools/backtest_executor.py`)

Executes backtests on remote GPU:
- SSH connection via tunnel
- Command execution with real-time monitoring
- Automatic result synchronization
- Batch execution support
- Full logging and error handling

**Usage**:
```powershell
# Single backtest
python tools/backtest_executor.py `
  --tunnel-url "tcp://0.tcp.ngrok.io:12345" `
  --strategy FreqAIHybridStrategy `
  --timerange 20250901-20251012 `
  --pairs BTC/USDT:USDT

# Multiple pairs
python tools/backtest_executor.py `
  --tunnel-url "tcp://0.tcp.ngrok.io:12345" `
  --strategy FreqAIHybridStrategy `
  --timerange 20250901-20251012 `
  --pairs BTC/USDT:USDT ETH/USDT:USDT SOL/USDT:USDT
```

### 3. Batch Executor (Python API)

For advanced batch execution:

```python
from tools.backtest_executor import ColabBacktestExecutor, BacktestConfig

# Define configurations
configs = [
    BacktestConfig(
        strategy="FreqAIHybridStrategy",
        timerange="20250901-20251012",
        pairs=["BTC/USDT:USDT"]
    ),
    BacktestConfig(
        strategy="FreqAIHybridStrategy",
        timerange="20250801-20250831",
        pairs=["ETH/USDT:USDT", "SOL/USDT:USDT"]
    ),
]

# Execute batch
executor = ColabBacktestExecutor(tunnel_url="tcp://0.tcp.ngrok.io:12345")
try:
    executor.connect()
    results = executor.execute_batch(configs)
    
    # Analyze results
    for result in results:
        print(f"Strategy: {result['config'].strategy}")
        print(f"Timerange: {result['config'].timerange}")
        print(f"Profit: {result['results']['total_profit_abs']} USDT")
        print(f"Sharpe: {result['results']['sharpe_ratio']}")
        print(f"Drawdown: {result['results']['max_drawdown']}%")
        print("-" * 50)
finally:
    executor.disconnect()
```

## Setup Guide

### Step 1: Install ngrok

1. Download: https://ngrok.com/download
2. Extract to: `C:\Program Files\ngrok\`
3. Add to PATH
4. Get auth token: https://dashboard.ngrok.com/get-started/your-authtoken
5. Authenticate:
```powershell
ngrok authtoken YOUR_AUTH_TOKEN
```

### Step 2: Configure Tunnel

Edit `config/tunnel_config.json`:
```json
{
  "tunnel_type": "ngrok",
  "local_port": 8888,
  "auth_token": "YOUR_NGROK_AUTH_TOKEN",
  "region": "us",
  "protocol": "tcp"
}
```

### Step 3: Prepare Colab Instance

1. Open Colab notebook
2. Enable GPU: Runtime → Change runtime type → GPU (T4)
3. Install SSH server:
```python
# In Colab cell
!apt-get install -y openssh-server
!mkdir -p /var/run/sshd
!echo 'root:password' | chpasswd
!echo 'PermitRootLogin yes' >> /etc/ssh/sshd_config
!echo 'PasswordAuthentication yes' >> /etc/ssh/sshd_config
!service ssh start

# Clone repository
!git clone https://github.com/aminak58/freqai-futures-strategy.git
%cd freqai-futures-strategy

# Install dependencies
!pip install freqtrade[freqai]
```

4. Note the local port (default: 22)

### Step 4: Start Tunnel

```powershell
python tools/tunnel_manager.py start
```

Output will show tunnel URL:
```
✅ Tunnel active: tcp://0.tcp.ngrok.io:12345
```

### Step 5: Execute Backtest

```powershell
python tools/backtest_executor.py `
  --tunnel-url "tcp://0.tcp.ngrok.io:12345" `
  --strategy FreqAIHybridStrategy `
  --timerange 20250901-20251012 `
  --pairs BTC/USDT:USDT
```

### Step 6: Monitor Progress

The executor will show real-time progress:
```
2025-10-13 01:15:23 - INFO - Connecting to Colab via tunnel...
2025-10-13 01:15:25 - INFO - ✅ Connected to Colab
2025-10-13 01:15:26 - INFO - Starting backtest: FreqAIHybridStrategy - 20250901-20251012
2025-10-13 01:15:27 - INFO - Command: freqtrade backtesting --strategy FreqAIHybridStrategy ...
2025-10-13 01:15:30 - INFO - Training model for BTC/USDT:USDT...
2025-10-13 01:18:42 - INFO - Backtesting pair 1/1: BTC/USDT:USDT...
2025-10-13 01:32:15 - INFO - Results downloaded: backtest_results/backtest_FreqAIHybridStrategy_20250901-20251012_20251013_013215.json
2025-10-13 01:32:15 - INFO - ✅ Backtest completed in 16.8 minutes
```

### Step 7: Review Results

Results are automatically downloaded to `backtest_results/`:
```
backtest_results/
├── backtest_FreqAIHybridStrategy_20250901-20251012_20251013_013215.json
└── batch_results_20251013_013230.json
```

## Benefits

### vs. Manual Notebook Execution

| Aspect | Manual Notebook | Professional Automation |
|--------|----------------|------------------------|
| **Scalability** | 1 backtest at a time | Batch execution |
| **Monitoring** | Manual checking | Real-time logs |
| **Error Handling** | Manual retry | Automatic retry |
| **Result Sync** | Manual download | Automatic download |
| **Reproducibility** | Low | High |
| **Professional** | ❌ Amateur | ✅ Professional |

### Advantages

1. **Structured**: Clear command interface
2. **Monitored**: Real-time progress tracking
3. **Automated**: No manual intervention needed
4. **Scalable**: Batch execution support
5. **Reliable**: Error handling and recovery
6. **Professional**: Production-ready code

## Troubleshooting

### Tunnel won't start

```powershell
# Check if ngrok is installed
ngrok version

# Check if auth token is set
ngrok config check

# Try alternative: cloudflared
# Edit config/tunnel_config.json: "tunnel_type": "cloudflared"
```

### Can't connect to Colab

1. Verify SSH server is running in Colab
2. Check tunnel URL is correct
3. Verify firewall settings
4. Try alternative port

### Backtest fails

1. Check Colab has data files
2. Verify strategy file exists
3. Check GPU is available
4. Review executor logs

## Advanced Usage

### Custom SSH Key

```powershell
python tools/backtest_executor.py `
  --tunnel-url "tcp://0.tcp.ngrok.io:12345" `
  --ssh-key "C:\Users\YourUser\.ssh\id_rsa" `
  --strategy FreqAIHybridStrategy `
  --timerange 20250901-20251012
```

### Environment Variables

```powershell
# Set ngrok token via environment
$env:NGROK_AUTH_TOKEN = "your_token_here"
python tools/tunnel_manager.py start
```

### Batch with Different Models

```python
from tools.backtest_executor import BacktestConfig

configs = [
    BacktestConfig(
        strategy="FreqAIHybridStrategy",
        timerange="20250901-20251012",
        pairs=["BTC/USDT:USDT"],
        freqai_model="LightGBMRegressorMultiTarget"
    ),
    BacktestConfig(
        strategy="FreqAIHybridStrategy",
        timerange="20250901-20251012",
        pairs=["BTC/USDT:USDT"],
        freqai_model="CatboostRegressorMultiTarget"  # Different model
    ),
]
```

## Security Notes

1. **Never commit auth tokens** to git
2. Use environment variables for sensitive data
3. Rotate auth tokens regularly
4. Use SSH keys instead of passwords
5. Keep tunnel URLs private

## Future Enhancements

- [ ] Web dashboard for monitoring
- [ ] Slack/Discord notifications
- [ ] Automatic parameter optimization
- [ ] Result comparison and analysis
- [ ] Multi-GPU support
- [ ] Cost tracking and optimization

---

**This is how professional automation should be done.**

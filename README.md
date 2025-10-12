# FreqAI Futures Strategy

Professional machine learning-based trading strategy for Binance USDT-M Perpetual Futures using FreqAI + LightGBM.

## Features

- **ML-powered predictions**: LightGBM multi-target regression with GPU acceleration
- **Market regime detection**: Trend, volatility, and volume analysis
- **80+ technical indicators**: Multi-timeframe feature engineering
- **Dynamic leverage**: Confidence-based position sizing
- **Professional automation**: SSH tunneling for remote GPU execution
- **Comprehensive testing**: 33% coverage → targeting 80%+

## Project Structure

```
freqai-futures-strategy/
├── config/                  # Configuration files
│   ├── config.json         # Freqtrade config
│   └── tunnel_config.json  # SSH tunnel config
├── user_data/
│   └── strategies/
│       └── FreqAIHybridStrategy.py  # Main strategy
├── tools/                   # Automation tools
│   ├── tunnel_manager.py   # SSH tunnel manager  
│   └── backtest_executor.py # Remote backtest executor
├── tests/                   # Test suite
├── monitoring/              # Performance monitoring
└── docs/                    # Documentation
    ├── guides/             # Setup and usage guides
    ├── architecture/       # Technical architecture
    └── deprecated/         # Archived documentation
```

## Quick Start

### 1. Setup Environment

```powershell
# Create virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### 2. Download Historical Data

```powershell
freqtrade download-data `
  --exchange binance `
  --pairs BTC/USDT:USDT ETH/USDT:USDT SOL/USDT:USDT `
  --timeframes 5m 15m 1h `
  --days 365 `
  --trading-mode futures `
  --config config/config.json
```

### 3. Run Tests

```powershell
pytest tests/ --cov=user_data/strategies --cov-report=term-missing
```

### 4. Local Backtest (CPU)

```powershell
freqtrade backtesting `
  --strategy FreqAIHybridStrategy `
  --config config/config.json `
  --freqaimodel LightGBMRegressorMultiTarget `
  --timerange 20250901-20251012 `
  --export trades
```

## Professional GPU Automation

### Why Tunneling?

Manual notebook execution is:
- ❌ Not scalable for multiple backtests
- ❌ Error-prone (file mounting, Drive access)
- ❌ Unprofessional and inefficient

Our solution:
- ✅ Automated SSH tunnel via ngrok/cloudflared
- ✅ Structured command execution with monitoring
- ✅ Automatic result synchronization
- ✅ Batch execution support
- ✅ Full logging and error handling

### Setup Tunnel

1. **Install ngrok**:
```powershell
# Download from https://ngrok.com/download
# Extract to C:\Program Files\ngrok\
# Add to PATH
ngrok authtoken YOUR_AUTH_TOKEN
```

2. **Configure tunnel**:
```json
// config/tunnel_config.json
{
  "tunnel_type": "ngrok",
  "local_port": 8888,
  "auth_token": "YOUR_NGROK_TOKEN",
  "region": "us"
}
```

3. **Start tunnel**:
```powershell
python tools/tunnel_manager.py start
# Output: ✅ Tunnel active: tcp://0.tcp.ngrok.io:12345
```

### Execute Remote Backtest

**Single backtest**:
```powershell
python tools/backtest_executor.py `
  --tunnel-url "tcp://0.tcp.ngrok.io:12345" `
  --strategy FreqAIHybridStrategy `
  --timerange 20250901-20251012 `
  --pairs BTC/USDT:USDT
```

**Batch execution**:
```python
from tools.backtest_executor import ColabBacktestExecutor, BacktestConfig

# Define backtest configurations
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

# Execute all backtests
executor = ColabBacktestExecutor(tunnel_url="tcp://0.tcp.ngrok.io:12345")
executor.connect()
results = executor.execute_batch(configs)
executor.disconnect()

# Results automatically saved to backtest_results/
```

### Monitoring

All executions are logged with:
- Real-time progress updates
- Execution time tracking
- Automatic result download
- Error handling and recovery
- JSON result files with timestamps

```powershell
# View tunnel status
python tools/tunnel_manager.py status

# Stop tunnel
python tools/tunnel_manager.py stop
```

## Strategy Details

**FreqAIHybridStrategy** features:
- **Market Regime Detection**: Trend/volatility/volume classification
- **ML Predictions**: LightGBM multi-target (ROI, stop-loss, position size)
- **Technical Indicators**: RSI, MACD, Bollinger Bands, ATR, Fibonacci, Volume
- **Multi-timeframe**: 5m (primary) + 15m + 1h analysis
- **Risk Management**: Dynamic leverage, adaptive stop-loss, confidence filtering

## Development

### Testing

```powershell
# Run all tests
pytest tests/

# With coverage report
pytest tests/ --cov=user_data/strategies --cov-report=html

# View coverage: htmlcov/index.html
```

### CI/CD

GitHub Actions workflows:
- `1-tests.yml`: Run test suite on every push
- `2-docker.yml`: Build and push Docker images
- `3-strategy-validation.yml`: Validate strategy logic

### Monitoring

```powershell
cd monitoring
python compare_versions.py  # Compare strategy versions
python generate_report.py   # Generate performance report
```

## Documentation

- **Setup Guide**: `docs/guides/SETUP_GUIDE.md`
- **Architecture**: `docs/architecture/UNIFIED_ARCHITECTURE.md`
- **Glossary**: `docs/guides/GLOSSARY.md`
- **FAQ**: `docs/guides/FAQ.md`

## Current Status

- ✅ Strategy implemented with FreqAI
- ✅ Inf/nan bugs fixed
- ✅ CI/CD pipelines working
- ✅ Professional SSH tunneling system
- ✅ Automated backtest executor
- 🔄 Test coverage: 33% → Target: 80%+
- 📋 Phase 2: LSTM implementation

## Technology Stack

- **Trading**: Freqtrade 2025.9.1
- **ML**: LightGBM with GPU support
- **Automation**: ngrok/cloudflared tunneling
- **Testing**: pytest + coverage
- **CI/CD**: GitHub Actions
- **Monitoring**: Custom analytics tools

## Requirements

- Python 3.11+
- Freqtrade 2025.9.1
- TA-Lib
- LightGBM
- ngrok (for remote execution)
- Docker (optional)

## License

MIT License

## Support

For issues:
1. Check `docs/guides/FAQ.md`
2. Review GitHub Issues
3. Create new issue with details

---

**Built with professional standards. No amateur solutions.**

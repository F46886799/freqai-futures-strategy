# FreqAI Futures Strategy

[![CI/CD](https://github.com/aminak58/freqai-futures-strategy/workflows/3-backtest/badge.svg)](https://github.com/aminak58/freqai-futures-strategy/actions)
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Self-governing AI trading system** for Binance USDT-M Perpetual Futures with autonomous risk management, drift detection, and adaptive retraining.

Built with FreqAI + LightGBM + comprehensive governance layer.

## ✨ Key Features

### 🤖 Core Trading Intelligence
- **ML-powered predictions**: LightGBM multi-target regression (next 5/15/60-min returns)
- **Market regime detection**: Trend/volatility/volume-based context awareness
- **80+ technical indicators**: Multi-timeframe feature engineering (5m/15m/1h)
- **Dynamic leverage**: Confidence-based position sizing (2-5x)
- **Adaptive stops**: ATR-based dynamic stop-loss with governance constraints

### 🛡️ Autonomous Governance System
- **Hard risk constraints**: 2% daily loss cap, 10% MDD limit, position sizing caps
- **Performance monitoring**: Real-time PF/Sharpe/WinRate/MDD tracking
- **Drift detection**: PSI (feature drift) + ADWIN (concept drift)
- **Adaptive risk scaling**: warn (0.75×) → degrade (0.5×) → halt (0×)
- **Intelligent retraining**: 12h base cadence + event-driven triggers
- **State machine**: none → warn → degrade → halt → resume with cooldown logic

### 🔧 Development Infrastructure
- **Windows-native development**: Local Python 3.11 + venv
- **CI/CD automation**: GitHub Actions with governance integration
- **Comprehensive testing**: pytest with governance scenarios
- **Production-ready monitoring**: Metrics extraction, decision logging, audit trail

## 📁 Project Structure

```
freqai-futures-strategy/
├── config/
│   ├── config.json                # Freqtrade configuration
│   └── governance_policy.yaml     # Risk & retraining policy
├── user_data/strategies/
│   └── FreqAIHybridStrategy.py    # Main strategy (543 lines)
├── monitoring/
│   ├── governance_decider.py      # Decision engine (495 lines)
│   ├── governance_runtime.py      # Runtime adapter (74 lines)
│   ├── extract_metrics.py         # Metrics extraction
│   ├── compare_versions.py        # Performance comparison
│   ├── generate_report.py         # Report generation
│   └── retrain_scheduler.py       # Retraining coordinator
├── tests/
│   ├── test_strategy_logic.py     # Strategy unit tests
│   ├── test_governance_decider.py # Governance tests (4/4 passing)
│   └── test_integration.py        # Integration tests
├── docs/
│   ├── guides/                    # Setup and development guides
│   ├── architecture/              # Technical architecture docs
│   ├── sessions/                  # Development session notes
│   └── deprecated/                # Archived documentation
├── .github/workflows/
│   ├── 1-code-quality.yml         # Linting & formatting
│   ├── 2-unit-tests.yml           # Pytest execution
│   ├── 3-backtest.yml             # Backtest + governance
│   └── 4-performance-tracking.yml # Metrics tracking
└── GOVERNANCE_INTEGRATION_SUMMARY.md  # Complete governance spec
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

### 4. Run Backtest

```powershell
freqtrade backtesting `
  --strategy FreqAIHybridStrategy `
  --config config/config.json `
  --freqaimodel LightGBMRegressorMultiTarget `
  --timerange 20250901-20251012 `
  --export trades
```

### 5. Run Governance Analysis

```powershell
# Extract metrics from backtest output
python monitoring/extract_metrics.py backtest_results/backtest-result-*.json

# Run governance decision engine
python monitoring/governance_decider.py `
  --policy config/governance_policy.yaml `
  --latest monitoring/latest_metrics.json `
  --history monitoring/metrics_history.csv `
  --out monitoring/governance_decisions.jsonl

# Check governance status
python -c "from monitoring.governance_runtime import get_governance_state; state = get_governance_state(); print(f'Status: {state.status}, Risk: {state.risk_multiplier}x')"
```

### 6. Check Retraining Schedule

```powershell
# Check if retraining is due
python monitoring/retrain_scheduler.py --dry-run

# Force retrain (if needed)
python monitoring/retrain_scheduler.py --force
```

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
- **Governance Integration**: Real-time risk adaptation based on performance metrics

## Governance System

The strategy includes an autonomous governance layer that monitors performance and adapts risk in real-time:

### Features

- **Performance Monitoring**: Tracks Profit Factor, Sharpe Ratio, Win Rate, Max Drawdown
- **Drift Detection**: PSI (Population Stability Index) and concept drift detection
- **Automatic Risk Adjustment**: Dynamically scales position sizes and leverage
- **Retraining Triggers**: Schedules model retraining based on performance degradation
- **Hard Constraints**: Enforces max leverage, stop-loss bounds, and exposure limits

### Status Levels

| Status | Entry | Shorts | Risk Multiplier | Stops |
|--------|-------|--------|----------------|-------|
| **Normal** | ✅ Full | ✅ Enabled | 1.0x | Base ATR |
| **Warn** | ✅ Reduced | ✅ Enabled | 0.75x | Base ATR |
| **Degrade** | ✅ Reduced | ❌ Disabled | 0.5x | ATR × 1.25 |
| **Halt** | ❌ Blocked | ❌ Blocked | 0x | N/A |

### Quick Start

After running a backtest:

```powershell
# 1. Extract metrics
python monitoring/extract_metrics.py backtest_output.txt

# 2. Run governance decision
python monitoring/governance_decider.py `
  --policy config/governance_policy.yaml `
  --latest monitoring/latest_metrics.json `
  --history monitoring/metrics_history.csv `
  --out monitoring/governance_decisions.jsonl

# 3. Strategy automatically reads last decision on next run
```

**See `GOVERNANCE_QUICKSTART.md` for complete setup and tuning guide.**

## Development

### Testing

## 🧪 Testing & Validation

```powershell
# Run all tests
pytest tests/ -v

# With coverage report
pytest tests/ --cov=user_data/strategies --cov=monitoring --cov-report=html

# View coverage report
start htmlcov/index.html

# Run specific test suite
pytest tests/test_governance_decider.py -v
```

**Current Test Status:**
- ✅ Strategy logic tests
- ✅ Governance decider tests (4/4 passing)
- ✅ Integration tests
- 📊 Coverage: ~33% → Target: 80%+

## 🚀 CI/CD Pipeline

GitHub Actions workflows automatically run on every push/PR:

1. **Code Quality** (`1-code-quality.yml`):
   - Linting with flake8
   - Format checking with black
   - Type checking with mypy

2. **Unit Tests** (`2-unit-tests.yml`):
   - pytest execution
   - Coverage reporting
   - Artifact upload

3. **Backtest + Governance** (`3-backtest.yml`):
   - Download MTF data (5m/15m/1h)
   - Run backtest
   - Extract metrics
   - **Run governance_decider** → decisions.jsonl
   - Upload artifacts (results + metrics + decisions)
   - Display governance status in summary/PR comments

4. **Performance Tracking** (`4-performance-tracking.yml`):
   - Historical performance comparison
   - Metrics trending
   - Automated reporting

## 📊 Monitoring & Analytics

```powershell
# Extract metrics from backtest
python monitoring/extract_metrics.py backtest_results/backtest-result-*.json

# Compare strategy versions
python monitoring/compare_versions.py --baseline v1.0 --current v1.1

# Generate performance report
python monitoring/generate_report.py --output reports/monthly_report.html
```

## 📚 Documentation

### Core Documentation
- **[Governance Integration Summary](GOVERNANCE_INTEGRATION_SUMMARY.md)** - Complete governance system spec
- **[Governance Quickstart](GOVERNANCE_QUICKSTART.md)** - Quick start guide for governance
- **[Governance Spec](monitoring/GOVERNANCE_SPEC.md)** - Technical design document

### Development Guides
- **[Setup Guide](docs/guides/SETUP_GUIDE.md)** - Complete setup instructions
- **[Development Guide](docs/guides/DEVELOPMENT_GUIDE.md)** - Development workflow
- **[CI/CD Guide](docs/guides/CI_CD_GUIDE.md)** - CI/CD pipeline documentation
- **[Current Status](docs/guides/CURRENT_STATUS.md)** - Project status tracker

### Architecture & Design
- **[Unified Architecture](docs/architecture/UNIFIED_ARCHITECTURE.md)** - Complete system architecture
- **[LSTM Architecture](docs/architecture/LSTM_ARCHITECTURE_DESIGN.md)** - LSTM design considerations
- **[Regime Detection](docs/architecture/REGIME_DETECTION_ALIGNMENT.md)** - Regime detection design
- **[MVP Documentation](docs/architecture/MVP_DOCUMENTATION.md)** - MVP scope and features

### Reference
- **[Glossary](docs/guides/GLOSSARY.md)** - Technical terms and definitions
- **[FAQ](docs/guides/FAQ.md)** - Frequently asked questions
- **[Roadmap](docs/deprecated/ROADMAP.md)** - Development roadmap (archived)

## 📈 Current Status

### ✅ Completed
- FreqAI strategy with LightGBM multi-target regression
- Market regime detection (trend/volatility/volume)
- 80+ technical indicators across multiple timeframes
- Dynamic leverage and adaptive stop-loss
- **Comprehensive governance system:**
  - Hard risk constraints (2% daily loss, 10% MDD)
  - Performance monitoring (PF/Sharpe/WinRate/MDD)
  - Drift detection (PSI + ADWIN)
  - Adaptive risk scaling (warn/degrade/halt/resume)
  - Intelligent retraining scheduler
  - CI/CD integration
- Testing framework (33% coverage)
- CI/CD pipelines with automated governance

### 🔄 In Progress
- Increasing test coverage to 80%+
- Documentation refinement
- Evaluation protocol (walk-forward CV)

### 📋 Next Phase: RL Integration
**Staged approach:**
1. **Contextual Bandit** (Phase 1):
   - Action: entry/exit/hold decisions
   - Context: regime + features + governance state
   - Reward: risk-adjusted returns with safety penalties
   - Safety: Hard constraints from governance

2. **Actor-Critic** (Phase 2):
   - Policy: position sizing + timing
   - Value: risk-adjusted Q-values
   - Training: Offline with replay buffer
   - Integration: Via FreqAI custom model

3. **Production Deployment** (Phase 3):
   - Online fine-tuning with safety constraints
   - A/B testing against baseline
   - Gradual rollout with monitoring

**Prerequisites (current focus):**
- [ ] Define evaluation protocol (walk-forward + time-series CV)
- [ ] Design signal audit diagnostics
- [ ] Review and baseline repository state
- [ ] Create Agile/Scrum framework for RL development

## 🛠️ Technology Stack

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| Trading Framework | Freqtrade | 2025.10-dev | Core trading engine |
| ML Framework | FreqAI | Latest | Model training & prediction |
| ML Model | LightGBM | Latest | Multi-target regression |
| Exchange | Binance | CCXT 4.5.6 | USDT-M Perpetual Futures |
| Language | Python | 3.11.9 | Core development |
| Testing | pytest + coverage | Latest | Unit & integration tests |
| CI/CD | GitHub Actions | - | Automated workflows |
| Monitoring | Custom Python | - | Metrics & governance |
| Config | PyYAML | 6.0.2 | Policy configuration |
| Environment | Windows + venv | - | Local development |

## 📦 Requirements

### Core Dependencies
```
freqtrade==2025.10.dev
ccxt==4.5.6
lightgbm>=4.0.0
ta-lib>=0.4.28
numpy>=1.24.0
pandas>=2.0.0
scikit-learn>=1.3.0
PyYAML==6.0.2
```

### Development Dependencies
```
pytest>=7.4.0
pytest-cov>=4.1.0
black>=23.0.0
flake8>=6.0.0
mypy>=1.5.0
```

### Installation
```powershell
# Core dependencies
pip install -r requirements.txt

# Development dependencies
pip install -r requirements-dev.txt
```

## 🤝 Contributing

This is a private research project. For collaboration:
1. Review documentation in `docs/`
2. Check current status and roadmap
3. Follow existing code standards
4. Write tests for new features
5. Update documentation

## 📄 License

MIT License - see LICENSE file for details

## 💬 Support & Contact

**Issues & Bugs:**
1. Check `docs/guides/FAQ.md`
2. Search existing GitHub Issues
3. Create new issue with:
   - Clear description
   - Steps to reproduce
   - Expected vs actual behavior
   - Environment details

**Questions:**
- Review documentation first
- Check session notes in `docs/sessions/`
- Consult architecture docs in `docs/architecture/`

---

**Built with professional standards. Self-governing AI with transparent governance.**

*Last updated: October 13, 2025*

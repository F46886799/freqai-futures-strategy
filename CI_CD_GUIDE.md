# 🚀 راهنمای کامل CI/CD برای FreqAI Strategy

## 📋 فهرست مطالب

1. [معرفی](#معرفی)
2. [معماری CI/CD](#معماری-cicd)
3. [GitHub Actions Workflows](#github-actions-workflows)
4. [سیستم Monitoring](#سیستم-monitoring)
5. [Testing Framework](#testing-framework)
6. [راه‌اندازی](#راه‌اندازی)
7. [استفاده روزمره](#استفاده-روزمره)
8. [Troubleshooting](#troubleshooting)

---

## 🎯 معرفی

این سیستم CI/CD برای **توسعه قابل رصد و تکرارپذیر** استراتژی FreqAI طراحی شده است.

### مزایای کلیدی

✅ **Automated Testing**: هر commit تست می‌شود  
✅ **Performance Tracking**: metrics در طول زمان ردیابی می‌شوند  
✅ **Version Comparison**: مقایسه خودکار versions  
✅ **Quality Assurance**: code quality چک می‌شود  
✅ **Reproducibility**: نتایج قابل تکرار هستند  

---

## 🏗️ معماری CI/CD

```
┌─────────────────────────────────────────────────────────────┐
│                    Developer Workflow                        │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
                      ┌───────────────┐
                      │  Git Push     │
                      └───────┬───────┘
                              │
                    ┌─────────┴─────────┐
                    ▼                   ▼
        ┌─────────────────┐   ┌─────────────────┐
        │ Code Quality    │   │  Unit Tests     │
        │ - Linting       │   │ - Strategy      │
        │ - Formatting    │   │ - Config        │
        │ - Security      │   │ - Integration   │
        └────────┬────────┘   └────────┬────────┘
                 │                     │
                 └──────────┬──────────┘
                            ▼
                   ┌─────────────────┐
                   │  Backtest       │
                   │ - Data Download │
                   │ - Run Backtest  │
                   │ - Extract Metrics│
                   └────────┬────────┘
                            │
                            ▼
                   ┌─────────────────┐
                   │ Performance     │
                   │ - Track Metrics │
                   │ - Compare Versions│
                   │ - Generate Report│
                   └─────────────────┘
```

---

## 🔄 GitHub Actions Workflows

### 1. Code Quality & Linting

**File:** `.github/workflows/1-code-quality.yml`

**Trigger:** هر push یا PR

**مراحل:**
1. ✅ Check code formatting (Black)
2. ✅ Check import sorting (isort)
3. ✅ Lint با flake8
4. ✅ Lint با pylint
5. ✅ Type check با mypy
6. ✅ Security scan با bandit

**زمان اجرا:** ~2-3 دقیقه

**مثال خروجی:**
```
✅ Syntax checks completed
✅ Linting completed
✅ Type checking completed
✅ Security scan completed
```

---

### 2. Unit Tests

**File:** `.github/workflows/2-unit-tests.yml`

**Trigger:** هر push یا PR

**مراحل:**
1. ✅ Test روی Python 3.10 & 3.11
2. ✅ Run unit tests با coverage
3. ✅ Test strategy import
4. ✅ Validate configuration

**زمان اجرا:** ~3-5 دقیقه

**Coverage Target:** > 70%

---

### 3. Automated Backtest

**File:** `.github/workflows/3-backtest.yml`

**Trigger:** 
- Push به master
- Manual dispatch
- تغییر در strategy یا config

**مراحل:**
1. 📥 Pull Docker image
2. 📊 Download historical data (90 days)
3. 🚀 Run backtest
4. 📈 Parse results
5. 💾 Upload artifacts
6. 📝 Comment on PR

**زمان اجرا:** ~15-30 دقیقه

**Artifacts:**
- `backtest_output.txt`
- `backtest-results-*.json`
- Performance metrics

---

### 4. Performance Tracking

**File:** `.github/workflows/4-performance-tracking.yml`

**Trigger:**
- Push به master
- هفتگی (Sundays 00:00 UTC)
- Manual dispatch

**مراحل:**
1. 📊 Download 180-day data
2. 🚀 Run comprehensive backtest
3. 📈 Extract metrics
4. 💾 Save to history
5. 📊 Generate HTML report
6. 📉 Compare with previous runs

**زمان اجرا:** ~30-60 دقیقه

**Artifacts:**
- `metrics_history.csv`
- `performance_report.html`
- Comparison charts

---

## 📊 سیستم Monitoring

### Structure

```
monitoring/
├── extract_metrics.py      # استخراج metrics از backtest
├── generate_report.py      # تولید گزارش HTML
├── compare_versions.py     # مقایسه versions
├── metrics_history.csv     # تاریخچه metrics (auto-generated)
├── latest_metrics.json     # آخرین metrics (auto-generated)
└── README.md              # مستندات monitoring
```

### Metrics Tracked

| Metric | توضیح | Target |
|--------|-------|--------|
| Total Profit % | سود کل | > 10% |
| Win Rate % | نرخ برد | > 50% |
| Total Trades | تعداد معاملات | > 100 |
| Sharpe Ratio | Risk-adjusted return | > 1.0 |
| Max Drawdown % | حداکثر افت | < -15% |
| Avg Duration | میانگین مدت معامله | - |

### استفاده

```bash
# استخراج metrics
python monitoring/extract_metrics.py backtest_output.txt

# تولید گزارش
python monitoring/generate_report.py

# مقایسه versions
python monitoring/compare_versions.py
```

---

## 🧪 Testing Framework

### Test Structure

```
tests/
├── test_strategy_logic.py
│   ├── TestStrategyBasics
│   ├── TestDataFrameGeneration
│   ├── TestMarketRegimeDetection
│   ├── TestEntryExitSignals
│   ├── TestRiskManagement
│   └── TestConfiguration
└── test_integration.py
    ├── TestDockerIntegration
    ├── TestConfigurationIntegration
    ├── TestFileStructure
    └── TestMonitoringSystem
```

### Running Tests

```bash
# تمام تست‌ها
pytest tests/ -v

# با coverage
pytest tests/ -v --cov=user_data/strategies --cov-report=html

# تست خاص
pytest tests/test_strategy_logic.py::TestStrategyBasics -v
```

### Test Coverage

**Current Target:** 70%+

**Coverage Report:**
```bash
# Generate HTML report
pytest tests/ --cov=user_data/strategies --cov-report=html

# Open report
start htmlcov/index.html  # Windows
```

---

## 🚀 راه‌اندازی

### پیش‌نیازها

✅ GitHub repository  
✅ GitHub Actions enabled  
✅ Python 3.10+ (local)  
✅ Docker Desktop (local)  

### مرحله 1: Push به GitHub

```bash
# Add all files
git add .

# Commit
git commit -m "Add CI/CD infrastructure"

# Push
git push origin master
```

### مرحله 2: بررسی Workflows

1. رفتن به GitHub repository
2. کلیک روی tab "Actions"
3. مشاهده workflows در حال اجرا

### مرحله 3: Local Setup

```bash
# Install testing dependencies
pip install pytest pytest-cov pytest-asyncio pytest-mock

# Install monitoring dependencies
pip install pandas numpy matplotlib

# Install dev dependencies
pip install black flake8 pylint isort mypy bandit

# Run tests locally
pytest tests/ -v
```

---

## 💼 استفاده روزمره

### Workflow توسعه‌دهنده

#### 1. شروع کار روی Feature جدید

```bash
# Create branch
git checkout -b feature/lstm-model

# Make changes
# ...

# Run tests locally
pytest tests/ -v

# Check code quality
flake8 user_data/strategies/
black --check user_data/strategies/

# Commit
git add .
git commit -m "Add LSTM model implementation"

# Push
git push origin feature/lstm-model
```

#### 2. بررسی CI Results

1. رفتن به GitHub → Actions
2. مشاهده workflow runs
3. بررسی:
   - ✅ Code Quality passed
   - ✅ Unit Tests passed
   - ✅ Backtest completed

#### 3. مقایسه Performance

```bash
# Download artifacts از GitHub Actions
# یا run local:

# Run backtest
docker run --rm \
  -v ${PWD}/user_data:/freqtrade/user_data \
  -v ${PWD}/config:/freqtrade/config \
  freqtradeorg/freqtrade:stable_freqairl backtesting \
  --strategy FreqAIHybridStrategy \
  --config /freqtrade/config/config.json \
  --timerange 20241001-20250101 \
  2>&1 | tee backtest_output.txt

# Extract metrics
python monitoring/extract_metrics.py backtest_output.txt

# Compare
python monitoring/compare_versions.py
```

#### 4. Merge به Master

```bash
# Create PR
gh pr create --title "Add LSTM Model" --body "Description..."

# بعد از review و CI pass
gh pr merge
```

---

## 📈 Performance Dashboard

### مشاهده گزارش‌ها

#### در GitHub Actions

1. رفتن به Actions → Performance Tracking
2. انتخاب latest run
3. Scroll down به Artifacts
4. Download `performance-tracking-*`
5. Extract و باز کردن `performance_report.html`

#### Local Generation

```bash
# Generate report
python monitoring/generate_report.py

# Open in browser
start monitoring/performance_report.html  # Windows
open monitoring/performance_report.html   # Mac/Linux
```

### گزارش HTML شامل:

- 📊 Key metrics (Profit, Win Rate, Trades, Drawdown)
- 📈 Historical performance table
- 🎨 Visual charts (if matplotlib installed)
- 📉 Trend analysis
- 🏆 Best performance records

---

## 🔧 Troubleshooting

### مشکل 1: Workflow Failed

**علائم:**
- ❌ Red X در GitHub Actions
- Build failed

**راه حل:**
```bash
# 1. بررسی logs در GitHub
# کلیک روی failed job → مشاهده error

# 2. اجرای local
pytest tests/ -v
flake8 user_data/strategies/

# 3. Fix و push مجدد
git add .
git commit -m "Fix CI issues"
git push
```

### مشکل 2: Backtest Timeout

**علائم:**
- Workflow timeout after 120 min

**راه حل:**
```yaml
# Edit .github/workflows/3-backtest.yml
# کاهش timerange یا days:

--days 30  # به جای 90
```

### مشکل 3: Out of Disk Space

**علائم:**
- Docker pull failed
- No space left

**راه حل:**
Workflow automatically cleans up, but if still failing:
```yaml
# در workflow، اضافه کردن:
- name: Clean up space
  run: |
    docker system prune -af
    df -h
```

### مشکل 4: Tests Failing Locally

**علائم:**
- Tests pass in CI but fail locally

**راه حل:**
```bash
# 1. بررسی Python version
python --version  # باید 3.10+ باشد

# 2. Install fresh dependencies
pip install -r requirements.txt --force-reinstall

# 3. Clear pytest cache
rm -rf .pytest_cache
pytest tests/ -v
```

### مشکل 5: Metrics Not Extracted

**علائم:**
- CSV file empty
- No metrics in report

**راه حل:**
```bash
# 1. بررسی output file format
cat backtest_output.txt | grep -i "summary"

# 2. اجرای با debug
python monitoring/extract_metrics.py backtest_output.txt --debug

# 3. Manual extraction
# Edit extract_metrics.py regex patterns
```

---

## 🎓 Best Practices

### Development

1. ✅ **Test Before Commit**: همیشه local tests اجرا کنید
2. ✅ **Small Commits**: commit های کوچک و focused
3. ✅ **Descriptive Messages**: پیام‌های واضح برای commits
4. ✅ **Feature Branches**: برای هر feature یک branch

### Testing

1. ✅ **Write Tests First**: TDD approach
2. ✅ **High Coverage**: > 70% coverage target
3. ✅ **Integration Tests**: برای changes بزرگ
4. ✅ **Mock External Dependencies**: سرعت بالاتر

### Monitoring

1. ✅ **Track All Backtests**: ذخیره metrics بعد از هر run
2. ✅ **Weekly Reviews**: بررسی هفتگی performance
3. ✅ **Set Thresholds**: alert برای performance degradation
4. ✅ **Document Changes**: توضیح تغییرات مهم

### CI/CD

1. ✅ **Fast Feedback**: workflows سریع (< 30 min)
2. ✅ **Clear Failures**: error messages واضح
3. ✅ **Artifact Retention**: نگهداری نتایج برای 30-90 روز
4. ✅ **Manual Triggers**: امکان اجرای manual

---

## 📊 Metrics & KPIs

### Development Metrics

| Metric | Target | Current |
|--------|--------|---------|
| Test Coverage | > 70% | TBD |
| Build Time | < 30 min | ~20 min |
| Test Success Rate | > 95% | TBD |
| Code Quality Score | A | TBD |

### Strategy Performance

| Metric | Target | Notes |
|--------|--------|-------|
| Sharpe Ratio | > 1.0 | Risk-adjusted |
| Max Drawdown | < -15% | Risk management |
| Win Rate | > 50% | Consistency |
| Total Profit | > 10% | Per 3 months |

---

## 🔮 آینده و Roadmap

### Phase 1: ✅ MVP (Completed)
- ✅ GitHub Actions workflows
- ✅ Testing framework
- ✅ Monitoring system
- ✅ Documentation

### Phase 2: 🔄 Enhancement (Next)
- [ ] Docker build caching
- [ ] Performance benchmarking
- [ ] Automated deployment
- [ ] Slack/Discord notifications

### Phase 3: 🔮 Advanced (Future)
- [ ] A/B testing framework
- [ ] ML model versioning
- [ ] Real-time monitoring dashboard
- [ ] Auto-rollback on regression

---

## 📚 منابع اضافی

### Documentation
- [GitHub Actions Docs](https://docs.github.com/en/actions)
- [Pytest Documentation](https://docs.pytest.org/)
- [Freqtrade Docs](https://www.freqtrade.io/)

### Related Files
- [Monitoring README](monitoring/README.md)
- [SETUP_GUIDE.md](SETUP_GUIDE.md)
- [MVP_DOCUMENTATION.md](MVP_DOCUMENTATION.md)

---

## 🤝 Contributing

اگر می‌خواهید به بهبود CI/CD کمک کنید:

1. Fork repository
2. Create feature branch
3. Make changes
4. Run tests
5. Submit PR

---

## 📞 پشتیبانی

برای مشکلات مربوط به CI/CD:

1. بررسی [Troubleshooting](#troubleshooting)
2. چک کردن GitHub Actions logs
3. اجرای local برای debug
4. ایجاد GitHub Issue

---

**آخرین بروزرسانی:** اکتبر 2025  
**نسخه:** 1.0.0  
**نویسنده:** Strategy Team

---

**✅ CI/CD شما آماده است! به توسعه قابل رصد و تکرارپذیر خوش آمدید!** 🚀

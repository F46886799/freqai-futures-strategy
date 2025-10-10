# Monitoring & Testing System

## 📊 Monitoring System

### Overview
سیستم monitoring برای ردیابی عملکرد استراتژی در طول زمان طراحی شده است.

### Components

#### 1. `extract_metrics.py`
استخراج metrics از خروجی backtest

**استفاده:**
```bash
python monitoring/extract_metrics.py backtest_output.txt
```

**Metrics استخراج شده:**
- Total Trades
- Win Rate
- Total Profit
- Sharpe Ratio
- Max Drawdown
- Average Trade Duration
- Best/Worst Pairs

#### 2. `generate_report.py`
تولید گزارش HTML از تاریخچه metrics

**استفاده:**
```bash
python monitoring/generate_report.py
```

**خروجی:**
- `monitoring/performance_report.html` - گزارش تعاملی HTML

#### 3. `compare_versions.py`
مقایسه عملکرد بین versions مختلف

**استفاده:**
```bash
python monitoring/compare_versions.py
```

**تحلیل‌ها:**
- مقایسه latest با previous
- بهترین عملکرد تاریخی
- تحلیل روند

---

## 🧪 Testing System

### Test Structure

```
tests/
├── test_strategy_logic.py    # تست منطق استراتژی
└── test_integration.py        # تست‌های integration
```

### Running Tests

#### تمام تست‌ها
```bash
pytest tests/ -v
```

#### تست خاص
```bash
pytest tests/test_strategy_logic.py -v
```

#### با coverage
```bash
pytest tests/ -v --cov=user_data/strategies --cov-report=html
```

### Test Categories

#### 1. Strategy Logic Tests
- تست initialization استراتژی
- تست properties و configuration
- تست indicator generation
- تست market regime detection
- تست entry/exit signals

#### 2. Integration Tests
- تست Docker integration
- تست configuration completeness
- تست file structure
- تست monitoring system

---

## 📈 Metrics History

### Storage Format

Metrics در فایل CSV ذخیره می‌شوند:
```
monitoring/metrics_history.csv
```

### Schema
```csv
timestamp,total_trades,win_rate,total_profit,sharpe_ratio,max_drawdown,avg_trade_duration,best_pair,worst_pair
2025-10-10T12:00:00,342,54.2,15.23,1.45,-8.34,2:15:00,BTC/USDT:USDT,SOL/USDT:USDT
```

---

## 🚀 CI/CD Integration

### Automated Workflows

1. **Code Quality** - هر push
   - Linting
   - Formatting
   - Type checking
   - Security scan

2. **Unit Tests** - هر push
   - Strategy tests
   - Configuration validation
   - Python 3.10 & 3.11

3. **Backtest** - push به master
   - Download data
   - Run backtest
   - Extract metrics
   - Upload results

4. **Performance Tracking** - هفتگی
   - Long-term backtest
   - Metrics collection
   - Trend analysis
   - HTML report

---

## 📊 Performance Dashboard

### Viewing Reports

گزارش‌های HTML را می‌توانید مشاهده کنید:

1. **Local:**
   ```bash
   # Generate report
   python monitoring/generate_report.py
   
   # Open in browser
   start monitoring/performance_report.html  # Windows
   open monitoring/performance_report.html   # Mac
   ```

2. **CI/CD:**
   - رفتن به GitHub Actions
   - انتخاب workflow run
   - دانلود artifacts
   - باز کردن `performance_report.html`

### Metrics Tracked

- ✅ Total Profit %
- ✅ Win Rate %
- ✅ Total Trades
- ✅ Sharpe Ratio
- ✅ Max Drawdown %
- ✅ Average Trade Duration
- ✅ Best/Worst Pairs

---

## 🔧 Setup Requirements

### Python Packages

```bash
pip install pytest pytest-cov pandas numpy matplotlib
```

### Docker

```bash
docker pull freqtradeorg/freqtrade:stable_freqairl
```

---

## 💡 Usage Examples

### مثال 1: اجرای Backtest و ذخیره Metrics

```bash
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

# Generate report
python monitoring/generate_report.py
```

### مثال 2: مقایسه Versions

```bash
# Run backtest for version 1
git checkout v1.0
# ... run backtest & extract metrics ...

# Run backtest for version 2
git checkout v1.1
# ... run backtest & extract metrics ...

# Compare
python monitoring/compare_versions.py
```

### مثال 3: CI/CD Manual Trigger

```bash
# Trigger backtest workflow manually
gh workflow run 3-backtest.yml \
  -f timerange=20240101-20241231 \
  -f strategy=FreqAIHybridStrategy
```

---

## 📝 Best Practices

### Monitoring

1. ✅ همیشه metrics را بعد از هر backtest ذخیره کنید
2. ✅ گزارش‌های هفتگی تولید کنید
3. ✅ تغییرات بزرگ را با versions قبلی مقایسه کنید
4. ✅ Threshold alerts تنظیم کنید

### Testing

1. ✅ تست‌ها را قبل از commit اجرا کنید
2. ✅ Coverage را بالای 70% نگه دارید
3. ✅ Integration tests برای تغییرات بزرگ اضافه کنید
4. ✅ Mock data برای unit tests استفاده کنید

### CI/CD

1. ✅ Workflows را بعد از تغییرات مهم بررسی کنید
2. ✅ Artifacts را برای بررسی نگه دارید
3. ✅ Failed builds را فوراً fix کنید
4. ✅ Performance regressions را ردیابی کنید

---

## 🆘 Troubleshooting

### مشکل: Metrics استخراج نمی‌شود

**راه حل:**
```bash
# بررسی فرمت output
cat backtest_output.txt | grep -i "total profit"

# اجرای manual
python monitoring/extract_metrics.py backtest_output.txt --debug
```

### مشکل: Tests fail می‌کنند

**راه حل:**
```bash
# اجرای با verbose
pytest tests/ -vv

# اجرای تک تک
pytest tests/test_strategy_logic.py::TestStrategyBasics::test_strategy_initialization -v
```

### مشکل: GitHub Actions fail می‌شود

**راه حل:**
1. بررسی logs در GitHub Actions
2. اجرای local با همان commands
3. بررسی Docker image version
4. بررسی file paths

---

## 📚 Additional Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [GitHub Actions Docs](https://docs.github.com/en/actions)
- [Pandas Documentation](https://pandas.pydata.org/docs/)

---

**آخرین بروزرسانی:** اکتبر 2025

# 🚀 مراحل بعدی پروژه

**تاریخ:** 12 اکتبر 2025  
**وضعیت CI/CD:** ✅ کاملاً فعال و تست شده

---

## ✅ Issue #1: CI/CD Fixes - **CLOSED** ✅

### موفقیت‌ها:
- ✅ GitHub Actions کار می‌کند (Python 3.10 و 3.11)
- ✅ TA-Lib نصب می‌شود
- ✅ Freqtrade[freqai] نصب می‌شود
- ✅ همه تست‌ها موفق (25 passed, 4 skipped)
- ✅ Coverage: 33% baseline

### لینک‌ها:
- [Workflow موفق](https://github.com/aminak58/freqai-futures-strategy/actions/runs/18436489967)
- [Issue #1 - Closed](https://github.com/aminak58/freqai-futures-strategy/issues/1)

---

## 📋 Issues باز (اولویت‌بندی شده)

### 🔴 اولویت بالا

#### 1️⃣ Issue #5: دانلود Historical Data
**وضعیت:** 🟡 آماده شروع  
**تخمین زمان:** 2-3 ساعت

**چرا اول؟**
- بدون data نمی‌توان training کرد
- بدون data نمی‌توان backtest کرد
- سایر Issues به data نیاز دارند

**مراحل:**
```bash
# 1. دانلود data با Freqtrade
freqtrade download-data \
  --exchange binance \
  --pairs BTC/USDT:USDT ETH/USDT:USDT SOL/USDT:USDT BNB/USDT:USDT \
  --timeframes 5m 15m 1h \
  --days 365 \
  --trading-mode futures \
  --config config/config.json

# 2. Validation
python scripts/validate_data.py

# 3. Split data (train/val/test)
python scripts/split_data.py
```

**ملزومات:**
- ⚠️ VPN برای دسترسی به Binance
- 📦 ~500 MB فضای خالی
- ⏱️ ~10-20 دقیقه زمان دانلود

**Deliverables:**
- [ ] Data downloaded در `user_data/data/binance/futures/`
- [ ] Data validation report
- [ ] Train/validation/test splits

---

#### 2️⃣ Issue #3: پیاده‌سازی LSTM
**وضعیت:** ⏳ بعد از Issue #5  
**تخمین زمان:** 5-7 ساعت

**مراحل:**
1. **ایجاد Model Architecture**
   ```python
   user_data/models/
   ├── lstm_model.py         # LSTM architecture
   ├── data_processor.py     # Data pipeline
   └── train_lstm.py         # Training script
   ```

2. **Training Pipeline**
   - Sequence generation (look_back=60)
   - Batch training
   - Early stopping
   - Model checkpointing

3. **Integration با Strategy**
   - اضافه کردن LSTM predictions به `populate_indicators`
   - Ensemble: LightGBM + LSTM
   - Weighted combination

**Dependencies جدید:**
```bash
pip install tensorflow>=2.13.0 keras>=2.13.0
```

**Deliverables:**
- [ ] LSTM model trained
- [ ] Validation metrics (MSE, MAE, R²)
- [ ] Integration tests
- [ ] Backtesting results

---

### 🟡 اولویت متوسط

#### 3️⃣ Issue #2: افزایش Coverage به 80%+
**وضعیت:** ⏳ می‌تواند موازی انجام شود  
**تخمین زمان:** 3-4 ساعت

**فوکوس اصلی:**
- 103 خط پوشش نداده شده
- Regime detection tests
- Entry/Exit signal tests
- Leverage calculation tests
- Mock FreqAI dependencies

**مراحل:**
```python
# 1. Mock FreqAI
pytest fixtures for:
- IFreqaiModel
- DataProvider
- FreqAI context

# 2. Test scenarios
- test_regime_detection_trending_up()
- test_regime_detection_trending_down()
- test_regime_detection_high_volatility()
- test_entry_long_conditions()
- test_entry_short_conditions()
- test_exit_conditions()
- test_leverage_calculation()
```

**Deliverables:**
- [ ] Coverage 80%+
- [ ] همه critical paths tested
- [ ] CI/CD badge به README

---

### 🟢 اولویت پایین

#### 4️⃣ Issue #4: Documentation Organization
**وضعیت:** ✅ تکمیل شده  
این Issue قبلاً انجام شده است.

---

## 📅 جدول زمانی پیشنهادی

### هفته 1: Data \u0026 Infrastructure
- **روز 1-2:** Issue #5 - دانلود و validation data
- **روز 3:** بررسی data quality و آماده‌سازی

### هفته 2: LSTM Implementation
- **روز 1-2:** Model architecture و data pipeline
- **روز 3-4:** Training و validation
- **روز 5:** Integration با strategy

### هفته 3: Testing \u0026 Optimization
- **روز 1-2:** Issue #2 - افزایش coverage
- **روز 3-4:** Backtesting comprehensive
- **روز 5:** Hyperparameter tuning

---

## 🛠️ ابزارهای مورد نیاز

### برای Issue #5 (Data):
```bash
# Local
freqtrade download-data --help

# یا Docker
docker run --rm freqtradeorg/freqtrade:stable_freqairl download-data --help
```

### برای Issue #3 (LSTM):
```bash
pip install tensorflow keras scikit-learn
```

### برای Issue #2 (Testing):
```bash
pytest tests/ -v --cov=user_data/strategies --cov-report=html
```

---

## 📊 معیارهای موفقیت

### Technical Metrics:
- ✅ Coverage \u003e 80%
- ✅ Data quality score \u003e 95%
- ✅ LSTM validation loss \u003c 0.05
- ✅ Backtest Sharpe ratio \u003e 1.5

### Business Metrics:
- 🎯 Win rate \u003e 60%
- 🎯 Max drawdown \u003c 15%
- 🎯 Profit factor \u003e 1.8
- 🎯 Monthly return \u003e 10%

---

## 🔗 مراجع مفید

### Documentation:
- [Architecture](docs/architecture/UNIFIED_ARCHITECTURE.md)
- [LSTM Design](docs/architecture/LSTM_ARCHITECTURE_DESIGN.md)
- [Development Guide](docs/guides/DEVELOPMENT_GUIDE.md)

### External:
- [Freqtrade Docs](https://www.freqtrade.io/en/stable/)
- [TensorFlow LSTM](https://www.tensorflow.org/guide/keras/rnn)
- [pytest Documentation](https://docs.pytest.org/)

---

## ❓ سوالات متداول

**Q: از کجا شروع کنم؟**  
A: از Issue #5 شروع کنید - دانلود data اولین قدم است.

**Q: چطور می‌توانم کمک کنم؟**  
A: Issues با برچسب `good first issue` مناسب شروع هستند.

**Q: چقدر زمان می‌برد؟**  
A: تخمین کل: 2-3 هفته برای پیاده‌سازی کامل.

**Q: نیاز به GPU دارم؟**  
A: برای LSTM training مفید است اما اجباری نیست. CPU هم کار می‌کند.

---

**آخرین بروزرسانی:** 12 اکتبر 2025  
**وضعیت پروژه:** 🟢 Active Development  
**Team:** Solo Developer + GitHub Copilot

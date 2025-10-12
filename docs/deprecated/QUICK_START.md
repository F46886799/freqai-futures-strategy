# 🚀 Quick Start Guide - FreqAI Hybrid Strategy

## مراحل سریع راه‌اندازی (15 دقیقه)

### ✅ پیش‌نیازها
- [x] Docker Desktop نصب شده
- [x] VPN فعال (برای دسترسی به Binance)
- [x] حداقل 10GB فضای خالی دیسک
- [x] حداقل 8GB RAM

---

## 🎯 مرحله 1: بررسی Setup (2 دقیقه)

```powershell
# بررسی Docker
docker --version
docker-compose --version

# بررسی فایل‌های پروژه
cd c:\freqai-futures-strategy
ls
```

**باید ببینید:**
- `docker-compose-freqai.yml`
- `config/config.json`
- `user_data/strategies/FreqAIHybridStrategy.py`

---

## 📥 مرحله 2: دانلود داده (5-10 دقیقه)

```powershell
# Pull کردن image Docker
docker pull freqtradeorg/freqtrade:stable_freqairl

# ورود به container
docker run -it --rm -v c:\freqai-futures-strategy\user_data:/freqtrade/user_data freqtradeorg/freqtrade:stable_freqairl bash

# داخل container:
freqtrade download-data \
  --exchange binance \
  --timeframes 5m 15m 1h \
  --pairs BTC/USDT ETH/USDT SOL/USDT \
  --days 365 \
  --data-dir /freqtrade/user_data/data

# برای خروج
exit
```

**توضیح:**
- `--days 365`: یک سال داده (برای test سریع)
- برای backtest واقعی: `--days 1855` (5 سال)

---

## 🧪 مرحله 3: Backtesting سریع (3-5 دقیقه)

```powershell
docker run -it --rm `
  -v c:\freqai-futures-strategy\user_data:/freqtrade/user_data `
  -v c:\freqai-futures-strategy\config:/freqtrade/config `
  freqtradeorg/freqtrade:stable_freqairl `
  backtesting `
  --strategy FreqAIHybridStrategy `
  --strategy-path /freqtrade/user_data/strategies `
  --config /freqtrade/config/config.json `
  --freqaimodel LightGBMRegressorMultiTarget `
  --timerange 20240701-20250101
```

**اولین اجرا:**
- طول می‌کشد (5-10 دقیقه) چون مدل را train می‌کند
- مدل ذخیره می‌شود در `user_data/models/`

**اجراهای بعدی:**
- سریع (< 1 دقیقه) چون از مدل cached استفاده می‌کند

---

## 📊 مرحله 4: بررسی نتایج

بعد از backtest، خروجی شبیه این خواهد بود:

```
============================================== SUMMARY METRICS ==============================================
| Metric                | Value              |
|-----------------------|--------------------|
| Total Profit %        | 15.23%            |
| Sharpe Ratio          | 1.45              |
| Max Drawdown          | -8.34%            |
| Win Rate              | 54.2%             |
| Total Trades          | 342               |
| Avg Trade Duration    | 2h 15m            |
=============================================================================================================
```

**نتایج خوب:**
- Total Profit > 10%
- Sharpe > 1.0
- Max Drawdown < 20%
- Win Rate > 50%

---

## 🔄 مرحله 5: Dry Run (تست Real-Time)

### ویرایش config برای dry run:

در `C:\strategy\config\config.json`:
```json
{
    "dry_run": true,
    "dry_run_wallet": 1000,
    ...
}
```

### اجرای dry run:

```powershell
docker-compose -f C:\strategy\docker-compose-freqai.yml up -d
```

### مشاهده logs:

```powershell
# Realtime logs
docker-compose -f C:\strategy\docker-compose-freqai.yml logs -f

# فقط 100 خط آخر
docker-compose -f C:\strategy\docker-compose-freqai.yml logs --tail=100
```

### توقف:

```powershell
docker-compose -f C:\strategy\docker-compose-freqai.yml down
```

---

## 🎨 مرحله 6: مشاهده Plots (اختیاری)

### نصب dependencies برای plotting:

```powershell
docker run -it --rm \
  -v C:\strategy\user_data:/freqtrade/user_data \
  freqtradeorg/freqtrade:stable_freqairl bash

# داخل container:
pip install plotly

freqtrade plot-dataframe \
  --strategy FreqAIHybridStrategy \
  --config /freqtrade/config/config.json \
  --pairs BTC/USDT \
  --indicators1 ema_50,ema_200 \
  --indicators2 regime \
  --export-filename /freqtrade/user_data/plot_BTC.html

exit
```

سپس فایل `user_data/plot_BTC.html` را با browser باز کنید.

---

## ⚙️ تنظیمات سریع

### کاهش پیچیدگی (برای testing سریع‌تر):

```json
// config.json
"freqai": {
    "train_period_days": 15,        // کاهش از 30
    "backtest_period_days": 3,      // کاهش از 7
    "feature_parameters": {
        "include_timeframes": ["5m"],     // فقط 5m
        "indicator_periods_candles": [10, 20],  // کاهش periods
        "include_corr_pairlist": []       // بدون correlation pairs
    }
}
```

### افزایش دقت (برای production):

```json
"freqai": {
    "train_period_days": 60,        // افزایش
    "feature_parameters": {
        "include_timeframes": ["5m", "15m", "1h", "4h"],
        "indicator_periods_candles": [10, 20, 50, 100, 200],
        "include_shifted_candles": 3,
        "DI_threshold": 0.8
    },
    "model_training_parameters": {
        "n_estimators": 2000,           // افزایش
        "learning_rate": 0.01,          // کاهش
        "max_depth": 10                 // افزایش
    }
}
```

---

## 🔍 بررسی سلامت سیستم

### چک کردن مدل‌های trained:

```powershell
docker run -it --rm -v C:\strategy\user_data:/freqtrade/user_data freqtradeorg/freqtrade:stable_freqairl bash

ls -lh /freqtrade/user_data/models/hybrid_lstm_ensemble/

# باید ببینید:
# - sub-train-*.joblib (مدل‌های trained)
# - historic_predictions.pkl
# - pair_dictionary.json
```

### چک کردن logs:

```powershell
# آخرین errors
docker-compose -f C:\strategy\docker-compose-freqai.yml logs | grep ERROR

# آخرین predictions
docker-compose -f C:\strategy\docker-compose-freqai.yml logs | grep "prediction"

# آخرین trades
docker-compose -f C:\strategy\docker-compose-freqai.yml logs | grep "ENTER\|EXIT"
```

---

## 🐛 عیب‌یابی سریع

### مشکل 1: "No data available"
```powershell
# دانلود مجدد
docker run -it --rm -v C:\strategy\user_data:/freqtrade/user_data freqtradeorg/freqtrade:stable_freqairl bash
freqtrade download-data --exchange binance --timeframes 5m 15m 1h --pairs BTC/USDT --days 400
```

### مشکل 2: "Strategy not found"
```powershell
# بررسی استراتژی
docker run -it --rm -v C:\strategy\user_data:/freqtrade/user_data freqtradeorg/freqtrade:stable_freqairl bash
ls -la /freqtrade/user_data/strategies/
cat /freqtrade/user_data/strategies/FreqAIHybridStrategy.py | head -20
```

### مشکل 3: "Connection refused" (Binance)
```
علت: VPN خاموش است یا API rate limit
راه حل:
1. VPN را روشن کنید
2. صبر کنید (rate limit 1200 req/min)
3. از ccxt_config استفاده کنید:
```

```json
"exchange": {
    "ccxt_config": {
        "rateLimit": 500
    }
}
```

### مشکل 4: Memory کم
```powershell
# کاهش pairs
# در config.json:
"pair_whitelist": ["BTC/USDT", "ETH/USDT"]  // فقط 2 pair

# یا کاهش features:
"feature_parameters": {
    "include_timeframes": ["5m"],
    "indicator_periods_candles": [20]
}
```

---

## 📈 گام‌های بعدی

### 1. Hyperopt (بهینه‌سازی)
```powershell
docker run -it --rm \
  -v C:\strategy\user_data:/freqtrade/user_data \
  -v C:\strategy\config:/freqtrade/config \
  freqtradeorg/freqtrade:stable_freqairl \
  hyperopt \
  --strategy FreqAIHybridStrategy \
  --hyperopt-loss SharpeHyperOptLoss \
  --timerange 20240101-20250101 \
  --epochs 100 \
  --spaces buy sell
```

### 2. Live Trading (با احتیاط!)
```json
// config.json
{
    "dry_run": false,  // ⚠️ DANGER! Real money
    "exchange": {
        "key": "your_api_key",
        "secret": "your_api_secret"
    }
}
```

**قبل از live:**
1. ✅ Backtest موفق (profit > 10%, sharpe > 1.0)
2. ✅ Dry run یک هفته بدون مشکل
3. ✅ API keys با محدودیت (no withdrawal)
4. ✅ شروع با capital کم ($100-500)
5. ✅ Max risk per trade < 2%

---

## 📚 منابع مفید

### Commands Reference:
```powershell
# لیست containers
docker ps -a

# حذف containers قدیمی
docker-compose -f docker-compose-freqai.yml down

# حذف volumes (⚠️ تمام data پاک می‌شود)
docker-compose -f docker-compose-freqai.yml down -v

# مشاهده resource usage
docker stats

# ورود به running container
docker exec -it freqtrade_strategy bash
```

### FreqAI Commands:
```bash
# داخل container:

# List strategies
freqtrade list-strategies

# Test strategy
freqtrade test-pairlist

# Plot profit
freqtrade plot-profit

# Show trades
freqtrade show-trades

# Database analysis
freqtrade trades-to-ohlcv
```

---

## 🎯 Checklist راه‌اندازی

- [ ] Docker نصب و اجرا شد
- [ ] VPN فعال است
- [ ] فایل‌های config و strategy ساخته شدند
- [ ] داده‌ها دانلود شدند (حداقل 1 سال)
- [ ] Backtest با موفقیت اجرا شد
- [ ] نتایج backtest رضایت‌بخش بود
- [ ] Dry run راه‌اندازی شد
- [ ] Logs بررسی شدند
- [ ] مدل‌ها ذخیره شدند
- [ ] Documentation خوانده شد

---

## 💡 نکات مهم

1. **همیشه با Dry Run شروع کنید**
2. **Backtest ≠ Live Performance** (معمولاً live ضعیف‌تر است)
3. **Risk Management > Strategy** (مهم‌تر از استراتژی است)
4. **Start Small, Scale Gradually** (شروع کوچک، رشد تدریجی)
5. **Monitor Daily** (روزانه مانیتور کنید)
6. **Keep Learning** (مدام یاد بگیرید)

---

## 🆘 کمک بیشتر

اگر گیر کردید:
1. [MVP_DOCUMENTATION.md](./MVP_DOCUMENTATION.md) را بخوانید
2. [Freqtrade Docs](https://www.freqtrade.io/en/stable/)
3. [Discord Channel](https://discord.gg/freqtrade)
4. GitHub Issues

---

**موفق باشید! 🚀**

*Remember: Trading involves risk. Never invest more than you can afford to lose.*

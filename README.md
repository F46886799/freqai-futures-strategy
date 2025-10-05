# 🤖 FreqAI Hybrid Futures Trading Strategy

استراتژی پیشرفته معاملاتی با استفاده از **Freqtrade + FreqAI + LightGBM** برای ترید Futures با Leverage در صرافی Binance.

---

## 📊 ویژگی‌های کلیدی

### ⚡ Futures Trading با Leverage
- **Trading Mode:** Futures (USDT-M Perpetual)
- **Margin:** Isolated (مدیریت ریسک بهتر)
- **Leverage:** Dynamic 2x-5x (بسته به شرایط بازار)
- **Positions:** LONG & SHORT (دو طرفه)

### 🧠 Machine Learning با FreqAI
- **Model:** LightGBM Regressor (Multi-Target)
- **Training:** Sliding Window 30 روزه
- **Features:** 1,386 ویژگی از Multi-Timeframe (5m/15m/1h)
- **Outlier Detection:** SVM برای حذف نویز
- **Predictions:** سه هدف (price change, volatility, volume surge)

### 📈 Hybrid Indicators
- **Trend:** EMA, Supertrend, ADX
- **Momentum:** RSI, MACD, Stochastic
- **Volume:** OBV, MFI, Volume indicators
- **Volatility:** ATR, Bollinger Bands
- **Market Regime:** 4 رژیم (Trending Bull/Bear, High Vol, Sideways)

---

## 🚀 نصب سریع

### پیش‌نیازها
- Docker Desktop
- Git
- VPN فعال (برای ایران)

### مراحل نصب

```bash
# 1. Clone کردن
git clone <YOUR_REPO_URL>
cd strategy

# 2. Pull کردن Docker Image (13.8 GB)
docker pull freqtradeorg/freqtrade:stable_freqairl

# 3. دانلود داده
docker run --rm -v ${PWD}/user_data:/freqtrade/user_data \
  freqtradeorg/freqtrade:stable_freqairl download-data \
  --exchange binance \
  --pairs BTC/USDT:USDT ETH/USDT:USDT SOL/USDT:USDT \
  --timeframes 5m 15m 1h \
  --days 500 \
  --trading-mode futures

# 4. اجرای Backtest
docker run --rm \
  -v ${PWD}/user_data:/freqtrade/user_data \
  -v ${PWD}/config:/freqtrade/config \
  freqtradeorg/freqtrade:stable_freqairl backtesting \
  --strategy FreqAIHybridStrategy \
  --strategy-path /freqtrade/user_data/strategies \
  --config /freqtrade/config/config.json \
  --freqaimodel LightGBMRegressorMultiTarget \
  --timerange 20241001-20250101
```

**📖 راهنمای کامل:** [SETUP_GUIDE.md](./SETUP_GUIDE.md)

---

## 📁 ساختار پروژه

```
strategy/
├── config/
│   └── config.json                    # کانفیگ اصلی (Futures)
├── user_data/
│   ├── strategies/
│   │   └── FreqAIHybridStrategy.py   # استراتژی اصلی
│   └── data/                          # داده‌ها (git ignore)
├── docker-compose.yml                 # Docker setup
├── MVP_DOCUMENTATION.md               # مستندات کامل فارسی
├── QUICK_START.md                     # راهنمای سریع فارسی
├── SETUP_GUIDE.md                     # راهنمای نصب تفصیلی
└── README.md                          # این فایل
```

---

## ⚠️ هشدارها

### 🚨 قبل از Live Trading:
1. ✅ حداقل 3 ماه backtest موفق
2. ✅ 2 هفته Dry Run بدون مشکل
3. ✅ شروع با leverage پایین (2x)
4. ✅ شروع با سرمایه کم (50-100 USDT)
5. ✅ استفاده از isolated margin

### 🔒 امنیت:
- ❌ هرگز API Key را commit نکنید
- ✅ از `.gitignore` استفاده کنید
- ✅ Whitelist IP در Binance

---

## 📚 مستندات

- **[SETUP_GUIDE.md](./SETUP_GUIDE.md)** - راهنمای نصب کامل
- **[MVP_DOCUMENTATION.md](./MVP_DOCUMENTATION.md)** - مستندات فنی
- **[QUICK_START.md](./QUICK_START.md)** - شروع سریع
- **[Freqtrade Docs](https://www.freqtrade.io/)** - مستندات رسمی

---

## ⚖️ Disclaimer

**هشدار:** استفاده از این استراتژی به معنای پذیرش ریسک‌های مالی است. این نرم‌افزار "همان‌طور که هست" ارائه می‌شود بدون هیچ‌گونه ضمانت. لطفاً با مقادیر کم شروع کنید و ریسک را مدیریت کنید.

**موفق باشید! 🚀**

# 🚀 راهنمای راه‌اندازی روی PC شخصی

این پروژه شامل استراتژی Freqtrade با FreqAI برای معاملات Futures با Leverage است.

---

## 📋 پیش‌نیازها

✅ موارد زیر باید روی PC شخصی شما نصب باشند:
- **Docker Desktop** (برای ویندوز/مک/لینوکس)
- **Git** (برای clone کردن ریپو)
- **VPN فعال** (برای دسترسی به Binance از ایران)

---

## 🔧 مراحل نصب و راه‌اندازی

### مرحله 1: Clone کردن ریپوزیتوری

```bash
git clone <YOUR_REPO_URL>
cd strategy
```

### مرحله 2: Pull کردن Docker Image

این image حدود **13.8 GB** حجم دارد و باید یکبار دانلود شود:

```bash
docker pull freqtradeorg/freqtrade:stable_freqairl
```

⏱️ **زمان دانلود:** 20-45 دقیقه (بسته به سرعت اینترنت)

### مرحله 3: بررسی ساختار فایل‌ها

پس از clone، ساختار باید به این شکل باشد:

```
strategy/
├── config/
│   └── config.json              # کانفیگ اصلی (Futures mode)
├── user_data/
│   ├── strategies/
│   │   └── FreqAIHybridStrategy.py   # استراتژی اصلی
│   └── data/                    # این پوشه خالی است (باید دیتا دانلود شود)
├── docker-compose.yml           # برای اجرای آسان‌تر
├── MVP_DOCUMENTATION.md         # مستندات کامل
├── QUICK_START.md              # راهنمای سریع
└── SETUP_GUIDE.md              # این فایل
```

### مرحله 4: دانلود داده‌های تاریخی

**⚠️ مهم:** باید دیتای Futures با فرمت صحیح دانلود شود.

#### 🔹 دانلود سریع (30 روز - برای تست اولیه)

```bash
docker run --rm -v ${PWD}/user_data:/freqtrade/user_data \
  freqtradeorg/freqtrade:stable_freqairl download-data \
  --exchange binance \
  --pairs BTC/USDT:USDT ETH/USDT:USDT SOL/USDT:USDT \
  --timeframes 5m 15m 1h \
  --days 30 \
  --trading-mode futures \
  --data-format-ohlcv feather
```

⏱️ زمان: **30-60 ثانیه**

#### 🔹 دانلود کامل (500 روز - برای backtest واقعی)

```bash
docker run --rm -v ${PWD}/user_data:/freqtrade/user_data \
  freqtradeorg/freqtrade:stable_freqairl download-data \
  --exchange binance \
  --pairs BTC/USDT:USDT ETH/USDT:USDT SOL/USDT:USDT \
  --timeframes 5m 15m 1h \
  --days 500 \
  --trading-mode futures \
  --data-format-ohlcv feather
```

⏱️ زمان: **2-3 دقیقه**

**✅ تأیید دانلود موفق:**

```bash
# چک کردن فایل‌های دانلود شده
ls user_data/data/binance/
```

باید این فایل‌ها را ببینید:
```
BTC_USDT_USDT-5m.feather
BTC_USDT_USDT-15m.feather
BTC_USDT_USDT-1h.feather
ETH_USDT_USDT-5m.feather
ETH_USDT_USDT-15m.feather
ETH_USDT_USDT-1h.feather
SOL_USDT_USDT-5m.feather
SOL_USDT_USDT-15m.feather
SOL_USDT_USDT-1h.feather
```

**🚨 فرمت نام فایل مهم است:**
- ✅ صحیح: `BTC_USDT_USDT-5m.feather` (Futures)
- ❌ اشتباه: `BTC_USDT-5m.feather` (Spot)

---

## 🧪 اجرای Backtest

### روش 1: با Docker Command (توصیه می‌شود)

```bash
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

### روش 2: با Docker Compose

```bash
docker-compose up backtest
```

### مانیتورینگ پیشرفت

```bash
# مشاهده لاگ‌های زنده
docker logs -f <container_id>

# یافتن Container ID
docker ps | grep freqtrade
```

---

## ⏱️ زمان‌بندی انتظار

| عملیات | زمان تقریبی |
|--------|------------|
| Pull کردن Docker Image | 20-45 دقیقه |
| دانلود داده 30 روزه | 30-60 ثانیه |
| دانلود داده 500 روزه | 2-3 دقیقه |
| Backtest 1 ماهه | 30-45 دقیقه |
| Backtest 3 ماهه | 3-7 ساعت |
| Hyperopt (100 epochs) | 2-3 ساعت |

---

## 📊 بررسی نتایج

پس از اتمام backtest، نتایج در `user_data/backtest_results/` ذخیره می‌شوند.

### مشاهده خلاصه نتایج

```bash
docker run --rm \
  -v ${PWD}/user_data:/freqtrade/user_data \
  freqtradeorg/freqtrade:stable_freqairl backtesting-analysis
```

### ساخت نمودارها

```bash
# نمودار سود
docker run --rm \
  -v ${PWD}/user_data:/freqtrade/user_data \
  freqtradeorg/freqtrade:stable_freqairl plot-profit

# نمودار کندل‌ها و اندیکاتورها
docker run --rm \
  -v ${PWD}/user_data:/freqtrade/user_data \
  freqtradeorg/freqtrade:stable_freqairl plot-dataframe \
  --strategy FreqAIHybridStrategy \
  --pairs BTC/USDT:USDT
```

---

## ⚙️ تنظیمات پیشرفته

### 1. افزایش تعداد پیرها

ویرایش `config/config.json`:

```json
"pair_whitelist": [
    "BTC/USDT:USDT",
    "ETH/USDT:USDT",
    "SOL/USDT:USDT",
    "BNB/USDT:USDT",
    "AVAX/USDT:USDT"
]
```

**⚠️ توجه:** باید دیتای پیر جدید را دانلود کنید.

### 2. تغییر Leverage

ویرایش `user_data/strategies/FreqAIHybridStrategy.py`:

```python
def leverage(self, ...):
    if regime == 3 or di_value > 1.5:
        return 2.0  # محافظه‌کارانه
    elif regime in [1, 2] and di_value < 0.5:
        return 10.0  # تهاجمی (قبلاً 5x بود)
    else:
        return 5.0  # پیش‌فرض (قبلاً 3x بود)
```

### 3. تنظیم FreqAI

ویرایش `config/config.json` - بخش `freqai`:

```json
"train_period_days": 30,        # کاهش برای سرعت بیشتر
"backtest_period_days": 7,      # افزایش برای تست دقیق‌تر
"expiration_hours": 2,          # مدل‌های قدیمی‌تر قابل استفاده
```

---

## 🐛 عیب‌یابی

### مشکل 1: "No history found"

**علت:** فرمت نام فایل اشتباه است (Spot به جای Futures)

**راه‌حل:**
```bash
# حذف فایل‌های قدیمی
rm user_data/data/binance/*.feather

# دانلود دوباره با --trading-mode futures
docker run --rm -v ${PWD}/user_data:/freqtrade/user_data \
  freqtradeorg/freqtrade:stable_freqairl download-data \
  --exchange binance \
  --pairs BTC/USDT:USDT ETH/USDT:USDT SOL/USDT:USDT \
  --timeframes 5m 15m 1h \
  --days 500 \
  --trading-mode futures
```

### مشکل 2: "All training data dropped due to NaNs"

**علت:** داده کافی برای training وجود ندارد

**راه‌حل:**
```bash
# دانلود داده بیشتر
docker run --rm -v ${PWD}/user_data:/freqtrade/user_data \
  freqtradeorg/freqtrade:stable_freqairl download-data \
  --exchange binance \
  --pairs BTC/USDT:USDT ETH/USDT:USDT SOL/USDT:USDT \
  --timeframes 5m 15m 1h \
  --days 700 \
  --trading-mode futures
```

### مشکل 3: Container بلافاصله خارج می‌شود

**راه‌حل:**
```bash
# چک کردن لاگ‌های خطا
docker logs <container_id>

# اجرای interactive برای دیباگ
docker run -it --rm \
  -v ${PWD}/user_data:/freqtrade/user_data \
  -v ${PWD}/config:/freqtrade/config \
  freqtradeorg/freqtrade:stable_freqairl /bin/bash
```

---

## 📝 نکات مهم

### ✅ قبل از اجرای Live Trading:

1. **حداقل 3 ماه backtest موفق**
2. **2 هفته Dry Run بدون خطا**
3. **شروع با leverage پایین (2x-3x)**
4. **استفاده از isolated margin**
5. **تست با مبلغ کم (50-100 USDT)**

### ⚠️ هشدارهای امنیتی:

- **هرگز API Key را commit نکنید**
- از `config.json.example` استفاده کنید
- API Key واقعی را فقط local نگه دارید
- Whitelist IP را در Binance فعال کنید

---

## 🔄 به‌روزرسانی

```bash
# Pull کردن آخرین تغییرات
git pull origin main

# به‌روزرسانی Docker Image
docker pull freqtradeorg/freqtrade:stable_freqairl

# Restart containers
docker-compose down
docker-compose up -d
```

---

## 📚 منابع بیشتر

- **MVP Documentation:** [MVP_DOCUMENTATION.md](./MVP_DOCUMENTATION.md)
- **Quick Start:** [QUICK_START.md](./QUICK_START.md)
- **Freqtrade Docs:** https://www.freqtrade.io/
- **FreqAI Guide:** https://www.freqtrade.io/en/stable/freqai/

---

## 💬 پشتیبانی

اگر مشکلی داشتید:
1. لاگ‌های خطا را چک کنید: `docker logs <container_id>`
2. مستندات Freqtrade را مطالعه کنید
3. Issue جدید در GitHub باز کنید

---

**موفق باشید! 🚀**

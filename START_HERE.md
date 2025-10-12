# 🎯 Quick Start - Offline Colab Backtest

## ✅ آماده‌سازی کامل شد!

### چیزهایی که انجام شد:
- ✅ داده‌ها فشرده شد: `binance_data.zip` (10.1 MB)
- ✅ فایل در Google Drive آپلود شد: `MyDrive/FreqAI/binance_data.zip`
- ✅ Notebook Offline ساخته شد

---

## 🚀 حالا اجرا کن! (3 مرحله ساده)

### مرحله 1: باز کردن Notebook

کلیک کن روی این لینک:

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/aminak58/freqai-futures-strategy/blob/master/FreqAI_GPU_Backtest_Offline.ipynb)

🔗 یا مستقیم: https://colab.research.google.com/github/aminak58/freqai-futures-strategy/blob/master/FreqAI_GPU_Backtest_Offline.ipynb

---

### مرحله 2: فعال کردن GPU

**Runtime → Change runtime type → Hardware accelerator → GPU (T4) → Save**

---

### مرحله 3: اجرا!

**Runtime → Run all** (یا `Ctrl + F9`)

- اولین بار اجازه دسترسی به Google Drive می‌خواهد ✅
- فایل `binance_data.zip` را پیدا و Extract می‌کند 📦
- Backtest را با GPU اجرا می‌کند 🚀

---

## ⏱️ چقدر طول می‌کشد؟

| مرحله | زمان |
|-------|------|
| Mount Drive + Extract | ~30 ثانیه |
| Install Dependencies | ~2 دقیقه |
| GPU Backtest (2 ماه, 1 pair) | ~15-20 دقیقه |
| **جمع کل** | **~20-25 دقیقه** |

---

## 🎨 پارامترها (قابل تغییر)

در سلول دوم notebook:

```python
TIMERANGE = '20250901-20251012'  # بازه زمانی
PAIRS = ['BTC/USDT:USDT']        # جفت ارزها

# اگر مسیر فایل در Drive متفاوت است:
DRIVE_ZIP_PATH = '/content/drive/MyDrive/FreqAI/binance_data.zip'
```

**مثال برای چند جفت ارز:**
```python
PAIRS = ['BTC/USDT:USDT', 'ETH/USDT:USDT', 'SOL/USDT:USDT']
```

---

## 📊 نتایج

بعد از اتمام، خروجی شبیه این خواهد بود:

```
======================================================================
📈 BACKTEST RESULTS - FreqAI Hybrid Strategy
======================================================================

💰 Total Profit: 1234.56 USDT (12.34%)
📊 Sharpe Ratio: 1.85
📉 Max Drawdown: 8.5%

🎯 Total Trades: 145
✅ Wins: 89
❌ Losses: 56
📊 Win Rate: 61.38%

⏱️  Avg Trade Duration: 4h 32m
💵 Avg Profit: 0.85%
======================================================================
```

**نتایج را copy کن و به من بده تا با هم تحلیل کنیم!** 🔍

---

## 🔧 عیب‌یابی

### ❌ "File not found: binance_data.zip"

**راه حل:**
1. مطمئن شو فایل در مسیر صحیح است: `MyDrive/FreqAI/binance_data.zip`
2. یا `DRIVE_ZIP_PATH` را در سلول اول تغییر بده

### ❌ "GPU NOT FOUND"

**راه حل:**
1. Runtime → Change runtime type → GPU → Save
2. Runtime → Restart runtime
3. دوباره Run all

### ❌ "Permission denied" برای Drive

**راه حل:**
- وقتی Colab اجازه می‌خواهد، Allow بزن
- اگر نزدی: Runtime → Restart runtime → دوباره اجرا کن

---

## 🎉 بعد از اجرا

### اگر نتایج خوب بود ✅:
- تبریک! Strategy کار می‌کند 🎊
- بازه را افزایش بده (6-12 ماه)
- جفت ارزهای بیشتر تست کن
- برو سراغ Issue #2 (Test Coverage)

### اگر نتایج بد بود ❌:
- نگران نباش! اولین backtest است
- پارامترها را tune می‌کنیم
- Strategy را بهینه می‌کنیم

---

## 📚 منابع

- **Repository:** https://github.com/aminak58/freqai-futures-strategy
- **Colab Guide:** [COLAB_GPU_GUIDE.md](./COLAB_GPU_GUIDE.md)
- **Geo-Restriction Fix:** [COLAB_GEO_RESTRICTION_FIX.md](./COLAB_GEO_RESTRICTION_FIX.md)

---

**🚀 آماده‌ای؟ برو و Backtest رو اجرا کن!**

بعد نتایج رو برام بفرست! 📊

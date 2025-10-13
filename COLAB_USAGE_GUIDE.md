# 🚀 Colab GPU Backtest - راهنمای استفاده

## ⚠️ **مهم: مشکل Binance و راه‌حل**

**مشکل:** Binance آدرس‌های IP آمریکا رو مسدود می‌کنه (Error 451). Colab توی آمریکا هست.

**راه‌حل:** Notebook خودکار از **Proxy** استفاده می‌کنه تا این محدودیت رو دور بزنه.

### چطور کار می‌کنه؟
1. **Cell 7** چندین proxy رایگان رو تست می‌کنه
2. اولین proxy که کار کنه رو انتخاب می‌کنه
3. متغیرهای محیطی `HTTP_PROXY` و `HTTPS_PROXY` رو تنظیم می‌کنه
4. دسترسی به Binance API رو تست می‌کنه
5. اگر همه proxy ها fail کردن → backtest ممکنه fail بشه

### اگر همه proxy ها fail کردن:
- **گزینه 1:** از VPN استفاده کنید (خارج از ایران/آمریکا)
- **گزینه 2:** Kaggle امتحان کنید (به جای Colab)
- **گزینه 3:** روی سیستم محلی با VPN

---

## 📋 آماده‌سازی اولیه (فقط یکبار)

### 1. Google Drive
- فضای خالی: حداقل 1 گیگابایت
- برای ذخیره نتایج backtest

### 2. GitHub Token (اختیاری - فقط برای push کردن logs)
اگر می‌خواهید logs را به GitHub push کنید:

1. برید به: https://github.com/settings/tokens
2. کلیک کنید: **Generate new token (classic)**
3. نام: `Colab Runner`
4. دسترسی: فقط `repo` (tick بزنید)
5. Generate token
6. کپی کنید (فقط یکبار نشان داده می‌شود!)

⚠️ **نکته:** Token رو جایی امن نگه دارید!

---

## 🎯 استفاده

### روش 1: در مرورگر

1. برید به: https://colab.research.google.com/
2. **File > Upload notebook**
3. Upload کنید: `Colab_GPU_Backtest.ipynb`
4. **Runtime > Change runtime type > T4 GPU**
5. **Runtime > Run all**
6. منتظر بمانید (~10-15 دقیقه)
7. نتایج در Google Drive شما: `FreqAI_Backtest_Results/`

### روش 2: مستقیم از GitHub

1. برید به: https://colab.research.google.com/
2. **File > Open notebook > GitHub**
3. URL: `https://github.com/aminak58/freqai-futures-strategy`
4. انتخاب کنید: `Colab_GPU_Backtest.ipynb`
5. ادامه مراحل بالا...

---

## ⚙️ تنظیمات Backtest

در **Cell 6** پارامترها رو تغییر بدید:

```python
STRATEGY = "FreqAIHybridStrategy"    # نام استراتژی
TIMERANGE = "20250901-20251012"      # بازه زمانی
PAIRS = "BTC/USDT:USDT ETH/USDT:USDT" # جفت ارزها
```

---

## 📊 نتایج

### در Google Drive:
```
MyDrive/
└── FreqAI_Backtest_Results/
    └── backtest_20251013_143022/
        ├── backtest-result.json
        ├── backtest-result.html
        ├── trades.json
        └── SUMMARY.txt
```

### دانلود کردن:

**گزینه 1: دانلود دستی**
- برید Google Drive
- پیدا کنید: `FreqAI_Backtest_Results/backtest_XXX/`
- دانلود کنید

**گزینه 2: Google Drive Desktop** (توصیه می‌شه!)
- نصب کنید: [Google Drive for Desktop](https://www.google.com/drive/download/)
- خودکار sync می‌شه با کامپیوتر شما

**گزینه 3: rclone** (برای Linux/Mac)
```bash
rclone sync gdrive:FreqAI_Backtest_Results/ ./backtest_results/
```

---

## 🔄 اجرای دوباره

1. باز کنید notebook در Colab
2. تغییر بدید پارامترها (Cell 6)
3. **Runtime > Run all**
4. منتظر نتایج جدید

---

## 💡 نکات مهم

### ✅ مزایا:
- ✅ **GPU رایگان** T4 (Google Colab)
- ✅ **بدون SSH/Tunnel** - خیلی ساده
- ✅ **نتایج در Drive** - امن و دائمی
- ✅ **یکبار setup** - بعدش فقط Run
- ✅ **Git clean** - نتایج توی repo نمی‌رن

### ⚠️ محدودیت‌ها:
- Colab رایگان: 12 ساعت session (کافیه!)
- اگه idle باشه، disconnect می‌شه
- GPU محدود به T4 (خیلی خوبه برای backtest)

### 🚀 سرعت:
- CPU (local): ~30 دقیقه
- GPU (Colab): ~5-10 دقیقه
- **3-5 برابر سریعتر!** 🎉

### 💾 ذخیره داده:
اگه می‌خواید backtest سریعتر باشه:
1. دانلود کنید داده‌های historical خودتون
2. فشرده کنید به ZIP
3. آپلود کنید به Drive: `MyDrive/FreqAI/binance_data.zip`
4. Notebook خودش detect می‌کنه و استفاده می‌کنه

---

## 🔧 Troubleshooting

### مشکل: GPU فعال نیست
**حل:** 
- Runtime > Change runtime type
- Hardware accelerator > GPU
- Save

### مشکل: Dependencies نصب نمی‌شه
**حل:**
```python
!pip install --upgrade pip
!pip install --force-reinstall 'freqtrade[freqai]'
```

### مشکل: Drive mount نمی‌شه
**حل:**
- اجازه بدید به Colab برای دسترسی به Drive
- اگه باز نشد، یکبار disconnect و reconnect کنید

### مشکل: Repository clone نمی‌شه
**حل:**
```python
!git config --global http.postBuffer 524288000
!git clone https://github.com/aminak58/freqai-futures-strategy.git
```

---

## 📞 پشتیبانی

اگه مشکلی پیش اومد:
1. چک کنید Cell آخر (Troubleshooting)
2. بررسی کنید error message
3. بازنویسی کنید notebook و دوباره run کنید

---

## 🎓 مثال کامل

```python
# تنظیمات برای backtest 1 ماهه BTC
STRATEGY = "FreqAIHybridStrategy"
TIMERANGE = "20250901-20251001"
PAIRS = "BTC/USDT:USDT"
```

**زمان تقریبی:** 5-7 دقیقه

```python
# تنظیمات برای backtest 3 ماهه چند جفت ارز
STRATEGY = "FreqAIHybridStrategy"
TIMERANGE = "20250701-20251001"
PAIRS = "BTC/USDT:USDT ETH/USDT:USDT SOL/USDT:USDT"
```

**زمان تقریبی:** 10-15 دقیقه

---

**✨ حال ببرید از GPU رایگان! 🚀**

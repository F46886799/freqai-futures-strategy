# 🚨 راهنمای رفع مشکل Binance Geo-Restriction در Colab

## ❌ مشکل: 
```
"Service unavailable from a restricted location"
```

**دلیل:** Google Colab از سرورهای آمریکایی استفاده می‌کند و Binance در آمریکا محدود است.

---

## ✅ راه‌حل: استفاده از داده‌های محلی

### مرحله 1️⃣: فشرده کردن داده‌های محلی

در سیستم محلی خود (Windows):

```powershell
# رفتن به فولدر پروژه
cd C:\freqai-futures-strategy

# فشرده کردن داده‌ها
Compress-Archive -Path user_data\data\binance\* -DestinationPath binance_data.zip -Force
```

این فایل `binance_data.zip` را خواهید داشت (~50-100 MB).

---

### مرحله 2️⃣: آپلود به Google Drive

1. برو به [Google Drive](https://drive.google.com/)
2. یک فولدر جدید بساز: `FreqAI`
3. فایل `binance_data.zip` را آپلود کن

---

### مرحله 3️⃣: استفاده از Notebook جدید

من یک نسخه جدید از notebook ساختم که:
- ✅ از Google Drive داده می‌خواند
- ✅ نیازی به Binance API ندارد
- ✅ فقط backtest می‌کند (بدون download)

**فایل جدید:** `FreqAI_GPU_Backtest_Offline.ipynb`

---

### مرحله 4️⃣: اجرا در Colab

1. باز کن: [FreqAI_GPU_Backtest_Offline.ipynb](https://colab.research.google.com/github/aminak58/freqai-futures-strategy/blob/master/FreqAI_GPU_Backtest_Offline.ipynb)
2. GPU فعال کن
3. اجازه دسترسی به Google Drive بده
4. Run All!

---

## 🆚 مقایسه: راه‌حل‌ها

| روش | مزایا | معایب | زمان |
|-----|-------|-------|------|
| **Colab + Drive** | ✅ بدون محدودیت IP<br>✅ GPU رایگان<br>✅ داده‌های از قبل دانلود شده | ⚠️ نیاز به آپلود یکبار (~5 دقیقه) | 15-20 دقیقه |
| **Local CPU** | ✅ کنترل کامل | ❌ خیلی آهسته (4-6 ساعت) | 4-6 ساعت |
| **Kaggle** | ✅ GPU رایگان | ❌ GPU allocation مشکل دارد | نامشخص |

---

## 💡 گزینه جایگزین: استفاده از Binance Testnet

اگر نمی‌خواهی از Google Drive استفاده کنی، می‌توانی از **Binance Testnet** استفاده کنی که محدودیت جغرافیایی ندارد.

### تغییر در `config/config.json`:

```json
{
  "exchange": {
    "name": "binance",
    "ccxt_config": {
      "urls": {
        "api": {
          "public": "https://testnet.binancefuture.com",
          "private": "https://testnet.binancefuture.com"
        }
      }
    }
  }
}
```

**اما:** داده‌های Testnet محدود هستند و ممکن است کامل نباشند.

---

## 🎯 توصیه نهایی

**بهترین روش:** استفاده از **Colab + Google Drive** با داده‌های از قبل دانلود شده

چرا؟
- ✅ سریع (GPU T4)
- ✅ داده‌های کامل (365 روز)  
- ✅ بدون محدودیت
- ✅ رایگان

---

**آیا کمک کنم notebook جدید (Offline) را بسازیم?** 📝

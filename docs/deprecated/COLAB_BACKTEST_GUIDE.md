# 🚀 راهنمای Backtest در Google Colab با GPU

## 🎯 چرا Colab؟
- ✅ **GPU رایگان** (T4/V100) - 10-20x سریع‌تر از CPU
- ✅ **12 ساعت runtime** - کافی برای backtest کامل
- ✅ **رایگان** - نیاز به پرداخت نیست
- ✅ **نصب آسان** - همه چیز در یک notebook

**زمان تخمینی:**
- با CPU (محلی): 4-6 ساعت ⏰
- با GPU (Colab): **30-60 دقیقه** ⚡

---

## 📋 مراحل Setup

### 1️⃣ باز کردن Google Colab

1. برو به: https://colab.research.google.com/
2. `File` → `New notebook`
3. تغییر Runtime به GPU:
   - `Runtime` → `Change runtime type`
   - `Hardware accelerator` → **T4 GPU**
   - `Save`

---

### 2️⃣ نصب Freqtrade

در cell اول:

```python
# نصب TA-Lib
!wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz
!tar -xzf ta-lib-0.4.0-src.tar.gz
%cd ta-lib
!./configure --prefix=/usr
!make
!make install
%cd ..

# نصب Freqtrade
!pip install freqtrade[freqai] -q
!pip install technical pandas-ta -q

print("✅ Freqtrade نصب شد!")
```

---

### 3️⃣ Upload کردن فایل‌های پروژه

**Option A: از GitHub (توصیه می‌شود)**

```python
!git clone https://github.com/aminak58/freqai-futures-strategy.git
%cd freqai-futures-strategy

# یا اگر repo private است:
!git clone https://<YOUR_TOKEN>@github.com/aminak58/freqai-futures-strategy.git
%cd freqai-futures-strategy
```

**Option B: Upload دستی**

```python
from google.colab import files
import os

# ساخت ساختار
!mkdir -p user_data/strategies
!mkdir -p config

# Upload strategy
print("📤 Upload کنید: FreqAIHybridStrategy.py")
uploaded = files.upload()
!mv FreqAIHybridStrategy.py user_data/strategies/

# Upload config
print("📤 Upload کنید: config.json")
uploaded = files.upload()
!mv config.json config/
```

---

### 4️⃣ دانلود Data (در Colab)

```python
# دانلود 1 سال data
!freqtrade download-data \
  --exchange binance \
  --pairs BTC/USDT:USDT ETH/USDT:USDT SOL/USDT:USDT \
  --timeframes 5m 15m 1h \
  --days 365 \
  --trading-mode futures \
  --config config/config.json

print("✅ Data دانلود شد!")
```

⚠️ **نکته:** اگر در ایران هستید، VPN لازم است. می‌توانید data را از سیستم محلی upload کنید:

```python
# Upload data folder (zip شده)
from google.colab import files
uploaded = files.upload()

!unzip data.zip -d user_data/
```

---

### 5️⃣ اجرای Backtest با GPU

```python
# بررسی GPU
!nvidia-smi

# اجرای backtest
!freqtrade backtesting \
  --strategy FreqAIHybridStrategy \
  --config config/config.json \
  --freqaimodel LightGBMRegressorMultiTarget \
  --timerange 20250101-20251012 \
  --export trades

print("🎉 Backtest تمام شد!")
```

---

### 6️⃣ مشاهده و Download نتایج

```python
# نمایش نتایج
!cat user_data/backtest_results/backtest-result.json

# Download نتایج
from google.colab import files

# Download backtest results
files.download('user_data/backtest_results/backtest-result.json')

# Download trained models (اختیاری)
!zip -r models.zip user_data/models/
files.download('models.zip')

print("📥 فایل‌ها download شدند!")
```

---

## 📊 مقایسه Performance

| محیط | سخت‌افزار | زمان تخمینی | هزینه |
|------|----------|-------------|-------|
| **محلی (CPU)** | CPU معمولی | 4-6 ساعت ⏰ | رایگان |
| **Colab (GPU)** | T4 GPU | **30-60 دقیقه** ⚡ | رایگان |
| **Colab Pro** | V100/A100 | 15-30 دقیقه 🚀 | $10/ماه |

---

## 🔧 بهینه‌سازی‌ها برای Colab

### کاهش استفاده از RAM:

```python
# در config.json
{
  "freqai": {
    "train_period_days": 20,  # به جای 30
    "backtest_period_days": 10,  # به جای 7
  }
}
```

### استفاده از Cached Models:

```python
# Upload models قبلی (اگر دارید)
!unzip models.zip -d user_data/

# Freqtrade از models cached استفاده می‌کند
```

---

## ⚠️ نکات مهم

### 1. محدودیت زمانی
- Colab رایگان: **12 ساعت** runtime
- اگر disconnect شد، باید دوباره setup کنید
- برای training‌های طولانی، از Colab Pro استفاده کنید

### 2. ذخیره Progress
```python
# هر 1 ساعت models را backup کنید
import shutil
from datetime import datetime

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
shutil.make_archive(f'models_backup_{timestamp}', 'zip', 'user_data/models')
files.download(f'models_backup_{timestamp}.zip')
```

### 3. Monitoring
```python
# نمایش progress
!tail -f user_data/logs/freqtrade.log
```

---

## 🐛 عیب‌یابی

### خطا: "No GPU available"
```python
# بررسی GPU
import torch
print(f"CUDA available: {torch.cuda.is_available()}")
print(f"GPU: {torch.cuda.get_device_name(0)}")

# اگر False بود:
# Runtime → Change runtime type → Hardware accelerator → T4 GPU
```

### خطا: "Out of memory"
```python
# کاهش batch size در config
# یا استفاده از timerange کوچک‌تر:
!freqtrade backtesting ... --timerange 20250701-20251012
```

### خطا: "TA-Lib not found"
```python
# نصب مجدد TA-Lib
!apt-get install -y libta-lib0-dev
!pip install TA-Lib
```

---

## 📝 Notebook کامل (کپی-پیست آماده)

```python
# ========== Cell 1: Setup ==========
!wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz
!tar -xzf ta-lib-0.4.0-src.tar.gz
%cd ta-lib
!./configure --prefix=/usr
!make
!make install
%cd ..

!pip install freqtrade[freqai] technical pandas-ta -q

# ========== Cell 2: Clone Project ==========
!git clone https://github.com/aminak58/freqai-futures-strategy.git
%cd freqai-futures-strategy

# ========== Cell 3: Check GPU ==========
!nvidia-smi
import torch
print(f"✅ GPU available: {torch.cuda.is_available()}")

# ========== Cell 4: Download Data ==========
!freqtrade download-data \
  --exchange binance \
  --pairs BTC/USDT:USDT ETH/USDT:USDT SOL/USDT:USDT \
  --timeframes 5m 15m 1h \
  --days 365 \
  --trading-mode futures \
  --config config/config.json

# ========== Cell 5: Run Backtest ==========
!freqtrade backtesting \
  --strategy FreqAIHybridStrategy \
  --config config/config.json \
  --freqaimodel LightGBMRegressorMultiTarget \
  --timerange 20250101-20251012 \
  --export trades

# ========== Cell 6: Download Results ==========
from google.colab import files
files.download('user_data/backtest_results/backtest-result.json')
```

---

## 🎯 مزایای Colab برای پروژه ما

1. ✅ **سرعت**: 10-20x سریع‌تر
2. ✅ **رایگان**: بدون هزینه
3. ✅ **مناسب برای LSTM**: وقتی LSTM اضافه کنیم، GPU الزامی است
4. ✅ **Testing سریع**: می‌توانیم چندین strategy test کنیم
5. ✅ **Hyperopt**: برای بهینه‌سازی parameters

---

## 🔗 منابع

- [Google Colab](https://colab.research.google.com/)
- [Freqtrade Installation](https://www.freqtrade.io/en/stable/installation/)
- [FreqAI Documentation](https://www.freqtrade.io/en/stable/freqai/)

---

**نکته نهایی:** بعد از موفقیت backtest در Colab، می‌توانیم trained models را download کنیم و در سیستم محلی برای live trading استفاده کنیم! 🚀

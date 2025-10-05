# ✅ Checklist آماده‌سازی برای Push به GitHub

این checklist را قبل از push به GitHub بررسی کنید.

---

## 📦 فایل‌های ضروری

- [x] `README.md` - راهنمای اصلی
- [x] `SETUP_GUIDE.md` - راهنمای نصب تفصیلی
- [x] `MVP_DOCUMENTATION.md` - مستندات فنی کامل
- [x] `QUICK_START.md` - راهنمای سریع
- [x] `.gitignore` - نادیده گرفتن فایل‌های بزرگ
- [x] `docker-compose.yml` - تنظیمات Docker
- [x] `config/config.json` - کانفیگ اصلی
- [x] `user_data/strategies/FreqAIHybridStrategy.py` - استراتژی

---

## 🚫 فایل‌هایی که نباید Push شوند

این فایل‌ها در `.gitignore` هستند:

- [ ] `user_data/data/*.feather` (15.8 MB) - داده‌های تاریخی
- [ ] `user_data/models/` - مدل‌های trained
- [ ] `user_data/backtest_results/` - نتایج backtest
- [ ] `user_data/logs/` - فایل‌های log
- [ ] Docker image (13.8 GB) - نمی‌تواند push شود

---

## 🔒 امنیت

- [ ] API Key در `config.json` خالی است (`""`)
- [ ] Secret Key در `config.json` خالی است (`""`)
- [ ] هیچ اطلاعات حساس در فایل‌ها نیست
- [ ] `.gitignore` فایل‌های حساس را پوشش می‌دهد

---

## 📝 مستندات

- [x] README.md واضح و کامل است
- [x] SETUP_GUIDE.md راهنمای گام‌به‌گام دارد
- [x] تمام دستورات Docker صحیح و تست شده هستند
- [x] Troubleshooting guide موجود است

---

## 🧪 تست نهایی

قبل از push، این مراحل را تست کنید:

### 1. بررسی حجم Repository

```bash
cd C:\strategy
du -sh .git  # لینوکس/مک
# یا
Get-ChildItem -Recurse | Measure-Object -Property Length -Sum  # ویندوز
```

**✅ حجم باید < 50 MB باشد** (بدون .git)

### 2. بررسی فایل‌های Staged

```bash
git status
git ls-files --cached | wc -l  # تعداد فایل‌ها
```

**✅ نباید فایل .feather یا model موجود باشد**

### 3. تست Git Ignore

```bash
git status --ignored
```

**✅ فایل‌های بزرگ باید در لیست ignored باشند**

---

## 🚀 دستورات Push

### اولین بار (Initial Commit)

```bash
cd C:\strategy

# 1. Initialize Git (اگر قبلاً نکرده‌اید)
git init

# 2. افزودن remote
git remote add origin <YOUR_REPO_URL>

# 3. افزودن فایل‌ها
git add .

# 4. بررسی چه چیزی اضافه می‌شود
git status

# 5. Commit
git commit -m "Initial commit: FreqAI Hybrid Futures Strategy MVP

- Futures leverage trading strategy (2x-5x)
- FreqAI + LightGBM integration
- LONG & SHORT position support
- Multi-timeframe features (5m/15m/1h)
- SVM outlier detection
- Dynamic market regime detection
- Complete documentation in Farsi
- Docker setup included"

# 6. Push
git push -u origin main
```

### به‌روزرسانی‌های بعدی

```bash
# 1. بررسی تغییرات
git status

# 2. افزودن تغییرات جدید
git add .

# 3. Commit با پیام مناسب
git commit -m "Update: توضیح تغییرات"

# 4. Push
git push
```

---

## 📊 حجم فایل‌ها (تخمینی)

| Item | Size | Push به GitHub? |
|------|------|-----------------|
| کد Python | < 1 MB | ✅ بله |
| Config files | < 100 KB | ✅ بله |
| Documentation | < 500 KB | ✅ بله |
| Docker Compose | < 10 KB | ✅ بله |
| **Data files (.feather)** | **15.8 MB** | ❌ خیر |
| **Models** | **متغیر** | ❌ خیر |
| **Docker Image** | **13.8 GB** | ❌ خیر |
| **Total (بدون data/models)** | **< 5 MB** | ✅ OK |

---

## 🔍 بررسی نهایی قبل از Push

```bash
# حجم repository بدون .git
cd C:\strategy
Get-ChildItem -Recurse -File | Where-Object { 
    $_.FullName -notlike "*\.git\*" -and
    $_.FullName -notlike "*\user_data\data\*" -and
    $_.FullName -notlike "*\user_data\models\*"
} | Measure-Object -Property Length -Sum | 
Select-Object @{N='SizeMB';E={[math]::Round($_.Sum/1MB,2)}}
```

**انتظار: < 5 MB**

---

## 📥 دستورات Clone روی PC جدید

```bash
# 1. Clone
git clone <YOUR_REPO_URL>
cd strategy

# 2. Pull Docker Image
docker pull freqtradeorg/freqtrade:stable_freqairl

# 3. دانلود Data
docker run --rm -v ${PWD}/user_data:/freqtrade/user_data \
  freqtradeorg/freqtrade:stable_freqairl download-data \
  --exchange binance \
  --pairs BTC/USDT:USDT ETH/USDT:USDT SOL/USDT:USDT \
  --timeframes 5m 15m 1h \
  --days 500 \
  --trading-mode futures

# 4. Run Backtest
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

---

## ⚠️ مشکلات متداول

### مشکل 1: "File too large" error

**علت:** فایل بزرگ‌تر از 100 MB

**راه‌حل:**
```bash
# یافتن فایل‌های بزرگ
git ls-files | xargs -I{} ls -lh {} | sort -k5 -h

# حذف از Git
git rm --cached <large_file>

# اضافه به .gitignore
echo "<large_file>" >> .gitignore
```

### مشکل 2: Push خیلی کند است

**علت:** فایل‌های زیاد یا بزرگ

**راه‌حل:**
```bash
# بررسی حجم
git count-objects -vH

# فشرده‌سازی
git gc --aggressive
```

### مشکل 3: "API Key committed" warning

**راه‌حل:**
```bash
# حذف history حاوی API key
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch config/config.json" \
  --prune-empty --tag-name-filter cat -- --all

# Force push (خطرناک!)
git push --force
```

---

## ✅ Checklist نهایی

قبل از `git push`:

- [ ] همه تغییرات committed شده
- [ ] `.gitignore` صحیح است
- [ ] فایل‌های بزرگ ignore شده‌اند
- [ ] API Key ها خالی هستند
- [ ] مستندات کامل است
- [ ] حجم repository < 50 MB
- [ ] README.md واضح و مفید است
- [ ] دستورات Docker تست شده‌اند

---

**آماده Push هستید! 🚀**


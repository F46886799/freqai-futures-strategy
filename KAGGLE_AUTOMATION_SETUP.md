# 🚀 راهنمای راه‌اندازی Kaggle Automation

## مقایسه روش‌ها

| ویژگی | Colab SSH (روش دوست) | Kaggle API (پیشنهادی) |
|-------|---------------------|---------------------|
| **دائمی بودن** | ❌ نیاز به باز کردن notebook | ✅ کاملاً خودکار |
| **Trigger خودکار** | ❌ دستی | ✅ با هر push |
| **Session Timeout** | ❌ 12 ساعت | ✅ بدون محدودیت workflow |
| **امنیت** | ⚠️ Token در notebook | ✅ GitHub Secrets |
| **Setup اولیه** | متوسط | ساده |
| **نیاز به باز کردن UI** | ✅ هر بار | ❌ هیچ‌وقت |
| **GPU رایگان** | ✅ T4 | ✅ P100/T4 |

---

## 📋 پیش‌نیازها

1. حساب کاربری Kaggle
2. دسترسی به GitHub Repository
3. 10 دقیقه وقت برای setup

---

## 🔧 راه‌اندازی گام‌به‌گام

### گام 1️⃣: دریافت Kaggle API Credentials

1. برو به [Kaggle Account Settings](https://www.kaggle.com/settings/account)
2. اسکرول به پایین تا بخش **API**
3. کلیک کن روی **Create New API Token**
4. فایل `kaggle.json` دانلود میشه با محتوای:
   ```json
   {
     "username": "your-kaggle-username",
     "key": "abc123xyz..."
   }
   ```

### گام 2️⃣: افزودن Secrets به GitHub

1. برو به [Repository Settings → Secrets and variables → Actions](https://github.com/aminak58/freqai-futures-strategy/settings/secrets/actions)
2. کلیک **New repository secret**
3. اضافه کن:
   - **Name:** `KAGGLE_USERNAME`
   - **Value:** مقدار `username` از فایل `kaggle.json`
4. دوباره کلیک **New repository secret**
5. اضافه کن:
   - **Name:** `KAGGLE_KEY`
   - **Value:** مقدار `key` از فایل `kaggle.json`

### گام 3️⃣: فعال‌سازی Workflow

workflow فایل `.github/workflows/5-kaggle-backtest.yml` آماده است!

**Commit و Push کن:**
```bash
git add .github/workflows/5-kaggle-backtest.yml
git add KAGGLE_AUTOMATION_SETUP.md
git commit -m "feat: Add Kaggle GPU automation workflow"
git push origin master
```

### گام 4️⃣: تست اولیه (دستی)

1. برو به [Actions tab](https://github.com/aminak58/freqai-futures-strategy/actions)
2. انتخاب کن: **🚀 Kaggle GPU Backtest (Automated)**
3. کلیک **Run workflow**
4. (اختیاری) تنظیم کن:
   - **Timerange:** `20250701-20251012` (برای تست سریع‌تر)
   - **Pairs:** `BTC/USDT:USDT` (فقط یک جفت)
5. کلیک **Run workflow**

### گام 5️⃣: مشاهده نتایج

بعد از اجرای workflow:

1. در GitHub Actions → کلیک روی workflow run → ببین Summary
2. لینک Kaggle kernel نمایش داده میشه
3. برو به Kaggle و نتایج backtest رو ببین

---

## 🔄 استفاده روزمره (خودکار!)

از این به بعد:

```bash
# 1. تغییرات در strategy
vim user_data/strategies/FreqAIHybridStrategy.py

# 2. Commit
git add .
git commit -m "update: improved regime detection"

# 3. Push
git push

# ✨ تمام! 
# Workflow خودکار trigger میشه
# Backtest روی Kaggle GPU اجرا میشه
# نتایج در Actions قابل مشاهده است
```

**بدون:**
- ❌ باز کردن Colab
- ❌ اجرای دستی notebook
- ❌ SSH connection
- ❌ نگرانی از timeout

---

## 🎛️ تنظیمات پیشرفته

### تغییر Trigger Conditions

در `.github/workflows/5-kaggle-backtest.yml`:

```yaml
on:
  push:
    branches: [master, develop]  # اضافه کردن branch دیگر
    paths:
      - 'user_data/strategies/**'
      - 'config/**'  # trigger برای تغییرات config هم
```

### Scheduled Backtest (مثلاً هر شب)

اضافه کن به `on:`:

```yaml
on:
  schedule:
    - cron: '0 2 * * *'  # هر شب ساعت 2 صبح UTC
```

### نتایج در Artifact

برای دانلود خودکار نتایج، اضافه کن:

```yaml
- name: 📦 Upload Results
  uses: actions/upload-artifact@v3
  with:
    name: backtest-results
    path: user_data/backtest_results/
```

---

## 🆚 مقایسه با روش Colab SSH

### Colab SSH (روش دوست):
```bash
# هر بار:
1. باز کن Colab notebook
2. Run کن setup cell (SSH + ngrok)
3. منتظر بمان تا SSH آماده شود
4. ssh root@xyz.ngrok.io -p 12345
5. cd repo && git pull
6. python backtest...
7. بعد از 12 ساعت → تکرار از مرحله 1
```

### Kaggle Automation (این روش):
```bash
# فقط یکبار setup:
1. افزودن Kaggle credentials به GitHub Secrets
2. Push کردن workflow file

# بعد از آن، برای همیشه:
git push  # ✨ همین!
```

---

## 🔍 Troubleshooting

### ❌ Error: "Could not find kaggle.json"
- مطمئن شو که `KAGGLE_USERNAME` و `KAGGLE_KEY` در GitHub Secrets درست هستند

### ❌ Kernel fails with "403 Forbidden"
- Kaggle account باید verified باشد (شماره تلفن)
- بررسی کن: [Kaggle Settings](https://www.kaggle.com/settings)

### ❌ "No module named freqai"
- نسخه freqtrade در script باید شامل `[freqai]` باشد
- بررسی کن خط `pip install freqtrade[freqai]`

### ⚠️ Backtest خیلی طول میکشه
- تایمرنج رو کمتر کن: `20250901-20251012` (2 ماه)
- یا فقط یک pair: `BTC/USDT:USDT`

---

## 📊 نتایج مورد انتظار

بعد از backtest موفق، خروجی شبیه این:

```
✅ Backtest completed successfully!

💰 Total Profit: 1234.56 USDT
📈 Profit %: 12.34%
📊 Sharpe Ratio: 1.85
📉 Max Drawdown: -8.5%
🎯 Win Rate: 58%
🔢 Total Trades: 342
```

---

## 🚀 مرحله بعدی

بعد از راه‌اندازی موفق:

1. ✅ **Issue #2:** افزایش test coverage (workflow test هم خودکاره!)
2. ✅ **Issue #3:** LSTM implementation (روی Kaggle GPU بسیار سریع‌تر)
3. ✅ **Optimization:** Hyperparameter tuning خودکار
4. ✅ **Monitoring:** نتایج backtest رو در dashboard نمایش بده

---

## 💡 نکته نهایی

**روش Colab SSH** برای debugging تعاملی خوبه.
**روش Kaggle API** برای automation و CI/CD حرفه‌ای.

**هر دو رو میتونی داشته باشی!** 🎯
- Kaggle برای هر push خودکار
- Colab SSH برای تست دستی و debugging

---

## 📞 کمک و پشتیبانی

اگه مشکلی پیش اومد:
1. بررسی کن [GitHub Actions Logs](https://github.com/aminak58/freqai-futures-strategy/actions)
2. بررسی کن [Kaggle Kernel Output](https://www.kaggle.com/code/your-username/freqai-backtest/output)
3. یا Issue باز کن در repository

---

**ساخته شده با ❤️ برای FreqAI Futures Strategy**

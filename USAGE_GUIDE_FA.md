# استفاده از سیستم اتوماسیون GPU

## مراحل استفاده

### قدم 1️⃣: دریافت توکن ngrok (یکبار)

1. برو به: https://dashboard.ngrok.com/signup
2. ثبت‌نام کن (رایگان)
3. برو به: https://dashboard.ngrok.com/get-started/your-authtoken
4. کپی کن توکن را

---

### قدم 2️⃣: راه‌اندازی Colab

1. **باز کن این notebook را در Colab**:
   
   https://colab.research.google.com/github/aminak58/freqai-futures-strategy/blob/master/Colab_Remote_Setup.ipynb

2. **فعال کن GPU**:
   - Runtime → Change runtime type → GPU (T4) → Save

3. **اجرا کن تمام سل‌ها** (Runtime → Run all یا Ctrl+F9)

4. **وارد کن توکن ngrok** وقتی پرسید

5. **یادداشت کن اطلاعات اتصال**:
   ```
   Tunnel URL: tcp://0.tcp.ngrok.io:12345
   Password: abc123xyz456
   ```

---

### قدم 3️⃣: اجرای بکتست از کامپیوتر محلی

در PowerShell محلی:

```powershell
# اطمینان از نصب dependencies
pip install paramiko requests

# اجرای بکتست
python tools/backtest_executor.py `
  --tunnel-url "tcp://0.tcp.ngrok.io:12345" `
  --password "abc123xyz456" `
  --strategy FreqAIHybridStrategy `
  --timerange 20250901-20251012 `
  --pairs BTC/USDT:USDT
```

---

### قدم 4️⃣: مشاهده نتایج

نتایج به صورت خودکار دانلود می‌شوند در:
```
backtest_results/
├── backtest_FreqAIHybridStrategy_20250901-20251012_TIMESTAMP.json
```

---

## اجرای Batch (چندین بکتست)

```python
from tools.backtest_executor import ColabBacktestExecutor, BacktestConfig

# تعریف بکتست‌ها
configs = [
    BacktestConfig(
        strategy="FreqAIHybridStrategy",
        timerange="20250901-20251012",
        pairs=["BTC/USDT:USDT"]
    ),
    BacktestConfig(
        strategy="FreqAIHybridStrategy",
        timerange="20250801-20250831",
        pairs=["ETH/USDT:USDT"]
    ),
    BacktestConfig(
        strategy="FreqAIHybridStrategy",
        timerange="20250701-20250731",
        pairs=["SOL/USDT:USDT"]
    ),
]

# اجرا
executor = ColabBacktestExecutor(
    tunnel_url="tcp://0.tcp.ngrok.io:12345",
    password="abc123xyz456"
)

try:
    executor.connect()
    print("✅ متصل شد به Colab GPU")
    
    results = executor.execute_batch(configs)
    
    # نمایش نتایج
    print("\n" + "="*70)
    print("خلاصه نتایج")
    print("="*70)
    
    for i, result in enumerate(results, 1):
        if 'error' not in result:
            r = result['results']
            print(f"\n{i}. {result['config'].pairs[0]} - {result['config'].timerange}")
            print(f"   💰 سود: {r['total_profit_abs']:.2f} USDT ({r['total_profit_pct']:.2f}%)")
            print(f"   📊 Sharpe: {r['sharpe_ratio']:.3f}")
            print(f"   📉 Drawdown: {r['max_drawdown']:.2f}%")
            print(f"   🎯 Win Rate: {r['win_rate']:.1f}%")
            print(f"   ⏱️ زمان: {result['elapsed_seconds']/60:.1f} دقیقه")
        else:
            print(f"\n{i}. ❌ خطا: {result['error']}")
    
finally:
    executor.disconnect()
    print("\n✅ اتصال قطع شد")
```

---

## نکات مهم

### ✅ مزایا

- **سرعت**: 10-15x سریعتر از CPU (GPU vs CPU)
- **رایگان**: Colab رایگان با GPU T4
- **خودکار**: اتصال، اجرا، دانلود همه خودکار
- **Batch**: اجرای چندین بکتست پشت سر هم
- **مانیتورینگ**: لاگ لحظه‌ای پیشرفت

### ⚠️ محدودیت‌ها

- **زمان**: حداکثر 12 ساعت session در Colab
- **GPU**: ممکن است در ساعات شلوغ کند شود
- **شبکه**: نیاز به اینترنت پایدار

### 🔧 عیب‌یابی

#### اگر tunnel وصل نشد:
```powershell
# بررسی کن توکن ngrok را درست وارد کردی
# یا از یک توکن جدید استفاده کن
```

#### اگر SSH متصل نشد:
```powershell
# مطمئن شو password درست است
# مطمئن شو tunnel URL درست است (tcp://...)
```

#### اگر بکتست fail شد:
```powershell
# بررسی کن data در Colab هست
# بررسی کن strategy file صحیح است
# نگاه کن به لاگ‌های خطا
```

---

## مثال کامل

```powershell
# 1. نصب dependencies
pip install paramiko requests

# 2. تک بکتست
python tools/backtest_executor.py `
  --tunnel-url "tcp://0.tcp.ngrok.io:12345" `
  --password "your_password" `
  --strategy FreqAIHybridStrategy `
  --timerange 20250901-20251012 `
  --pairs BTC/USDT:USDT

# 3. چند جفت ارز
python tools/backtest_executor.py `
  --tunnel-url "tcp://0.tcp.ngrok.io:12345" `
  --password "your_password" `
  --strategy FreqAIHybridStrategy `
  --timerange 20250901-20251012 `
  --pairs BTC/USDT:USDT ETH/USDT:USDT SOL/USDT:USDT
```

---

## سوالات متداول

**Q: آیا باید هر بار توکن ngrok جدید بگیرم؟**
A: خیر. یکبار توکن بگیر و همیشه استفاده کن.

**Q: می‌تونم بیش از 12 ساعت استفاده کنم؟**
A: خیر. Colab رایگان 12 ساعت محدودیت داره. بعدش باید session جدید باز کنی.

**Q: آیا می‌تونم چندین بکتست همزمان اجرا کنم؟**
A: خیر. هر session یک بکتست. ولی می‌تونی batch execution کنی (یکی بعد از دیگری).

**Q: اگر connection قطع شد چی؟**
A: نگران نباش. می‌تونی دوباره وصل شی. نتایج تا اون لحظه ذخیره شده.

**Q: آیا امنه؟**
A: بله. password فقط برای این session است و بعد از disconnect دیگه کار نمی‌کنه.

---

## پشتیبانی

اگر مشکلی داشتی:
1. ببین `docs/guides/AUTOMATION.md` برای جزئیات بیشتر
2. چک کن GitHub Issues
3. Issue جدید باز کن با جزئیات کامل

---

**این روش حرفه‌ای است. استفاده کن! 🚀**

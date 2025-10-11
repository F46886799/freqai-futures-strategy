# 🔍 بررسی نیازمندی‌ها و راه‌اندازی محیط توسعه

**تاریخ:** 12 اکتبر 2025

---

## 📋 نیازمندی‌های Freqtrade

### Python Version
**Freqtrade 2025.1** پشتیبانی می‌کند:
- ✅ **Python 3.10** (Recommended)
- ✅ **Python 3.11** (Recommended) 
- ✅ **Python 3.12** (Supported)
- ❌ Python 3.9 و پایین‌تر (Deprecated)
- ❌ Python 3.13 (هنوز پشتیبانی نمی‌شود)

**شما:** Python 3.13.5 ❌  
**توصیه:** استفاده از Python 3.11 که در `C:\` دارید ✅

---

## ⚠️ مشکل فعلی

شما Python 3.13.5 در PATH دارید که Freqtrade هنوز از آن پشتیبانی نمی‌کند.

**راه‌حل:**
1. استفاده از Python 3.11 موجود در `C:\`
2. ایجاد Virtual Environment با Python 3.11
3. نصب Freqtrade در venv

---

## 🛠️ راهنمای نصب صحیح

### گام 1: بررسی Python 3.11

```powershell
# بررسی مسیر Python 3.11
C:\Python311\python.exe --version
# یا
py -3.11 --version
```

**انتظار:** `Python 3.11.x`

---

### گام 2: ایجاد Virtual Environment

```powershell
cd c:\freqai-futures-strategy

# ایجاد venv با Python 3.11
C:\Python311\python.exe -m venv venv

# یا اگر py launcher نصب است:
py -3.11 -m venv venv
```

---

### گام 3: فعال‌سازی Virtual Environment

```powershell
# در PowerShell
.\venv\Scripts\Activate.ps1

# اگر با خطای execution policy مواجه شدید:
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned

# سپس دوباره:
.\venv\Scripts\Activate.ps1
```

**بعد از فعال‌سازی، prompt باید این شکلی باشد:**
```
(venv) PS C:\freqai-futures-strategy>
```

---

### گام 4: آپدیت pip

```powershell
python -m pip install --upgrade pip setuptools wheel
```

---

### گام 5: نصب Freqtrade

```powershell
# نصب Freqtrade با تمام dependencies
pip install freqtrade[all]

# یا برای FreqAI:
pip install freqtrade[freqai]
```

**توضیح extras:**
- `[all]`: همه ویژگی‌ها شامل FreqAI
- `[freqai]`: فقط FreqAI و ML dependencies
- `[hyperopt]`: برای بهینه‌سازی
- `[plot]`: برای نمودارها

---

### گام 6: نصب Dependencies پروژه

```powershell
# Development dependencies
pip install -r requirements-dev.txt

# Project dependencies
pip install -r requirements.txt

# Technical libraries برای استراتژی
pip install technical pandas-ta ta-lib
```

**⚠️ نکته:** `ta-lib` ممکن است در Windows نیاز به binary نصب از wheel داشته باشد:
```powershell
# دانلود wheel از: https://www.lfd.uci.edu/~gohlke/pythonlibs/#ta-lib
pip install TA_Lib-0.4.XX-cp311-cp311-win_amd64.whl
```

---

### گام 7: تست نصب

```powershell
# بررسی Freqtrade
freqtrade --version

# بررسی Python و libraries
python -c "import freqtrade; print(freqtrade.__version__)"
python -c "import pandas; print('pandas:', pandas.__version__)"
python -c "import numpy; print('numpy:', numpy.__version__)"

# تست استراتژی
python -c "import sys; sys.path.insert(0, 'user_data/strategies'); from FreqAIHybridStrategy import FreqAIHybridStrategy; print('Strategy OK')"
```

---

## 📦 لیست کامل Dependencies

### Core (Freqtrade)
```
freqtrade[freqai]>=2025.1
```

### ML & Data Science
```
scikit-learn>=1.3.0
lightgbm>=4.0.0
xgboost>=2.0.0
catboost>=1.2.0
tensorflow>=2.13.0  # برای LSTM (اختیاری)
torch>=2.0.0        # جایگزین TensorFlow (اختیاری)
```

### Technical Analysis
```
technical>=1.4.0
pandas-ta>=0.3.14
ta-lib  # نیاز به binary install
```

### Testing
```
pytest>=7.4.0
pytest-cov>=4.1.0
pytest-mock>=3.11.0
pytest-asyncio>=0.21.0
```

### Code Quality
```
black>=23.0.0
isort>=5.12.0
flake8>=6.0.0
pylint>=2.17.0
mypy>=1.4.0
```

### Monitoring & Notifications
```
python-telegram-bot>=20.0
requests>=2.31.0
plotly>=5.17.0
streamlit>=1.27.0
```

---

## 🔧 اصلاح workflow های GitHub

### مشکل فعلی در workflows

بررسی `.github/workflows/2-unit-tests.yml`:

```yaml
strategy:
  matrix:
    python-version: ['3.10', '3.11']  # ✅ درست
```

**مشکلات احتمالی:**

1. **Dependencies نصب نمی‌شوند**
   ```yaml
   - name: Install dependencies
     run: |
       python -m pip install --upgrade pip
       pip install freqtrade[freqai]  # ⚠️ این خط احتمالاً نیست
       pip install pytest pytest-cov
   ```

2. **TA-Lib موجود نیست** (در Ubuntu نیاز به build)
   ```yaml
   - name: Install TA-Lib
     run: |
       wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz
       tar -xzf ta-lib-0.4.0-src.tar.gz
       cd ta-lib/ && ./configure --prefix=/usr && make && sudo make install
   ```

3. **Strategy import می‌کند اما Freqtrade context ندارد**

---

## ✅ راه‌حل پیشنهادی

### گزینه 1: تست با Mock (سریع‌تر)

```python
# در test_strategy_logic.py
import pytest
from unittest.mock import Mock, patch

@pytest.fixture
def mock_freqtrade_context():
    """Mock Freqtrade context"""
    with patch('freqtrade.strategy.IStrategy'):
        yield

def test_with_mock(mock_freqtrade_context):
    # تست‌های شما
    pass
```

### گزینه 2: نصب کامل Freqtrade در CI

```yaml
# .github/workflows/2-unit-tests.yml
- name: Install Freqtrade and dependencies
  run: |
    # TA-Lib
    sudo apt-get update
    sudo apt-get install -y build-essential wget
    wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz
    tar -xzf ta-lib-0.4.0-src.tar.gz
    cd ta-lib/ && ./configure --prefix=/usr && make && sudo make install
    cd ..
    
    # Python packages
    pip install --upgrade pip setuptools wheel
    pip install freqtrade[freqai]
    pip install technical pandas-ta
    pip install -r requirements-dev.txt
```

### گزینه 3: استفاده از Docker در CI (توصیه می‌شود)

```yaml
jobs:
  test-in-docker:
    runs-on: ubuntu-latest
    container:
      image: freqtradeorg/freqtrade:stable_freqairl
    steps:
      - uses: actions/checkout@v4
      - name: Run tests
        run: |
          pip install pytest pytest-cov
          pytest tests/ -v
```

---

## 📝 چک‌لیست راه‌اندازی

### Local Development

- [ ] Python 3.11 در سیستم نصب است
- [ ] Virtual environment ایجاد شده
- [ ] venv فعال شده
- [ ] pip آپدیت شده
- [ ] Freqtrade نصب شده (`freqtrade --version`)
- [ ] Dependencies نصب شده
- [ ] TA-Lib نصب شده (اگر نیاز است)
- [ ] استراتژی import می‌شود بدون خطا
- [ ] تست‌ها اجرا می‌شوند (`pytest tests/ -v`)

### GitHub Actions

- [ ] Python version صحیح است (3.10 یا 3.11)
- [ ] Freqtrade در workflow نصب می‌شود
- [ ] TA-Lib در Ubuntu نصب می‌شود (اگر نیاز است)
- [ ] تمام dependencies نصب می‌شوند
- [ ] تست‌ها pass می‌شوند یا با `continue-on-error: true`

---

## 🚀 دستورات سریع

### راه‌اندازی اولیه (بار اول)

```powershell
# 1. ایجاد venv
py -3.11 -m venv venv

# 2. فعال‌سازی
.\venv\Scripts\Activate.ps1

# 3. نصب Freqtrade
pip install --upgrade pip
pip install freqtrade[freqai]

# 4. نصب dependencies
pip install -r requirements-dev.txt
pip install technical pandas-ta

# 5. تست
pytest tests/ -v
```

### استفاده روزمره

```powershell
# فعال‌سازی venv
.\venv\Scripts\Activate.ps1

# اجرای تست‌ها
pytest tests/ -v --cov

# اجرای backtest (با Docker - توصیه می‌شود)
docker run --rm -v ${PWD}/user_data:/freqtrade/user_data `
  freqtradeorg/freqtrade:stable_freqairl backtesting `
  --strategy FreqAIHybridStrategy `
  --config config/config.json
```

---

## ❓ سوالات متداول

### Q: چرا Python 3.13 کار نمی‌کند؟
A: Freqtrade و dependencies آن هنوز با Python 3.13 تست نشده‌اند. برخی packages ممکن است binary wheels نداشته باشند.

### Q: آیا باید حتماً venv استفاده کنم؟
A: بله! برای جلوگیری از conflict بین packages و نصب تمیز.

### Q: Docker بهتر است یا نصب مستقیم؟
A: **Docker برای production/backtest** (راحت‌تر و سریع‌تر)  
**نصب مستقیم برای development** (debug و توسعه راحت‌تر)

### Q: TA-Lib اجباری است؟
A: خیر، اگر از `technical` و `pandas-ta` استفاده کنید نیازی نیست.

---

## 📞 کمک بیشتر

اگر مشکلی داشتید:
1. بررسی [FAQ.md](FAQ.md)
2. بررسی logs دقیق
3. جستجو در [Freqtrade Issues](https://github.com/freqtrade/freqtrade/issues)
4. ایجاد Issue در repo شما

---

**بعدی:** پس از راه‌اندازی محیط، به [CURRENT_STATUS.md](CURRENT_STATUS.md) برگردید.

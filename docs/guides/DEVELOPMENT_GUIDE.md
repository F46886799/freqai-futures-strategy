# 🚀 راهنمای شروع توسعه

**تاریخ:** 12 اکتبر 2025

---

## 📋 چک‌لیست شروع

### ✅ مستندات (تکمیل شده)
- [x] README.md
- [x] QUICK_START.md
- [x] SETUP_GUIDE.md
- [x] MVP_DOCUMENTATION.md
- [x] FAQ.md
- [x] GLOSSARY.md
- [x] ROADMAP.md

### 🔴 کارهای فوری (این هفته)

#### 1. تکمیل Unit Tests (روز 1-2)
#### 2. تست CI/CD Workflows (روز 3-4)  
#### 3. بهبود Monitoring (روز 5)

---

## 🎯 مرحله 1: تکمیل Unit Tests

### فایل‌های موجود:
```
tests/
├── __init__.py
├── test_strategy_logic.py (نیمه‌کامل)
├── test_main.py
└── test_integration.py (نیمه‌کامل)
```

### کارهای لازم:

#### A. تکمیل `test_strategy_logic.py`

**وضعیت فعلی:** کلاس‌های پایه موجود است  
**نیاز:** تکمیل تست‌های زیر

```python
# تست‌های مورد نیاز:

class TestMarketRegimeDetection:
    """تست تشخیص رژیم بازار"""
    def test_regime_calculation()
    def test_trending_up_detection()
    def test_trending_down_detection()
    def test_high_volatility_detection()
    def test_range_market_detection()

class TestEntryExitSignals:
    """تست سیگنال‌های ورود و خروج"""
    def test_long_entry_conditions()
    def test_short_entry_conditions()
    def test_long_exit_conditions()
    def test_short_exit_conditions()

class TestLeverageCalculation:
    """تست محاسبه leverage"""
    def test_leverage_in_trending_market()
    def test_leverage_in_volatile_market()
    def test_leverage_in_range_market()
    def test_max_leverage_limit()

class TestRiskManagement:
    """تست مدیریت ریسک"""
    def test_stoploss_calculation()
    def test_trailing_stop()
    def test_position_sizing()
    def test_max_open_trades()
```

**دستور اجرا:**
```powershell
cd c:\freqai-futures-strategy
pytest tests/test_strategy_logic.py -v --cov=user_data/strategies
```

---

#### B. ایجاد `test_freqai.py`

**فایل جدید:** `tests/test_freqai.py`

```python
"""
Tests for FreqAI Integration
"""
import pytest
from FreqAIHybridStrategy import FreqAIHybridStrategy

class TestFreqAIIntegration:
    """تست FreqAI features"""
    
    def test_feature_engineering()
    def test_informative_pairs()
    def test_feature_expansion()
    def test_multi_timeframe_features()

class TestModelPredictions:
    """تست پیش‌بینی‌های مدل"""
    
    def test_prediction_format()
    def test_prediction_range()
    def test_outlier_handling()
    def test_multi_target_predictions()

class TestRegimeFeatures:
    """تست regime features"""
    
    def test_regime_features_exist()
    def test_regime_values_valid()
    def test_multi_horizon_regimes()
```

**دستور ایجاد:**
```powershell
# کپی template
Copy-Item tests/test_strategy_logic.py tests/test_freqai.py
# ویرایش محتوا
code tests/test_freqai.py
```

---

#### C. تکمیل `test_integration.py`

**کارهای لازم:**

```python
class TestDockerIntegration:
    """تست Docker"""
    def test_docker_image_exists()
    def test_docker_container_runs()
    def test_strategy_loads_in_container()

class TestDataDownload:
    """تست دانلود داده"""
    def test_download_futures_data()
    def test_data_format_correct()
    def test_multiple_timeframes()

class TestBacktestExecution:
    """تست backtest"""
    def test_backtest_runs()
    def test_backtest_output_valid()
    def test_freqai_model_training()
```

---

### 📊 Target Coverage: 80%+

**فعلی:** ~30% (تخمینی)  
**هدف:** > 80%

**بررسی coverage:**
```powershell
pytest tests/ -v --cov=user_data/strategies --cov-report=html
# باز کردن htmlcov/index.html
```

---

## 🔄 مرحله 2: تست CI/CD Workflows

### فایل‌های موجود:
```
.github/workflows/
├── 1-code-quality.yml ✅
├── 2-unit-tests.yml ✅
├── 3-backtest.yml ✅
└── 4-performance-tracking.yml ✅
```

### کارهای لازم:

#### A. بررسی محتوای Workflows

```powershell
# بررسی هر workflow
Get-Content .github/workflows/1-code-quality.yml
Get-Content .github/workflows/2-unit-tests.yml
Get-Content .github/workflows/3-backtest.yml
Get-Content .github/workflows/4-performance-tracking.yml
```

#### B. تست Local (قبل از push)

**نصب dependencies:**
```powershell
pip install -r requirements-dev.txt
```

**تست code quality:**
```powershell
# Black (formatting)
black --check user_data/strategies/ tests/ monitoring/

# isort (imports)
isort --check-only user_data/strategies/ tests/ monitoring/

# flake8 (linting)
flake8 user_data/strategies/ tests/ monitoring/

# pylint
pylint user_data/strategies/FreqAIHybridStrategy.py
```

#### C. Commit و Push برای تست Workflows

```powershell
git add .
git commit -m "test: بررسی CI/CD workflows"
git push origin master
```

**مشاهده نتایج:**
```
https://github.com/aminak58/freqai-futures-strategy/actions
```

---

## 📡 مرحله 3: بهبود Monitoring System

### فایل‌های موجود:
```
monitoring/
├── __init__.py ✅
├── extract_metrics.py ✅
├── generate_report.py ✅
└── compare_versions.py ✅
```

### کارهای لازم:

#### A. اضافه کردن Telegram Notifications

**فایل جدید:** `monitoring/telegram_notifier.py`

```python
"""
Telegram Notification System
"""
import os
from telegram import Bot
from telegram.error import TelegramError

class TelegramNotifier:
    def __init__(self):
        self.token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.chat_id = os.getenv('TELEGRAM_CHAT_ID')
        self.bot = Bot(token=self.token) if self.token else None
    
    def send_backtest_results(self, metrics: dict):
        """ارسال نتایج backtest"""
        if not self.bot:
            return
        
        message = f"""
🤖 **Backtest Results**

📊 **Metrics:**
• Total Profit: {metrics.get('total_profit', 0)}%
• Win Rate: {metrics.get('win_rate', 0)}%
• Sharpe Ratio: {metrics.get('sharpe_ratio', 0)}
• Max Drawdown: {metrics.get('max_drawdown', 0)}%
• Total Trades: {metrics.get('total_trades', 0)}

⏰ {metrics.get('timestamp', 'N/A')}
        """
        
        try:
            self.bot.send_message(
                chat_id=self.chat_id,
                text=message,
                parse_mode='Markdown'
            )
        except TelegramError as e:
            print(f"❌ Error sending to Telegram: {e}")
```

**نصب:**
```powershell
pip install python-telegram-bot
```

**استفاده:**
```python
from monitoring.telegram_notifier import TelegramNotifier

notifier = TelegramNotifier()
notifier.send_backtest_results(metrics)
```

---

#### B. اضافه کردن Discord Webhook

**فایل جدید:** `monitoring/discord_notifier.py`

```python
"""
Discord Webhook System
"""
import os
import requests
from datetime import datetime

class DiscordNotifier:
    def __init__(self):
        self.webhook_url = os.getenv('DISCORD_WEBHOOK_URL')
    
    def send_alert(self, title: str, description: str, color: int = 3066993):
        """ارسال alert به Discord"""
        if not self.webhook_url:
            return
        
        embed = {
            "title": title,
            "description": description,
            "color": color,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        data = {"embeds": [embed]}
        
        try:
            response = requests.post(
                self.webhook_url,
                json=data,
                headers={'Content-Type': 'application/json'}
            )
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"❌ Error sending to Discord: {e}")
```

---

#### C. Dashboard تعاملی (Streamlit)

**فایل جدید:** `monitoring/dashboard.py`

```python
"""
Interactive Dashboard for Monitoring
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

st.set_page_config(
    page_title="FreqAI Strategy Monitor",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 FreqAI Hybrid Strategy - Performance Dashboard")

# Load metrics history
@st.cache_data
def load_metrics():
    metrics_file = Path("monitoring/metrics_history.csv")
    if metrics_file.exists():
        return pd.read_csv(metrics_file)
    return pd.DataFrame()

metrics = load_metrics()

if not metrics.empty:
    # Metrics over time
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Latest Total Profit", 
                  f"{metrics['total_profit'].iloc[-1]:.2f}%")
    
    with col2:
        st.metric("Latest Win Rate", 
                  f"{metrics['win_rate'].iloc[-1]:.2f}%")
    
    with col3:
        st.metric("Latest Sharpe Ratio", 
                  f"{metrics['sharpe_ratio'].iloc[-1]:.2f}")
    
    with col4:
        st.metric("Total Backtests", len(metrics))
    
    # Charts
    st.subheader("📈 Performance Over Time")
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=metrics['timestamp'],
        y=metrics['total_profit'],
        mode='lines+markers',
        name='Total Profit %'
    ))
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("No metrics data available yet. Run a backtest first!")
```

**اجرا:**
```powershell
pip install streamlit plotly
streamlit run monitoring/dashboard.py
```

---

## 📝 مرحله 4: به‌روزرسانی README

اضافه کردن بخش "مشارکت در توسعه":

```markdown
## 🤝 مشارکت در توسعه

### برای شروع:
1. خواندن [ROADMAP.md](ROADMAP.md)
2. خواندن [DEVELOPMENT_GUIDE.md](DEVELOPMENT_GUIDE.md)
3. انتخاب یک task
4. ایجاد branch
5. پیاده‌سازی + تست
6. Pull Request

### Standards:
- ✅ Test coverage > 80%
- ✅ Pylint score > 8/10
- ✅ همه functions دارای docstring
- ✅ Code formatted با Black
```

---

## 🎯 چک‌لیست نهایی

### قبل از Commit:
- [ ] همه تست‌ها pass شوند
- [ ] Coverage > 80%
- [ ] Code formatting (black)
- [ ] Import sorting (isort)
- [ ] Linting (flake8, pylint)
- [ ] مستندات آپدیت شده

### Commit Message Format:
```
<type>: <subject>

<body>

<footer>
```

**Types:**
- `feat`: ویژگی جدید
- `fix`: رفع باگ
- `docs`: تغییر مستندات
- `test`: اضافه/تغییر تست
- `refactor`: بازنویسی کد
- `perf`: بهبود performance
- `chore`: کارهای maintenance

**مثال:**
```bash
git commit -m "test: اضافه کردن تست‌های regime detection

- تست تشخیص trending up/down
- تست تشخیص high volatility
- تست تشخیص range market
- coverage افزایش یافت به 65%
"
```

---

## 📚 منابع مفید

### مستندات
- [Freqtrade Testing](https://www.freqtrade.io/en/stable/strategy-customization/#strategy-tests)
- [pytest Documentation](https://docs.pytest.org/)
- [GitHub Actions](https://docs.github.com/en/actions)

### ابزارها
- **Testing**: pytest, pytest-cov, pytest-mock
- **Linting**: black, isort, flake8, pylint
- **Monitoring**: streamlit, plotly, prometheus
- **Notifications**: python-telegram-bot, requests

---

## 💬 پشتیبانی

- **Issues**: https://github.com/aminak58/freqai-futures-strategy/issues
- **Discussions**: https://github.com/aminak58/freqai-futures-strategy/discussions
- **Email**: [your-email]

---

**موفق باشید! 🚀**

# 🎯 تطبیق رژیم دیتکشن: MVP ↔ LSTM

## تاریخ: 10 اکتبر 2025
## هدف: رفع دوگانگی و هماهنگ‌سازی کامل

---

## ✅ وضعیت فعلی: رژیم دیتکشن موجود است!

### 📍 مکان در کد:
**فایل:** `user_data/strategies/FreqAIHybridStrategy.py`  
**خطوط:** 206-237

### 🔍 پیاده‌سازی فعلی:

```python
# ========== MARKET REGIME DETECTION ==========

# 1. Trend Detection (EMA-based)
ema_short = ta.EMA(dataframe, timeperiod=20)
ema_long = ta.EMA(dataframe, timeperiod=50)
dataframe["%-trend_strength"] = (ema_short - ema_long) / ema_long

# 2. Volatility Regime
atr_20 = ta.ATR(dataframe, timeperiod=20)
dataframe["%-volatility_regime"] = atr_20 / dataframe["close"]

# 3. Volume Regime
volume_ma = dataframe["volume"].rolling(window=20).mean()
dataframe["%-volume_regime"] = dataframe["volume"] / volume_ma

# 4. Classification
dataframe["%-market_regime"] = 0  # Default: Range

trend_up = dataframe["%-trend_strength"] > self.trend_threshold.value
trend_down = dataframe["%-trend_strength"] < -self.trend_threshold.value
high_vol = dataframe["%-volatility_regime"] > self.volatility_threshold.value * 0.02

dataframe.loc[trend_up & ~high_vol, "%-market_regime"] = 1  # Trending Up
dataframe.loc[trend_down & ~high_vol, "%-market_regime"] = 2  # Trending Down
dataframe.loc[high_vol, "%-market_regime"] = 3  # High Volatility

# 5. Multi-Horizon Regimes
dataframe["%-regime_short"] = dataframe["%-market_regime"].rolling(window=10).mean()
dataframe["%-regime_medium"] = dataframe["%-market_regime"].rolling(window=50).mean()
dataframe["%-regime_long"] = dataframe["%-market_regime"].rolling(window=200).mean()
```

### 📊 خروجی‌های موجود:

| Feature | معنی | مقدار | استفاده |
|---------|------|-------|----------|
| `%-market_regime` | رژیم فعلی | 0-3 | Classification |
| `%-regime_short` | میانگین کوتاه‌مدت | Continuous | 10 کندل |
| `%-regime_medium` | میانگین میان‌مدت | Continuous | 50 کندل |
| `%-regime_long` | میانگین بلندمدت | Continuous | 200 کندل |
| `%-trend_strength` | قدرت ترند | Continuous | EMA ratio |
| `%-volatility_regime` | سطح نوسان | Continuous | ATR/price |
| `%-volume_regime` | رژیم حجم | Continuous | Volume ratio |

---

## 🔄 تطبیق با طراحی LSTM

### ❌ چیزی که نباید اتفاق بیفتد:
```python
# اشتباه: نادیده گرفتن رژیم موجود و ساخت یک سیستم جدید
class NewRegimeDetection:  # ❌ دوگانگی
    def detect(self):
        # محاسبات جدید برای regime
        ...
```

### ✅ چیزی که باید اتفاق بیفتد:
```python
# درست: استفاده از رژیم موجود به عنوان input
class RegimeAwareLSTM:  # ✅ یکپارچه
    def __init__(self):
        # از رژیم موجود استفاده می‌کنیم
        self.regime_features = [
            '%-market_regime',      # از MVP
            '%-regime_short',       # از MVP
            '%-regime_medium',      # از MVP
            '%-regime_long',        # از MVP
            '%-trend_strength',     # از MVP
            '%-volatility_regime',  # از MVP
            '%-volume_regime'       # از MVP
        ]
```

---

## 🏗️ معماری یکپارچه

```
┌─────────────────────────────────────────────────────────────┐
│                   FreqAIHybridStrategy                       │
│                   (MVP - موجود و کار می‌کند)                │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  populate_indicators()                                       │
│  ├─ Technical Indicators (RSI, MACD, ...)                  │
│  ├─ Volume Indicators                                       │
│  └─ ⭐ Market Regime Detection ⭐                            │
│       ├─ trend_strength                                     │
│       ├─ volatility_regime                                  │
│       ├─ volume_regime                                      │
│       └─ market_regime (0-3)                                │
│                                                              │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   │ Features (including regime)
                   ▼
┌─────────────────────────────────────────────────────────────┐
│              RegimeAwareLSTM (جدید - در حال ساخت)           │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  __init__():                                                 │
│    ✅ از regime موجود استفاده می‌کند (input feature)        │
│    ✅ Regime Embedding (categorical → dense)                │
│    ✅ Multi-timeframe LSTMs                                 │
│    ✅ Regime-Aware Attention                                │
│                                                              │
│  forward():                                                  │
│    1. LSTM processing (5m, 15m, 1h)                        │
│    2. Regime embedding                                      │
│    3. Concatenation                                         │
│    4. Regime-aware attention                                │
│    5. Multi-target predictions                              │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 🎯 جریان داده (Data Flow)

### مرحله 1: محاسبه Features (MVP Strategy)
```python
# در FreqAIHybridStrategy.populate_indicators()
dataframe = strategy.populate_indicators(dataframe)

# خروجی شامل:
# - Technical indicators
# - Volume indicators  
# - ⭐ Regime features (7 features)
```

### مرحله 2: آماده‌سازی برای LSTM
```python
# در FreqAIModel (جدید)
def prepare_features_for_lstm(dataframe):
    features = {
        # Raw OHLCV
        '5m_ohlcv': extract_ohlcv(dataframe, '5m'),
        '15m_ohlcv': extract_ohlcv(dataframe, '15m'),
        '1h_ohlcv': extract_ohlcv(dataframe, '1h'),
        
        # Technical indicators
        'technical': extract_technical(dataframe),
        
        # ⭐ Regime features (از MVP می‌آید)
        'regime': {
            'categorical': dataframe['%-market_regime'].values,     # 0-3
            'continuous': np.stack([
                dataframe['%-trend_strength'].values,
                dataframe['%-volatility_regime'].values,
                dataframe['%-volume_regime'].values,
                dataframe['%-regime_short'].values,
                dataframe['%-regime_medium'].values,
                dataframe['%-regime_long'].values
            ], axis=1)
        }
    }
    return features
```

### مرحله 3: پیش‌بینی با LSTM
```python
# LSTM می‌داند که در چه regime است
predictions = lstm_model(
    x_5m=features['5m_ohlcv'],
    x_15m=features['15m_ohlcv'],
    x_1h=features['1h_ohlcv'],
    regime=features['regime']['categorical'],  # ← از MVP
    regime_continuous=features['regime']['continuous']  # ← از MVP
)
```

---

## 🔬 مثال عملی: یک Trade واقعی

### 🕐 زمان: 2025-10-10 14:35:00
### 💹 جفت‌ارز: BTC/USDT:USDT

```python
# ====== STEP 1: محاسبه رژیم (MVP Strategy) ======
dataframe = strategy.populate_indicators(dataframe)

# محاسبات MVP:
ema_20 = 62500
ema_50 = 61800
trend_strength = (62500 - 61800) / 61800 = 0.0113  # > 0.005 → Trending Up

atr = 450
volatility_regime = 450 / 62500 = 0.0072  # < 0.02 → Low Vol

regime = 1  # Trending Up ✓

# ====== STEP 2: LSTM processing ======
lstm_input = {
    '5m': {
        'open': 62450,
        'high': 62580,
        'low': 62420,
        'close': 62500,
        'volume': 245.5,
        'rsi': 58.3,
        'macd': 12.5,
        # ... سایر indicators
    },
    '15m': {
        'ema_20': 62480,
        'supertrend': 'LONG',
        'pattern': 'bullish_flag',
        # ...
    },
    '1h': {
        'adx': 28.5,
        'trend_intensity': 0.75,
        # ...
    },
    'regime': 1,  # ← از MVP
    'regime_features': {
        'trend_strength': 0.0113,
        'volatility': 0.0072,
        'volume_regime': 1.2
    }
}

predictions = lstm_model(lstm_input)

# ====== STEP 3: LSTM خروجی ======
{
    'entry_quality': 0.87,    # سیگنال 5m قوی
    'confirm_prob': 0.92,     # 15m تأیید می‌کند
    'trend_score': 0.78,      # 1h هم صعودی
    'volatility': 0.0068      # نوسان پایش‌بینی شده
}

# ====== STEP 4: تصمیم‌گیری ======
# چون:
# - regime = 1 (Trending Up) ← از MVP
# - entry_quality = 0.87 > 0.7 ← از LSTM
# - confirm_prob = 0.92 > 0.8 ← از LSTM (اجباری)
# - trend_score = 0.78 > 0.7 ← از LSTM
# - volatility = 0.0068 < 0.01 ← از LSTM

# پس:
signal = 'LONG'
leverage = calculate_leverage(
    regime=1,           # ← MVP: Trending Up
    entry=0.87,         # ← LSTM
    confirm=0.92,       # ← LSTM
    trend=0.78,         # ← LSTM
    vol=0.0068          # ← LSTM
)
# leverage = 4x (کمی محافظه‌کارانه، چون vol پایین است)

entry_price = 62500
position_size = account_balance * 0.05 * 4  # 5% risk با 4x leverage
```

---

## 📊 مزایای این رویکرد یکپارچه

### 1. **بدون دوگانگی** ✅
- یک source of truth برای regime
- همه از همان رژیم استفاده می‌کنند
- کد تمیز و قابل maintain

### 2. **تست‌پذیری** ✅
```python
# می‌توانیم regime را از MVP بگیریم و backtest کنیم
def test_with_mvp_regime():
    regime = mvp_strategy.detect_regime(dataframe)
    predictions = lstm_model.predict(dataframe, regime=regime)
    results = backtest(predictions)
    assert results['win_rate'] > 0.9

# یا می‌توانیم regime را manually set کنیم
def test_in_specific_regime():
    regime = 1  # Force Trending Up
    predictions = lstm_model.predict(dataframe, regime=regime)
    # ...
```

### 3. **قابلیت مقایسه** ✅
```python
# می‌توانیم ببینیم LSTM بدون regime چقدر خوب است
results_with_regime = backtest(use_regime=True)
results_without_regime = backtest(use_regime=False)

print(f"با regime: {results_with_regime['sharpe']}")
print(f"بدون regime: {results_without_regime['sharpe']}")
# → نشان می‌دهد که regime چقدر کمک می‌کند
```

### 4. **تفسیرپذیری** ✅
```python
# می‌دانیم چرا LSTM یک سیگنال داد
def explain_prediction(prediction, regime):
    if regime == 1 and prediction['entry_quality'] > 0.8:
        return "سیگنال قوی: ما در Trending Up هستیم و LSTM pattern صعودی قوی دیده"
    elif regime == 3 and prediction['entry_quality'] > 0.8:
        return "⚠️ هشدار: اگرچه LSTM سیگنال قوی دیده، ولی رژیم High Volatility است"
```

### 5. **Incremental Development** ✅
```python
# فاز 1: فقط از regime استفاده کنیم (بدون تغییر LSTM)
if regime in [1, 2]:  # Trending
    allow_trade = True
else:  # Range or High Vol
    allow_trade = False

# فاز 2: regime را به LSTM بدهیم (به عنوان feature)
lstm_features = [..., regime, ...]

# فاز 3: Regime-aware attention (پیشرفته)
attention_weights = calculate_attention(hidden, regime)
```

---

## 🚀 مراحل پیاده‌سازی بدون دوگانگی

### Week 1: Integration Testing
```bash
# 1. تست کنیم که regime از MVP درست محاسبه می‌شود
pytest tests/test_regime_detection.py

# 2. ببینیم regime در چه درصدی از زمان چیست
python analyze_regime_distribution.py
# خروجی:
# Regime 0 (Range): 35%
# Regime 1 (Trending Up): 25%
# Regime 2 (Trending Down): 22%
# Regime 3 (High Vol): 18%
```

### Week 2: Feature Pipeline
```python
# اضافه کردن regime به FreqAI features
def feature_engineering(self, dataframe, **kwargs):
    # ابتدا MVP indicators (شامل regime)
    dataframe = self.populate_indicators(dataframe)
    
    # سپس LSTM-specific features
    dataframe = self.add_lstm_features(dataframe)
    
    # اطمینان از وجود regime
    assert '%-market_regime' in dataframe.columns
    assert '%-regime_short' in dataframe.columns
    
    return dataframe
```

### Week 3: LSTM Training با Regime
```python
# Training با regime به عنوان input
X_train = prepare_features(df_train, include_regime=True)
y_train = prepare_targets(df_train)

model.fit(
    X_train, y_train,
    regime=df_train['%-market_regime'].values  # ← از MVP
)

# Validation per regime
for regime in [0, 1, 2, 3]:
    mask = df_val['%-market_regime'] == regime
    X_val_regime = X_val[mask]
    y_val_regime = y_val[mask]
    
    score = model.evaluate(X_val_regime, y_val_regime)
    print(f"Regime {regime}: {score}")
```

### Week 4: Backtest با Regime Analysis
```python
# Backtest کامل
results = backtest_with_regime_analysis(
    strategy=lstm_strategy,
    regime_source='mvp',  # از MVP می‌گیریم
    start_date='2024-01-01',
    end_date='2025-01-01'
)

# نتایج per regime
print(results.by_regime)
#   Regime | Trades | Win Rate | Sharpe | Max DD
#   0      | 145    | 85%      | 2.1    | -8%
#   1      | 230    | 92%      | 3.5    | -5%
#   2      | 220    | 90%      | 3.2    | -6%
#   3      | 85     | 75%      | 1.5    | -12%
```

---

## 📝 چک‌لیست تطبیق

- [x] رژیم دیتکشن در MVP موجود است (خط 206-237)
- [x] 7 regime feature در MVP وجود دارد
- [x] تستهای regime در test_strategy_logic.py موجود است
- [ ] اضافه کردن regime به LSTM input pipeline
- [ ] پیاده‌سازی Regime Embedding layer
- [ ] پیاده‌سازی Regime-Aware Attention
- [ ] Training با regime stratification
- [ ] Backtest با per-regime analysis
- [ ] Documentation به‌روزرسانی شود

---

## ✅ تأییدیه عدم دوگانگی

```
✓ یک منبع اصلی: FreqAIHybridStrategy.populate_indicators()
✓ یک پایپ‌لاین داده: MVP → LSTM
✓ یک روش تست: تستهای موجود + تستهای جدید
✓ یک سیستم مانیتورینگ: CI/CD موجود
✓ یک مستندسازی: این سند + MVP_DOCUMENTATION.md

✗ دو سیستم regime: خیر
✗ کدهای تکراری: خیر
✗ تناقض در پیش‌بینی‌ها: خیر
```

---

## 🎯 نتیجه‌گیری

**رژیم دیتکشن قبلاً در MVP پیاده‌سازی شده و کار می‌کند.**

**LSTM از آن استفاده می‌کند، نه اینکه جایگزین آن شود.**

**این یک رویکرد مکمل است که بهترین هر دو دنیا را ترکیب می‌کند:**
- 🧮 Rule-based (MVP Regime) → سریع، قابل فهم، قابل هایپراوپت
- 🧠 AI-based (LSTM) → adaptive، pattern recognition، context-aware

**دوگانگی وجود ندارد. یکپارچگی کامل است.** ✅

---

**آماده برای شروع پیاده‌سازی LSTM با استفاده از رژیم موجود.**

**📅 تاریخ شروع:** امروز  
**🎯 هدف:** 90% Win Rate → 95% Win Rate با LSTM Enhancement

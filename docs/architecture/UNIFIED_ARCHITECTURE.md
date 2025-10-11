# 🎯 معماری یکپارچه: MVP + LSTM با رژیم دیتکشن

## 📍 وضعیت فعلی
- ✅ **MVP Strategy**: کامل و عملیاتی (`FreqAIHybridStrategy.py`)
- 🚧 **LSTM Network**: در حال توسعه (طراحی معماری کامل شده)
- ✅ **Regime Detection**: عملیاتی در MVP و آماده استفاده در LSTM
- 📋 **CI/CD Pipeline**: در حال طراحی

---

## نمای کلی سیستم

```
╔══════════════════════════════════════════════════════════════════╗
║                     سیستم معاملاتی یکپارچه                       ║
╚══════════════════════════════════════════════════════════════════╝
                               │
                ┌──────────────┴───────────────┐
                │                              │
    ┌───────────▼──────────┐      ┌───────────▼──────────┐
    │   MVP Strategy        │      │   LSTM Enhancement   │
    │   (موجود و کار کن)   │──────▶│   (در حال ساخت)     │
    └───────────┬──────────┘      └──────────────────────┘
                │
                │
┌───────────────▼────────────────────────────────────────────────┐
│                    📊 REGIME DETECTION                          │
│                    (هسته مشترک)                                │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌────────────────────┐  ┌────────────────────┐               │
│  │  Trend Analysis    │  │  Volatility Regime │               │
│  │  EMA(20) vs EMA(50)│  │  ATR / Price       │               │
│  │  ────────────────► │  │  ────────────────► │               │
│  │  trend_strength    │  │  volatility_regime │               │
│  └────────────────────┘  └────────────────────┘               │
│                                                                 │
│  ┌────────────────────┐  ┌─────────────────────────────────┐  │
│  │  Volume Regime     │  │  Market Regime (0-3)            │  │
│  │  Vol / MA(20)      │  │  ─────────────────────────────► │  │
│  │  ────────────────► │  │  0=Range, 1=Up, 2=Down, 3=HighV│  │
│  │  volume_regime     │  │                                  │  │
│  └────────────────────┘  └─────────────────────────────────┘  │
│                                                                 │
│  Output Features:                                               │
│  ✓ market_regime (categorical: 0-3)                           │
│  ✓ regime_short, regime_medium, regime_long (continuous)      │
│  ✓ trend_strength, volatility_regime, volume_regime           │
│                                                                 │
└────┬────────────────────────────────────────────────┬─────────┘
     │                                                 │
     │ ┌───────────────────────────────────────────┐  │
     │ │      این features به همه می‌رسند         │  │
     │ └───────────────────────────────────────────┘  │
     │                                                 │
     ▼                                                 ▼
┌─────────────────────────┐                ┌──────────────────────────┐
│   MVP Strategy Logic    │                │   LSTM Neural Network    │
├─────────────────────────┤                ├──────────────────────────┤
│                         │                │                          │
│  populate_entry_trend(): │                │  Input Layer:           │
│                         │                │  ├─ 5m OHLCV            │
│  if regime in [1, 2]:  │                │  ├─ 15m OHLCV           │
│    # Trending           │                │  ├─ 1h OHLCV            │
│    check ML prediction  │                │  └─ ⭐ Regime Features  │
│  elif regime == 3:     │                │                          │
│    # High Vol           │                │  Hidden Layers:          │
│    tighter stops        │                │  ├─ LSTM 5m (64)        │
│  else:                  │                │  ├─ LSTM 15m (64)       │
│    # Range              │                │  ├─ LSTM 1h (32)        │
│    skip or lower lev    │                │  ├─ Regime Embedding    │
│                         │                │  └─ ⭐ Regime Attention │
│  return signal          │                │                          │
│                         │                │  Output:                 │
│                         │                │  ├─ Entry Quality        │
│                         │                │  ├─ Confirm Prob         │
│                         │                │  ├─ Trend Score          │
│                         │                │  └─ Volatility Pred      │
└─────────┬───────────────┘                └──────────┬───────────────┘
          │                                           │
          │                                           │
          └────────────┬──────────────────────────────┘
                       │
                       ▼
            ┌────────────────────────┐
            │  Trading Decision      │
            ├────────────────────────┤
            │                        │
            │  Signal: LONG/SHORT    │
            │  Leverage: 2x-5x       │
            │  Position Size: ...    │
            │  Stop Loss: ...        │
            │                        │
            │  Regime Context: 1     │
            │  (Trending Up)         │
            └────────────────────────┘
```

---

## 🔄 جریان داده در یک Trade واقعی

### ⏰ Time: 14:35:00 | 📈 Pair: BTC/USDT:USDT | 💰 Price: 62,500

```
1️⃣  Raw Market Data
    ├─ 5m:  OHLCV + Volume + ...
    ├─ 15m: OHLCV + Volume + ...
    └─ 1h:  OHLCV + Volume + ...
            │
            ▼
2️⃣  FreqAIHybridStrategy.populate_indicators()
    ├─ Technical Indicators
    │  ├─ RSI(14) = 58.3
    │  ├─ MACD = 12.5
    │  ├─ ADX(14) = 28.5
    │  └─ ...
    │
    └─ ⭐ Regime Detection (خط 206-237)
       ├─ EMA(20) = 62,500
       ├─ EMA(50) = 61,800
       ├─ trend_strength = (62500-61800)/61800 = 0.0113
       ├─ ATR(20) = 450
       ├─ volatility_regime = 450/62500 = 0.0072
       │
       └─ Classification:
          trend_strength > 0.005 ✓
          volatility < 0.02 ✓
          → market_regime = 1 (Trending Up) ✅
            │
            ├─────────────────┬─────────────────┐
            │                 │                 │
            ▼                 ▼                 ▼
3️⃣  MVP Strategy      LSTM Model      Monitoring
    │                 │                 │
    ├─ regime=1       ├─ Input:        ├─ Log:
    │  → Trending     │  ├─ OHLCV      │  "Regime: 1"
    │                 │  ├─ Technical   │  "Trending Up"
    ├─ Check:         │  └─ regime=1   │  "Confidence: High"
    │  di_value>0.5   │                 │
    │  ✓              │  Processing:    └─ Store in CSV
    │                 │  ├─ LSTM(5m)
    ├─ Prediction:    │  ├─ LSTM(15m)
    │  &-prediction   │  ├─ LSTM(1h)
    │  = 0.0125       │  ├─ Regime Emb
    │  (1.25% gain)   │  └─ Attention
    │                 │     (focus on
    │                 │      trend signals)
    │                 │
    │                 │  Output:
    │                 │  ├─ entry_quality = 0.87
    │                 │  ├─ confirm_prob = 0.92
    │                 │  ├─ trend_score = 0.78
    │                 │  └─ volatility = 0.0068
    │                 │
    └─────────────────┴─────────────────┘
                      │
                      ▼
4️⃣  Decision Engine
    ├─ Regime Check: 1 (Trending Up) ✓
    ├─ MVP Prediction: 0.0125 (positive) ✓
    ├─ LSTM Entry: 0.87 > 0.7 ✓
    ├─ LSTM Confirm: 0.92 > 0.8 ✓ (mandatory)
    ├─ LSTM Trend: 0.78 > 0.7 ✓
    └─ LSTM Volatility: 0.0068 < 0.01 ✓
                      │
                      ▼
5️⃣  Leverage Calculator
    if regime == 1 AND all_checks_pass:
        base_leverage = 3x
        if trend_score > 0.75: +1x
        if volatility < 0.01: +0x (safe)
        → leverage = 4x ✅
                      │
                      ▼
6️⃣  Execute Trade
    ┌────────────────────────────┐
    │ LONG BTC/USDT:USDT         │
    │ Entry: 62,500              │
    │ Leverage: 4x               │
    │ Size: 0.08 BTC             │
    │ Stop: 62,200 (-0.48%)     │
    │ Target: 63,500 (+1.6%)    │
    │                            │
    │ Context:                   │
    │ ├─ Regime: Trending Up     │
    │ ├─ Confidence: High (0.87) │
    │ └─ Risk: Low (0.0068)     │
    └────────────────────────────┘
```

---

## 📊 مقایسه: قبل و بعد از LSTM

### 🔵 **سیستم فعلی (MVP فقط)**

```python
# FreqAIHybridStrategy.py
def populate_entry_trend(dataframe, metadata):
    conditions = []
    
    # 1. رژیم چک (manual)
    regime = dataframe['%-market_regime']
    if regime in [1, 2]:  # فقط trending
        
        # 2. ML prediction چک
        if dataframe['&-prediction'] > 0.005:
            
            # 3. DI threshold چک
            if dataframe['do_predict'] == 1:
                conditions.append(dataframe['di_values'] < 1.0)
    
    # نتیجه: Simple but limited
    # ✓ کار می‌کند
    # ✓ قابل فهم
    # ✗ Context-unaware
    # ✗ One-size-fits-all thresholds
```

### 🟢 **سیستم جدید (MVP + LSTM)**

```python
# RegimeAwareLSTM
def populate_entry_trend(dataframe, metadata):
    # 1. رژیم از MVP (همان کد قبلی)
    regime = dataframe['%-market_regime']
    
    # 2. LSTM predictions (جدید)
    lstm_out = lstm_model.predict(
        dataframe, 
        regime=regime  # ← context
    )
    
    conditions = []
    
    # 3. Regime-aware logic (جدید)
    if regime == 1:  # Trending Up
        # LSTM یاد گرفته کدام 5m patterns در این regime کار می‌کنند
        if lstm_out['entry_quality'] > 0.75:
            if lstm_out['confirm_prob'] > 0.85:
                leverage = 4x
                
    elif regime == 0:  # Range
        # LSTM یاد گرفته mean reversion patterns
        if lstm_out['entry_quality'] > 0.85:  # سختگیرانه‌تر
            if lstm_out['volatility'] < 0.005:  # خیلی کم ریسک
                leverage = 2x
    
    elif regime == 3:  # High Vol
        # LSTM یاد گرفته فقط strongest setups
        if lstm_out['entry_quality'] > 0.90:  # بسیار سختگیرانه
            if lstm_out['confirm_prob'] > 0.95:
                leverage = 2x  # محافظه‌کارانه
    
    # نتیجه: Smart and adaptive
    # ✓ کار می‌کند
    # ✓ Context-aware
    # ✓ Regime-specific thresholds
    # ✓ Pattern recognition
    # ✓ Higher win rate
```

---

## 🎯 چرا این معماری کار می‌کند؟

### 1. **تقسیم کار واضح**

```
MVP Regime Detection:
├─ مسئولیت: "الان بازار چه حالی دارد؟"
├─ روش: Rule-based (EMA, ATR, Volume)
├─ سرعت: بسیار سریع
├─ قابلیت توضیح: 100%
└─ قابل Hyperopt: ✓

LSTM Pattern Recognition:
├─ مسئولیت: "در این حالت بازار، کدام pattern کار می‌کند؟"
├─ روش: Deep Learning
├─ سرعت: سریع (پس از training)
├─ قابلیت توضیح: Attention weights
└─ قابل Hyperopt: ✗ (اما auto-learning)
```

### 2. **مکمل، نه رقیب**

```
سؤال: باید Long بزنیم؟

MVP می‌گوید:
"بازار Trending Up است (regime=1)"
"EMA crossover داریم"
"Volume بالاست"
→ اگر در گذشته، این شرایط = خوب بوده

LSTM می‌گوید:
"من 1000 نمونه از regime=1 دیده‌ام"
"در 87% اوقات، وقتی این pattern (RSI=58, MACD=12, ...) در regime=1 بود"
"قیمت 1.2% رفت بالا"
→ پس: entry_quality = 0.87

Combined:
regime=1 (context) + entry_quality=0.87 (pattern) = Strong LONG ✅
```

### 3. **Fail-Safe**

```python
# اگر LSTM دیوانه شود:
if lstm_out['entry_quality'] > 0.95 and regime == 3:
    # ⚠️ هشدار: LSTM سیگنال بسیار قوی می‌دهد
    # اما رژیم High Volatility است
    # → نادیده بگیر یا leverage کم کن
    leverage = 2x  # Override
    
# اگر Regime اشتباه باشد:
# LSTM از 100+ features دیگر هم استفاده می‌کند
# و می‌تواند خودش market condition را تشخیص دهد
```

---

## 📈 مسیر پیاده‌سازی

```
┌─────────────────────────────────────────────────────────┐
│ Week 1: تست و آماده‌سازی                                │
├─────────────────────────────────────────────────────────┤
│ ✓ بررسی regime distribution در historical data        │
│ ✓ تست MVP regime detection accuracy                   │
│ ✓ آماده‌سازی feature pipeline                         │
└─────────────────────────────────────────────────────────┘
                          ▼
┌─────────────────────────────────────────────────────────┐
│ Week 2: پیاده‌سازی LSTM Basic                          │
├─────────────────────────────────────────────────────────┤
│ ✓ ساخت RegimeEmbedding layer                          │
│ ✓ پیاده‌سازی Multi-timeframe LSTMs                    │
│ ✓ Training اولیه بدون attention                       │
└─────────────────────────────────────────────────────────┘
                          ▼
┌─────────────────────────────────────────────────────────┐
│ Week 3: Regime-Aware Attention                          │
├─────────────────────────────────────────────────────────┤
│ ✓ پیاده‌سازی RegimeAttention module                   │
│ ✓ Training با attention                               │
│ ✓ Visualization attention weights                      │
└─────────────────────────────────────────────────────────┘
                          ▼
┌─────────────────────────────────────────────────────────┐
│ Week 4: Integration و Backtest                         │
├─────────────────────────────────────────────────────────┤
│ ✓ یکپارچه‌سازی با FreqAIHybridStrategy                │
│ ✓ Backtest per-regime                                  │
│ ✓ مقایسه با MVP baseline                              │
│ ✓ Hyperopt regime-specific thresholds                  │
└─────────────────────────────────────────────────────────┘
                          ▼
┌─────────────────────────────────────────────────────────┐
│ Week 5+: Fine-tuning و Production                      │
├─────────────────────────────────────────────────────────┤
│ ✓ Training روی داده‌های بیشتر                         │
│ ✓ A/B testing در dry-run                              │
│ ✓ مانیتورینگ و logging                                │
│ ✓ Deployment به production                            │
└─────────────────────────────────────────────────────────┘
```

---

## 🔑 نکات کلیدی

### ✅ باید انجام شود:
1. از regime موجود استفاده شود (نه ساخت جدید)
2. LSTM به صورت مکمل باشد (نه جایگزین)
3. تست per-regime انجام شود
4. Attention weights بررسی شود (interpretability)
5. Fail-safe mechanisms وجود داشته باشد

### ❌ نباید انجام شود:
1. نادیده گرفتن regime detection موجود
2. ساخت یک سیستم جدید و مستقل
3. فقط به LSTM اعتماد کردن (بدون MVP)
4. نادیده گرفتن سیستم 90% win rate فعلی
5. Over-engineering (شروع با ساده‌ترین نسخه)

---

## 📚 مستندات مرتبط

1. **[REGIME_DETECTION_ALIGNMENT.md](REGIME_DETECTION_ALIGNMENT.md)**  
   تطبیق کامل و دقیق MVP ↔ LSTM

2. **[LSTM_ARCHITECTURE_DESIGN.md](LSTM_ARCHITECTURE_DESIGN.md)**  
   معماری فنی کامل LSTM

3. **[MVP_DOCUMENTATION.md](MVP_DOCUMENTATION.md)**  
   مستندات استراتژی فعلی

4. **[CI_CD_GUIDE.md](CI_CD_GUIDE.md)**  
   راهنمای کامل CI/CD

5. **[README.md](README.md)**  
   نمای کلی پروژه

---

## 🎯 هدف نهایی

```
سیستم فعلی: 90% Win Rate (با تنظیم دستی)
                    ▼
         اضافه کردن LSTM Enhancement
                    ▼
هدف: 95% Win Rate (با یادگیری خودکار الگوها)
      + کاهش زمان تحلیل دستی
      + افزایش تعداد فرصت‌های شناسایی شده
      + Adaptive به شرایط مختلف بازار
```

---

**✅ دوگانگی وجود ندارد. سیستم یکپارچه است.**

**🚀 آماده برای پیاده‌سازی.**

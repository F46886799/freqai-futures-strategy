# 🧠 LSTM Architecture Design - با رژیم دیتکشن

## تاریخ: 10 اکتبر 2025
## نسخه: 1.0 - طراحی اولیه

---

## 🎯 فلسفه طراحی: Regime-Aware LSTM

### مفهوم اصلی
ترکیب **رژیم دیتکشن موجود** (EMA-based) با **LSTM** برای یادگیری الگوهای خاص هر رژیم.

```
┌──────────────────────────────────────────────────────────┐
│                    Input Pipeline                         │
├──────────────────────────────────────────────────────────┤
│                                                           │
│  Raw Market Data                 Regime Features         │
│  ├─ 5m OHLCV                     ├─ market_regime (0-3) │
│  ├─ 15m OHLCV                    ├─ regime_short        │
│  └─ 1h OHLCV                     ├─ regime_medium       │
│                                   └─ regime_long         │
│  Technical Features                                       │
│  ├─ RSI, MACD, ADX               Regime-Aware Features   │
│  ├─ Bollinger, ATR               ├─ trend_strength      │
│  └─ Volume, OBV                  ├─ volatility_regime   │
│                                   └─ volume_regime       │
└──────────────────────────────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────┐
│              Multi-Timeframe LSTM Network                 │
├──────────────────────────────────────────────────────────┤
│                                                           │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │  5m LSTM    │  │  15m LSTM   │  │  1h LSTM    │     │
│  │  (64 units) │  │  (64 units) │  │  (32 units) │     │
│  │  Bidirect.  │  │  Bidirect.  │  │  Bidirect.  │     │
│  └─────┬───────┘  └─────┬───────┘  └─────┬───────┘     │
│        │                │                │               │
│        └────────────────┴────────────────┘               │
│                         │                                │
│                    Concatenate                           │
│                         │                                │
│                    ┌────▼────┐                          │
│                    │ Regime  │                          │
│                    │ Context │                          │
│                    │  Layer  │                          │
│                    └────┬────┘                          │
│                         │                                │
│                  ┌──────▼──────┐                        │
│                  │   Attention  │ ← رژیم‌محور           │
│                  │   Mechanism  │                        │
│                  └──────┬──────┘                        │
│                         │                                │
│                  ┌──────▼──────┐                        │
│                  │   Dense      │                        │
│                  │   (128)      │                        │
│                  └──────┬──────┘                        │
│                         │                                │
│              ┌──────────┴──────────┐                    │
│              │                     │                     │
└──────────────┼─────────────────────┼────────────────────┘
               │                     │
               ▼                     ▼
    ┌──────────────────┐   ┌──────────────────┐
    │  Entry Quality   │   │ Confirmation     │
    │  (5m Scalp)      │   │ Probability      │
    │  [0-1]           │   │ (15m Filter)     │
    └──────────────────┘   └──────────────────┘
               │                     │
               ▼                     ▼
    ┌──────────────────┐   ┌──────────────────┐
    │  Trend Score     │   │ Volatility       │
    │  (1h Optional)   │   │ Prediction       │
    │  [0-1]           │   │ [0-∞]            │
    └──────────────────┘   └──────────────────┘
```

---

## 📊 رژیم دیتکشن: MVP vs LSTM

### 🏛️ **MVP Strategy** (موجود در `FreqAIHybridStrategy.py`)

```python
# خط 206-237
# Regime Detection (EMA-based)
ema_short = ta.EMA(dataframe, timeperiod=20)
ema_long = ta.EMA(dataframe, timeperiod=50)
trend_strength = (ema_short - ema_long) / ema_long

# Volatility
atr_20 = ta.ATR(dataframe, timeperiod=20)
volatility_regime = atr_20 / dataframe["close"]

# Classification
# 0 = Range, 1 = Trending Up, 2 = Trending Down, 3 = High Volatility
if trend_strength > threshold: regime = 1
elif trend_strength < -threshold: regime = 2
elif volatility_regime > vol_threshold: regime = 3
else: regime = 0

# Three horizons
regime_short (10 candles)
regime_medium (50 candles)
regime_long (200 candles)
```

**✅ مزایا:**
- ساده و قابل فهم
- سریع محاسبه می‌شود
- قابل hyperopt
- به عنوان feature برای ML

**❌ محدودیت‌ها:**
- فقط 4 رژیم (ساده‌سازی بیش از حد)
- فقط EMA-based (یک دیدگاه)
- خطاهای false signal در بازارهای پرنوسان

### 🧠 **LSTM Enhancement** (طراحی جدید)

```python
# رژیم به عنوان Input + Learning
class RegimeAwareLSTM:
    def __init__(self):
        # 1. رژیم موجود را به عنوان feature استفاده می‌کنیم
        self.regime_features = [
            'market_regime',      # 0-3 (categorical → one-hot)
            'regime_short',       # Rolling mean 10
            'regime_medium',      # Rolling mean 50
            'regime_long',        # Rolling mean 200
            'trend_strength',     # Continuous
            'volatility_regime',  # Continuous
            'volume_regime'       # Continuous
        ]
        
        # 2. LSTM خودش الگوهای regime-specific را یاد می‌گیرد
        # مثلاً:
        # - در regime=1 (Trending Up): EMA crossovers معتبر
        # - در regime=3 (High Vol): فقط strong confirmations
        # - در regime=0 (Range): mean reversion signals
        
        # 3. Attention mechanism روی regime focus می‌کند
        self.attention = RegimeAttention()
```

**✅ مزایا:**
- از رژیم موجود استفاده می‌کند (نصف کار آماده است!)
- LSTM الگوهای پیچیده‌تر هر رژیم را یاد می‌گیرد
- Attention می‌تواند regime transitions را catch کند
- مکمل است، نه جایگزین!

---

## 🏗️ معماری کامل LSTM

### 1️⃣ **Input Layer: Feature Engineering**

```python
def prepare_regime_aware_features(dataframe: DataFrame) -> Dict[str, np.ndarray]:
    """
    ترکیب رژیم موجود + features جدید
    """
    
    # ========== GROUP A: Raw Market Data ==========
    # این features به LSTM می‌رسند
    raw_features_5m = [
        'open', 'high', 'low', 'close', 'volume'
    ]
    
    raw_features_15m = [
        'open_15m', 'high_15m', 'low_15m', 'close_15m', 'volume_15m'
    ]
    
    raw_features_1h = [
        'open_1h', 'high_1h', 'low_1h', 'close_1h', 'volume_1h'
    ]
    
    # ========== GROUP B: Regime Features (از MVP) ==========
    # این features از strategy موجود می‌آیند
    regime_features = {
        # Categorical (one-hot encoded)
        'market_regime': [0, 1, 2, 3],  # 4 regimes
        
        # Continuous regime indicators
        'regime_short': dataframe['%-regime_short'],
        'regime_medium': dataframe['%-regime_medium'],
        'regime_long': dataframe['%-regime_long'],
        
        # Regime components
        'trend_strength': dataframe['%-trend_strength'],
        'volatility_regime': dataframe['%-volatility_regime'],
        'volume_regime': dataframe['%-volume_regime']
    }
    
    # ========== GROUP C: Technical Indicators ==========
    # برای هر timeframe
    technical_5m = {
        # Trend
        'rsi_14': ta.RSI(dataframe, 14),
        'macd': ta.MACD(dataframe),
        'adx_14': ta.ADX(dataframe, 14),
        
        # Volatility
        'bb_upper', 'bb_middle', 'bb_lower': ta.BBANDS(dataframe),
        'atr_14': ta.ATR(dataframe, 14),
        
        # Volume
        'obv': ta.OBV(dataframe),
        'mfi_14': ta.MFI(dataframe, 14),
        
        # Scalping-specific (5m only)
        'rsi_divergence': detect_rsi_divergence(dataframe),
        'volume_spike': dataframe['volume'] / dataframe['volume'].rolling(20).mean(),
        'price_momentum': dataframe['close'].pct_change(5)
    }
    
    technical_15m = {
        # Trend confirmation
        'ema_20', 'ema_50', 'ema_200',
        'supertrend': calculate_supertrend(dataframe),
        'trend_quality': calculate_trend_quality(dataframe),
        
        # Pattern recognition
        'support_resistance': identify_sr_levels(dataframe),
        'chart_patterns': detect_patterns(dataframe)
    }
    
    technical_1h = {
        # Macro trend
        'adx_strength': ta.ADX(dataframe, 14),
        'trend_intensity': calculate_trend_intensity(dataframe),
        
        # Momentum scoring
        'momentum_score': calculate_momentum_score(dataframe),
        'trend_score': calculate_trend_score(dataframe)
    }
    
    # ========== GROUP D: Crypto-Specific Features ==========
    crypto_features = {
        'funding_rate': get_funding_rate(),  # از Binance API
        'liquidation_volume': get_liquidation_data(),
        'open_interest': get_open_interest(),
        'long_short_ratio': get_long_short_ratio()
    }
    
    return {
        '5m': np.concatenate([raw_features_5m, technical_5m]),
        '15m': np.concatenate([raw_features_15m, technical_15m]),
        '1h': np.concatenate([raw_features_1h, technical_1h]),
        'regime': regime_features,  # ← از MVP می‌آید
        'crypto': crypto_features
    }
```

### 2️⃣ **LSTM Network Architecture**

```python
class RegimeAwareLSTM(nn.Module):
    """
    Multi-timeframe LSTM با Regime Context
    """
    
    def __init__(self, config):
        super().__init__()
        
        # ========== Regime Embedding ==========
        # تبدیل regime categorical به dense vector
        self.regime_embedding = nn.Embedding(
            num_embeddings=4,  # 4 regimes
            embedding_dim=8
        )
        
        # ========== Multi-Timeframe LSTMs ==========
        # هر timeframe یک LSTM مخصوص دارد
        
        # 5m: سریع‌ترین، برای scalping
        self.lstm_5m = nn.LSTM(
            input_size=50,  # تعداد features 5m
            hidden_size=64,
            num_layers=2,
            bidirectional=True,  # Past + Future context
            dropout=0.2,
            batch_first=True
        )
        
        # 15m: فیلتر تأیید
        self.lstm_15m = nn.LSTM(
            input_size=40,  # تعداد features 15m
            hidden_size=64,
            num_layers=2,
            bidirectional=True,
            dropout=0.2,
            batch_first=True
        )
        
        # 1h: اسکورینگ ماکرو
        self.lstm_1h = nn.LSTM(
            input_size=30,  # تعداد features 1h
            hidden_size=32,
            num_layers=2,
            bidirectional=True,
            dropout=0.2,
            batch_first=True
        )
        
        # ========== Regime Context Layer ==========
        # این layer رژیم را با LSTM outputs ترکیب می‌کند
        lstm_concat_size = (64*2) + (64*2) + (32*2)  # Bidirectional doubles size
        regime_size = 8 + 3  # Embedding + continuous features
        
        self.regime_context = nn.Sequential(
            nn.Linear(lstm_concat_size + regime_size, 256),
            nn.LayerNorm(256),
            nn.ReLU(),
            nn.Dropout(0.3)
        )
        
        # ========== Regime-Aware Attention ==========
        # Attention که روی regime focus می‌کند
        self.attention = RegimeAttention(
            hidden_size=256,
            num_regimes=4
        )
        
        # ========== Output Heads ==========
        # Multi-target predictions
        
        # Head 1: Entry Quality (5m scalping signal)
        self.entry_head = nn.Sequential(
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(128, 1),
            nn.Sigmoid()  # 0-1: quality score
        )
        
        # Head 2: Confirmation Probability (15m filter)
        self.confirm_head = nn.Sequential(
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(128, 1),
            nn.Sigmoid()  # 0-1: confirmation prob
        )
        
        # Head 3: Trend Score (1h optional, for leverage)
        self.trend_head = nn.Sequential(
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(128, 1),
            nn.Sigmoid()  # 0-1: trend strength
        )
        
        # Head 4: Volatility Prediction (risk management)
        self.volatility_head = nn.Sequential(
            nn.Linear(256, 64),
            nn.ReLU(),
            nn.Linear(64, 1),
            nn.Softplus()  # Always positive
        )
    
    def forward(self, x_5m, x_15m, x_1h, regime, regime_continuous):
        """
        Forward pass with regime awareness
        
        Args:
            x_5m: (batch, seq_len, 50) - 5m features
            x_15m: (batch, seq_len, 40) - 15m features
            x_1h: (batch, seq_len, 30) - 1h features
            regime: (batch,) - categorical regime [0-3]
            regime_continuous: (batch, 3) - [trend_strength, vol, volume]
        """
        
        # ========== Process each timeframe ==========
        lstm_5m_out, _ = self.lstm_5m(x_5m)   # (batch, seq, 128)
        lstm_15m_out, _ = self.lstm_15m(x_15m) # (batch, seq, 128)
        lstm_1h_out, _ = self.lstm_1h(x_1h)    # (batch, seq, 64)
        
        # Take last timestep from each
        lstm_5m_last = lstm_5m_out[:, -1, :]   # (batch, 128)
        lstm_15m_last = lstm_15m_out[:, -1, :] # (batch, 128)
        lstm_1h_last = lstm_1h_out[:, -1, :]   # (batch, 64)
        
        # Concatenate all timeframes
        lstm_concat = torch.cat([
            lstm_5m_last, 
            lstm_15m_last, 
            lstm_1h_last
        ], dim=1)  # (batch, 320)
        
        # ========== Add Regime Context ==========
        # Embed categorical regime
        regime_embed = self.regime_embedding(regime)  # (batch, 8)
        
        # Combine with continuous regime features
        regime_full = torch.cat([
            regime_embed,
            regime_continuous
        ], dim=1)  # (batch, 11)
        
        # Merge LSTM outputs with regime
        combined = torch.cat([lstm_concat, regime_full], dim=1)  # (batch, 331)
        
        # Pass through regime context layer
        context = self.regime_context(combined)  # (batch, 256)
        
        # ========== Regime-Aware Attention ==========
        # Attention weights based on current regime
        attended = self.attention(context, regime)  # (batch, 256)
        
        # ========== Generate Predictions ==========
        entry_quality = self.entry_head(attended)      # (batch, 1)
        confirm_prob = self.confirm_head(attended)      # (batch, 1)
        trend_score = self.trend_head(attended)         # (batch, 1)
        volatility = self.volatility_head(attended)     # (batch, 1)
        
        return {
            'entry_quality': entry_quality,      # 5m signal strength
            'confirm_prob': confirm_prob,        # 15m confirmation
            'trend_score': trend_score,          # 1h trend quality
            'volatility': volatility             # Risk estimate
        }


class RegimeAttention(nn.Module):
    """
    Attention mechanism که بسته به regime، 
    روی timeframes مختلف focus می‌کند
    """
    
    def __init__(self, hidden_size, num_regimes):
        super().__init__()
        
        # هر regime یک attention pattern دارد
        self.regime_attention_weights = nn.Parameter(
            torch.randn(num_regimes, hidden_size, hidden_size)
        )
        
        self.softmax = nn.Softmax(dim=-1)
    
    def forward(self, hidden, regime):
        """
        Args:
            hidden: (batch, hidden_size) - combined features
            regime: (batch,) - current regime [0-3]
        """
        batch_size = hidden.size(0)
        
        # Get attention matrix for each sample's regime
        attention_matrices = self.regime_attention_weights[regime]  # (batch, hidden, hidden)
        
        # Apply attention
        # hidden: (batch, 1, hidden) @ attention: (batch, hidden, hidden) 
        # = (batch, 1, hidden)
        hidden_expanded = hidden.unsqueeze(1)
        attended = torch.bmm(hidden_expanded, attention_matrices)
        attended = attended.squeeze(1)  # (batch, hidden)
        
        # Normalize
        attended = self.softmax(attended)
        
        # Apply to original hidden
        output = hidden * attended
        
        return output
```

---

## 🎯 چگونه رژیم در LSTM استفاده می‌شود؟

### مثال عملی:

```python
# در هنگام training و prediction:

# 1. محاسبه رژیم (از MVP strategy)
regime = strategy.detect_market_regime(dataframe)
# regime = 1 (Trending Up)

# 2. آماده‌سازی features
features = prepare_features(dataframe)

# 3. Feed به LSTM
predictions = model(
    x_5m=features['5m'],
    x_15m=features['15m'],
    x_1h=features['1h'],
    regime=regime,  # ← اینجا رژیم وارد می‌شود
    regime_continuous=[trend_strength, volatility, volume]
)

# 4. LSTM می‌داند که:
# "ما در رژیم Trending Up هستیم"
# پس:
# - روی 5m trend following signals focus کن
# - 15m باید trend alignment تأیید کند
# - 1h باید momentum قوی نشان دهد
# - از mean reversion signals اجتناب کن (مخصوص Range regime)

# 5. خروجی:
entry_quality = 0.85   # سیگنال قوی برای LONG
confirm_prob = 0.90    # تأیید بالا از 15m
trend_score = 0.80     # 1h هم trending است
volatility = 0.015     # نوسان پایین → می‌توان leverage بالاتر زد
```

---

## 📊 تطبیق با سیستم 90% Win Rate شما

### سیستم فعلی شما:
```
5m اسکلپ (primary) 
+ 15m تأیید اجباری (mandatory filter)
+ 1h اسکورینگ (optional, for leverage)
= 90% Win Rate
```

### چگونه LSTM این سیستم را enhance می‌کند:

```python
class YourProvenSystem_Enhanced:
    """
    سیستم 90% شما + LSTM Intelligence
    """
    
    def generate_signal(self, dataframe):
        # ========== STEP 1: 5m Scalp Signal ==========
        # قبلاً: شما manually pattern می‌دیدید
        # حالا: LSTM pattern recognition
        
        regime = detect_regime(dataframe)  # از MVP
        
        entry_quality = lstm_model.predict_entry(
            dataframe_5m=dataframe,
            regime=regime  # ← LSTM می‌داند چه regime است
        )
        
        # اگر regime=1 (Trending Up):
        # → LSTM روی breakout patterns focus می‌کند
        # اگر regime=0 (Range):
        # → LSTM روی mean reversion focus می‌کند
        
        # ========== STEP 2: 15m Mandatory Confirmation ==========
        # قبلاً: شما manually chart 15m را چک می‌کردید
        # حالا: LSTM multi-timeframe correlation
        
        confirm_prob = lstm_model.predict_confirmation(
            dataframe_5m=dataframe,
            dataframe_15m=dataframe_15m,
            regime=regime
        )
        
        # LSTM یاد می‌گیرد که:
        # - چه زمانی 5m signal با 15m align است
        # - کدام 15m patterns معتبر هستند
        # - چگونه false confirmations را فیلتر کند
        
        # ========== STEP 3: 1h Optional Scoring ==========
        # قبلاً: برای افزایش leverage
        # حالا: LSTM dynamic leverage recommendation
        
        trend_score = lstm_model.predict_trend(
            dataframe_1h=dataframe_1h,
            regime=regime
        )
        
        volatility = lstm_model.predict_volatility(
            dataframe_5m=dataframe,
            regime=regime
        )
        
        # ========== STEP 4: Dynamic Leverage ==========
        leverage = self.calculate_leverage(
            entry_quality=entry_quality,
            confirm_prob=confirm_prob,
            trend_score=trend_score,
            volatility=volatility,
            regime=regime  # ← رژیم در leverage هم دخیل است
        )
        
        # مثال:
        # entry=0.9, confirm=0.95, trend=0.85, vol=0.01, regime=1
        # → leverage = 5x (golden setup)
        
        # entry=0.7, confirm=0.8, trend=0.6, vol=0.03, regime=3
        # → leverage = 2x (high volatility, conservative)
        
        return {
            'signal': 'LONG' if entry_quality > 0.7 else 'NONE',
            'entry_quality': entry_quality,
            'confirmation': confirm_prob > 0.8,  # اجباری
            'leverage': leverage,
            'regime': regime
        }
```

---

## 🔑 کلید موفقیت: رژیم به عنوان Context، نه جایگزین

### ❌ اشتباه: نادیده گرفتن رژیم موجود
```python
# بد: LSTM همه چیز را از صفر یاد بگیرد
lstm_model.fit(raw_ohlcv_only)  # ❌ کند و غیرکارآمد
```

### ✅ درست: استفاده از رژیم به عنوان Prior Knowledge
```python
# خوب: از رژیم موجود به عنوان راهنما استفاده کن
lstm_model.fit(
    features=raw_ohlcv + technical_indicators,
    regime=regime_from_mvp,  # ← این نصف کار را آماده می‌کند
    targets=[entry, confirm, trend, volatility]
)

# LSTM فقط باید یاد بگیرد:
# "در هر regime، کدام patterns کار می‌کنند"
# نه اینکه "regime چیست" (این را MVP می‌دهد)
```

---

## 📈 مزایای این رویکرد

### 1. **سرعت Training**
- رژیم از قبل محاسبه شده → LSTM سریع‌تر converge می‌شود
- کمتر data نیاز است (چون context داریم)

### 2. **Interpretability**
- می‌دانیم چرا LSTM یک signal داد (به خاطر regime)
- می‌توانیم per-regime performance بسنجیم

### 3. **Robustness**
- اگر LSTM اشتباه کند، رژیم فیلتر می‌کند
- اگر رژیم اشتباه کند، LSTM تصحیح می‌کند

### 4. **ترکیب Rule-Based + AI**
- بهترین هر دو دنیا
- Rule-based (regime) → fast, interpretable
- AI (LSTM) → adaptive, pattern recognition

---

## 🚀 مراحل پیاده‌سازی

### Phase 1: استفاده از رژیم موجود (این هفته)
```python
# 1. رژیم را از strategy بخوانیم
regime_features = strategy.populate_indicators(dataframe)
regime = regime_features['%-market_regime']

# 2. به LSTM بدهیم
lstm_input = prepare_features_with_regime(dataframe, regime)

# 3. Train کنیم
model.fit(lstm_input)
```

### Phase 2: تست per-regime performance (هفته بعد)
```python
# برای هر regime جداگانه backtest
results_regime_0 = backtest(regime=0)  # Range
results_regime_1 = backtest(regime=1)  # Trending Up
results_regime_2 = backtest(regime=2)  # Trending Down
results_regime_3 = backtest(regime=3)  # High Vol

# ببینیم LSTM در کدام regime بهترین عملکرد را دارد
```

### Phase 3: Regime-Specific Tuning (ماه بعد)
```python
# هایپرپارامترهای مخصوص هر regime
if regime == 1:  # Trending Up
    entry_threshold = 0.7
    leverage_max = 5x
elif regime == 3:  # High Vol
    entry_threshold = 0.85  # سختگیرانه‌تر
    leverage_max = 2x       # محافظه‌کارانه‌تر
```

---

## 📝 خلاصه تصمیمات

| جنبه | تصمیم | دلیل |
|------|-------|------|
| **رژیم دیتکشن** | از MVP موجود استفاده شود | قبلاً پیاده‌سازی و تست شده |
| **نقش رژیم** | Input feature + Context | Complementary, not replacement |
| **LSTM Architecture** | Multi-timeframe + Attention | هماهنگ با سیستم 5m/15m/1h |
| **Attention Mechanism** | Regime-aware | Focus بر اساس regime |
| **Training Strategy** | Regime-stratified | برای هر regime جداگانه بهینه |

---

## ✅ چک‌لیست پیاده‌سازی

- [ ] خواندن regime از `FreqAIHybridStrategy.py`
- [ ] اضافه کردن regime به feature pipeline
- [ ] پیاده‌سازی `RegimeEmbedding` layer
- [ ] پیاده‌سازی `RegimeAttention` mechanism
- [ ] تست training با و بدون regime (مقایسه)
- [ ] Backtest per-regime analysis
- [ ] Hyperopt regime-specific thresholds

---

**تاریخ بعدی بررسی:** پس از پیاده‌سازی Phase 1

**نکته مهم:** این طراحی با سیستم MVP کامل هماهنگ است و آن را جایگزین نمی‌کند، بلکه enhance می‌کند. 🚀

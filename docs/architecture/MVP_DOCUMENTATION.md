# 📊 Freqtrade Hybrid ML Strategy - MVP Documentation (FUTURES)

## نسخه: 1.0.0 MVP - Futures Leverage Trading
**تاریخ:** اکتبر 2025  
**نویسنده:** Strategy Team
**Trading Mode:** Futures (USDT-M Perpetual)

---

## 🎯 هدف پروژه

ساخت یک استراتژی معاملاتی **Situation-Aware** برای **Futures با اهرم** با استفاده از:
- **Machine Learning Models**: LSTM + XGBoost + RandomForest + LightGBM
- **Ensemble Learning**: Weighted Ensemble → Stacked Ensemble  
- **Reinforcement Learning**: Policy Maker با PPO
- **Market Regime Detection**: تشخیص خودکار وضعیت بازار
- **Dynamic Indicators**: پنجره‌های adaptive بر اساس market regime
- **LONG/SHORT Trading**: معاملات دوطرفه با leverage متغیر

---

## ⚡ ویژگی‌های Futures

### Trading Mode
- **Market**: Binance USDT-M Perpetual Futures
- **Pairs**: BTC/USDT:USDT, ETH/USDT:USDT, SOL/USDT:USDT
- **Margin Mode**: Isolated (ایزوله - ریسک محدود به هر معامله)
- **Leverage**: Dynamic 2x-5x (بر اساس market regime)

### LONG & SHORT Entries
- **LONG**: وقتی مدل پیش‌بینی صعودی می‌کند
- **SHORT**: وقتی مدل پیش‌بینی نزولی می‌کند
- **هر دو جهت**: استراتژی می‌تواند همزمان هر دو سمت بازار را trade کند

### Dynamic Leverage
- **2x**: در بازار پرنوسان (High Volatility) یا confidence پایین
- **3x**: در شرایط عادی (Range Market)
- **5x**: در بازار trending با confidence بالا

⚠️ **نکته مهم**: این استراتژی برای **معاملات اهرم‌دار** طراحی شده. در Spot فقط LONG عمل می‌کند.

---

## 📁 ساختار پروژه

```
c:\freqai-futures-strategy\
├── freqtrade/                 # Freqtrade source code
├── user_data/
│   ├── strategies/
│   │   └── FreqAIHybridStrategy.py    # استراتژی اصلی MVP
│   ├── data/                          # داده‌های تاریخی
│   ├── logs/                          # لاگ‌ها
│   └── models/                        # مدل‌های trained
├── config/
│   └── config.json                    # کانفیگ اصلی
├── docker-compose-freqai.yml          # Docker setup
└── MVP_DOCUMENTATION.md               # این فایل

```

---

## 🏗️ معماری MVP (نسخه فعلی)

### ✅ آنچه پیاده‌سازی شده:

#### 1. **Feature Engineering (هوشمند)**
- **Multi-Timeframe Features**: 5m, 15m, 1h
- **Auto-Expansion**: ویژگی‌ها به صورت خودکار در timeframes مختلف expand می‌شوند
- **Technical Indicators**:
  - RSI, MFI, ADX (momentum)
  - SMA, EMA (trend)
  - Bollinger Bands, ATR (volatility)
  - MACD (trend + momentum)
  - Volume indicators
  
#### 2. **Market Regime Detection** ⭐ (Situation Awareness)
- **4 Regime Types**:
  - `0`: Range (خنثی)
  - `1`: Trending Up (صعودی)
  - `2`: Trending Down (نزولی)
  - `3`: High Volatility (نوسان بالا)
  
- **Detection Method**:
  - Trend Strength: بر اساس EMA(20) vs EMA(50)
  - Volatility: ATR normalized به قیمت
  - Volume: volume فعلی نسبت به میانگین
  
- **Multi-Horizon Regimes**:
  - Short-term (10 candles)
  - Medium-term (50 candles)  
  - Long-term (200 candles)

#### 3. **Multi-Target Predictions**
- **Target 1**: `&-s_close` - تغییر قیمت آینده (اصلی)
- **Target 2**: `&-s_volatility` - volatility آینده (risk management)
- **Target 3**: `&-s_volume` - افزایش volume (confirmation)

#### 4. **FreqAI Integration**
- **Models**: LightGBM, XGBoost, CatBoost (built-in)
- **Multi-Target Support**: پیش‌بینی همزمان چند target
- **Outlier Detection**: SVM برای حذف داده‌های outlier
- **Data Split**: 75/25 train/test
- **Retraining**: هر 30 دقیقه در حالت live

#### 5. **Entry/Exit Logic (LONG & SHORT)**
- **LONG Entry Conditions**:
  - پیش‌بینی صعودی مدل (`&-s_close` > threshold بالا)
  - اعتماد بالای مدل (`do_predict == 1`)
  - DI values پایین (نزدیک به داده‌های training)
  - خارج از regime پرنوسان
  - تأیید volume

- **SHORT Entry Conditions**:
  - پیش‌بینی نزولی مدل (`&-s_close` < threshold پایین)
  - اعتماد بالای مدل
  - DI values پایین  
  - خارج از regime پرنوسان
  - تأیید volume
  
- **LONG Exit**: پیش‌بینی منفی یا ورود به volatility بالا
- **SHORT Exit**: پیش‌بینی مثبت یا ورود به volatility بالا

#### 6. **Risk Management (Futures)**
- **Stoploss**: -5%
- **Trailing Stop**: فعال (1% با offset 2%)
- **Max Open Trades**: 3
- **Leverage**: Dynamic 2x-5x
- **Margin Mode**: Isolated
- **Position Sizing**: Unlimited (از کل balance استفاده می‌کند)

---

## ❌ آنچه هنوز پیاده نشده (برای نسخه‌های بعدی):

### 🔮 مرحله 2: Custom LSTM Model

```python
class LSTMFreqAI(BasePyTorchRegressor):
    """
    Custom LSTM for temporal pattern recognition
    """
    def __init__(self):
        self.model = nn.LSTM(
            input_size=n_features,
            hidden_size=128,
            num_layers=2,
            bidirectional=True,
            dropout=0.2
        )
        self.fc = nn.Linear(256, 3)  # 3 outputs for multi-target
    
    def fit(self, data_dictionary, dk):
        # Training with 5 years of data
        # Sequence length: 100 candles
        pass
```

**چرا LSTM؟**
- Gradient boosting models (XGB, LGBM) در patterns بلندمدت ضعیف‌تر هستند
- LSTM برای temporal dependencies عالی است
- با 5 سال data، patterns عمیق‌تری یاد می‌گیرد

---

### 🎯 مرحله 3: Stacked Ensemble (Meta-Learner)

```python
class MetaLearner(BaseRegressionModel):
    """
    Level-2 model: combines predictions from all base models
    """
    def fit(self, predictions_dict):
        # Input: predictions from LSTM, XGB, LGBM, CatBoost
        # Output: final weighted prediction
        
        meta_features = np.column_stack([
            predictions_dict['lstm'],
            predictions_dict['xgboost'],
            predictions_dict['lightgbm'],
            predictions_dict['catboost']
        ])
        
        # Train meta-model on out-of-fold predictions
        self.meta_model = LGBMRegressor(
            n_estimators=100,
            learning_rate=0.01
        )
        self.meta_model.fit(meta_features, labels)
```

**چرا Stacking؟**
- ترکیب بهتر از weighted average
- Meta-model یاد می‌گیرد که کدام model در چه شرایطی بهتر است
- Adaptive weighting بر اساس market conditions

---

### 🤖 مرحله 4: Reinforcement Learning Agent

```python
class CustomRLEnv(Base5ActionRLEnv):
    """
    RL Environment with advanced reward function
    """
    def calculate_reward(self, action: int) -> float:
        if not self._is_valid(action):
            return -2
        
        # Multi-component reward
        pnl = self.get_unrealized_profit()
        sharpe = self.calculate_sharpe_ratio()
        drawdown = self.get_max_drawdown()
        duration = self._current_tick - self._last_trade_tick
        
        # Weighted reward
        reward = (
            pnl * 100 +              # Profit component
            sharpe * 10 -            # Risk-adjusted
            drawdown * 50 -          # Drawdown penalty
            (duration / 100) * 2     # Holding time penalty
        )
        
        return reward

# RL Config
"rl_config": {
    "train_cycles": 5,
    "model_type": "PPO",
    "policy_type": "MlpPolicy",
    "net_arch": [128, 128, 64],
    "learning_rate": 0.0003,
    "max_trade_duration_candles": 300,
    "model_reward_parameters": {
        "profit_aim": 0.02,
        "rr": 2.0,
        "sharpe_target": 1.5
    }
}
```

**چرا RL؟**
- تصمیم‌گیری adaptive بر اساس market state
- یاد می‌گیرد timing بهتری داشته باشد
- می‌تواند trade-off بین risk/reward را optimize کند

---

### 🔧 مرحله 5: Dynamic Indicator Windows

```python
def get_adaptive_period(self, dataframe, base_period=20):
    """
    Adjust indicator periods based on market regime
    """
    regime = dataframe['%-market_regime'].iloc[-1]
    volatility = dataframe['%-volatility_regime'].iloc[-1]
    
    if regime == 0:  # Range
        # Use longer periods in range markets
        return int(base_period * 1.5)
    elif regime == 3:  # High Volatility
        # Use shorter periods in volatile markets
        return int(base_period * 0.7)
    else:  # Trending
        return base_period

# Usage in feature engineering
def feature_engineering_expand_all(self, dataframe, period, **kwargs):
    # Adjust period based on regime
    adaptive_period = self.get_adaptive_period(dataframe, period)
    
    dataframe[f"%-rsi-period"] = ta.RSI(dataframe, timeperiod=adaptive_period)
    # ... other indicators
```

---

## 🚀 نحوه استفاده

### پیش‌نیازها:
```bash
# Docker Desktop باید نصب باشد
# VPN باید روشن باشد (برای دسترسی به Binance)
```

### 1. دانلود داده‌های تاریخی

```bash
# ورود به container
docker-compose -f docker-compose-freqai.yml run freqtrade bash

# دانلود 5 سال داده (1825 روز)
freqtrade download-data \
  --exchange binance \
  --timeframes 5m 15m 1h \
  --pairs BTC/USDT ETH/USDT BNB/USDT SOL/USDT XRP/USDT \
  --days 1825

# برای backtest، 30 روز اضافی برای training
# Total: 1825 + 30 = 1855 روز
```

### 2. Backtesting

```bash
# Backtest 3 ساله
freqtrade backtesting \
  --strategy FreqAIHybridStrategy \
  --config config/config.json \
  --freqaimodel LightGBMRegressorMultiTarget \
  --timerange 20220101-20250101
```

**نکته مهم**: اولین backtest زمان‌بر است چون باید مدل‌ها را train کند. backtestهای بعدی سریع‌تر هستند (مدل‌های cached استفاده می‌شوند).

### 3. Dry Run (تست بدون ریسک)

```bash
# Start dry run
docker-compose -f docker-compose-freqai.yml up -d

# مشاهده logs
docker-compose -f docker-compose-freqai.yml logs -f freqtrade
```

### 4. Hyperopt (بهینه‌سازی پارامترها)

```bash
freqtrade hyperopt \
  --strategy FreqAIHybridStrategy \
  --config config/config.json \
  --hyperopt-loss SharpeHyperOptLoss \
  --timerange 20230101-20250101 \
  --epochs 500 \
  --spaces buy sell
```

**پارامترهای قابل بهینه‌سازی:**
- `buy_di_threshold`: حد آستانه DI برای ورود
- `sell_di_threshold`: حد آستانه DI برای خروج
- `trend_threshold`: حد تشخیص trend
- `volatility_threshold`: حد تشخیص volatility

---

## 📊 معیارهای ارزیابی

### Backtest Metrics:
- **Total Profit**: سود کل
- **Sharpe Ratio**: > 1.5 (عالی)
- **Max Drawdown**: < 20% (قابل قبول)
- **Win Rate**: > 50%
- **Profit Factor**: > 1.5
- **Average Trade Duration**: 5m-1h (short-term)

### Model Metrics (FreqAI):
- **R² Score**: > 0.3 (برای regression)
- **DI Threshold**: < 1.0 (predictions trustworthy)
- **Training Time**: < 5 min per pair
- **Prediction Latency**: < 100ms

---

## 🐛 عیب‌یابی رایج

### 1. مدل دقت پایینی دارد
**علت احتمالی:**
- Features کافی نیستند
- Training data کم است
- Outliers زیاد هستند

**راه حل:**
```json
// در config.json
"feature_parameters": {
    "indicator_periods_candles": [10, 20, 50, 100],  // افزایش periods
    "include_shifted_candles": 3,  // افزایش shifted candles
    "DI_threshold": 0.8,  // سخت‌گیری بیشتر
    "use_SVM_to_remove_outliers": true
}
```

### 2. Backtesting خیلی طول می‌کشد
**راه حل:**
```json
"freqai": {
    "backtest_period_days": 14,  // بجای 7
    "train_period_days": 15  // بجای 30
}
```

### 3. مدل‌ها expired می‌شوند
**علت:** `live_retrain_hours` خیلی بالاست

**راه حل:**
```json
"freqai": {
    "live_retrain_hours": 0.25,  // هر 15 دقیقه
    "expiration_hours": 0.5
}
```

### 4. خطای "No data available"
**علت:** داده دانلود نشده یا timerange اشتباه است

**راه حل:**
```bash
# دانلود مجدد با timerange بیشتر
freqtrade download-data --days 2000
```

---

## 📈 نقشه راه توسعه

### ✅ فاز 1: MVP (کامل شده)
- [x] Setup پروژه
- [x] FreqAI integration
- [x] Market regime detection
- [x] Multi-target predictions
- [x] Entry/Exit logic
- [x] Backtesting infrastructure

### 🔄 فاز 2: LSTM Integration (4-5 روز)
- [ ] Custom LSTM model (BasePyTorchRegressor)
- [ ] Training pipeline (5 years data)
- [ ] Integration با FreqAI
- [ ] Comparison با gradient boosting

### 🔄 فاز 3: Stacked Ensemble (2-3 روز)
- [ ] Meta-learner implementation
- [ ] Out-of-fold predictions
- [ ] Weighted averaging
- [ ] Performance evaluation

### 🔄 فاز 4: RL Agent (5-7 روز)
- [ ] Custom environment (Base5ActionRLEnv)
- [ ] Advanced reward function
- [ ] PPO training
- [ ] Integration با ensemble predictions
- [ ] TensorBoard monitoring

### 🔄 فاز 5: Dynamic Windows (2-3 روز)
- [ ] Adaptive period calculation
- [ ] Regime-based adjustment
- [ ] A/B testing
- [ ] Performance comparison

### 🔄 فاز 6: Production Ready (3-4 روز)
- [ ] Live testing (dry run)
- [ ] Performance monitoring
- [ ] Alert system
- [ ] Database logging
- [ ] Dashboard (FreqUI)

**تخمین کل:** 4-5 هفته برای MVP کامل

---

## 🔐 امنیت و Best Practices

### API Keys:
```bash
# هرگز API keys را commit نکنید!
# از environment variables استفاده کنید

export BINANCE_API_KEY="your_key"
export BINANCE_API_SECRET="your_secret"
```

### Backtesting قبل از Live:
```
1. Backtest 3-year → ارزیابی کلی
2. Backtest recent 6-month → بررسی performance اخیر
3. Dry run 1 week → تست real-time
4. Live با capital کم → risk management
5. Scale up تدریجی
```

### Risk Management Rules:
- **Max Risk per Trade**: 1-2% of capital
- **Max Drawdown Alert**: 15%
- **Daily Loss Limit**: 5%
- **Max Open Trades**: 3-5
- **Diversification**: حداقل 5 pairs

---

## 📚 منابع آموزشی

### Freqtrade Documentation:
- [FreqAI Configuration](https://www.freqtrade.io/en/stable/freqai-configuration/)
- [Feature Engineering](https://www.freqtrade.io/en/stable/freqai-feature-engineering/)
- [Reinforcement Learning](https://www.freqtrade.io/en/stable/freqai-reinforcement-learning/)

### Machine Learning:
- [LSTM for Time Series](https://colah.github.io/posts/2015-08-Understanding-LSTMs/)
- [Ensemble Methods](https://scikit-learn.org/stable/modules/ensemble.html)
- [Stable Baselines3 RL](https://stable-baselines3.readthedocs.io/)

### Trading:
- [Market Microstructure](https://www.investopedia.com/terms/m/microstructure.asp)
- [Risk Management](https://www.babypips.com/learn/forex/risk-management)

---

## 🙋 سوالات متداول (FAQ)

### Q1: چرا از Docker استفاده می‌کنیم؟
**A:** Docker محیطی ایزوله و reproducible فراهم می‌کند. همچنین تمام dependencies را مدیریت می‌کند.

### Q2: آیا GPU لازم است؟
**A:** برای MVP نه. اما برای LSTM training، GPU بسیار سریع‌تر است (10-20x).

### Q3: چقدر capital لازم است؟
**A:** برای dry run هیچ. برای live، حداقل $500-1000 توصیه می‌شود.

### Q4: چقدر سود می‌توانم انتظار داشته باشم؟
**A:** بستگی به market conditions دارد. انتظار واقع‌بینانه: 5-15% ماهانه (با risk management مناسب).

### Q5: آیا می‌توانم برای Futures استفاده کنم؟
**A:** بله، ولی باید leverage و risk management را تنظیم کنید.

---

## 📞 پشتیبانی

اگر سوال یا مشکلی دارید:
1. [Freqtrade Discord](https://discord.gg/freqtrade)
2. [GitHub Issues](https://github.com/freqtrade/freqtrade/issues)
3. [Documentation](https://www.freqtrade.io/)

---

## 📝 تغییرات (Changelog)

### v1.0.0 (Oct 2025) - MVP
- ✅ Initial MVP release
- ✅ Market regime detection
- ✅ Multi-target predictions
- ✅ FreqAI integration
- ✅ Backtesting ready

### v1.1.0 (Planned) - LSTM
- 🔄 Custom LSTM model
- 🔄 5-year training
- 🔄 Temporal patterns

### v1.2.0 (Planned) - Ensemble
- 🔄 Meta-learner
- 🔄 Stacked ensemble
- 🔄 Adaptive weighting

### v2.0.0 (Planned) - RL
- 🔄 RL agent
- 🔄 Custom reward function
- 🔄 Production ready

---

**موفق باشید! 🚀📈**


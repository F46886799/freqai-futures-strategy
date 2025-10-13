# Evaluation Protocol Guide

**Version:** 1.0.0  
**Created:** October 2025  
**Status:** ✅ Active

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Why Evaluation Protocol Matters](#why-evaluation-protocol-matters)
3. [Three-Tier Validation](#three-tier-validation)
4. [Risk Constraints](#risk-constraints)
5. [Implementation Guide](#implementation-guide)
6. [Example Usage](#example-usage)
7. [Best Practices](#best-practices)
8. [FAQ](#faq)

---

## 🎯 Overview

The **Evaluation Protocol** is a comprehensive validation framework designed to prevent overfitting and ensure robust performance of RL trading strategies. It implements three complementary validation methods:

1. **Walk-Forward Validation** - Train on historical data, test on future unseen data
2. **Time-Series Cross-Validation** - Multiple train/test splits for stability assessment
3. **Out-of-Sample Holdout** - Final blind test on reserved data

All validations enforce **fixed risk constraints** to prevent optimization towards unrealistic metrics.

---

## 🚨 Why Evaluation Protocol Matters

### The Problem

```
❌ Common Mistakes in Strategy Evaluation:
├── Data Leakage: Training on future data
├── Overfitting: Optimizing to in-sample period
├── Look-Ahead Bias: Using information not available at prediction time
├── Survivorship Bias: Only testing on surviving assets
└── Parameter Tuning on Test Set: Invalidating out-of-sample results
```

### The Solution

```
✅ Proper Evaluation Protocol:
├── Strict time-based splits (no future data in training)
├── Multiple validation windows (not just one lucky period)
├── Fixed risk constraints (can't optimize to unrealistic goals)
├── Out-of-sample holdout (final blind test)
└── Transparent reporting (all metrics, not cherry-picked)
```

### Real-World Impact

| Aspect | Without Protocol | With Protocol |
|--------|------------------|---------------|
| **In-Sample Sharpe** | 3.5 | 1.8 |
| **Out-of-Sample Sharpe** | 0.2 💀 | 1.2 ✅ |
| **Production Sharpe** | -0.5 🔥 | 1.0 ✅ |
| **Survival Rate** | 10% | 70% |

**Key Insight:** Strategies that look amazing in backtest often fail in production. Proper evaluation catches this before you lose money.

---

## 🔄 Three-Tier Validation

### 1️⃣ Walk-Forward Validation

**Purpose:** Simulate realistic deployment with rolling time windows.

**How it works:**
```
Timeline:
├─────────────────────────────────────────────────────────────────►
│   Train   │ Test │         │         │         │         │
│    90d    │  30d │         │         │         │         │
│           │      │  Train  │ Test    │         │         │
│           │      │   90d   │  30d    │         │         │
│           │      │         │         │  Train  │ Test    │
│           │      │         │         │   90d   │  30d    │
└───────────┴──────┴─────────┴─────────┴─────────┴─────────┘
          Step=30d (roll forward monthly)
```

**Configuration:**
```python
config = EvaluationConfig(
    train_window_days=90,   # 3 months training
    test_window_days=30,    # 1 month testing
    step_size_days=30,      # Roll forward monthly
)
```

**Key Benefits:**
- ✅ Tests strategy on multiple market regimes
- ✅ Reveals performance stability over time
- ✅ Catches regime-specific overfitting
- ✅ Most realistic simulation of production deployment

**When to use:**
- Primary validation method for all strategies
- Before committing to RL model architecture
- After hyperparameter tuning

---

### 2️⃣ Time-Series Cross-Validation

**Purpose:** Assess model stability with overlapping folds.

**How it works:**
```
Timeline (5 folds):
├─────────────────────────────────────────────────────────────────►
│   Fold 1 Train   │ Test │                                   │
│                  │      │                                   │
│      Fold 2 Train        │ Test │                           │
│                          │      │                           │
│         Fold 3 Train            │ Test │                    │
│                                 │      │                    │
│            Fold 4 Train                │ Test │             │
│                                        │      │             │
│               Fold 5 Train                    │ Test │      │
└───────────────────────────────────────────────┴──────┴──────┘
```

**Configuration:**
```python
config = EvaluationConfig(
    n_splits=5,  # 5 cross-validation folds
)
```

**Key Benefits:**
- ✅ More robust than single train/test split
- ✅ Reveals variance in performance
- ✅ Better use of available data
- ✅ Identifies if strategy works only in specific periods

**When to use:**
- Model selection (comparing architectures)
- Hyperparameter validation
- Feature engineering experiments

---

### 3️⃣ Out-of-Sample Holdout

**Purpose:** Final blind test on completely unseen data.

**How it works:**
```
Timeline:
├─────────────────────────────────────────────────────────────────►
│                                                                  │
│      In-Sample (80%)            │    Out-of-Sample (20%)        │
│  (All development happens here) │  (NEVER TOUCH until final)    │
│                                 │                               │
└─────────────────────────────────┴───────────────────────────────┘
                                  ↑
                            Sacred Barrier
                    (Cross only once, at the very end)
```

**Configuration:**
```python
config = EvaluationConfig(
    oos_holdout_pct=20.0,  # Reserve 20% for final test
)
```

**Key Benefits:**
- ✅ True measure of generalization
- ✅ Prevents overtuning to validation results
- ✅ Most honest metric for stakeholders
- ✅ Best predictor of production performance

**When to use:**
- **ONLY ONCE** - at the very end of development
- After all model selection, tuning, feature engineering
- Before deploying to production
- For final reporting to stakeholders

**⚠️ Critical Rule:** Never tune based on OOS results. If OOS fails, go back to in-sample development.

---

## 🛡️ Risk Constraints

All validation methods enforce **fixed risk constraints** to prevent unrealistic optimization.

### Default Constraints

```python
@dataclass
class RiskConstraints:
    max_drawdown_pct: float = 20.0      # Maximum drawdown
    min_sharpe_ratio: float = 0.5       # Minimum Sharpe
    max_leverage: int = 10              # Maximum leverage
    max_position_pct: float = 30.0      # Max position size
    max_daily_loss_pct: float = 5.0     # Daily circuit breaker
    min_win_rate_pct: float = 30.0      # Minimum win rate
```

### Why Fixed Constraints?

**Without constraints:**
```python
# Optimizer finds:
Sharpe = 10.0  # Amazing!
Max Drawdown = 95%  # Disaster! 💀
Win Rate = 10%  # Unacceptable
Leverage = 50x  # Suicidal
```

**With constraints:**
```python
# Optimizer must balance:
Sharpe = 1.5  # Realistic
Max Drawdown = 18%  # Within risk tolerance ✅
Win Rate = 45%  # Acceptable ✅
Leverage = 5x  # Conservative ✅
```

### Customizing Constraints

```python
# Conservative (capital preservation)
conservative = RiskConstraints(
    max_drawdown_pct=10.0,
    min_sharpe_ratio=1.0,
    max_leverage=3,
)

# Aggressive (growth focused)
aggressive = RiskConstraints(
    max_drawdown_pct=30.0,
    min_sharpe_ratio=0.3,
    max_leverage=15,
)

# Your custom constraints
custom = RiskConstraints(
    max_drawdown_pct=15.0,
    min_sharpe_ratio=0.8,
    max_daily_loss_pct=3.0,  # Tighter daily limit
)
```

---

## 🔨 Implementation Guide

### Step 1: Install Dependencies

```bash
# Already in requirements.txt, but ensure you have:
pip install pandas numpy
```

### Step 2: Basic Usage

```python
from src.evaluation_protocol import (
    EvaluationProtocol,
    EvaluationConfig,
    RiskConstraints
)
import pandas as pd

# 1. Load your backtest data
data = pd.read_parquet("user_data/backtest_data.parquet")
# Must have DatetimeIndex and OHLCV columns

# 2. Configure evaluation
config = EvaluationConfig(
    train_window_days=90,
    test_window_days=30,
    step_size_days=30,
    n_splits=5,
    oos_holdout_pct=20.0,
)

# 3. Initialize protocol
protocol = EvaluationProtocol(config)

# 4. Define strategy function
def my_strategy(data, is_training=True):
    """
    Your strategy implementation.
    
    Args:
        data: DataFrame with OHLCV and features
        is_training: Whether this is training or testing
        
    Returns:
        Dict with metrics: num_trades, total_pnl, sharpe_ratio, etc.
    """
    # Run your strategy here
    # For Freqtrade integration, call backtesting module
    
    return {
        'num_trades': 100,
        'total_pnl': 1500.0,
        'sharpe_ratio': 1.2,
        'max_drawdown_pct': 15.0,
        'win_rate_pct': 55.0,
    }

# 5. Run validations
wf_results = protocol.walk_forward_validation(data, my_strategy)
cv_results = protocol.time_series_cv(data, my_strategy)
oos_result = protocol.out_of_sample_test(data, my_strategy)

# 6. Generate reports
wf_report = protocol.generate_report(wf_results)
cv_report = protocol.generate_report(cv_results)

print(f"Walk-Forward Avg Sharpe: {wf_report['avg_test_sharpe']:.2f}")
print(f"Cross-Validation Avg Sharpe: {cv_report['avg_test_sharpe']:.2f}")
print(f"Out-of-Sample Sharpe: {oos_result.test_sharpe:.2f}")
```

### Step 3: Integrating with Freqtrade

```python
from freqtrade.optimize.backtesting import Backtesting
from freqtrade.configuration import Configuration

def freqtrade_strategy_fn(data, is_training=True):
    """
    Strategy function that uses Freqtrade backtesting.
    """
    # Configure Freqtrade
    config = Configuration.from_files(["config/config.json"])
    
    # Override date range based on data
    config['timerange'] = f"{data.index[0].strftime('%Y%m%d')}-{data.index[-1].strftime('%Y%m%d')}"
    
    # Run backtest
    backtesting = Backtesting(config)
    results = backtesting.start()
    
    # Extract metrics
    stats = results['results_metrics']
    
    return {
        'num_trades': stats['total_trades'],
        'total_pnl': stats['profit_total'],
        'sharpe_ratio': stats.get('sharpe', 0.0),
        'max_drawdown_pct': abs(stats['max_drawdown_percentage']),
        'win_rate_pct': stats['winning_percentage'],
    }

# Use with protocol
wf_results = protocol.walk_forward_validation(data, freqtrade_strategy_fn)
```

---

## 📊 Example Usage

### Complete Example

```python
"""
Complete evaluation workflow for RL strategy development.
"""
import logging
from pathlib import Path
from src.evaluation_protocol import (
    EvaluationProtocol,
    EvaluationConfig,
    RiskConstraints
)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    # 1. Load data
    data_path = Path("user_data/data/binance/futures")
    # Assume we have preprocessed data with features
    data = load_and_preprocess_data(data_path)
    
    # 2. Configure with custom constraints
    custom_constraints = RiskConstraints(
        max_drawdown_pct=15.0,  # Conservative
        min_sharpe_ratio=0.8,   # Realistic
        max_leverage=5,         # Moderate
    )
    
    config = EvaluationConfig(
        train_window_days=90,
        test_window_days=30,
        step_size_days=30,
        n_splits=5,
        oos_holdout_pct=20.0,
        risk_constraints=custom_constraints,
    )
    
    # 3. Initialize
    protocol = EvaluationProtocol(config)
    
    # 4. Run all validations
    logger.info("Starting walk-forward validation...")
    wf_results = protocol.walk_forward_validation(data, my_strategy)
    
    logger.info("Starting time-series CV...")
    cv_results = protocol.time_series_cv(data, my_strategy)
    
    logger.info("Starting out-of-sample test...")
    oos_result = protocol.out_of_sample_test(data, my_strategy)
    
    # 5. Generate comprehensive report
    wf_report = protocol.generate_report(wf_results)
    cv_report = protocol.generate_report(cv_results)
    
    # 6. Print summary
    print("\n" + "="*60)
    print("EVALUATION SUMMARY")
    print("="*60)
    
    print(f"\n📊 Walk-Forward Validation ({len(wf_results)} windows)")
    print(f"  Avg Test Sharpe: {wf_report['avg_test_sharpe']:.2f} ± {wf_report['std_test_sharpe']:.2f}")
    print(f"  Avg Test MDD: {wf_report['avg_test_mdd_pct']:.1f}%")
    print(f"  Passed Constraints: {wf_report['passed_constraints_pct']:.1f}%")
    
    print(f"\n📊 Time-Series CV ({config.n_splits} folds)")
    print(f"  Avg Test Sharpe: {cv_report['avg_test_sharpe']:.2f} ± {cv_report['std_test_sharpe']:.2f}")
    print(f"  Avg Test MDD: {cv_report['avg_test_mdd_pct']:.1f}%")
    print(f"  Passed Constraints: {cv_report['passed_constraints_pct']:.1f}%")
    
    print(f"\n🎯 Out-of-Sample Test (FINAL)")
    print(f"  Test Sharpe: {oos_result.test_sharpe:.2f}")
    print(f"  Test MDD: {oos_result.test_mdd_pct:.1f}%")
    print(f"  Test Win Rate: {oos_result.test_win_rate_pct:.1f}%")
    print(f"  Passed Constraints: {'✅ YES' if oos_result.passed_constraints else '❌ NO'}")
    
    if oos_result.constraint_violations:
        print(f"\n  ⚠️ Violations:")
        for violation in oos_result.constraint_violations:
            print(f"    - {violation}")
    
    # 7. Decision
    if oos_result.passed_constraints and oos_result.test_sharpe > 0.8:
        print("\n✅ Strategy PASSED evaluation - Ready for production testing")
    else:
        print("\n❌ Strategy FAILED evaluation - Back to development")
    
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
```

---

## ✅ Best Practices

### DO's ✅

1. **Always use time-based splits**
   ```python
   # ✅ Correct: Train on past, test on future
   train = data['2023-01-01':'2023-03-31']
   test = data['2023-04-01':'2023-04-30']
   ```

2. **Reserve OOS data from day one**
   ```python
   # ✅ Correct: Set aside 20% immediately
   split_idx = int(len(data) * 0.8)
   dev_data = data[:split_idx]  # Use this for all development
   oos_data = data[split_idx:]   # NEVER TOUCH until final test
   ```

3. **Run multiple validation methods**
   ```python
   # ✅ Correct: Use all three methods
   wf_results = protocol.walk_forward_validation(data, strategy)
   cv_results = protocol.time_series_cv(data, strategy)
   oos_result = protocol.out_of_sample_test(data, strategy)
   ```

4. **Enforce risk constraints**
   ```python
   # ✅ Correct: Set realistic constraints
   constraints = RiskConstraints(
       max_drawdown_pct=15.0,
       min_sharpe_ratio=0.8,
   )
   ```

5. **Report all metrics, not cherry-picked**
   ```python
   # ✅ Correct: Report mean, std, worst case
   print(f"Sharpe: {mean:.2f} ± {std:.2f} (worst: {min:.2f})")
   ```

### DON'Ts ❌

1. **Don't use random splits**
   ```python
   # ❌ Wrong: Random split destroys time-series structure
   from sklearn.model_selection import train_test_split
   train, test = train_test_split(data, test_size=0.2)  # BAD!
   ```

2. **Don't tune on test set**
   ```python
   # ❌ Wrong: Testing on same data used for tuning
   for params in param_grid:
       model = train(train_data, params)
       score = evaluate(test_data)  # If you use this to select params...
       if score > best_score:
           best_params = params  # ...test set is now invalid!
   ```

3. **Don't look at OOS during development**
   ```python
   # ❌ Wrong: Peeking at OOS invalidates it
   oos_result = protocol.out_of_sample_test(data, strategy)
   if oos_result.sharpe < 1.0:
       # Adjust strategy  # BAD! You just contaminated OOS
   ```

4. **Don't ignore failed validations**
   ```python
   # ❌ Wrong: Cherry-picking good results
   if wf_report['avg_sharpe'] > 1.5:
       print("Strategy is great!")  # What about the bad windows?
   ```

5. **Don't optimize for metrics alone**
   ```python
   # ❌ Wrong: Sharpe=5.0 but MDD=80%
   # Always check risk-adjusted metrics and constraints
   ```

---

## ❓ FAQ

### Q1: How much data do I need?

**Minimum:**
- Walk-forward: 6 months (4 windows × 90-day train + 30-day test)
- Time-series CV: 6 months (5 folds)
- OOS holdout: 20% of available data

**Recommended:**
- 2+ years for robust validation
- Multiple market regimes (bull, bear, sideways)
- Recent data (not just 2017-2018 crypto bull market)

### Q2: What if my strategy fails OOS test?

**Do NOT:**
- ❌ Adjust strategy based on OOS results
- ❌ Re-run OOS test multiple times
- ❌ Cherry-pick different OOS periods

**DO:**
- ✅ Accept that strategy overfit to in-sample
- ✅ Go back to development (forget OOS results)
- ✅ Improve strategy using in-sample methods
- ✅ Only re-test OOS after significant changes

### Q3: Can I use the same OOS period for multiple strategies?

**Answer:** Yes, but with caution.

- If testing completely different approaches: OK
- If testing variants of same strategy: You're contaminating OOS
- Best practice: Reserve multiple OOS periods (e.g., 20%, 10%, 10%)

### Q4: How do I integrate with Freqtrade hyperopt?

**Answer:** Use walk-forward validation in hyperopt objective:

```python
from src.evaluation_protocol import EvaluationProtocol

class MyHyperOpt(IHyperOpt):
    def hyperopt_space(self):
        # Define hyperparameters
        pass
    
    @staticmethod
    def objective(results, **params):
        # Instead of using single backtest result:
        protocol = EvaluationProtocol()
        wf_results = protocol.walk_forward_validation(data, strategy)
        report = protocol.generate_report(wf_results)
        
        # Return avg walk-forward performance
        return report['avg_test_sharpe']
```

### Q5: What metrics should I track?

**Essential:**
- Sharpe Ratio (risk-adjusted returns)
- Maximum Drawdown (worst-case loss)
- Win Rate (% winning trades)
- Total Trades (statistical significance)

**Advanced:**
- Sortino Ratio (downside-adjusted)
- Calmar Ratio (return/MDD)
- Profit Factor (gross profit / gross loss)
- Average Trade Duration

**Red Flags:**
- Sharpe >3.0 (likely overfitting)
- Win Rate >70% (suspicious)
- MDD <5% (too good to be true)
- Very few trades (<50 per year)

---

## 🔗 References

### Internal Documentation
- [PROJECT_STATE.md](../PROJECT_STATE.md) - Complete project overview
- [SCRUM_FRAMEWORK.md](../SCRUM_FRAMEWORK.md) - Sprint 1 details
- [UNIFIED_ARCHITECTURE.md](../docs/architecture/UNIFIED_ARCHITECTURE.md) - System design

### External Resources
- [Advances in Financial Machine Learning (Marcos López de Prado)](https://www.wiley.com/en-us/Advances+in+Financial+Machine+Learning-p-9781119482086)
- [Time Series Cross-Validation](https://robjhyndman.com/hyndsight/tscv/)
- [Walk-Forward Analysis (Wikipedia)](https://en.wikipedia.org/wiki/Walk_forward_optimization)

---

## 📝 Changelog

### v1.0.0 (October 2025)
- ✅ Initial implementation
- ✅ Walk-forward validation
- ✅ Time-series cross-validation
- ✅ Out-of-sample holdout
- ✅ Risk constraints enforcement
- ✅ Comprehensive documentation

---

**Document Owner:** Strategy Team  
**Last Updated:** October 13, 2025  
**Status:** Active - Sprint 1, US 1.1

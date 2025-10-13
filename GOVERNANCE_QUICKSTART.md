# Governance System Integration - Quick Start

This guide shows how to use the governance system that monitors performance and adapts risk in real-time.

## ✅ System Validated

- ✅ Governance decider: 4/4 tests passed
- ✅ Runtime adapter: Successfully reads policy + decisions
- ✅ Strategy integration: Entry/leverage/stoploss adapted by governance state

## How It Works

```
Backtest/Live → Metrics → governance_decider → decisions.jsonl → Strategy reads & adapts
```

## Quick Test (Already Done)

1. **Install dependency:**
   ```powershell
   pip install PyYAML==6.0.2
   ```

2. **Run tests:**
   ```powershell
   python -m pytest tests/test_governance_decider.py -v
   ```
   Result: ✅ 4 passed in 3.87s

3. **Generate decision from metrics:**
   ```powershell
   python monitoring/governance_decider.py --policy config/governance_policy.yaml --latest monitoring/latest_metrics.json --history monitoring/metrics_history.csv --out monitoring/governance_decisions.jsonl
   ```
   Result: ✅ Status "warn" with risk_multiplier 0.75x (Sharpe 0.35 < 0.5 threshold)

4. **Check strategy integration:**
   ```powershell
   python -c "import sys; sys.path.insert(0, '.'); from monitoring.governance_runtime import get_governance_state; state = get_governance_state(); print(f'Status: {state.status}, Risk: {state.risk_multiplier}x')"
   ```
   Result: ✅ Status: warn, Risk: 0.75x

## Real Usage After Backtest

After running a backtest, extract metrics and run governance decider:

```powershell
# 1. Extract metrics from backtest output
python monitoring/extract_metrics.py backtest_output.txt

# 2. Run governance decider
python monitoring/governance_decider.py `
  --policy config/governance_policy.yaml `
  --latest monitoring/latest_metrics.json `
  --history monitoring/metrics_history.csv `
  --out monitoring/governance_decisions.jsonl

# 3. Strategy automatically reads last decision on next run
```

## What Strategy Does With Governance State

- **Status: none/resume** → Normal operation
- **Status: warn** → Reduce position size by risk_multiplier (0.75x)
- **Status: degrade** → Cut risk to 0.5x, disable shorts, tighten stops 1.25x
- **Status: halt** → Block all new entries (risk_multiplier = 0)

## Files Created

- `monitoring/governance_decider.py` — Decision engine
- `monitoring/governance_runtime.py` — Runtime adapter for strategy
- `tests/test_governance_decider.py` — Unit tests
- `config/governance_policy.yaml` — Policy template (tunable)
- `monitoring/GOVERNANCE_SPEC.md` — Design doc
- `monitoring/governance_decisions.jsonl` — Decision log (append-only)

## Current Governance State

Last decision (2025-10-13):
```json
{
  "timestamp": "2025-10-13T15:50:41Z",
  "status": "warn",
  "reason": ["pf_min_short", "sharpe_min_short"],
  "actions": {
    "risk_multiplier": 0.75,
    "tighten_stop_factor": 1.0,
    "disable_shorts": false
  }
}
```

Strategy will automatically apply 0.75x risk until metrics recover above policy thresholds.

## Next Steps (Optional)

1. Add CI job to run decider after every backtest
2. Wire `schedule_retrain_at` to actual retrain mechanism
3. Tune policy thresholds via walk-forward validation

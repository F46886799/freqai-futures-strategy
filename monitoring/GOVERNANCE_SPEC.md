# Self-Governing Agent: Hard Risk Constraints & Retraining Policy

This document specifies the guardrails and triggers needed to make the strategy self-governing with minimal autonomy, per roadmap. It does not change executable code.

## Objectives
- Enforce hard risk and capital constraints at trade and portfolio levels.
- Detect when the model’s regime or data distribution has shifted.
- Decide when to degrade risk, halt entries, and schedule retraining.
- Provide transparent logging and reproducible decisions.

## Contract (inputs/outputs)
- Inputs
  - monitoring/latest_metrics.json and metrics_history.csv
  - Governance policy file: config/governance_policy.yaml
  - Optional: model residuals, feature distributions, regime labels
- Outputs
  - governance_decisions.jsonl (append-only)
  - Signals: warn, degrade, halt, resume, schedule_retrain_at

## Risk Constraints (hard)
- Per-trade: leverage ≤ max_leverage, risk fraction ≤ max_risk_fraction, position size ≤ max_position_size_fraction
- Stops: dynamic ATR-based, clamped between min_stop_pct and max_stop_pct
- Portfolio: open trades ≤ max_open_trades, gross exposure ≤ cap, net exposure ≤ cap
- Daily loss circuit breaker and overall max drawdown cap

## State/Regime Awareness
- Regime engine: choose one
  1) Regime + rolling quantiles: compute per-regime quantiles for key signals (preds, z, volume) on rolling window and update periodically.
  2) HMM: fit discrete states on selected features; map states to risk tiers; update periodically.
- OOD gate: block signals when feature vector is far from training (z > threshold or Mahalanobis).

## Drift & Performance Monitors
- Concept drift: ADWIN on prediction residuals.
- Population drift: PSI across key features vs training baseline.
- Performance: PF/Sharpe/Win-rate over short/mid windows; MDD spikes.

## Triggers & Actions
- Warn: minor breaches. Action: log; optionally reduce size slightly.
- Degrade: moderate breaches or drift. Action: cut risk (size 0.5x), tighten stops, disable shorts optionally; schedule retrain.
- Halt: severe breaches (daily loss, MDD spike) or OOD. Action: stop new entries, force retrain.
- Resume: metrics recover above policy mins, and cooldown satisfied.

## Retraining Policy
- Base cadence: time-based (e.g., 12h) with cooldown.
- Event-driven: trigger on drift/perf breaches as per policy.
- After retrain: run validation with safety margins on costs; resume per rules.

## Implementation Sketch
- monitoring/governance_decider.py (future):
  - Load policy YAML and metrics
  - Compute monitors (PF, Sharpe, MDD trends, PSI, ADWIN)
  - Evaluate gates (volatility, spread/slippage)
  - Decide: none | warn | degrade | halt; manage schedule_retrain_at
  - Emit to decisions log and stdout
- Tests:
  - tests/test_governance_decider.py with fixtures for edge cases: no trades, sharp MDD spike, PSI drift, ADWIN hit, cooldown logic

## Edge Cases
- 0-trade windows: skip PF/Sharpe; rely on drift and regime gates.
- Sudden exchange outages: spread/slippage gate forces halt.
- High-volatility regime: volatility_gate halts entries until resumed.

## Next Steps (upon approval)
1) Add governance_decider.py (read-only; no trade control yet) + tests.
2) Wire into CI job to emit decisions after every backtest.
3) Iterate thresholds via walk-forward evaluation; lock policy v1.

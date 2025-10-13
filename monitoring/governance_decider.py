"""
Governance Decider
Reads policy + metrics and emits governance decisions (warn/degrade/halt/resume)

Non-invasive: Does not modify strategy or configs. Appends JSONL decisions.

Usage:
  python monitoring/governance_decider.py \
    --policy config/governance_policy.yaml \
    --latest monitoring/latest_metrics.json \
    --history monitoring/metrics_history.csv \
    --out monitoring/governance_decisions.jsonl
"""
from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
import yaml


# -----------------------------
# Data classes
# -----------------------------


@dataclass
class Policy:
    raw: Dict[str, Any]

    @property
    def risk(self) -> Dict[str, Any]:
        return self.raw.get("risk", {})

    @property
    def retraining(self) -> Dict[str, Any]:
        return self.raw.get("retraining", {})

    @property
    def evaluation(self) -> Dict[str, Any]:
        return self.raw.get("evaluation", {})

    @property
    def risk_degradation(self) -> Dict[str, Any]:
        return self.raw.get("risk_degradation", {})

    @property
    def actions_warn_multiplier(self) -> float:
        return float(self.risk_degradation.get("on_warn", {}).get("position_size_multiplier", 1.0))

    @property
    def actions_degrade_multiplier(self) -> float:
        return float(self.risk_degradation.get("on_degrade", {}).get("position_size_multiplier", 0.5))

    @property
    def actions_tighten_stops_factor(self) -> float:
        return float(self.risk_degradation.get("on_degrade", {}).get("tighten_stops_factor", 1.0))

    @property
    def disable_shorts_on_degrade(self) -> bool:
        return bool(self.risk_degradation.get("on_degrade", {}).get("disable_shorts", False))

    @property
    def max_daily_loss_pct(self) -> Optional[float]:
        return float(self.risk.get("portfolio", {}).get("max_daily_loss_pct", 0.0))

    @property
    def max_drawdown_pct(self) -> Optional[float]:
        return float(self.risk.get("portfolio", {}).get("max_drawdown_pct", 0.0))

    # Performance triggers
    @property
    def perf_triggers(self) -> Dict[str, Any]:
        return self.retraining.get("performance_triggers", {})

    @property
    def pf_min_short(self) -> Optional[float]:
        v = self.perf_triggers.get("pf_min_short")
        return float(v) if v is not None else None

    @property
    def sharpe_min_short(self) -> Optional[float]:
        v = self.perf_triggers.get("sharpe_min_short")
        return float(v) if v is not None else None

    @property
    def winrate_drop_pp(self) -> Optional[float]:
        v = self.perf_triggers.get("winrate_drop_pp")
        return float(v) if v is not None else None

    @property
    def mdd_spike_factor(self) -> Optional[float]:
        v = self.perf_triggers.get("mdd_spike_factor")
        return float(v) if v is not None else None

    # Drift triggers
    @property
    def drift_triggers(self) -> Dict[str, Any]:
        return self.retraining.get("drift_triggers", {})

    @property
    def psi_warn(self) -> Optional[float]:
        v = self.drift_triggers.get("feature_drift", {}).get("psi_warn")
        return float(v) if v is not None else None

    @property
    def psi_retrain(self) -> Optional[float]:
        v = self.drift_triggers.get("feature_drift", {}).get("psi_retrain")
        return float(v) if v is not None else None

    @property
    def adwin_delta(self) -> Optional[float]:
        v = self.drift_triggers.get("residual_drift", {}).get("adwin_delta")
        return float(v) if v is not None else None

    # Actions grouping
    @property
    def warn_only(self) -> List[str]:
        return list(self.retraining.get("actions", {}).get("warn_only_thresholds", []))

    @property
    def degrade_then_retrain(self) -> List[str]:
        return list(self.retraining.get("actions", {}).get("degrade_then_retrain", []))

    @property
    def halt_and_retrain(self) -> List[str]:
        return list(self.retraining.get("actions", {}).get("halt_and_retrain", []))

    # Retrain cadence
    @property
    def time_based_hours(self) -> float:
        return float(self.retraining.get("cadence", {}).get("time_based_hours", 12))

    @property
    def min_hours_between_retrains(self) -> float:
        return float(self.retraining.get("cadence", {}).get("min_hours_between_retrains", 6))

    # Resume controls
    @property
    def resume_require_back_to_baseline(self) -> bool:
        return bool(self.retraining.get("resume_conditions", {}).get("require_back_to_baseline", True))

    @property
    def min_hours_after_retrain(self) -> float:
        return float(self.retraining.get("resume_conditions", {}).get("min_hours_after_retrain", 2))


# -----------------------------
# Utility functions
# -----------------------------


def load_policy(path: Path) -> Policy:
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return Policy(raw=data or {})


def load_metrics(latest_path: Path, history_path: Path) -> Tuple[Dict[str, Any], pd.DataFrame]:
    latest: Dict[str, Any] = {}
    if latest_path.exists():
        with open(latest_path, "r", encoding="utf-8") as f:
            latest = json.load(f)
    else:
        print(f"[WARN] Latest metrics not found: {latest_path}")

    if history_path.exists():
        df = pd.read_csv(history_path)
    else:
        print(f"[WARN] Metrics history not found: {history_path}")
        df = pd.DataFrame()

    return latest, df


def parse_iso8601(ts: str) -> datetime:
    try:
        return datetime.fromisoformat(ts.replace("Z", "+00:00"))
    except Exception:
        return datetime.now(timezone.utc)


def last_decision(decisions_log: Path) -> Optional[Dict[str, Any]]:
    if not decisions_log.exists():
        return None
    last = None
    with open(decisions_log, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                last = json.loads(line)
            except json.JSONDecodeError:
                continue
    return last


def median_of(series: pd.Series) -> Optional[float]:
    s = pd.to_numeric(series, errors="coerce").dropna()
    return float(np.median(s)) if len(s) else None


def evaluate_performance(policy: Policy, latest: Dict[str, Any], history: pd.DataFrame) -> Tuple[List[str], List[str]]:
    """Return (warn_reasons, degrade_or_halt_reasons). PF may be unavailable -> ignored."""
    warn: List[str] = []
    severe: List[str] = []

    # Sharpe
    sharpe_min = policy.sharpe_min_short
    latest_sharpe = safe_float(latest.get("sharpe_ratio"))
    if sharpe_min is not None and latest_sharpe is not None and latest_sharpe < sharpe_min:
        label = "sharpe_min_short"
        if label in policy.warn_only:
            warn.append(label)
        elif label in policy.degrade_then_retrain:
            severe.append(label)

    # PF - optional
    latest_pf = safe_float(latest.get("profit_factor"))
    if latest_pf is not None and policy.pf_min_short is not None:
        if latest_pf < policy.pf_min_short:
            label = "pf_min_short"
            if label in policy.warn_only:
                warn.append(label)
            elif label in policy.degrade_then_retrain:
                severe.append(label)

    # Winrate drop vs mid median
    wr_drop_pp = policy.winrate_drop_pp
    if wr_drop_pp is not None and not history.empty and "win_rate" in history.columns:
        # Use previous N entries as "mid" proxy (e.g., last 20)
        mid_n = 20 if len(history) >= 20 else max(1, len(history) - 1)
        mid_sample = history.tail(mid_n).iloc[:-1] if len(history) > 1 else history.tail(1)
        mid_median = median_of(mid_sample["win_rate"]) if not mid_sample.empty else None
        current_wr = safe_float(latest.get("win_rate"))
        if mid_median is not None and current_wr is not None:
            drop_pp = max(0.0, float(mid_median) - float(current_wr))
            if drop_pp >= wr_drop_pp:
                label = "winrate_drop_pp"
                if label in policy.warn_only:
                    warn.append(label)
                elif label in policy.degrade_then_retrain:
                    severe.append(label)

    # MDD spike factor vs mid median
    mdd_factor = policy.mdd_spike_factor
    if mdd_factor is not None and not history.empty and "max_drawdown" in history.columns:
        mid_n = 20 if len(history) >= 20 else max(1, len(history) - 1)
        mid_sample = history.tail(mid_n).iloc[:-1] if len(history) > 1 else history.tail(1)
        mid_median_mdd = median_of(mid_sample["max_drawdown"]) if not mid_sample.empty else None
        latest_mdd = safe_float(latest.get("max_drawdown"))
        if mid_median_mdd is not None and latest_mdd is not None and mid_median_mdd > 0:
            if latest_mdd > mdd_factor * mid_median_mdd:
                # Treat as HALT trigger by default
                severe.append("mdd_spike_factor")

    return warn, severe


def evaluate_drift(policy: Policy, features_baseline: Optional[Path], features_current: Optional[Path], residuals_path: Optional[Path]) -> Tuple[List[str], List[str]]:
    warn: List[str] = []
    severe: List[str] = []

    # PSI on features if provided as JSON histograms: {feature: {"bins": [...], "counts": [...]}}
    if features_baseline and features_current and features_baseline.exists() and features_current.exists():
        try:
            with open(features_baseline, "r", encoding="utf-8") as f:
                base = json.load(f)
            with open(features_current, "r", encoding="utf-8") as f:
                curr = json.load(f)
            psi = compute_psi_multi(base, curr)
            if policy.psi_retrain is not None and psi >= policy.psi_retrain:
                severe.append("feature_drift.psi_retrain")
            elif policy.psi_warn is not None and psi >= policy.psi_warn:
                warn.append("feature_drift.psi_warn")
        except Exception as e:
            print(f"[WARN] PSI evaluation failed: {e}")

    # Residual drift (simple Page-Hinkley as a lightweight proxy for ADWIN)
    if residuals_path and residuals_path.exists():
        try:
            df = pd.read_csv(residuals_path)
            if "residual" in df.columns and len(df) > 20:
                if page_hinkley_drift(df["residual"].values):
                    severe.append("residual_drift")
        except Exception as e:
            print(f"[WARN] Residual drift evaluation failed: {e}")

    return warn, severe


def compute_psi(bins: List[float], base_counts: List[float], curr_counts: List[float]) -> float:
    """Compute PSI for a single variable given identical bins and counts.
    Bins are edges; counts are frequencies per bin. Sums will be normalized.
    """
    base = np.array(base_counts, dtype=float)
    curr = np.array(curr_counts, dtype=float)
    if base.sum() == 0 or curr.sum() == 0:
        return 0.0
    p = base / base.sum()
    q = curr / curr.sum()
    # Avoid log(0)
    eps = 1e-12
    ratio = (q + eps) / (p + eps)
    return float(np.sum((q - p) * np.log(ratio)))


def compute_psi_multi(base: Dict[str, Any], curr: Dict[str, Any]) -> float:
    psis = []
    for feat, spec in base.items():
        if feat not in curr:
            continue
        bins = spec.get("bins")
        bcounts = spec.get("counts")
        ccounts = curr[feat].get("counts")
        if bins is None or bcounts is None or ccounts is None:
            continue
        try:
            psis.append(compute_psi(bins, bcounts, ccounts))
        except Exception:
            continue
    return float(np.nanmean(psis)) if psis else 0.0


def page_hinkley_drift(x: np.ndarray, delta: float = 0.005, lambda_: float = 50.0, alpha: float = 0.99) -> bool:
    """Simple Page-Hinkley change detection.
    Returns True if a significant increase in mean is detected.
    """
    mean = 0.0
    mT = 0.0
    for i, xi in enumerate(x):
        mean = alpha * mean + (1 - alpha) * xi
        mT = min(0.0, mT + xi - mean - delta)
        if -mT > lambda_:
            return True
    return False


def safe_float(v: Any) -> Optional[float]:
    try:
        if v is None:
            return None
        return float(v)
    except Exception:
        return None


def compute_schedule(policy: Policy, decisions_log: Path, now: datetime) -> str:
    next_time = now + timedelta(hours=policy.time_based_hours)
    # Respect cooldown
    last = last_decision(decisions_log)
    if last and "actions" in last and isinstance(last["actions"], dict):
        sch = last["actions"].get("schedule_retrain_at")
        if sch:
            try:
                last_scheduled = parse_iso8601(sch)
                cooldown_time = last_scheduled + timedelta(hours=policy.min_hours_between_retrains)
                if cooldown_time > next_time:
                    next_time = cooldown_time
            except Exception:
                pass
    return next_time.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def decide(policy: Policy,
           latest: Dict[str, Any],
           history: pd.DataFrame,
           decisions_log: Path,
           features_baseline: Optional[Path] = None,
           features_current: Optional[Path] = None,
           residuals_path: Optional[Path] = None,
           now: Optional[datetime] = None) -> Dict[str, Any]:
    now = now or datetime.now(timezone.utc)
    prev = last_decision(decisions_log)
    prev_status = prev.get("status") if prev else None

    warn_perf, severe_perf = evaluate_performance(policy, latest, history)
    warn_drift, severe_drift = evaluate_drift(policy, features_baseline, features_current, residuals_path)

    reasons_warn = warn_perf + warn_drift
    reasons_severe = severe_perf + severe_drift

    # Daily loss and absolute MDD caps if provided in latest metrics (not always available)
    # We treat max_drawdown cap as HALT if exceeded.
    latest_mdd = safe_float(latest.get("max_drawdown"))
    if policy.max_drawdown_pct and latest_mdd is not None and latest_mdd >= policy.max_drawdown_pct:
        reasons_severe.append("max_drawdown_cap")

    # Determine status priority: halt > degrade > warn > resume/none
    status = "none"
    actions: Dict[str, Any] = {}

    if any(r in policy.halt_and_retrain or r in ["mdd_spike_factor", "max_drawdown_cap"] for r in reasons_severe):
        status = "halt"
        actions = {
            "risk_multiplier": 0.0,
            "tighten_stop_factor": policy.actions_tighten_stops_factor,
            "disable_shorts": True,
            "schedule_retrain_at": compute_schedule(policy, decisions_log, now),
        }
    elif reasons_severe:
        status = "degrade"
        actions = {
            "risk_multiplier": policy.actions_degrade_multiplier,
            "tighten_stop_factor": policy.actions_tighten_stops_factor,
            "disable_shorts": policy.disable_shorts_on_degrade,
            "schedule_retrain_at": compute_schedule(policy, decisions_log, now),
        }
    elif reasons_warn:
        status = "warn"
        actions = {
            "risk_multiplier": policy.actions_warn_multiplier,
            "tighten_stop_factor": 1.0,
            "disable_shorts": False,
        }
    else:
        # Consider resume if previously degraded/halted and metrics are back above mins
        if prev_status in ("halt", "degrade"):
            ok = True
            if policy.resume_require_back_to_baseline:
                # Must satisfy sharpe and winrate drop constraints
                latest_sharpe = safe_float(latest.get("sharpe_ratio"))
                if policy.sharpe_min_short is not None and (latest_sharpe is None or latest_sharpe < policy.sharpe_min_short):
                    ok = False
                if policy.winrate_drop_pp is not None and not history.empty and "win_rate" in history.columns:
                    mid_n = 20 if len(history) >= 20 else max(1, len(history) - 1)
                    mid_sample = history.tail(mid_n).iloc[:-1] if len(history) > 1 else history.tail(1)
                    mid_median = median_of(mid_sample["win_rate"]) if not mid_sample.empty else None
                    current_wr = safe_float(latest.get("win_rate"))
                    if mid_median is None or current_wr is None:
                        ok = False
                    else:
                        drop_pp = max(0.0, float(mid_median) - float(current_wr))
                        if drop_pp >= policy.winrate_drop_pp:
                            ok = False
            if ok:
                status = "resume"
                actions = {
                    "risk_multiplier": 1.0,
                    "tighten_stop_factor": 1.0,
                    "disable_shorts": False,
                }

    decision = {
        "timestamp": now.astimezone(timezone.utc).isoformat().replace("+00:00", "Z"),
        "status": status,
        "reason": sorted(list(set(reasons_severe + reasons_warn))) if (reasons_severe or reasons_warn) else ["ok"],
        "actions": actions,
    }
    return decision


def append_jsonl(path: Path, obj: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(obj, ensure_ascii=False))
        f.write("\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--policy", default="config/governance_policy.yaml")
    ap.add_argument("--latest", default="monitoring/latest_metrics.json")
    ap.add_argument("--history", default="monitoring/metrics_history.csv")
    ap.add_argument("--out", default="monitoring/governance_decisions.jsonl")
    ap.add_argument("--features-baseline", default=None)
    ap.add_argument("--features-current", default=None)
    ap.add_argument("--residuals", default=None)
    args = ap.parse_args()

    policy = load_policy(Path(args.policy))
    latest, history = load_metrics(Path(args.latest), Path(args.history))
    decision = decide(
        policy=policy,
        latest=latest,
        history=history,
        decisions_log=Path(args.out),
        features_baseline=Path(args.features_baseline) if args.features_baseline else None,
        features_current=Path(args.features_current) if args.features_current else None,
        residuals_path=Path(args.residuals) if args.residuals else None,
    )

    append_jsonl(Path(args.out), decision)
    print(json.dumps(decision, indent=2))


if __name__ == "__main__":
    main()

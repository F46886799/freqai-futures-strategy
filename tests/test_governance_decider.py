import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from monitoring.governance_decider import Policy, decide


def policy_dict():
    return {
        "risk": {
            "portfolio": {
                "max_daily_loss_pct": 2.0,
                "max_drawdown_pct": 10.0,
            }
        },
        "retraining": {
            "performance_triggers": {
                "pf_min_short": 1.05,
                "sharpe_min_short": 0.5,
                "winrate_drop_pp": 10.0,
                "mdd_spike_factor": 1.5,
            },
            "drift_triggers": {
                "feature_drift": {"psi_warn": 0.2, "psi_retrain": 0.3},
                "residual_drift": {"adwin_delta": 0.002},
            },
            "actions": {
                "warn_only_thresholds": ["pf_min_short", "sharpe_min_short"],
                "degrade_then_retrain": ["winrate_drop_pp", "feature_drift.psi_retrain"],
                "halt_and_retrain": ["mdd_spike_factor"],
            },
            "cadence": {"time_based_hours": 12, "min_hours_between_retrains": 6},
            "resume_conditions": {"require_back_to_baseline": True, "min_hours_after_retrain": 2},
        },
        "risk_degradation": {
            "on_warn": {"position_size_multiplier": 0.75},
            "on_degrade": {"position_size_multiplier": 0.5, "disable_shorts": True, "tighten_stops_factor": 1.25},
        },
    }


def test_warn_scenario(tmp_path: Path):
    pol = Policy(policy_dict())
    latest = {"sharpe_ratio": 0.3, "win_rate": 55.0, "max_drawdown": 5.0}
    history = pd.DataFrame({
        "timestamp": ["t1", "t2"],
        "win_rate": [56.0, 55.5],
        "max_drawdown": [4.0, 4.5],
    })
    out = tmp_path / "decisions.jsonl"
    d = decide(pol, latest, history, out)
    assert d["status"] == "warn"
    assert d["actions"]["risk_multiplier"] == 0.75


def test_degrade_scenario(tmp_path: Path):
    pol = Policy(policy_dict())
    latest = {"sharpe_ratio": 0.8, "win_rate": 40.0, "max_drawdown": 5.0}
    history = pd.DataFrame({
        "timestamp": ["t1", "t2", "t3", "t4", "t5"],
        "win_rate": [60.0, 58.0, 59.0, 57.0, 55.0],
        "max_drawdown": [4.0, 4.5, 4.2, 4.0, 4.3],
    })
    out = tmp_path / "decisions.jsonl"
    d = decide(pol, latest, history, out)
    assert d["status"] == "degrade"
    assert d["actions"]["risk_multiplier"] == 0.5
    assert d["actions"]["disable_shorts"] is True


def test_halt_scenario_due_to_mdd(tmp_path: Path):
    pol = Policy(policy_dict())
    latest = {"sharpe_ratio": 1.0, "win_rate": 55.0, "max_drawdown": 12.0}
    history = pd.DataFrame({
        "timestamp": ["t1", "t2"],
        "win_rate": [56.0, 55.5],
        "max_drawdown": [4.0, 4.5],
    })
    out = tmp_path / "decisions.jsonl"
    d = decide(pol, latest, history, out)
    assert d["status"] == "halt"
    assert d["actions"]["risk_multiplier"] == 0.0


def test_resume_after_recovery(tmp_path: Path):
    pol = Policy(policy_dict())
    # First: degrade decision
    history = pd.DataFrame({
        "timestamp": ["t1", "t2", "t3", "t4"],
        "win_rate": [60.0, 58.0, 59.0, 57.0],
        "max_drawdown": [4.0, 4.5, 4.2, 4.0],
    })
    latest_bad = {"sharpe_ratio": 0.6, "win_rate": 45.0, "max_drawdown": 5.0}
    out = tmp_path / "decisions.jsonl"
    d1 = decide(pol, latest_bad, history, out, now=datetime(2025, 10, 13, 12, 0, tzinfo=timezone.utc))
    with open(out, "a", encoding="utf-8") as f:
        f.write(json.dumps(d1) + "\n")

    # Then: metrics recover above thresholds -> resume
    latest_good = {"sharpe_ratio": 0.6, "win_rate": 58.0, "max_drawdown": 5.0}
    d2 = decide(pol, latest_good, history, out, now=datetime(2025, 10, 13, 16, 0, tzinfo=timezone.utc))
    assert d2["status"] in ("resume", "warn")  # resume or warn if PF missing

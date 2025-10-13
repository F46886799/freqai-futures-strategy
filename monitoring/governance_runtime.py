"""Runtime adapter to read governance policy and last decision.
This module is imported by the strategy to adapt risk and gating at runtime.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional

import yaml


@dataclass
class GovernanceState:
    status: str = "none"  # one of: none|warn|degrade|halt|resume
    risk_multiplier: float = 1.0
    tighten_stop_factor: float = 1.0
    disable_shorts: bool = False
    # Policy constraints (for enforcement in strategy)
    max_leverage: Optional[float] = None
    min_stop_pct: Optional[float] = None
    max_stop_pct: Optional[float] = None


def _read_last_decision(decisions_log: Path) -> Dict[str, Any]:
    if not decisions_log.exists():
        return {}
    last = {}
    try:
        with open(decisions_log, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    last = json.loads(line)
                except json.JSONDecodeError:
                    continue
    except Exception:
        return {}
    return last


def _read_policy(policy_path: Path) -> Dict[str, Any]:
    try:
        with open(policy_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    except Exception:
        return {}


def get_governance_state(
    policy_path: str = "config/governance_policy.yaml",
    decisions_path: str = "monitoring/governance_decisions.jsonl",
) -> GovernanceState:
    policy = _read_policy(Path(policy_path))
    last = _read_last_decision(Path(decisions_path))

    actions = last.get("actions", {}) if isinstance(last, dict) else {}
    status = last.get("status", "none") if isinstance(last, dict) else "none"

    # Extract policy constraints
    per_trade = (((policy.get("risk") or {}).get("per_trade")) or {})
    stop_cfg = (per_trade.get("stop") or {})

    return GovernanceState(
        status=str(status),
        risk_multiplier=float(actions.get("risk_multiplier", 1.0) or 1.0),
        tighten_stop_factor=float(actions.get("tighten_stop_factor", 1.0) or 1.0),
        disable_shorts=bool(actions.get("disable_shorts", False)),
        max_leverage=(float(per_trade.get("max_leverage")) if per_trade.get("max_leverage") is not None else None),
        min_stop_pct=(float(stop_cfg.get("min_stop_pct")) if stop_cfg.get("min_stop_pct") is not None else None),
        max_stop_pct=(float(stop_cfg.get("max_stop_pct")) if stop_cfg.get("max_stop_pct") is not None else None),
    )

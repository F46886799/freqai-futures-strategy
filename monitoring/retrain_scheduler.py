"""
Retrain Scheduler
Reads governance decisions and triggers retraining when scheduled.

This is a simple coordinator that can be:
- Run manually after each decision
- Integrated into CI/CD pipeline
- Run as a cron job or scheduled task
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional


def read_last_decision(decisions_log: Path) -> Optional[dict]:
    """Read the last governance decision from JSONL log."""
    if not decisions_log.exists():
        return None
    
    last = None
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
    except Exception as e:
        print(f"❌ Error reading decisions log: {e}")
        return None
    
    return last


def should_retrain(decision: dict, now: Optional[datetime] = None) -> tuple[bool, str]:
    """
    Check if retraining should be triggered.
    
    Returns:
        (should_retrain, reason)
    """
    now = now or datetime.now(timezone.utc)
    
    if not decision:
        return False, "No decision available"
    
    actions = decision.get("actions", {})
    scheduled_at = actions.get("schedule_retrain_at")
    
    if not scheduled_at:
        return False, "No retraining scheduled"
    
    try:
        scheduled_dt = datetime.fromisoformat(scheduled_at.replace("Z", "+00:00"))
    except Exception as e:
        return False, f"Invalid schedule format: {e}"
    
    if now >= scheduled_dt:
        status = decision.get("status", "unknown")
        reason_list = decision.get("reason", [])
        return True, f"Scheduled retrain reached (status: {status}, reasons: {', '.join(reason_list)})"
    else:
        delta = scheduled_dt - now
        return False, f"Retrain scheduled in {delta}"


def trigger_retrain(
    strategy: str = "FreqAIHybridStrategy",
    config: str = "config/config.json",
    freqai_model: str = "LightGBMRegressorMultiTarget",
    dry_run: bool = False,
) -> bool:
    """
    Trigger a retraining run via Freqtrade.
    
    In production, this would:
    - Stop live bot gracefully
    - Run training with latest data
    - Validate new model
    - Resume with new model if validation passes
    
    For now, this is a placeholder that logs the intent.
    """
    print(f"\n🔄 Triggering retraining:")
    print(f"   Strategy: {strategy}")
    print(f"   Config: {config}")
    print(f"   Model: {freqai_model}")
    
    if dry_run:
        print("   [DRY RUN] Would execute retraining command")
        return True
    
    # Example: Run Freqtrade in training mode
    # In practice, you'd integrate with your training pipeline
    cmd = [
        "freqtrade",
        "backtesting",
        "--strategy", strategy,
        "--config", config,
        "--freqaimodel", freqai_model,
        "--timerange", "20240101-",  # Train on all available data
        "--freqai-backtest-live-models",  # Use live models for validation
    ]
    
    print(f"   Command: {' '.join(cmd)}")
    print("   ⚠️  This is a placeholder. Integrate with your training pipeline.")
    
    # Uncomment to actually run:
    # try:
    #     result = subprocess.run(cmd, check=True, capture_output=True, text=True)
    #     print("   ✅ Retraining completed successfully")
    #     return True
    # except subprocess.CalledProcessError as e:
    #     print(f"   ❌ Retraining failed: {e}")
    #     return False
    
    return True


def main():
    parser = argparse.ArgumentParser(description="Retrain scheduler for governance-driven retraining")
    parser.add_argument(
        "--decisions",
        default="monitoring/governance_decisions.jsonl",
        help="Path to governance decisions log"
    )
    parser.add_argument(
        "--strategy",
        default="FreqAIHybridStrategy",
        help="Strategy name"
    )
    parser.add_argument(
        "--config",
        default="config/config.json",
        help="Config path"
    )
    parser.add_argument(
        "--freqai-model",
        default="LightGBMRegressorMultiTarget",
        help="FreqAI model class"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Check schedule but don't actually retrain"
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force retraining regardless of schedule"
    )
    
    args = parser.parse_args()
    
    decisions_path = Path(args.decisions)
    decision = read_last_decision(decisions_path)
    
    if not decision:
        print("ℹ️  No governance decisions found. Run governance_decider first.")
        sys.exit(0)
    
    status = decision.get("status", "unknown")
    print(f"📊 Last governance status: {status}")
    
    if args.force:
        print("⚠️  Force mode: triggering retrain immediately")
        success = trigger_retrain(
            strategy=args.strategy,
            config=args.config,
            freqai_model=args.freqai_model,
            dry_run=args.dry_run,
        )
        sys.exit(0 if success else 1)
    
    should, reason = should_retrain(decision)
    print(f"🔍 Retrain check: {reason}")
    
    if should:
        print("✅ Retraining condition met")
        success = trigger_retrain(
            strategy=args.strategy,
            config=args.config,
            freqai_model=args.freqai_model,
            dry_run=args.dry_run,
        )
        sys.exit(0 if success else 1)
    else:
        print("ℹ️  No retraining needed at this time")
        sys.exit(0)


if __name__ == "__main__":
    main()

"""
Signal Audit Diagnostics

This module provides comprehensive logging and analysis of the trading signal
gating funnel to understand why trades are being rejected at each stage.

The gating funnel includes:
1. do_predict (FreqAI model readiness)
2. DI_values (Dissimilarity Index - data drift detection)
3. Volume regime (healthy volume check)
4. Market regime (trend/volatility state)
5. Z-score threshold crossing
6. Quantile outlier detection
7. Governance decisions (risk management overrides)

Author: Strategy Team
Version: 1.0.0
Created: October 2025
"""

import logging
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field, asdict

logger = logging.getLogger(__name__)


@dataclass
class SignalAuditConfig:
    """Configuration for signal audit diagnostics"""
    # Output paths
    output_dir: Path = field(default_factory=lambda: Path("user_data/diagnostics"))
    csv_filename: str = "signal_audit.csv"
    
    # Logging frequency
    log_every_n_candles: int = 100  # Log summary every N candles
    
    # Thresholds for alerts
    alert_if_rejection_rate_above: float = 95.0  # Alert if >95% trades rejected
    alert_if_no_trades_for_n_candles: int = 1000  # Alert if no trades in 1000 candles


@dataclass
class GatingStats:
    """Statistics for one stage of the gating funnel"""
    stage_name: str
    passed_count: int = 0
    failed_count: int = 0
    rejection_rate_pct: float = 0.0
    
    def update(self, passed: bool):
        """Update statistics with new result"""
        if passed:
            self.passed_count += 1
        else:
            self.failed_count += 1
        
        total = self.passed_count + self.failed_count
        if total > 0:
            self.rejection_rate_pct = (self.failed_count / total) * 100


@dataclass
class SignalAuditRecord:
    """Record for one candle's signal audit"""
    timestamp: datetime
    pair: str
    
    # Gating funnel stages (True = passed, False = rejected)
    do_predict: bool
    di_ok: bool
    vol_ok: bool
    regime_ok: bool
    trend_strength_ok: bool
    z_score_signal: bool
    quantile_ok: bool
    governance_ok: bool
    
    # Values for diagnostics
    di_value: float = 0.0
    volume_regime: float = 0.0
    market_regime: int = 0
    trend_strength: float = 0.0
    z_score: float = 0.0
    quantile: float = 0.0
    governance_status: str = "none"
    governance_risk_multiplier: float = 1.0
    
    # Final decision
    enter_long: bool = False
    enter_short: bool = False
    
    # Rejection reason (first stage that rejected)
    rejection_stage: Optional[str] = None
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for CSV export"""
        return asdict(self)


class SignalAuditLogger:
    """
    Logger for trading signal gating funnel.
    
    Tracks each stage of the gating process to diagnose why trades
    are not being executed.
    
    Usage:
        audit = SignalAuditLogger()
        
        # In strategy's populate_entry_trend:
        for idx, row in dataframe.iterrows():
            record = SignalAuditRecord(
                timestamp=row.name,
                pair=metadata['pair'],
                do_predict=(row.get('do_predict', 0) == 1),
                di_ok=(row.get('DI_values', 1.0) < di_threshold),
                # ... other fields
            )
            audit.log_record(record)
        
        # Export to CSV
        audit.export_to_csv()
        
        # Get summary report
        report = audit.get_summary_report()
    """
    
    def __init__(self, config: Optional[SignalAuditConfig] = None):
        """
        Initialize signal audit logger.
        
        Args:
            config: Configuration (uses defaults if None)
        """
        self.config = config or SignalAuditConfig()
        self.config.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Storage for records
        self.records: List[SignalAuditRecord] = []
        
        # Statistics per stage
        self.stage_stats: Dict[str, GatingStats] = {
            'do_predict': GatingStats('do_predict'),
            'di_ok': GatingStats('DI check'),
            'vol_ok': GatingStats('Volume regime'),
            'regime_ok': GatingStats('Market regime'),
            'trend_strength_ok': GatingStats('Trend strength'),
            'z_score_signal': GatingStats('Z-score signal'),
            'quantile_ok': GatingStats('Quantile filter'),
            'governance_ok': GatingStats('Governance'),
        }
        
        # Counters
        self.total_candles_processed = 0
        self.total_trades_entered = 0
        self.candles_since_last_trade = 0
        
        logger.info(f"SignalAuditLogger initialized: {self.config.output_dir}")
    
    def log_record(self, record: SignalAuditRecord) -> None:
        """
        Log a signal audit record.
        
        Args:
            record: SignalAuditRecord with gating funnel results
        """
        # Determine rejection stage (first stage that failed)
        if not record.do_predict:
            record.rejection_stage = "do_predict"
        elif not record.di_ok:
            record.rejection_stage = "DI_check"
        elif not record.vol_ok:
            record.rejection_stage = "volume_regime"
        elif not record.regime_ok:
            record.rejection_stage = "market_regime"
        elif not record.trend_strength_ok:
            record.rejection_stage = "trend_strength"
        elif not record.z_score_signal:
            record.rejection_stage = "z_score_signal"
        elif not record.quantile_ok:
            record.rejection_stage = "quantile_filter"
        elif not record.governance_ok:
            record.rejection_stage = "governance"
        else:
            record.rejection_stage = None  # Passed all gates
        
        # Store record
        self.records.append(record)
        
        # Update statistics
        self.stage_stats['do_predict'].update(record.do_predict)
        self.stage_stats['di_ok'].update(record.di_ok)
        self.stage_stats['vol_ok'].update(record.vol_ok)
        self.stage_stats['regime_ok'].update(record.regime_ok)
        self.stage_stats['trend_strength_ok'].update(record.trend_strength_ok)
        self.stage_stats['z_score_signal'].update(record.z_score_signal)
        self.stage_stats['quantile_ok'].update(record.quantile_ok)
        self.stage_stats['governance_ok'].update(record.governance_ok)
        
        # Update counters
        self.total_candles_processed += 1
        
        if record.enter_long or record.enter_short:
            self.total_trades_entered += 1
            self.candles_since_last_trade = 0
        else:
            self.candles_since_last_trade += 1
        
        # Periodic logging
        if self.total_candles_processed % self.config.log_every_n_candles == 0:
            self._log_periodic_summary()
        
        # Alerts
        self._check_alerts()
    
    def _log_periodic_summary(self) -> None:
        """Log periodic summary of gating statistics"""
        logger.info(
            f"\n"
            f"=== Signal Audit Summary (after {self.total_candles_processed} candles) ===\n"
            f"Total trades entered: {self.total_trades_entered}\n"
            f"Candles since last trade: {self.candles_since_last_trade}\n"
            f"\n"
            f"Gating Funnel Rejection Rates:\n"
        )
        
        for stage_name, stats in self.stage_stats.items():
            logger.info(
                f"  {stats.stage_name:20s}: "
                f"Passed={stats.passed_count:6d}, "
                f"Failed={stats.failed_count:6d}, "
                f"Rejection={stats.rejection_rate_pct:5.1f}%"
            )
    
    def _check_alerts(self) -> None:
        """Check for alerting conditions"""
        # Alert if overall rejection rate is very high
        if self.total_candles_processed > 100:  # Only after enough samples
            overall_rejection_rate = (
                (self.total_candles_processed - self.total_trades_entered) 
                / self.total_candles_processed * 100
            )
            
            if overall_rejection_rate > self.config.alert_if_rejection_rate_above:
                logger.warning(
                    f"⚠️  ALERT: High rejection rate {overall_rejection_rate:.1f}% "
                    f"(threshold: {self.config.alert_if_rejection_rate_above}%)"
                )
        
        # Alert if no trades for extended period
        if self.candles_since_last_trade >= self.config.alert_if_no_trades_for_n_candles:
            logger.warning(
                f"⚠️  ALERT: No trades for {self.candles_since_last_trade} candles "
                f"(threshold: {self.config.alert_if_no_trades_for_n_candles})"
            )
            
            # Log which stage is causing most rejections
            worst_stage = max(
                self.stage_stats.items(),
                key=lambda x: x[1].rejection_rate_pct
            )
            logger.warning(
                f"   Worst rejection stage: {worst_stage[1].stage_name} "
                f"({worst_stage[1].rejection_rate_pct:.1f}% rejection rate)"
            )
    
    def export_to_csv(self, filename: Optional[str] = None) -> Path:
        """
        Export all records to CSV file.
        
        Args:
            filename: Optional custom filename (uses config default if None)
            
        Returns:
            Path to exported CSV file
        """
        if not self.records:
            logger.warning("No records to export")
            return None
        
        filename = filename or self.config.csv_filename
        output_path = self.config.output_dir / filename
        
        # Convert records to DataFrame
        df = pd.DataFrame([r.to_dict() for r in self.records])
        
        # Export to CSV
        df.to_csv(output_path, index=False)
        
        logger.info(f"Exported {len(self.records)} records to {output_path}")
        
        return output_path
    
    def get_summary_report(self) -> Dict:
        """
        Generate summary report of gating funnel performance.
        
        Returns:
            Dictionary with summary statistics
        """
        if not self.records:
            return {}
        
        # Overall stats
        total = self.total_candles_processed
        trades = self.total_trades_entered
        rejection_rate = ((total - trades) / total * 100) if total > 0 else 0
        
        # Stage-by-stage stats
        stage_summary = {}
        for stage_name, stats in self.stage_stats.items():
            stage_summary[stage_name] = {
                'passed': stats.passed_count,
                'failed': stats.failed_count,
                'rejection_rate_pct': stats.rejection_rate_pct,
            }
        
        # Rejection reasons distribution
        rejection_counts = {}
        for record in self.records:
            if record.rejection_stage:
                rejection_counts[record.rejection_stage] = \
                    rejection_counts.get(record.rejection_stage, 0) + 1
        
        # Sort by count
        top_rejection_reasons = sorted(
            rejection_counts.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        report = {
            'total_candles_processed': total,
            'total_trades_entered': trades,
            'overall_rejection_rate_pct': rejection_rate,
            'trades_per_1000_candles': (trades / total * 1000) if total > 0 else 0,
            'stage_summary': stage_summary,
            'top_rejection_reasons': top_rejection_reasons,
            'candles_since_last_trade': self.candles_since_last_trade,
        }
        
        return report
    
    def print_detailed_report(self) -> None:
        """Print detailed diagnostic report to console"""
        report = self.get_summary_report()
        
        if not report:
            print("No data to report")
            return
        
        print("\n" + "="*80)
        print("SIGNAL AUDIT DIAGNOSTIC REPORT")
        print("="*80)
        
        print(f"\n📊 Overall Statistics:")
        print(f"  Total candles processed: {report['total_candles_processed']:,}")
        print(f"  Total trades entered: {report['total_trades_entered']}")
        print(f"  Overall rejection rate: {report['overall_rejection_rate_pct']:.1f}%")
        print(f"  Trades per 1000 candles: {report['trades_per_1000_candles']:.1f}")
        print(f"  Candles since last trade: {report['candles_since_last_trade']}")
        
        print(f"\n🔍 Gating Funnel Rejection Rates:")
        print(f"  {'Stage':<25s} {'Passed':>10s} {'Failed':>10s} {'Rejection %':>12s}")
        print(f"  {'-'*60}")
        
        for stage_name, stats in report['stage_summary'].items():
            print(
                f"  {stage_name:<25s} "
                f"{stats['passed']:>10,d} "
                f"{stats['failed']:>10,d} "
                f"{stats['rejection_rate_pct']:>11.1f}%"
            )
        
        print(f"\n🚫 Top Rejection Reasons:")
        for reason, count in report['top_rejection_reasons'][:5]:
            pct = (count / report['total_candles_processed'] * 100)
            print(f"  {reason:30s}: {count:6,d} ({pct:5.1f}%)")
        
        # Recommendations
        print(f"\n💡 Recommendations:")
        
        # Find stages with >90% rejection
        high_rejection_stages = [
            (name, stats['rejection_rate_pct'])
            for name, stats in report['stage_summary'].items()
            if stats['rejection_rate_pct'] > 90.0
        ]
        
        if high_rejection_stages:
            print(f"\n  ⚠️  High rejection stages (>90%):")
            for stage, rate in high_rejection_stages:
                print(f"    - {stage}: {rate:.1f}%")
                
                # Stage-specific recommendations
                if stage == 'do_predict':
                    print(f"      → Check FreqAI model training status")
                    print(f"      → Verify sufficient training data")
                elif stage == 'di_ok':
                    print(f"      → DI threshold may be too strict")
                    print(f"      → Consider relaxing buy_di_threshold parameter")
                elif stage == 'vol_ok':
                    print(f"      → Volume regime filter may be too restrictive")
                    print(f"      → Review vol_min and vol_max parameters")
                elif stage == 'regime_ok':
                    print(f"      → Market regime filter rejecting too many setups")
                    print(f"      → Consider allowing more regime types")
                elif stage == 'governance_ok':
                    print(f"      → Governance system is halting entries")
                    print(f"      → Check governance_decisions.jsonl for reasons")
        
        if report['overall_rejection_rate_pct'] > 95.0:
            print(f"\n  🔴 CRITICAL: >95% rejection rate!")
            print(f"     Strategy is barely trading. Review all filters.")
        elif report['overall_rejection_rate_pct'] > 80.0:
            print(f"\n  🟡 WARNING: >80% rejection rate")
            print(f"     Consider relaxing some filters for more opportunities")
        else:
            print(f"\n  ✅ Rejection rate is reasonable")
        
        print("\n" + "="*80 + "\n")


def create_sample_audit_data() -> pd.DataFrame:
    """Create sample audit data for testing visualization"""
    dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='5min')
    
    records = []
    for timestamp in dates:
        # Simulate gating funnel with realistic rejection rates
        do_predict = np.random.random() > 0.3  # 70% pass
        di_ok = np.random.random() > 0.5 if do_predict else False  # 50% pass if do_predict
        vol_ok = np.random.random() > 0.4 if di_ok else False  # 60% pass if DI ok
        regime_ok = np.random.random() > 0.6 if vol_ok else False  # 40% pass if vol ok
        trend_ok = np.random.random() > 0.5 if regime_ok else False  # 50% pass
        z_signal = np.random.random() > 0.8 if trend_ok else False  # 20% pass
        quantile_ok = np.random.random() > 0.3 if z_signal else False  # 70% pass
        governance_ok = np.random.random() > 0.1 if quantile_ok else False  # 90% pass
        
        enter_long = governance_ok and np.random.random() > 0.5
        
        record = SignalAuditRecord(
            timestamp=timestamp,
            pair="BTC/USDT:USDT",
            do_predict=do_predict,
            di_ok=di_ok,
            vol_ok=vol_ok,
            regime_ok=regime_ok,
            trend_strength_ok=trend_ok,
            z_score_signal=z_signal,
            quantile_ok=quantile_ok,
            governance_ok=governance_ok,
            di_value=np.random.uniform(0, 2),
            volume_regime=np.random.uniform(0.5, 3.0),
            market_regime=np.random.choice([0, 1, 2, 3]),
            z_score=np.random.randn(),
            enter_long=enter_long,
        )
        
        records.append(record.to_dict())
    
    return pd.DataFrame(records)


if __name__ == "__main__":
    # Example usage
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Create audit logger
    audit = SignalAuditLogger()
    
    # Generate sample data
    logger.info("Generating sample audit data...")
    sample_df = create_sample_audit_data()
    
    # Log records
    for _, row in sample_df.iterrows():
        record = SignalAuditRecord(**{k: v for k, v in row.items() if k in SignalAuditRecord.__annotations__})
        audit.log_record(record)
    
    # Export to CSV
    csv_path = audit.export_to_csv()
    logger.info(f"CSV exported to: {csv_path}")
    
    # Print detailed report
    audit.print_detailed_report()

"""
Evaluation Protocol for RL Strategy Development

This module provides a comprehensive evaluation framework for validating
trading strategies with fixed risk constraints and proper time-series
cross-validation to prevent data leakage.

Author: Strategy Team
Version: 1.0.0
Created: October 2025
"""

import logging
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from pathlib import Path

logger = logging.getLogger(__name__)


@dataclass
class RiskConstraints:
    """Fixed risk constraints for all evaluations"""
    max_drawdown_pct: float = 20.0  # Maximum drawdown threshold
    min_sharpe_ratio: float = 0.5   # Minimum acceptable Sharpe
    max_leverage: int = 10          # Maximum leverage allowed
    max_position_pct: float = 30.0  # Max position size as % of capital
    max_daily_loss_pct: float = 5.0 # Daily loss circuit breaker
    min_win_rate_pct: float = 30.0  # Minimum win rate threshold
    
    def validate(self, metrics: Dict[str, float]) -> Tuple[bool, List[str]]:
        """
        Validate metrics against risk constraints.
        
        Args:
            metrics: Dictionary of performance metrics
            
        Returns:
            Tuple of (is_valid, list_of_violations)
        """
        violations = []
        
        if metrics.get('max_drawdown_pct', 0) > self.max_drawdown_pct:
            violations.append(
                f"Max drawdown {metrics['max_drawdown_pct']:.2f}% exceeds limit {self.max_drawdown_pct}%"
            )
        
        if metrics.get('sharpe_ratio', 0) < self.min_sharpe_ratio:
            violations.append(
                f"Sharpe ratio {metrics['sharpe_ratio']:.2f} below minimum {self.min_sharpe_ratio}"
            )
        
        if metrics.get('win_rate_pct', 0) < self.min_win_rate_pct:
            violations.append(
                f"Win rate {metrics['win_rate_pct']:.2f}% below minimum {self.min_win_rate_pct}%"
            )
        
        return len(violations) == 0, violations


@dataclass
class EvaluationConfig:
    """Configuration for evaluation protocol"""
    # Walk-forward settings
    train_window_days: int = 90        # 3 months training
    test_window_days: int = 30         # 1 month testing
    step_size_days: int = 30           # Roll forward by 1 month
    
    # Time-series CV settings
    n_splits: int = 5                   # Number of CV folds
    
    # Out-of-sample holdout
    oos_holdout_pct: float = 20.0      # Reserve 20% for final test
    
    # Risk constraints
    risk_constraints: RiskConstraints = field(default_factory=RiskConstraints)
    
    # Evaluation settings
    initial_capital: float = 10000.0
    transaction_cost_pct: float = 0.1  # 10 bps per trade
    slippage_pct: float = 0.05         # 5 bps slippage
    
    # Results directory
    results_dir: Path = field(default_factory=lambda: Path("user_data/evaluation"))


@dataclass
class WalkForwardResult:
    """Results from one walk-forward window"""
    window_id: int
    train_start: datetime
    train_end: datetime
    test_start: datetime
    test_end: datetime
    
    # Training metrics
    train_trades: int = 0
    train_pnl: float = 0.0
    train_sharpe: float = 0.0
    train_mdd_pct: float = 0.0
    
    # Test metrics
    test_trades: int = 0
    test_pnl: float = 0.0
    test_sharpe: float = 0.0
    test_mdd_pct: float = 0.0
    test_win_rate_pct: float = 0.0
    
    # Risk validation
    passed_constraints: bool = False
    constraint_violations: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for reporting"""
        return {
            'window_id': self.window_id,
            'train_start': self.train_start.isoformat(),
            'train_end': self.train_end.isoformat(),
            'test_start': self.test_start.isoformat(),
            'test_end': self.test_end.isoformat(),
            'train_trades': self.train_trades,
            'train_pnl': self.train_pnl,
            'train_sharpe': self.train_sharpe,
            'train_mdd_pct': self.train_mdd_pct,
            'test_trades': self.test_trades,
            'test_pnl': self.test_pnl,
            'test_sharpe': self.test_sharpe,
            'test_mdd_pct': self.test_mdd_pct,
            'test_win_rate_pct': self.test_win_rate_pct,
            'passed_constraints': self.passed_constraints,
            'constraint_violations': self.constraint_violations,
        }


class EvaluationProtocol:
    """
    Comprehensive evaluation protocol for RL strategy development.
    
    Implements:
    1. Walk-forward validation (train on historical, test on unseen future)
    2. Time-series cross-validation (multiple train/test splits)
    3. Out-of-sample holdout (final blind test)
    4. Fixed risk constraints (prevent overfitting to metrics)
    
    Usage:
        config = EvaluationConfig()
        protocol = EvaluationProtocol(config)
        
        # Walk-forward validation
        wf_results = protocol.walk_forward_validation(backtest_data)
        
        # Time-series CV
        cv_results = protocol.time_series_cv(backtest_data)
        
        # Final OOS test
        oos_results = protocol.out_of_sample_test(backtest_data)
    """
    
    def __init__(self, config: Optional[EvaluationConfig] = None):
        """
        Initialize evaluation protocol.
        
        Args:
            config: Evaluation configuration (uses defaults if None)
        """
        self.config = config or EvaluationConfig()
        self.config.results_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"Evaluation protocol initialized with config: {self.config}")
    
    def walk_forward_validation(
        self,
        data: pd.DataFrame,
        strategy_fn: Any,  # Function that takes data and returns trades
    ) -> List[WalkForwardResult]:
        """
        Perform walk-forward validation.
        
        Args:
            data: Full dataset with OHLCV and features
            strategy_fn: Callable that takes data slice and returns trade results
            
        Returns:
            List of WalkForwardResult objects
        """
        logger.info("Starting walk-forward validation")
        
        results = []
        train_window = timedelta(days=self.config.train_window_days)
        test_window = timedelta(days=self.config.test_window_days)
        step_size = timedelta(days=self.config.step_size_days)
        
        # Ensure data has datetime index
        if not isinstance(data.index, pd.DatetimeIndex):
            raise ValueError("Data must have DatetimeIndex")
        
        start_date = data.index[0]
        end_date = data.index[-1]
        
        window_id = 1
        current_start = start_date
        
        while current_start + train_window + test_window <= end_date:
            train_end = current_start + train_window
            test_start = train_end
            test_end = test_start + test_window
            
            logger.info(
                f"Window {window_id}: "
                f"Train [{current_start.date()} to {train_end.date()}], "
                f"Test [{test_start.date()} to {test_end.date()}]"
            )
            
            # Split data
            train_data = data[current_start:train_end]
            test_data = data[test_start:test_end]
            
            # Run strategy on train period
            train_metrics = strategy_fn(train_data, is_training=True)
            
            # Run strategy on test period
            test_metrics = strategy_fn(test_data, is_training=False)
            
            # Validate against risk constraints
            passed, violations = self.config.risk_constraints.validate(test_metrics)
            
            result = WalkForwardResult(
                window_id=window_id,
                train_start=current_start,
                train_end=train_end,
                test_start=test_start,
                test_end=test_end,
                train_trades=train_metrics.get('num_trades', 0),
                train_pnl=train_metrics.get('total_pnl', 0.0),
                train_sharpe=train_metrics.get('sharpe_ratio', 0.0),
                train_mdd_pct=train_metrics.get('max_drawdown_pct', 0.0),
                test_trades=test_metrics.get('num_trades', 0),
                test_pnl=test_metrics.get('total_pnl', 0.0),
                test_sharpe=test_metrics.get('sharpe_ratio', 0.0),
                test_mdd_pct=test_metrics.get('max_drawdown_pct', 0.0),
                test_win_rate_pct=test_metrics.get('win_rate_pct', 0.0),
                passed_constraints=passed,
                constraint_violations=violations,
            )
            
            results.append(result)
            
            # Move window forward
            current_start += step_size
            window_id += 1
        
        logger.info(f"Walk-forward validation complete: {len(results)} windows evaluated")
        self._save_results(results, "walk_forward_results.csv")
        
        return results
    
    def time_series_cv(
        self,
        data: pd.DataFrame,
        strategy_fn: Any,
    ) -> List[WalkForwardResult]:
        """
        Perform time-series cross-validation.
        
        Similar to walk-forward but with overlapping folds for more robust
        evaluation of model stability.
        
        Args:
            data: Full dataset
            strategy_fn: Strategy function
            
        Returns:
            List of CV results
        """
        logger.info(f"Starting time-series CV with {self.config.n_splits} splits")
        
        results = []
        total_days = (data.index[-1] - data.index[0]).days
        fold_size_days = total_days // (self.config.n_splits + 1)
        
        for fold_id in range(1, self.config.n_splits + 1):
            train_end_days = fold_id * fold_size_days
            test_end_days = (fold_id + 1) * fold_size_days
            
            train_start = data.index[0]
            train_end = train_start + timedelta(days=train_end_days)
            test_start = train_end
            test_end = train_start + timedelta(days=test_end_days)
            
            logger.info(
                f"Fold {fold_id}/{self.config.n_splits}: "
                f"Train [{train_start.date()} to {train_end.date()}], "
                f"Test [{test_start.date()} to {test_end.date()}]"
            )
            
            train_data = data[train_start:train_end]
            test_data = data[test_start:test_end]
            
            train_metrics = strategy_fn(train_data, is_training=True)
            test_metrics = strategy_fn(test_data, is_training=False)
            
            passed, violations = self.config.risk_constraints.validate(test_metrics)
            
            result = WalkForwardResult(
                window_id=fold_id,
                train_start=train_start,
                train_end=train_end,
                test_start=test_start,
                test_end=test_end,
                train_trades=train_metrics.get('num_trades', 0),
                train_pnl=train_metrics.get('total_pnl', 0.0),
                train_sharpe=train_metrics.get('sharpe_ratio', 0.0),
                train_mdd_pct=train_metrics.get('max_drawdown_pct', 0.0),
                test_trades=test_metrics.get('num_trades', 0),
                test_pnl=test_metrics.get('total_pnl', 0.0),
                test_sharpe=test_metrics.get('sharpe_ratio', 0.0),
                test_mdd_pct=test_metrics.get('max_drawdown_pct', 0.0),
                test_win_rate_pct=test_metrics.get('win_rate_pct', 0.0),
                passed_constraints=passed,
                constraint_violations=violations,
            )
            
            results.append(result)
        
        logger.info(f"Time-series CV complete: {self.config.n_splits} folds evaluated")
        self._save_results(results, "time_series_cv_results.csv")
        
        return results
    
    def out_of_sample_test(
        self,
        data: pd.DataFrame,
        strategy_fn: Any,
    ) -> WalkForwardResult:
        """
        Perform final out-of-sample test on held-out data.
        
        This is the "final exam" - strategy should never see this data
        during development or hyperparameter tuning.
        
        Args:
            data: Full dataset
            strategy_fn: Strategy function
            
        Returns:
            Single result for OOS period
        """
        logger.info(f"Starting out-of-sample test (holdout: {self.config.oos_holdout_pct}%)")
        
        # Split into in-sample and out-of-sample
        split_idx = int(len(data) * (1 - self.config.oos_holdout_pct / 100))
        
        in_sample_data = data.iloc[:split_idx]
        oos_data = data.iloc[split_idx:]
        
        logger.info(
            f"In-sample: [{in_sample_data.index[0].date()} to {in_sample_data.index[-1].date()}]"
        )
        logger.info(
            f"Out-of-sample: [{oos_data.index[0].date()} to {oos_data.index[-1].date()}]"
        )
        
        # Train on in-sample
        train_metrics = strategy_fn(in_sample_data, is_training=True)
        
        # Test on OOS (this is the critical metric)
        oos_metrics = strategy_fn(oos_data, is_training=False)
        
        # Validate
        passed, violations = self.config.risk_constraints.validate(oos_metrics)
        
        result = WalkForwardResult(
            window_id=0,  # Special ID for OOS
            train_start=in_sample_data.index[0],
            train_end=in_sample_data.index[-1],
            test_start=oos_data.index[0],
            test_end=oos_data.index[-1],
            train_trades=train_metrics.get('num_trades', 0),
            train_pnl=train_metrics.get('total_pnl', 0.0),
            train_sharpe=train_metrics.get('sharpe_ratio', 0.0),
            train_mdd_pct=train_metrics.get('max_drawdown_pct', 0.0),
            test_trades=oos_metrics.get('num_trades', 0),
            test_pnl=oos_metrics.get('total_pnl', 0.0),
            test_sharpe=oos_metrics.get('sharpe_ratio', 0.0),
            test_mdd_pct=oos_metrics.get('max_drawdown_pct', 0.0),
            test_win_rate_pct=oos_metrics.get('win_rate_pct', 0.0),
            passed_constraints=passed,
            constraint_violations=violations,
        )
        
        logger.info(
            f"Out-of-sample test complete: "
            f"Sharpe={result.test_sharpe:.2f}, "
            f"MDD={result.test_mdd_pct:.2f}%, "
            f"Passed={result.passed_constraints}"
        )
        
        self._save_results([result], "oos_test_result.csv")
        
        return result
    
    def _save_results(self, results: List[WalkForwardResult], filename: str) -> None:
        """Save results to CSV"""
        df = pd.DataFrame([r.to_dict() for r in results])
        output_path = self.config.results_dir / filename
        df.to_csv(output_path, index=False)
        logger.info(f"Results saved to {output_path}")
    
    def generate_report(self, results: List[WalkForwardResult]) -> Dict[str, Any]:
        """
        Generate summary report from evaluation results.
        
        Args:
            results: List of evaluation results
            
        Returns:
            Dictionary with summary statistics
        """
        if not results:
            return {}
        
        test_sharpes = [r.test_sharpe for r in results]
        test_mdds = [r.test_mdd_pct for r in results]
        test_win_rates = [r.test_win_rate_pct for r in results]
        passed_count = sum(1 for r in results if r.passed_constraints)
        
        report = {
            'num_windows': len(results),
            'avg_test_sharpe': np.mean(test_sharpes),
            'std_test_sharpe': np.std(test_sharpes),
            'avg_test_mdd_pct': np.mean(test_mdds),
            'max_test_mdd_pct': np.max(test_mdds),
            'avg_test_win_rate_pct': np.mean(test_win_rates),
            'passed_constraints_pct': (passed_count / len(results)) * 100,
            'passed_count': passed_count,
            'failed_count': len(results) - passed_count,
        }
        
        logger.info(f"Evaluation Report: {report}")
        
        return report


def example_usage():
    """Example usage of evaluation protocol"""
    # Configure evaluation
    config = EvaluationConfig(
        train_window_days=90,
        test_window_days=30,
        n_splits=5,
        oos_holdout_pct=20.0,
    )
    
    # Initialize protocol
    protocol = EvaluationProtocol(config)
    
    # Load your backtest data
    # data = pd.read_parquet("user_data/backtest_data.parquet")
    
    # Define strategy function
    def strategy_fn(data, is_training=True):
        """
        Your strategy implementation.
        Should return dict with metrics: num_trades, total_pnl, sharpe_ratio, etc.
        """
        # This is where you'd run your strategy/model
        return {
            'num_trades': 100,
            'total_pnl': 1500.0,
            'sharpe_ratio': 1.2,
            'max_drawdown_pct': 15.0,
            'win_rate_pct': 55.0,
        }
    
    # Run evaluations
    # wf_results = protocol.walk_forward_validation(data, strategy_fn)
    # cv_results = protocol.time_series_cv(data, strategy_fn)
    # oos_result = protocol.out_of_sample_test(data, strategy_fn)
    
    # Generate reports
    # wf_report = protocol.generate_report(wf_results)
    # cv_report = protocol.generate_report(cv_results)
    
    logger.info("Evaluation complete!")


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    example_usage()

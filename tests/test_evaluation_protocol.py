"""
Unit tests for evaluation protocol.

Tests cover:
- Risk constraints validation
- Walk-forward validation logic
- Time-series CV splits
- Out-of-sample holdout
- Report generation
"""

import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path
import tempfile

from src.evaluation_protocol import (
    RiskConstraints,
    EvaluationConfig,
    EvaluationProtocol,
    WalkForwardResult,
)


@pytest.fixture
def sample_data():
    """Create sample time-series data for testing"""
    dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='1h')
    data = pd.DataFrame({
        'open': np.random.randn(len(dates)).cumsum() + 100,
        'high': np.random.randn(len(dates)).cumsum() + 101,
        'low': np.random.randn(len(dates)).cumsum() + 99,
        'close': np.random.randn(len(dates)).cumsum() + 100,
        'volume': np.random.randint(1000, 10000, len(dates)),
    }, index=dates)
    return data


@pytest.fixture
def mock_strategy_good():
    """Mock strategy that passes risk constraints"""
    def strategy_fn(data, is_training=True):
        return {
            'num_trades': 100,
            'total_pnl': 1500.0,
            'sharpe_ratio': 1.2,
            'max_drawdown_pct': 15.0,
            'win_rate_pct': 55.0,
        }
    return strategy_fn


@pytest.fixture
def mock_strategy_bad():
    """Mock strategy that fails risk constraints"""
    def strategy_fn(data, is_training=True):
        return {
            'num_trades': 50,
            'total_pnl': -500.0,
            'sharpe_ratio': 0.2,
            'max_drawdown_pct': 35.0,
            'win_rate_pct': 25.0,
        }
    return strategy_fn


@pytest.fixture
def temp_results_dir():
    """Create temporary directory for test results"""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


class TestRiskConstraints:
    """Test risk constraints validation"""
    
    def test_default_constraints(self):
        """Test default risk constraints"""
        constraints = RiskConstraints()
        assert constraints.max_drawdown_pct == 20.0
        assert constraints.min_sharpe_ratio == 0.5
        assert constraints.max_leverage == 10
    
    def test_custom_constraints(self):
        """Test custom risk constraints"""
        constraints = RiskConstraints(
            max_drawdown_pct=10.0,
            min_sharpe_ratio=1.0,
            max_leverage=5,
        )
        assert constraints.max_drawdown_pct == 10.0
        assert constraints.min_sharpe_ratio == 1.0
        assert constraints.max_leverage == 5
    
    def test_validation_pass(self):
        """Test validation with metrics that pass constraints"""
        constraints = RiskConstraints()
        metrics = {
            'sharpe_ratio': 1.5,
            'max_drawdown_pct': 15.0,
            'win_rate_pct': 55.0,
        }
        
        passed, violations = constraints.validate(metrics)
        assert passed is True
        assert len(violations) == 0
    
    def test_validation_fail_drawdown(self):
        """Test validation fails on excessive drawdown"""
        constraints = RiskConstraints()
        metrics = {
            'sharpe_ratio': 1.5,
            'max_drawdown_pct': 25.0,  # Exceeds 20% limit
            'win_rate_pct': 55.0,
        }
        
        passed, violations = constraints.validate(metrics)
        assert passed is False
        assert len(violations) == 1
        assert "Max drawdown" in violations[0]
    
    def test_validation_fail_sharpe(self):
        """Test validation fails on low Sharpe ratio"""
        constraints = RiskConstraints()
        metrics = {
            'sharpe_ratio': 0.3,  # Below 0.5 minimum
            'max_drawdown_pct': 15.0,
            'win_rate_pct': 55.0,
        }
        
        passed, violations = constraints.validate(metrics)
        assert passed is False
        assert len(violations) == 1
        assert "Sharpe ratio" in violations[0]
    
    def test_validation_fail_win_rate(self):
        """Test validation fails on low win rate"""
        constraints = RiskConstraints()
        metrics = {
            'sharpe_ratio': 1.5,
            'max_drawdown_pct': 15.0,
            'win_rate_pct': 25.0,  # Below 30% minimum
        }
        
        passed, violations = constraints.validate(metrics)
        assert passed is False
        assert len(violations) == 1
        assert "Win rate" in violations[0]
    
    def test_validation_multiple_failures(self):
        """Test validation with multiple constraint violations"""
        constraints = RiskConstraints()
        metrics = {
            'sharpe_ratio': 0.2,     # Too low
            'max_drawdown_pct': 30.0, # Too high
            'win_rate_pct': 20.0,    # Too low
        }
        
        passed, violations = constraints.validate(metrics)
        assert passed is False
        assert len(violations) == 3


class TestEvaluationConfig:
    """Test evaluation configuration"""
    
    def test_default_config(self):
        """Test default configuration"""
        config = EvaluationConfig()
        assert config.train_window_days == 90
        assert config.test_window_days == 30
        assert config.n_splits == 5
        assert config.oos_holdout_pct == 20.0
    
    def test_custom_config(self):
        """Test custom configuration"""
        config = EvaluationConfig(
            train_window_days=60,
            test_window_days=20,
            n_splits=3,
        )
        assert config.train_window_days == 60
        assert config.test_window_days == 20
        assert config.n_splits == 3


class TestWalkForwardResult:
    """Test walk-forward result dataclass"""
    
    def test_create_result(self):
        """Test creating walk-forward result"""
        result = WalkForwardResult(
            window_id=1,
            train_start=datetime(2023, 1, 1),
            train_end=datetime(2023, 3, 31),
            test_start=datetime(2023, 4, 1),
            test_end=datetime(2023, 4, 30),
            test_sharpe=1.5,
            test_mdd_pct=12.0,
            passed_constraints=True,
        )
        
        assert result.window_id == 1
        assert result.test_sharpe == 1.5
        assert result.passed_constraints is True
    
    def test_to_dict(self):
        """Test converting result to dictionary"""
        result = WalkForwardResult(
            window_id=1,
            train_start=datetime(2023, 1, 1),
            train_end=datetime(2023, 3, 31),
            test_start=datetime(2023, 4, 1),
            test_end=datetime(2023, 4, 30),
        )
        
        result_dict = result.to_dict()
        assert result_dict['window_id'] == 1
        assert 'train_start' in result_dict
        assert 'test_sharpe' in result_dict


class TestEvaluationProtocol:
    """Test evaluation protocol"""
    
    def test_initialization(self, temp_results_dir):
        """Test protocol initialization"""
        config = EvaluationConfig(results_dir=temp_results_dir)
        protocol = EvaluationProtocol(config)
        
        assert protocol.config.train_window_days == 90
        assert protocol.config.results_dir.exists()
    
    def test_walk_forward_validation(self, sample_data, mock_strategy_good, temp_results_dir):
        """Test walk-forward validation"""
        config = EvaluationConfig(
            train_window_days=30,
            test_window_days=10,
            step_size_days=10,
            results_dir=temp_results_dir,
        )
        protocol = EvaluationProtocol(config)
        
        results = protocol.walk_forward_validation(sample_data, mock_strategy_good)
        
        # Should have multiple windows
        assert len(results) > 0
        
        # Check first result
        first_result = results[0]
        assert first_result.window_id == 1
        assert first_result.test_sharpe > 0
        assert first_result.passed_constraints is True
        
        # Verify CSV was saved
        csv_path = temp_results_dir / "walk_forward_results.csv"
        assert csv_path.exists()
    
    def test_walk_forward_validation_failures(self, sample_data, mock_strategy_bad, temp_results_dir):
        """Test walk-forward validation with failing strategy"""
        config = EvaluationConfig(
            train_window_days=30,
            test_window_days=10,
            step_size_days=10,
            results_dir=temp_results_dir,
        )
        protocol = EvaluationProtocol(config)
        
        results = protocol.walk_forward_validation(sample_data, mock_strategy_bad)
        
        # Should detect constraint violations
        assert any(not r.passed_constraints for r in results)
        assert any(len(r.constraint_violations) > 0 for r in results)
    
    def test_time_series_cv(self, sample_data, mock_strategy_good, temp_results_dir):
        """Test time-series cross-validation"""
        config = EvaluationConfig(
            n_splits=3,
            results_dir=temp_results_dir,
        )
        protocol = EvaluationProtocol(config)
        
        results = protocol.time_series_cv(sample_data, mock_strategy_good)
        
        # Should have n_splits results
        assert len(results) == 3
        
        # Check fold IDs
        fold_ids = [r.window_id for r in results]
        assert fold_ids == [1, 2, 3]
        
        # Verify CSV was saved
        csv_path = temp_results_dir / "time_series_cv_results.csv"
        assert csv_path.exists()
    
    def test_out_of_sample_test(self, sample_data, mock_strategy_good, temp_results_dir):
        """Test out-of-sample holdout test"""
        config = EvaluationConfig(
            oos_holdout_pct=20.0,
            results_dir=temp_results_dir,
        )
        protocol = EvaluationProtocol(config)
        
        result = protocol.out_of_sample_test(sample_data, mock_strategy_good)
        
        # Should have single result with window_id=0
        assert result.window_id == 0
        assert result.test_sharpe > 0
        assert result.passed_constraints is True
        
        # Verify train/test split is correct
        total_length = len(sample_data)
        train_length = len(sample_data[result.train_start:result.train_end])
        test_length = len(sample_data[result.test_start:result.test_end])
        
        # Test should be roughly 20% of total
        assert 0.15 < (test_length / total_length) < 0.25
        
        # Verify CSV was saved
        csv_path = temp_results_dir / "oos_test_result.csv"
        assert csv_path.exists()
    
    def test_generate_report(self):
        """Test report generation"""
        # Create mock results
        results = [
            WalkForwardResult(
                window_id=1,
                train_start=datetime(2023, 1, 1),
                train_end=datetime(2023, 3, 31),
                test_start=datetime(2023, 4, 1),
                test_end=datetime(2023, 4, 30),
                test_sharpe=1.5,
                test_mdd_pct=12.0,
                test_win_rate_pct=55.0,
                passed_constraints=True,
            ),
            WalkForwardResult(
                window_id=2,
                train_start=datetime(2023, 2, 1),
                train_end=datetime(2023, 4, 30),
                test_start=datetime(2023, 5, 1),
                test_end=datetime(2023, 5, 31),
                test_sharpe=1.2,
                test_mdd_pct=15.0,
                test_win_rate_pct=52.0,
                passed_constraints=True,
            ),
        ]
        
        protocol = EvaluationProtocol()
        report = protocol.generate_report(results)
        
        assert report['num_windows'] == 2
        assert 'avg_test_sharpe' in report
        assert 'std_test_sharpe' in report
        assert 'avg_test_mdd_pct' in report
        assert report['passed_constraints_pct'] == 100.0
    
    def test_generate_report_empty(self):
        """Test report generation with empty results"""
        protocol = EvaluationProtocol()
        report = protocol.generate_report([])
        
        assert report == {}
    
    def test_invalid_data_index(self, temp_results_dir):
        """Test error handling for non-datetime index"""
        config = EvaluationConfig(results_dir=temp_results_dir)
        protocol = EvaluationProtocol(config)
        
        # Create data with non-datetime index
        bad_data = pd.DataFrame({
            'close': [100, 101, 102, 103],
        })
        
        def dummy_strategy(data, is_training=True):
            return {'sharpe_ratio': 1.0}
        
        with pytest.raises(ValueError, match="DatetimeIndex"):
            protocol.walk_forward_validation(bad_data, dummy_strategy)


class TestIntegration:
    """Integration tests for complete workflows"""
    
    def test_complete_evaluation_workflow(self, sample_data, mock_strategy_good, temp_results_dir):
        """Test complete evaluation workflow"""
        config = EvaluationConfig(
            train_window_days=30,
            test_window_days=10,
            step_size_days=10,
            n_splits=3,
            oos_holdout_pct=20.0,
            results_dir=temp_results_dir,
        )
        protocol = EvaluationProtocol(config)
        
        # Run all three validation methods
        wf_results = protocol.walk_forward_validation(sample_data, mock_strategy_good)
        cv_results = protocol.time_series_cv(sample_data, mock_strategy_good)
        oos_result = protocol.out_of_sample_test(sample_data, mock_strategy_good)
        
        # Generate reports
        wf_report = protocol.generate_report(wf_results)
        cv_report = protocol.generate_report(cv_results)
        
        # All should succeed
        assert len(wf_results) > 0
        assert len(cv_results) == 3
        assert oos_result.window_id == 0
        
        # Reports should have expected structure
        assert 'avg_test_sharpe' in wf_report
        assert 'avg_test_sharpe' in cv_report
        
        # All results files should exist
        assert (temp_results_dir / "walk_forward_results.csv").exists()
        assert (temp_results_dir / "time_series_cv_results.csv").exists()
        assert (temp_results_dir / "oos_test_result.csv").exists()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

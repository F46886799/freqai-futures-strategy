"""
Unit tests for signal audit diagnostics.
"""

import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path
import tempfile

from diagnostics.signal_audit import (
    SignalAuditLogger,
    SignalAuditConfig,
    SignalAuditRecord,
    GatingStats,
    create_sample_audit_data,
)


@pytest.fixture
def temp_output_dir():
    """Create temporary directory for test outputs"""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def audit_config(temp_output_dir):
    """Create test configuration"""
    return SignalAuditConfig(
        output_dir=temp_output_dir,
        log_every_n_candles=10,
        alert_if_rejection_rate_above=90.0,
        alert_if_no_trades_for_n_candles=50,
    )


@pytest.fixture
def sample_record():
    """Create sample audit record"""
    return SignalAuditRecord(
        timestamp=datetime(2023, 1, 1, 12, 0),
        pair="BTC/USDT:USDT",
        do_predict=True,
        di_ok=True,
        vol_ok=True,
        regime_ok=True,
        trend_strength_ok=True,
        z_score_signal=True,
        quantile_ok=True,
        governance_ok=True,
        di_value=0.5,
        volume_regime=1.5,
        market_regime=1,
        z_score=0.8,
        enter_long=True,
    )


class TestGatingStats:
    """Test gating statistics"""
    
    def test_initialization(self):
        """Test GatingStats initialization"""
        stats = GatingStats("test_stage")
        assert stats.stage_name == "test_stage"
        assert stats.passed_count == 0
        assert stats.failed_count == 0
        assert stats.rejection_rate_pct == 0.0
    
    def test_update_passed(self):
        """Test updating with passed result"""
        stats = GatingStats("test")
        stats.update(True)
        
        assert stats.passed_count == 1
        assert stats.failed_count == 0
        assert stats.rejection_rate_pct == 0.0
    
    def test_update_failed(self):
        """Test updating with failed result"""
        stats = GatingStats("test")
        stats.update(False)
        
        assert stats.passed_count == 0
        assert stats.failed_count == 1
        assert stats.rejection_rate_pct == 100.0
    
    def test_rejection_rate_calculation(self):
        """Test rejection rate calculation"""
        stats = GatingStats("test")
        
        # 7 pass, 3 fail = 30% rejection
        for _ in range(7):
            stats.update(True)
        for _ in range(3):
            stats.update(False)
        
        assert stats.passed_count == 7
        assert stats.failed_count == 3
        assert stats.rejection_rate_pct == 30.0


class TestSignalAuditRecord:
    """Test signal audit record"""
    
    def test_create_record(self, sample_record):
        """Test creating audit record"""
        assert sample_record.pair == "BTC/USDT:USDT"
        assert sample_record.do_predict is True
        assert sample_record.enter_long is True
    
    def test_to_dict(self, sample_record):
        """Test converting record to dictionary"""
        record_dict = sample_record.to_dict()
        
        assert isinstance(record_dict, dict)
        assert record_dict['pair'] == "BTC/USDT:USDT"
        assert record_dict['do_predict'] is True
        assert 'timestamp' in record_dict


class TestSignalAuditLogger:
    """Test signal audit logger"""
    
    def test_initialization(self, audit_config):
        """Test logger initialization"""
        audit = SignalAuditLogger(audit_config)
        
        assert audit.config == audit_config
        assert audit.total_candles_processed == 0
        assert audit.total_trades_entered == 0
        assert len(audit.stage_stats) == 8
    
    def test_log_record_passed(self, audit_config, sample_record):
        """Test logging record that passes all gates"""
        audit = SignalAuditLogger(audit_config)
        audit.log_record(sample_record)
        
        assert audit.total_candles_processed == 1
        assert audit.total_trades_entered == 1
        assert sample_record.rejection_stage is None
        assert len(audit.records) == 1
    
    def test_log_record_rejected_early(self, audit_config):
        """Test logging record rejected at first gate"""
        record = SignalAuditRecord(
            timestamp=datetime(2023, 1, 1),
            pair="BTC/USDT:USDT",
            do_predict=False,  # Rejected here
            di_ok=True,
            vol_ok=True,
            regime_ok=True,
            trend_strength_ok=True,
            z_score_signal=True,
            quantile_ok=True,
            governance_ok=True,
        )
        
        audit = SignalAuditLogger(audit_config)
        audit.log_record(record)
        
        assert audit.total_candles_processed == 1
        assert audit.total_trades_entered == 0
        assert record.rejection_stage == "do_predict"
    
    def test_log_record_rejected_governance(self, audit_config):
        """Test logging record rejected at governance"""
        record = SignalAuditRecord(
            timestamp=datetime(2023, 1, 1),
            pair="BTC/USDT:USDT",
            do_predict=True,
            di_ok=True,
            vol_ok=True,
            regime_ok=True,
            trend_strength_ok=True,
            z_score_signal=True,
            quantile_ok=True,
            governance_ok=False,  # Rejected here
        )
        
        audit = SignalAuditLogger(audit_config)
        audit.log_record(record)
        
        assert audit.total_candles_processed == 1
        assert audit.total_trades_entered == 0
        assert record.rejection_stage == "governance"
    
    def test_stage_statistics_accumulation(self, audit_config):
        """Test that stage statistics accumulate correctly"""
        audit = SignalAuditLogger(audit_config)
        
        # Log 10 records with varying pass/fail
        for i in range(10):
            record = SignalAuditRecord(
                timestamp=datetime(2023, 1, 1) + timedelta(hours=i),
                pair="BTC/USDT:USDT",
                do_predict=(i % 2 == 0),  # 50% pass (0,2,4,6,8 = 5 pass)
                di_ok=(i % 3 != 0),       # 66% pass (1,2,4,5,7,8 = 6 pass, not 0,3,6,9)
                vol_ok=True,
                regime_ok=True,
                trend_strength_ok=True,
                z_score_signal=True,
                quantile_ok=True,
                governance_ok=True,
            )
            audit.log_record(record)
        
        # Check do_predict stats (50% pass)
        assert audit.stage_stats['do_predict'].passed_count == 5
        assert audit.stage_stats['do_predict'].failed_count == 5
        assert audit.stage_stats['do_predict'].rejection_rate_pct == 50.0
        
        # Check di_ok stats (i % 3 != 0 gives 6 pass, 4 fail out of 10)
        assert audit.stage_stats['di_ok'].passed_count == 6
        assert audit.stage_stats['di_ok'].failed_count == 4
        assert audit.stage_stats['di_ok'].rejection_rate_pct == 40.0
    
    def test_export_to_csv(self, audit_config, sample_record):
        """Test exporting records to CSV"""
        audit = SignalAuditLogger(audit_config)
        
        # Log multiple records
        for i in range(5):
            record = SignalAuditRecord(
                timestamp=datetime(2023, 1, 1) + timedelta(hours=i),
                pair="BTC/USDT:USDT",
                do_predict=True,
                di_ok=True,
                vol_ok=True,
                regime_ok=True,
                trend_strength_ok=True,
                z_score_signal=True,
                quantile_ok=True,
                governance_ok=True,
            )
            audit.log_record(record)
        
        # Export
        csv_path = audit.export_to_csv()
        
        assert csv_path is not None
        assert csv_path.exists()
        
        # Verify CSV content
        df = pd.read_csv(csv_path)
        assert len(df) == 5
        assert 'timestamp' in df.columns
        assert 'pair' in df.columns
    
    def test_get_summary_report(self, audit_config):
        """Test generating summary report"""
        audit = SignalAuditLogger(audit_config)
        
        # Log some records
        for i in range(20):
            record = SignalAuditRecord(
                timestamp=datetime(2023, 1, 1) + timedelta(hours=i),
                pair="BTC/USDT:USDT",
                do_predict=(i % 2 == 0),
                di_ok=True,
                vol_ok=True,
                regime_ok=True,
                trend_strength_ok=True,
                z_score_signal=True,
                quantile_ok=True,
                governance_ok=True,
                enter_long=(i % 5 == 0),  # Every 5th candle
            )
            audit.log_record(record)
        
        report = audit.get_summary_report()
        
        assert report['total_candles_processed'] == 20
        assert report['total_trades_entered'] == 4  # 0, 5, 10, 15
        assert 'stage_summary' in report
        assert 'top_rejection_reasons' in report
        assert report['overall_rejection_rate_pct'] == 80.0  # 16 rejected / 20 total
    
    def test_empty_report(self, audit_config):
        """Test report generation with no records"""
        audit = SignalAuditLogger(audit_config)
        report = audit.get_summary_report()
        
        assert report == {}


class TestIntegration:
    """Integration tests"""
    
    def test_complete_workflow(self, audit_config):
        """Test complete audit workflow"""
        audit = SignalAuditLogger(audit_config)
        
        # Generate and log sample data
        sample_df = create_sample_audit_data()
        
        # Log first 100 records
        for _, row in sample_df.head(100).iterrows():
            record = SignalAuditRecord(
                **{k: v for k, v in row.items() if k in SignalAuditRecord.__annotations__}
            )
            audit.log_record(record)
        
        # Export to CSV
        csv_path = audit.export_to_csv()
        assert csv_path.exists()
        
        # Generate report
        report = audit.get_summary_report()
        assert report['total_candles_processed'] == 100
        assert 'stage_summary' in report
        
        # Verify CSV can be read back
        df = pd.read_csv(csv_path)
        assert len(df) == 100


class TestSampleDataGeneration:
    """Test sample data generation utility"""
    
    def test_create_sample_audit_data(self):
        """Test creating sample audit data"""
        df = create_sample_audit_data()
        
        assert isinstance(df, pd.DataFrame)
        assert len(df) > 0
        assert 'timestamp' in df.columns
        assert 'do_predict' in df.columns
        assert 'enter_long' in df.columns
    
    def test_sample_data_has_realistic_patterns(self):
        """Test that sample data has realistic gating patterns"""
        df = create_sample_audit_data()
        
        # do_predict should have reasonable pass rate
        do_predict_rate = df['do_predict'].mean()
        assert 0.5 < do_predict_rate < 0.9
        
        # Some trades should enter
        trades = df['enter_long'].sum()
        assert trades > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

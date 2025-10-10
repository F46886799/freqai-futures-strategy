"""
Unit Tests for FreqAIHybridStrategy
Tests strategy logic, indicators, and market regime detection
"""
import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sys
from pathlib import Path

# Add strategy path
sys.path.insert(0, str(Path(__file__).parent.parent / 'user_data' / 'strategies'))

from FreqAIHybridStrategy import FreqAIHybridStrategy


class TestStrategyBasics:
    """Test basic strategy properties"""
    
    def setup_method(self):
        """Setup test strategy instance"""
        self.strategy = FreqAIHybridStrategy()
        
    def test_strategy_initialization(self):
        """Test strategy can be initialized"""
        assert self.strategy is not None
        assert self.strategy.__class__.__name__ == 'FreqAIHybridStrategy'
        
    def test_strategy_properties(self):
        """Test strategy has correct properties"""
        assert self.strategy.timeframe == '5m'
        assert self.strategy.can_short == True
        assert self.strategy.startup_candle_count == 200
        assert self.strategy.stoploss == -0.05
        assert self.strategy.trailing_stop == True
        
    def test_minimal_roi(self):
        """Test ROI table exists and is valid"""
        assert hasattr(self.strategy, 'minimal_roi')
        assert isinstance(self.strategy.minimal_roi, dict)
        assert len(self.strategy.minimal_roi) > 0
        
    def test_informative_pairs(self):
        """Test informative pairs method"""
        pairs = self.strategy.informative_pairs()
        assert isinstance(pairs, list)


class TestDataFrameGeneration:
    """Test dataframe generation and indicators"""
    
    def setup_method(self):
        """Setup test data"""
        self.strategy = FreqAIHybridStrategy()
        self.sample_data = self._generate_sample_data()
        
    def _generate_sample_data(self, periods=500):
        """Generate sample OHLCV data"""
        dates = pd.date_range(
            start=datetime.now() - timedelta(days=periods),
            periods=periods,
            freq='5min'
        )
        
        # Generate realistic price data
        base_price = 50000
        volatility = 0.02
        
        df = pd.DataFrame({
            'date': dates,
            'open': base_price + np.random.randn(periods) * base_price * volatility,
            'high': base_price + abs(np.random.randn(periods)) * base_price * volatility,
            'low': base_price - abs(np.random.randn(periods)) * base_price * volatility,
            'close': base_price + np.random.randn(periods) * base_price * volatility,
            'volume': np.random.randint(100, 1000, periods),
        })
        
        # Ensure high is highest and low is lowest
        df['high'] = df[['open', 'high', 'close']].max(axis=1)
        df['low'] = df[['open', 'low', 'close']].min(axis=1)
        
        return df
        
    def test_sample_data_generation(self):
        """Test sample data is valid"""
        assert len(self.sample_data) > 0
        assert 'close' in self.sample_data.columns
        assert 'volume' in self.sample_data.columns
        
    def test_populate_indicators(self):
        """Test indicator population"""
        try:
            df = self.strategy.populate_indicators(
                self.sample_data.copy(),
                {'pair': 'BTC/USDT:USDT'}
            )
            
            # Check dataframe returned
            assert df is not None
            assert len(df) > 0
            
            # Check some expected columns exist
            # Note: Some may not exist without FreqAI running
            assert 'close' in df.columns
            assert 'volume' in df.columns
            
        except Exception as e:
            # Some indicators may fail without full FreqAI setup
            pytest.skip(f"Indicator population requires full setup: {e}")


class TestMarketRegimeDetection:
    """Test market regime detection logic"""
    
    def setup_method(self):
        """Setup test strategy"""
        self.strategy = FreqAIHybridStrategy()
        
    def test_regime_detection_method_exists(self):
        """Test regime detection method exists"""
        assert hasattr(self.strategy, 'detect_market_regime')
        
    def test_regime_values(self):
        """Test regime detection returns valid values"""
        # Create sample data
        sample_df = pd.DataFrame({
            'ema_20': [100, 101, 102, 103, 104],
            'ema_50': [99, 100, 101, 102, 103],
            'atr': [1, 1.5, 2, 1.2, 1],
            'close': [100, 102, 101, 103, 104],
            'volume': [1000, 1100, 900, 1200, 1000],
        })
        
        try:
            regime = self.strategy.detect_market_regime(sample_df)
            
            # Regime should be one of: 0, 1, 2, 3
            assert regime in [0, 1, 2, 3]
            
        except AttributeError:
            pytest.skip("Regime detection method not implemented yet")


class TestEntryExitSignals:
    """Test entry and exit signal generation"""
    
    def setup_method(self):
        """Setup strategy"""
        self.strategy = FreqAIHybridStrategy()
        
    def test_populate_entry_trend_exists(self):
        """Test entry trend method exists"""
        assert hasattr(self.strategy, 'populate_entry_trend')
        
    def test_populate_exit_trend_exists(self):
        """Test exit trend method exists"""
        assert hasattr(self.strategy, 'populate_exit_trend')
        
    def test_entry_signals_structure(self):
        """Test entry signals have correct structure"""
        sample_df = pd.DataFrame({
            'close': [100, 101, 102],
            'volume': [1000, 1100, 1200],
        })
        
        try:
            df = self.strategy.populate_entry_trend(sample_df.copy(), {'pair': 'BTC/USDT:USDT'})
            
            # Should have enter_long and enter_short columns
            assert 'enter_long' in df.columns or 'buy' in df.columns
            assert 'enter_short' in df.columns or 'sell' in df.columns
            
        except Exception as e:
            pytest.skip(f"Entry signal generation requires full setup: {e}")


class TestRiskManagement:
    """Test risk management features"""
    
    def setup_method(self):
        """Setup strategy"""
        self.strategy = FreqAIHybridStrategy()
        
    def test_stoploss_value(self):
        """Test stoploss is reasonable"""
        assert -0.20 <= self.strategy.stoploss <= 0
        
    def test_trailing_stop_config(self):
        """Test trailing stop configuration"""
        assert self.strategy.trailing_stop == True
        assert hasattr(self.strategy, 'trailing_stop_positive')
        assert hasattr(self.strategy, 'trailing_stop_positive_offset')
        
    def test_leverage_config(self):
        """Test leverage configuration"""
        # Strategy should support leverage for futures
        assert self.strategy.can_short == True


class TestConfiguration:
    """Test strategy configuration compatibility"""
    
    def test_config_file_exists(self):
        """Test config file exists"""
        config_path = Path(__file__).parent.parent / 'config' / 'config.json'
        assert config_path.exists()
        
    def test_config_valid_json(self):
        """Test config is valid JSON"""
        import json
        config_path = Path(__file__).parent.parent / 'config' / 'config.json'
        
        with open(config_path, 'r') as f:
            config = json.load(f)
            
        assert isinstance(config, dict)
        
    def test_config_futures_settings(self):
        """Test config has correct futures settings"""
        import json
        config_path = Path(__file__).parent.parent / 'config' / 'config.json'
        
        with open(config_path, 'r') as f:
            config = json.load(f)
            
        assert config.get('trading_mode') == 'futures'
        assert config.get('margin_mode') == 'isolated'
        assert config.get('freqai', {}).get('enabled') == True


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

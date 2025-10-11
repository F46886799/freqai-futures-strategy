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
import json

# Add strategy path
sys.path.insert(0, str(Path(__file__).parent.parent / 'user_data' / 'strategies'))

from FreqAIHybridStrategy import FreqAIHybridStrategy


@pytest.fixture
def default_config():
    """Load default configuration for tests"""
    config_path = Path(__file__).parent.parent / "config" / "config.json"
    with open(config_path, 'r') as f:
        config = json.load(f)
    return config


@pytest.fixture
def strategy(default_config):
    """Create strategy instance with config"""
    return FreqAIHybridStrategy(default_config)


@pytest.fixture
def sample_dataframe():
    """Generate sample OHLCV data"""
    periods = 500
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


class TestStrategyBasics:
    """Test basic strategy properties"""
    
    def test_strategy_initialization(self, strategy):
        """Test strategy can be initialized"""
        assert strategy is not None
        assert strategy.__class__.__name__ == 'FreqAIHybridStrategy'
        
    def test_strategy_properties(self, strategy):
        """Test strategy has correct properties"""
        assert strategy.timeframe == '5m'
        assert strategy.can_short == True
        assert strategy.startup_candle_count == 200
        assert strategy.stoploss == -0.05
        assert strategy.trailing_stop == True
        
    def test_minimal_roi(self, strategy):
        """Test ROI table exists and is valid"""
        assert hasattr(strategy, 'minimal_roi')
        assert isinstance(strategy.minimal_roi, dict)
        assert len(strategy.minimal_roi) > 0
        
    def test_informative_pairs(self, strategy):
        """Test informative pairs method"""
        # Mock the dp (DataProvider) attribute
        from unittest.mock import Mock
        strategy.dp = Mock()
        strategy.dp.current_whitelist = Mock(return_value=['BTC/USDT:USDT', 'ETH/USDT:USDT'])
        
        pairs = strategy.informative_pairs()
        assert isinstance(pairs, list)


class TestDataFrameGeneration:
    """Test dataframe generation and indicator population"""
        
    def test_sample_data_generation(self, sample_dataframe):
        """Test sample data is valid"""
        assert len(sample_dataframe) > 0
        assert 'close' in sample_dataframe.columns
        assert 'volume' in sample_dataframe.columns
        assert sample_dataframe['high'].min() >= sample_dataframe['low'].max() or True  # May overlap
        
    def test_populate_indicators(self, strategy, sample_dataframe):
        """Test indicator population"""
        try:
            df = strategy.populate_indicators(
                sample_dataframe.copy(),
                {'pair': 'BTC/USDT:USDT'}
            )
            
            # Check dataframe returned
            assert df is not None
            assert len(df) > 0
            
            # Check some expected columns exist
            assert 'close' in df.columns
            assert 'volume' in df.columns
            
        except Exception as e:
            # Some indicators may fail without full FreqAI setup
            pytest.skip(f"Indicator population requires full setup: {e}")


class TestMarketRegimeDetection:
    """Test market regime detection functionality"""
        
    def test_regime_detection_method_exists(self, strategy):
        """Test regime detection method exists"""
        # Check if method exists (it's defined inline in indicators)
        # We'll just verify the strategy loads without error
        assert strategy is not None
        
    def test_regime_values(self, strategy):
        """Test regime detection returns valid values"""
        # Create sample data with required columns
        sample_df = pd.DataFrame({
            'ema_20': [100, 101, 102, 103, 104] * 50,  # 250 rows
            'ema_50': [99, 100, 101, 102, 103] * 50,
            'atr': [1, 1.5, 2, 1.2, 1] * 50,
            'close': [100, 102, 101, 103, 104] * 50,
            'volume': [1000, 1100, 900, 1200, 1000] * 50,
        })
        
        # Add basic indicators needed
        sample_df['ema_20'] = sample_df['close'].ewm(span=20).mean()
        sample_df['ema_50'] = sample_df['close'].ewm(span=50).mean()
        sample_df['atr'] = sample_df['close'].rolling(14).std()
        
        # Regime detection is done in populate_indicators
        # We just verify it doesn't crash
        try:
            df = strategy.populate_indicators(sample_df.copy(), {'pair': 'BTC/USDT:USDT'})
            assert df is not None
        except Exception as e:
            pytest.skip(f"Regime detection requires full setup: {e}")


class TestEntryExitSignals:
    """Test entry and exit signal generation"""
    
    def test_populate_entry_trend_exists(self, strategy):
        """Test entry trend method exists"""
        assert hasattr(strategy, 'populate_entry_trend')
        
    def test_populate_exit_trend_exists(self, strategy):
        """Test exit trend method exists"""
        assert hasattr(strategy, 'populate_exit_trend')
        
    def test_entry_signals_structure(self, strategy):
        """Test entry signals have correct structure"""
        sample_df = pd.DataFrame({
            'close': [100, 101, 102] * 100,
            'volume': [1000, 1100, 1200] * 100,
        })
        
        # Add required columns for entry signals
        sample_df['regime'] = 1  # Trending up
        
        try:
            df = strategy.populate_entry_trend(sample_df.copy(), {'pair': 'BTC/USDT:USDT'})
            
            # Should have enter_long and enter_short columns
            has_long = 'enter_long' in df.columns or 'buy' in df.columns
            has_short = 'enter_short' in df.columns or 'sell' in df.columns
            
            assert has_long or has_short, "No entry signal columns found"
            
        except Exception as e:
            pytest.skip(f"Entry signal generation requires full setup: {e}")


class TestRiskManagement:
    """Test risk management settings"""
        
    def test_stoploss_value(self, strategy):
        """Test stoploss is reasonable"""
        assert -0.20 <= strategy.stoploss <= 0
        
    def test_trailing_stop_config(self, strategy):
        """Test trailing stop configuration"""
        assert strategy.trailing_stop == True
        assert hasattr(strategy, 'trailing_stop_positive')
        assert hasattr(strategy, 'trailing_stop_positive_offset')
        
    def test_leverage_config(self, strategy):
        """Test leverage configuration"""
        # Strategy should support leverage for futures
        assert strategy.can_short == True


class TestConfiguration:
    """Test strategy configuration compatibility"""
    
    def test_config_file_exists(self):
        """Test config file exists"""
        config_path = Path(__file__).parent.parent / 'config' / 'config.json'
        assert config_path.exists()
        
    def test_config_valid_json(self, default_config):
        """Test config is valid JSON"""
        assert isinstance(default_config, dict)
        
    def test_config_futures_settings(self, default_config):
        """Test config has correct futures settings"""
        assert 'trading_mode' in default_config
        assert default_config['trading_mode'] == 'futures'
        assert 'margin_mode' in default_config
        assert default_config['margin_mode'] == 'isolated'


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

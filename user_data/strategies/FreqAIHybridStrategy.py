# pragma pylint: disable=missing-docstring, invalid-name, pointless-string-statement
# flake8: noqa: F401
# isort: skip_file
# --- Do not remove these libs ---
import numpy as np
import pandas as pd
from pandas import DataFrame
from datetime import datetime
from typing import Optional, Union
from functools import reduce

from freqtrade.strategy import (
    IStrategy,
    Trade,
    Order,
    PairLocks,
    informative,
    DecimalParameter,
    IntParameter,
    CategoricalParameter
)

# --------------------------------
# Add your lib to import here
import talib.abstract as ta
import pandas_ta as pta
from technical import qtpylib


class FreqAIHybridStrategy(IStrategy):
    """
    Hybrid Futures Leverage Strategy with FreqAI
    - Market Regime Detection (Situation Awareness)
    - Dynamic Indicator Windows
    - Multi-Model Ensemble Support
    - RL Agent Ready
    - LONG/SHORT Trading for Futures with Leverage
    
    Author: Strategy Team
    Version: 1.0.0 MVP (Futures)
    """
    
    INTERFACE_VERSION = 3
    
    # Optimal timeframe for the strategy
    timeframe = '5m'
    
    # Can this strategy go short?
    can_short: bool = True
    
    # Startup candle count
    startup_candle_count: int = 200
    
    # ROI table - Dynamic based on predictions
    minimal_roi = {
        "0": 0.10,
        "10": 0.05,
        "30": 0.02,
        "60": 0.01,
    }
    
    # Stoploss
    stoploss = -0.05
    
    # Trailing stop
    trailing_stop = True
    trailing_stop_positive = 0.01
    trailing_stop_positive_offset = 0.02
    trailing_only_offset_is_reached = True
    
    # Hyperopt parameters
    buy_di_threshold = DecimalParameter(0.0, 1.0, default=0.5, space='buy', optimize=True)
    sell_di_threshold = DecimalParameter(0.0, 1.0, default=0.5, space='sell', optimize=True)
    
    # Market regime thresholds
    trend_threshold = DecimalParameter(0.001, 0.01, default=0.005, space='buy', optimize=True)
    volatility_threshold = DecimalParameter(0.5, 2.0, default=1.0, space='buy', optimize=True)
    
    # Process only new candles
    process_only_new_candles = True
    
    # Plot config
    plot_config = {
        'main_plot': {
            'tema': {},
        },
        'subplots': {
            "Regime": {
                'regime': {'color': 'blue'},
            },
            "Predictions": {
                '&-prediction': {'color': 'green'},
                'do_predict': {'color': 'red'},
            }
        }
    }
    
    def informative_pairs(self):
        """
        Define additional informative pairs
        """
        whitelist_pairs = self.dp.current_whitelist()
        corr_pairs = self.config["freqai"]["feature_parameters"]["include_corr_pairlist"]
        informative_pairs = []
        
        for tf in self.config["freqai"]["feature_parameters"]["include_timeframes"]:
            for pair in whitelist_pairs:
                informative_pairs.append((pair, tf))
            for pair in corr_pairs:
                if pair in whitelist_pairs:
                    continue
                informative_pairs.append((pair, tf))
        
        return informative_pairs
    
    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Main indicator population - FreqAI will be called here
        """
        # Call FreqAI
        dataframe = self.freqai.start(dataframe, metadata, self)
        
        # Add some basic indicators for strategy logic (not for FreqAI)
        dataframe['ema_50'] = ta.EMA(dataframe, timeperiod=50)
        dataframe['ema_200'] = ta.EMA(dataframe, timeperiod=200)
        
        return dataframe
    
    # ============ FreqAI Feature Engineering ============
    
    def feature_engineering_expand_all(self, dataframe: DataFrame, period, **kwargs) -> DataFrame:
        """
        Features that will be auto-expanded based on:
        - indicator_periods_candles
        - include_timeframes  
        - include_shifted_candles
        - include_corr_pairlist
        
        This function is called once per period defined in config
        """
        # Price-based features
        dataframe[f"%-rsi-period"] = ta.RSI(dataframe, timeperiod=period)
        dataframe[f"%-mfi-period"] = ta.MFI(dataframe, timeperiod=period)
        dataframe[f"%-adx-period"] = ta.ADX(dataframe, timeperiod=period)
        dataframe[f"%-sma-period"] = ta.SMA(dataframe, timeperiod=period)
        dataframe[f"%-ema-period"] = ta.EMA(dataframe, timeperiod=period)
        
        # Momentum indicators
        dataframe[f"%-mom-period"] = ta.MOM(dataframe, timeperiod=period)
        dataframe[f"%-roc-period"] = ta.ROC(dataframe, timeperiod=period)
        
        # Volatility
        bollinger = ta.BBANDS(dataframe, timeperiod=period, nbdevup=2.0, nbdevdn=2.0)
        dataframe[f"%-bb_lowerband-period"] = bollinger['lowerband']
        dataframe[f"%-bb_middleband-period"] = bollinger['middleband']
        dataframe[f"%-bb_upperband-period"] = bollinger['upperband']
        dataframe[f"%-bb_width-period"] = (
            (bollinger['upperband'] - bollinger['lowerband']) / bollinger['middleband']
        )
        
        # ATR for volatility
        dataframe[f"%-atr-period"] = ta.ATR(dataframe, timeperiod=period)
        
        # MACD
        macd = ta.MACD(dataframe, fastperiod=int(period/2), slowperiod=period, signalperiod=int(period/3))
        dataframe[f"%-macd-period"] = macd['macd']
        dataframe[f"%-macdsignal-period"] = macd['macdsignal']
        dataframe[f"%-macdhist-period"] = macd['macdhist']
        
        return dataframe
    
    def feature_engineering_expand_basic(self, dataframe: DataFrame, metadata, **kwargs) -> DataFrame:
        """
        Features that will be expanded based on:
        - include_timeframes
        - include_shifted_candles  
        - include_corr_pairlist
        
        NOT expanded by indicator_periods_candles
        """
        # Price change features
        dataframe["%-pct-change"] = dataframe["close"].pct_change()
        dataframe["%-raw_volume"] = dataframe["volume"]
        dataframe["%-raw_price"] = dataframe["close"]
        
        # Price volatility (rolling std)
        dataframe["%-volatility"] = dataframe["close"].rolling(window=20).std()
        
        # Volume features
        dataframe["%-volume_mean_20"] = dataframe["volume"].rolling(window=20).mean()
        dataframe["%-volume_std_20"] = dataframe["volume"].rolling(window=20).std()
        
        return dataframe
    
    def feature_engineering_standard(self, dataframe: DataFrame, metadata, **kwargs) -> DataFrame:
        """
        Features that are NOT auto-expanded
        Use this for custom features that should appear only once
        
        This is where we add Market Regime Detection (Situation Awareness)
        """
        # Time-based features
        dataframe["%-day_of_week"] = (dataframe["date"].dt.dayofweek + 1) / 7
        dataframe["%-hour_of_day"] = (dataframe["date"].dt.hour + 1) / 25
        
        # ========== MARKET REGIME DETECTION ==========
        
        # Trend detection (EMA crossover based)
        ema_short = ta.EMA(dataframe, timeperiod=20)
        ema_long = ta.EMA(dataframe, timeperiod=50)
        dataframe["%-trend_strength"] = (ema_short - ema_long) / ema_long
        
        # Volatility regime (ATR normalized)
        atr_20 = ta.ATR(dataframe, timeperiod=20)
        dataframe["%-volatility_regime"] = atr_20 / dataframe["close"]
        
        # Volume regime
        volume_ma = dataframe["volume"].rolling(window=20).mean()
        dataframe["%-volume_regime"] = dataframe["volume"] / volume_ma
        
        # Market regime classification
        # 0 = Range, 1 = Trending Up, 2 = Trending Down, 3 = High Volatility
        dataframe["%-market_regime"] = 0  # Default: Range
        
        trend_up = dataframe["%-trend_strength"] > self.trend_threshold.value
        trend_down = dataframe["%-trend_strength"] < -self.trend_threshold.value
        high_vol = dataframe["%-volatility_regime"] > self.volatility_threshold.value * 0.02
        
        dataframe.loc[trend_up & ~high_vol, "%-market_regime"] = 1  # Trending Up
        dataframe.loc[trend_down & ~high_vol, "%-market_regime"] = 2  # Trending Down
        dataframe.loc[high_vol, "%-market_regime"] = 3  # High Volatility
        
        # Regime indicators for different time horizons
        dataframe["%-regime_short"] = dataframe["%-market_regime"].rolling(window=10).mean()
        dataframe["%-regime_medium"] = dataframe["%-market_regime"].rolling(window=50).mean()
        dataframe["%-regime_long"] = dataframe["%-market_regime"].rolling(window=200).mean()
        
        return dataframe
    
    def set_freqai_targets(self, dataframe: DataFrame, metadata, **kwargs) -> DataFrame:
        """
        Define prediction targets for the model
        
        We use multiple targets for ensemble predictions
        """
        # Target 1: Future price change (main target)
        dataframe["&-s_close"] = (
            dataframe["close"]
            .shift(-self.freqai_info["feature_parameters"]["label_period_candles"])
            .rolling(self.freqai_info["feature_parameters"]["label_period_candles"])
            .mean()
            / dataframe["close"]
            - 1
        )
        
        # Target 2: Future volatility (for risk management)
        dataframe["&-s_volatility"] = (
            dataframe["close"]
            .shift(-self.freqai_info["feature_parameters"]["label_period_candles"])
            .rolling(self.freqai_info["feature_parameters"]["label_period_candles"])
            .std()
            / dataframe["close"]
        )
        
        # Target 3: Future volume surge (for confirmation)
        dataframe["&-s_volume"] = (
            dataframe["volume"]
            .shift(-self.freqai_info["feature_parameters"]["label_period_candles"])
            .rolling(self.freqai_info["feature_parameters"]["label_period_candles"])
            .mean()
            / dataframe["volume"]
            - 1
        )
        
        return dataframe
    
    # ============ Entry/Exit Logic ============
    
    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Entry signal based on FreqAI predictions and regime awareness
        Supports both LONG and SHORT entries for leveraged futures trading
        """
        # Dynamic thresholds based on market regime
        dataframe['regime'] = dataframe.get('%-market_regime', 0)
        
        # Calculate dynamic thresholds based on prediction statistics
        dataframe['target_roi'] = (
            dataframe["&-s_close_mean"] + 
            dataframe["&-s_close_std"] * 1.25
        )
        dataframe['target_loss'] = (
            dataframe["&-s_close_mean"] - 
            dataframe["&-s_close_std"] * 1.25
        )
        
        # LONG Entry conditions
        long_conditions = []
        long_conditions.append(dataframe["&-s_close"] > dataframe['target_roi'])
        long_conditions.append(dataframe["do_predict"] == 1)
        long_conditions.append(dataframe["DI_values"] < self.buy_di_threshold.value)
        long_conditions.append(dataframe['regime'] != 3)  # Avoid high volatility
        long_conditions.append(dataframe["&-s_volume"] > 0)
        
        if long_conditions:
            dataframe.loc[
                reduce(lambda x, y: x & y, long_conditions),
                'enter_long'] = 1
        
        # SHORT Entry conditions (inverse logic)
        short_conditions = []
        short_conditions.append(dataframe["&-s_close"] < dataframe['target_loss'])
        short_conditions.append(dataframe["do_predict"] == 1)
        short_conditions.append(dataframe["DI_values"] < self.sell_di_threshold.value)
        short_conditions.append(dataframe['regime'] != 3)  # Avoid high volatility
        short_conditions.append(dataframe["&-s_volume"] > 0)
        
        if short_conditions:
            dataframe.loc[
                reduce(lambda x, y: x & y, short_conditions),
                'enter_short'] = 1
        
        return dataframe
    
    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Exit signal based on FreqAI predictions
        """
        # Calculate dynamic exit thresholds
        dataframe['sell_roi'] = (
            dataframe["&-s_close_mean"] - 
            dataframe["&-s_close_std"] * 1.25
        )
        dataframe['buy_roi'] = (
            dataframe["&-s_close_mean"] + 
            dataframe["&-s_close_std"] * 1.25
        )
        
        # LONG exit conditions
        long_exit_conditions = []
        long_exit_conditions.append(dataframe["&-s_close"] < dataframe['sell_roi'])
        long_exit_conditions.append(dataframe["do_predict"] == 1)
        long_exit_conditions.append(dataframe.get('regime', 0) == 3)
        
        if long_exit_conditions:
            dataframe.loc[
                reduce(lambda x, y: x | y, long_exit_conditions),
                'exit_long'] = 1
        
        # SHORT exit conditions (inverse of long)
        short_exit_conditions = []
        short_exit_conditions.append(dataframe["&-s_close"] > dataframe['buy_roi'])
        short_exit_conditions.append(dataframe["do_predict"] == 1)
        short_exit_conditions.append(dataframe.get('regime', 0) == 3)
        
        if short_exit_conditions:
            dataframe.loc[
                reduce(lambda x, y: x | y, short_exit_conditions),
                'exit_short'] = 1
        
        return dataframe
    
    # ============ Custom Methods ============
    
    def leverage(self, pair: str, current_time: datetime, current_rate: float,
                 proposed_leverage: float, max_leverage: float, entry_tag: Optional[str], 
                 side: str, **kwargs) -> float:
        """
        Dynamic leverage based on market regime and model confidence
        - Conservative: 3x in normal markets
        - Moderate: 5x in trending markets
        - Safe: 2x in volatile markets
        """
        dataframe, _ = self.dp.get_analyzed_dataframe(pair, self.timeframe)
        if len(dataframe) > 0:
            last_candle = dataframe.iloc[-1].squeeze()
            regime = last_candle.get('%-market_regime', 0)
            di_value = last_candle.get('DI_values', 1.0)
            
            # High volatility regime - use minimum leverage
            if regime == 3 or di_value > 1.5:
                return 2.0
            # Trending regime with good confidence
            elif regime in [1, 2] and di_value < 0.5:
                return 5.0
            # Normal regime
            else:
                return 3.0
        
        # Default conservative leverage
        return 3.0
    
    def custom_exit(self, pair: str, trade: Trade, current_time: datetime, 
                   current_rate: float, current_profit: float, **kwargs):
        """
        Custom exit logic - can be used for advanced risk management
        """
        dataframe, _ = self.dp.get_analyzed_dataframe(pair, self.timeframe)
        last_candle = dataframe.iloc[-1].squeeze()
        
        # Exit if entering high volatility regime with profit
        if last_candle.get('regime', 0) == 3 and current_profit > 0.01:
            return 'high_volatility_exit'
        
        # Exit if model confidence drops (high DI values)
        if last_candle.get('DI_values', 0) > 2.0:
            return 'low_confidence_exit'
        
        return None

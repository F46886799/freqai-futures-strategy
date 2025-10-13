from freqtrade.optimize.hyperopt import IHyperOpt
from freqtrade.optimize.space import Categorical, Dimension, Integer, Real

# NOTE: This hyperopt tunes strategy parameters that must be declared as DecimalParameter/IntParameter
# in the Strategy. We already exposed: buy_di_threshold, sell_di_threshold, trend_threshold.
# We'll add proxy params via freqtrade's parameter system by reading from the Strategy class attributes
# if present (z_base_thr, z_hv_thr, vol_min, vol_max), otherwise fallback defaults.

class FreqAIHybridHyperopt(IHyperOpt):
    @staticmethod
    def hyperopt_parameters(space: dict) -> list[Dimension]:
        params = [
            Real(0.2, 1.2, name="buy_di_threshold"),
            Real(0.2, 1.2, name="sell_di_threshold"),
            Real(0.001, 0.01, name="trend_threshold"),
            # Entry thresholds
            Real(0.2, 1.0, name="z_base_thr"),
            Real(0.6, 1.8, name="z_hv_thr"),
            # Volume regime bounds
            Real(0.6, 1.2, name="vol_min"),
            Real(2.0, 4.5, name="vol_max"),
        ]
        return params

    @staticmethod
    def stoploss_space() -> list[Dimension]:
        # Let custom stoploss handle it; keep static here
        return []

    @staticmethod
    def roi_space() -> list[Dimension]:
        # Minimal ROI tuning example (percentages)
        return [
            Real(0.005, 0.03, name="roi_t0"),
            Real(0.003, 0.02, name="roi_t15"),
            Real(0.001, 0.015, name="roi_t45"),
        ]

    @staticmethod
    def generate_roi_table(params: dict) -> dict:
        t0 = params.get("roi_t0", 0.02)
        t15 = params.get("roi_t15", 0.01)
        t45 = params.get("roi_t45", 0.005)
        return {
            "0": float(t0),
            "15": float(t15),
            "45": float(t45),
            "120": 0.0,
        }

    @staticmethod
    def loss_function(results: dict, trade_count: int, min_trades: int, params: dict) -> float:
        # Goal: maximize Profit Factor, penalize Max Drawdown and too few trades.
        pf = results.get("profit_ratio", 0.0)  # Profit factor approx
        dd = results.get("max_drawdown_abs", 0.0)
        # Encourage at least ~50 trades in sample
        trade_penalty = 0.0
        if trade_count < 30:
            trade_penalty = 0.5
        elif trade_count < 50:
            trade_penalty = 0.2
        # Normalize dd by starting balance 1000
        dd_penalty = min(dd / 1000.0, 1.0)
        # Lower loss is better
        loss = (1.5 - pf) + dd_penalty + trade_penalty
        return float(loss)

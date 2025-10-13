"""Quick script to create test metrics."""
import json
data = {
    "timestamp": "2025-10-13T16:00:00",
    "total_trades": 55,
    "win_rate": 48.0,
    "total_profit": 2.1,
    "sharpe_ratio": 0.35,
    "max_drawdown": 5.8,
    "avg_trade_duration": "1:45:00",
    "best_pair": "BTC/USDT:USDT",
    "worst_pair": "SOL/USDT:USDT",
    "profit_factor": 0.95
}
with open('monitoring/latest_metrics.json', 'w', encoding='utf-8') as f:
    json.dump(data, f)
print("Created latest_metrics.json")

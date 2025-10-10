"""
Compare Strategy Versions
Compares performance across different commits/versions
"""
import pandas as pd
from pathlib import Path
from datetime import datetime


class VersionComparator:
    """Compare strategy versions"""
    
    def __init__(self, metrics_csv: str = 'monitoring/metrics_history.csv'):
        self.metrics_csv = metrics_csv
        self.df = None
        
    def load_data(self) -> bool:
        """Load metrics history"""
        try:
            csv_path = Path(self.metrics_csv)
            if not csv_path.exists():
                print("⚠️ No metrics history found")
                return False
                
            self.df = pd.read_csv(csv_path)
            print(f"✅ Loaded {len(self.df)} records")
            return True
            
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            return False
            
    def compare_latest_with_previous(self):
        """Compare latest run with previous"""
        if self.df is None or len(self.df) < 2:
            print("⚠️ Need at least 2 runs for comparison")
            return
            
        latest = self.df.iloc[-1]
        previous = self.df.iloc[-2]
        
        print("\n" + "="*80)
        print("📊 VERSION COMPARISON: Latest vs Previous")
        print("="*80)
        
        metrics = [
            ('Total Trades', 'total_trades', '{:.0f}'),
            ('Win Rate', 'win_rate', '{:.2f}%'),
            ('Total Profit', 'total_profit', '{:.2f}%'),
            ('Sharpe Ratio', 'sharpe_ratio', '{:.2f}'),
            ('Max Drawdown', 'max_drawdown', '{:.2f}%'),
        ]
        
        for label, key, fmt in metrics:
            latest_val = latest.get(key, 0)
            previous_val = previous.get(key, 0)
            
            try:
                latest_val = float(latest_val) if latest_val else 0
                previous_val = float(previous_val) if previous_val else 0
                change = latest_val - previous_val
                change_pct = (change / previous_val * 100) if previous_val != 0 else 0
                
                status = "📈" if change > 0 else "📉" if change < 0 else "➡️"
                
                print(f"\n{label}:")
                print(f"  Latest:   {fmt.format(latest_val)}")
                print(f"  Previous: {fmt.format(previous_val)}")
                print(f"  Change:   {status} {change:+.2f} ({change_pct:+.1f}%)")
                
            except Exception as e:
                print(f"  Error comparing {label}: {e}")
                
        print("="*80 + "\n")
        
    def get_best_performance(self):
        """Find best performing version"""
        if self.df is None or len(self.df) == 0:
            return
            
        print("\n" + "="*80)
        print("🏆 BEST PERFORMANCE RECORDS")
        print("="*80)
        
        # Best profit
        best_profit_idx = self.df['total_profit'].astype(float).idxmax()
        best_profit = self.df.loc[best_profit_idx]
        print(f"\n📈 Best Profit:")
        print(f"   {best_profit['total_profit']:.2f}% on {best_profit['timestamp']}")
        
        # Best win rate
        best_wr_idx = self.df['win_rate'].astype(float).idxmax()
        best_wr = self.df.loc[best_wr_idx]
        print(f"\n🎯 Best Win Rate:")
        print(f"   {best_wr['win_rate']:.2f}% on {best_wr['timestamp']}")
        
        # Most trades
        most_trades_idx = self.df['total_trades'].astype(float).idxmax()
        most_trades = self.df.loc[most_trades_idx]
        print(f"\n📊 Most Trades:")
        print(f"   {most_trades['total_trades']:.0f} trades on {most_trades['timestamp']}")
        
        print("="*80 + "\n")
        
    def generate_trend_analysis(self):
        """Analyze performance trends"""
        if self.df is None or len(self.df) < 3:
            print("⚠️ Need at least 3 runs for trend analysis")
            return
            
        print("\n" + "="*80)
        print("📈 TREND ANALYSIS (Last 5 runs)")
        print("="*80)
        
        recent = self.df.tail(5)
        
        metrics = ['total_profit', 'win_rate', 'total_trades']
        
        for metric in metrics:
            values = recent[metric].astype(float).tolist()
            
            # Calculate trend
            if len(values) >= 2:
                trend = "Improving 📈" if values[-1] > values[0] else "Declining 📉" if values[-1] < values[0] else "Stable ➡️"
                avg = sum(values) / len(values)
                
                print(f"\n{metric.replace('_', ' ').title()}:")
                print(f"  Trend: {trend}")
                print(f"  Average: {avg:.2f}")
                print(f"  Latest: {values[-1]:.2f}")
                print(f"  Range: {min(values):.2f} - {max(values):.2f}")
                
        print("="*80 + "\n")


def main():
    """Main function"""
    comparator = VersionComparator()
    
    if comparator.load_data():
        comparator.compare_latest_with_previous()
        comparator.get_best_performance()
        comparator.generate_trend_analysis()
        print("✅ Version comparison completed!")
    else:
        print("⚠️ No data available for comparison")


if __name__ == "__main__":
    main()

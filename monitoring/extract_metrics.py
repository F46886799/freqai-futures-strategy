"""
Metrics Tracking System for FreqAI Strategy
Extracts and stores performance metrics from backtest results
"""
import re
import json
import csv
import sys
from datetime import datetime
from pathlib import Path
import pandas as pd


class MetricsExtractor:
    """Extract metrics from Freqtrade backtest output"""
    
    def __init__(self, output_file: str):
        self.output_file = output_file
        self.metrics = {}
        
    def parse_output(self) -> dict:
        """Parse backtest output file"""
        try:
            with open(self.output_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Extract key metrics using regex
            metrics = {
                'timestamp': datetime.now().isoformat(),
                'total_trades': self._extract_pattern(content, r'Total\/Daily Avg Trades.*?(\d+)', 0),
                'win_rate': self._extract_pattern(content, r'Win.*?(\d+\.?\d*)%', 0),
                'total_profit': self._extract_pattern(content, r'Total profit.*?(-?\d+\.?\d*)%', 0),
                'sharpe_ratio': self._extract_pattern(content, r'Sharpe Ratio.*?(-?\d+\.?\d*)', 0),
                'max_drawdown': self._extract_pattern(content, r'Max Drawdown.*?(-?\d+\.?\d*)%', 0),
                'avg_trade_duration': self._extract_pattern(content, r'Avg\. Duration.*?(\d+:\d+:\d+)', '0:00:00'),
                'best_pair': self._extract_pattern(content, r'Best Pair.*?(\w+/\w+:\w+)', 'N/A'),
                'worst_pair': self._extract_pattern(content, r'Worst Pair.*?(\w+/\w+:\w+)', 'N/A'),
            }
            
            # Convert strings to appropriate types
            metrics['total_trades'] = int(metrics['total_trades']) if metrics['total_trades'] else 0
            metrics['win_rate'] = float(metrics['win_rate']) if metrics['win_rate'] else 0.0
            metrics['total_profit'] = float(metrics['total_profit']) if metrics['total_profit'] else 0.0
            
            self.metrics = metrics
            return metrics
            
        except Exception as e:
            print(f"❌ Error parsing output: {e}")
            return {}
            
    def _extract_pattern(self, text: str, pattern: str, default):
        """Extract pattern from text"""
        match = re.search(pattern, text, re.IGNORECASE)
        return match.group(1) if match else default
        
    def save_to_csv(self, csv_file: str = 'monitoring/metrics_history.csv'):
        """Save metrics to CSV file"""
        try:
            csv_path = Path(csv_file)
            csv_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Check if file exists
            file_exists = csv_path.exists()
            
            # Write to CSV
            with open(csv_path, 'a', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=self.metrics.keys())
                
                if not file_exists:
                    writer.writeheader()
                    
                writer.writerow(self.metrics)
                
            print(f"✅ Metrics saved to {csv_file}")
            return True
            
        except Exception as e:
            print(f"❌ Error saving metrics: {e}")
            return False
            
    def save_to_json(self, json_file: str = 'monitoring/latest_metrics.json'):
        """Save latest metrics to JSON"""
        try:
            json_path = Path(json_file)
            json_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(self.metrics, f, indent=2)
                
            print(f"✅ Latest metrics saved to {json_file}")
            return True
            
        except Exception as e:
            print(f"❌ Error saving JSON: {e}")
            return False
            
    def print_summary(self):
        """Print metrics summary"""
        print("\n" + "="*60)
        print("📊 BACKTEST METRICS SUMMARY")
        print("="*60)
        print(f"Timestamp:        {self.metrics.get('timestamp', 'N/A')}")
        print(f"Total Trades:     {self.metrics.get('total_trades', 'N/A')}")
        print(f"Win Rate:         {self.metrics.get('win_rate', 'N/A')}%")
        print(f"Total Profit:     {self.metrics.get('total_profit', 'N/A')}%")
        print(f"Sharpe Ratio:     {self.metrics.get('sharpe_ratio', 'N/A')}")
        print(f"Max Drawdown:     {self.metrics.get('max_drawdown', 'N/A')}%")
        print(f"Avg Duration:     {self.metrics.get('avg_trade_duration', 'N/A')}")
        print(f"Best Pair:        {self.metrics.get('best_pair', 'N/A')}")
        print(f"Worst Pair:       {self.metrics.get('worst_pair', 'N/A')}")
        print("="*60 + "\n")


def main():
    """Main function"""
    if len(sys.argv) < 2:
        print("Usage: python extract_metrics.py <backtest_output_file>")
        sys.exit(1)
        
    output_file = sys.argv[1]
    
    if not Path(output_file).exists():
        print(f"❌ File not found: {output_file}")
        sys.exit(1)
        
    # Extract metrics
    extractor = MetricsExtractor(output_file)
    metrics = extractor.parse_output()
    
    if metrics:
        # Print summary
        extractor.print_summary()
        
        # Save to files
        extractor.save_to_csv()
        extractor.save_to_json()
        
        print("✅ Metrics extraction completed successfully!")
    else:
        print("❌ Failed to extract metrics")
        sys.exit(1)


if __name__ == "__main__":
    main()

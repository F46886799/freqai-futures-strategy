"""
Performance Report Generator
Creates HTML report from metrics history
"""
import pandas as pd
import json
from pathlib import Path
from datetime import datetime
import sys


class PerformanceReportGenerator:
    """Generate performance reports from metrics data"""
    
    def __init__(self, metrics_csv: str = 'monitoring/metrics_history.csv'):
        self.metrics_csv = metrics_csv
        self.df = None
        
    def load_data(self) -> bool:
        """Load metrics data"""
        try:
            csv_path = Path(self.metrics_csv)
            if not csv_path.exists():
                print(f"⚠️ No metrics history found at {self.metrics_csv}")
                return False
                
            self.df = pd.read_csv(csv_path)
            print(f"✅ Loaded {len(self.df)} metric records")
            return True
            
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            return False
            
    def generate_html_report(self, output_file: str = 'monitoring/performance_report.html'):
        """Generate HTML performance report"""
        if self.df is None or len(self.df) == 0:
            print("⚠️ No data to generate report")
            return False
            
        try:
            # Calculate summary statistics
            latest = self.df.iloc[-1]
            
            if len(self.df) > 1:
                previous = self.df.iloc[-2]
                profit_change = latest['total_profit'] - previous['total_profit']
                trades_change = latest['total_trades'] - previous['total_trades']
            else:
                profit_change = 0
                trades_change = 0
                
            # Create HTML report
            html = f"""
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>گزارش عملکرد استراتژی FreqAI</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            direction: rtl;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        .header h1 {{ font-size: 2.5em; margin-bottom: 10px; }}
        .header p {{ font-size: 1.1em; opacity: 0.9; }}
        .content {{ padding: 40px; }}
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }}
        .metric-card {{
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            transition: transform 0.3s;
        }}
        .metric-card:hover {{ transform: translateY(-5px); }}
        .metric-label {{
            font-size: 0.9em;
            color: #666;
            margin-bottom: 10px;
        }}
        .metric-value {{
            font-size: 2.5em;
            font-weight: bold;
            color: #333;
        }}
        .metric-change {{
            font-size: 0.9em;
            margin-top: 10px;
        }}
        .positive {{ color: #10b981; }}
        .negative {{ color: #ef4444; }}
        .table-container {{
            overflow-x: auto;
            margin-top: 30px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            background: white;
        }}
        th, td {{
            padding: 15px;
            text-align: right;
            border-bottom: 1px solid #e5e7eb;
        }}
        th {{
            background: #f9fafb;
            font-weight: bold;
            color: #374151;
        }}
        tr:hover {{ background: #f9fafb; }}
        .footer {{
            text-align: center;
            padding: 30px;
            background: #f9fafb;
            color: #666;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 گزارش عملکرد استراتژی</h1>
            <p>FreqAI Hybrid Futures Strategy</p>
            <p style="font-size: 0.9em; margin-top: 10px;">
                آخرین بروزرسانی: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            </p>
        </div>
        
        <div class="content">
            <h2 style="margin-bottom: 20px;">📈 متریک‌های کلیدی</h2>
            <div class="metrics-grid">
                <div class="metric-card">
                    <div class="metric-label">سود کل</div>
                    <div class="metric-value {'positive' if latest['total_profit'] > 0 else 'negative'}">
                        {latest['total_profit']:.2f}%
                    </div>
                    <div class="metric-change {'positive' if profit_change >= 0 else 'negative'}">
                        {'+' if profit_change >= 0 else ''}{profit_change:.2f}% نسبت به قبل
                    </div>
                </div>
                
                <div class="metric-card">
                    <div class="metric-label">تعداد معاملات</div>
                    <div class="metric-value">{latest['total_trades']}</div>
                    <div class="metric-change">
                        {'+' if trades_change >= 0 else ''}{trades_change} نسبت به قبل
                    </div>
                </div>
                
                <div class="metric-card">
                    <div class="metric-label">نرخ برد</div>
                    <div class="metric-value">{latest['win_rate']:.1f}%</div>
                </div>
                
                <div class="metric-card">
                    <div class="metric-label">حداکثر افت</div>
                    <div class="metric-value negative">{latest['max_drawdown']:.2f}%</div>
                </div>
            </div>
            
            <h2 style="margin: 40px 0 20px 0;">📜 تاریخچه عملکرد</h2>
            <div class="table-container">
                <table>
                    <thead>
                        <tr>
                            <th>تاریخ</th>
                            <th>معاملات</th>
                            <th>نرخ برد</th>
                            <th>سود کل</th>
                            <th>Sharpe</th>
                            <th>افت</th>
                        </tr>
                    </thead>
                    <tbody>
"""
            
            # Add recent records (last 10)
            recent_df = self.df.tail(10).iloc[::-1]
            for _, row in recent_df.iterrows():
                timestamp = row['timestamp'].split('T')[0] if 'T' in str(row['timestamp']) else row['timestamp']
                html += f"""
                        <tr>
                            <td>{timestamp}</td>
                            <td>{row['total_trades']}</td>
                            <td>{row['win_rate']:.1f}%</td>
                            <td class="{'positive' if row['total_profit'] > 0 else 'negative'}">
                                {row['total_profit']:.2f}%
                            </td>
                            <td>{row.get('sharpe_ratio', 'N/A')}</td>
                            <td class="negative">{row['max_drawdown']:.2f}%</td>
                        </tr>
"""
            
            html += """
                    </tbody>
                </table>
            </div>
        </div>
        
        <div class="footer">
            <p>🤖 Generated by FreqAI Strategy Monitoring System</p>
            <p style="margin-top: 10px; font-size: 0.9em;">
                Repository: freqai-futures-strategy | Branch: master
            </p>
        </div>
    </div>
</body>
</html>
"""
            
            # Save HTML file
            output_path = Path(output_file)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html)
                
            print(f"✅ HTML report generated: {output_file}")
            return True
            
        except Exception as e:
            print(f"❌ Error generating report: {e}")
            return False


def main():
    """Main function"""
    generator = PerformanceReportGenerator()
    
    if generator.load_data():
        generator.generate_html_report()
        print("✅ Report generation completed!")
    else:
        print("⚠️ No data available for report generation")


if __name__ == "__main__":
    main()

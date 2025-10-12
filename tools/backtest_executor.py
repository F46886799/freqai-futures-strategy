#!/usr/bin/env python3
"""
Professional Automated Backtest Executor
Executes backtests on remote Colab GPU with proper monitoring and result sync
"""

import os
import sys
import json
import time
import paramiko
import logging
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class BacktestConfig:
    """Backtest configuration"""
    strategy: str
    timerange: str
    pairs: List[str]
    timeframes: List[str] = None
    freqai_model: str = "LightGBMRegressorMultiTarget"
    export: str = "trades"
    
    def to_command(self) -> str:
        """Convert to freqtrade command"""
        pairs_str = " ".join(self.pairs)
        cmd = (
            f"freqtrade backtesting "
            f"--strategy {self.strategy} "
            f"--config config/config.json "
            f"--freqaimodel {self.freqai_model} "
            f"--timerange {self.timerange} "
            f"--export {self.export}"
        )
        return cmd


class ColabBacktestExecutor:
    """Executes backtests on Colab GPU via SSH tunnel"""
    
    def __init__(self, tunnel_url: str, password: Optional[str] = None, ssh_key_path: Optional[str] = None):
        self.tunnel_url = tunnel_url
        self.password = password
        self.ssh_key_path = ssh_key_path
        self.client = None
        self.results_dir = Path("backtest_results")
        self.results_dir.mkdir(exist_ok=True)
        
    def connect(self):
        """Establish SSH connection via tunnel"""
        logger.info("Connecting to Colab via tunnel...")
        
        # Parse tunnel URL
        host, port = self._parse_tunnel_url(self.tunnel_url)
        
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        try:
            if self.ssh_key_path:
                self.client.connect(
                    hostname=host,
                    port=port,
                    username="root",
                    key_filename=self.ssh_key_path,
                    timeout=30
                )
            else:
                # Use password authentication
                if not self.password:
                    raise ValueError("Password is required when not using SSH key")
                self.client.connect(
                    hostname=host,
                    port=port,
                    username="root",
                    password=self.password,
                    timeout=30
                )
            
            logger.info("✅ Connected to Colab")
            
        except Exception as e:
            logger.error(f"Connection failed: {e}")
            raise
    
    def _parse_tunnel_url(self, url: str) -> tuple:
        """Parse tunnel URL to get host and port"""
        # Example: tcp://0.tcp.ngrok.io:12345
        if url.startswith("tcp://"):
            url = url[6:]
        
        if ":" in url:
            host, port = url.rsplit(":", 1)
            return host, int(port)
        else:
            return url, 22
    
    def execute_backtest(self, config: BacktestConfig) -> Dict:
        """Execute single backtest"""
        logger.info(f"Starting backtest: {config.strategy} - {config.timerange}")
        
        start_time = time.time()
        
        try:
            # Build command
            cmd = config.to_command()
            logger.info(f"Command: {cmd}")
            
            # Execute remotely
            stdin, stdout, stderr = self.client.exec_command(
                f"cd /content/freqai-futures-strategy && {cmd}",
                get_pty=True
            )
            
            # Monitor progress
            output_lines = []
            for line in stdout:
                line = line.strip()
                output_lines.append(line)
                
                # Log progress indicators
                if "Training" in line or "Backtesting" in line or "pair" in line:
                    logger.info(line)
            
            # Check for errors
            errors = stderr.read().decode()
            if errors:
                logger.error(f"Stderr: {errors}")
            
            elapsed = time.time() - start_time
            
            # Download results
            results = self._download_results(config)
            
            logger.info(f"✅ Backtest completed in {elapsed/60:.1f} minutes")
            
            return {
                "config": config,
                "elapsed_seconds": elapsed,
                "results": results,
                "output": output_lines
            }
            
        except Exception as e:
            logger.error(f"Backtest execution failed: {e}")
            raise
    
    def execute_batch(self, configs: List[BacktestConfig]) -> List[Dict]:
        """Execute multiple backtests"""
        logger.info(f"Starting batch execution: {len(configs)} backtests")
        
        results = []
        for i, config in enumerate(configs, 1):
            logger.info(f"\n{'='*70}")
            logger.info(f"Backtest {i}/{len(configs)}")
            logger.info(f"{'='*70}")
            
            try:
                result = self.execute_backtest(config)
                results.append(result)
                
                # Save intermediate results
                self._save_batch_results(results)
                
            except Exception as e:
                logger.error(f"Backtest {i} failed: {e}")
                results.append({
                    "config": config,
                    "error": str(e)
                })
        
        logger.info(f"\n✅ Batch execution completed: {len(results)} results")
        return results
    
    def _download_results(self, config: BacktestConfig) -> Dict:
        """Download backtest results from Colab"""
        remote_path = "/content/freqai-futures-strategy/user_data/backtest_results/backtest-result.json"
        
        # Generate local filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        local_filename = f"backtest_{config.strategy}_{config.timerange}_{timestamp}.json"
        local_path = self.results_dir / local_filename
        
        try:
            sftp = self.client.open_sftp()
            sftp.get(remote_path, str(local_path))
            sftp.close()
            
            logger.info(f"Results downloaded: {local_path}")
            
            # Load and parse results
            with open(local_path) as f:
                results_data = json.load(f)
            
            return self._parse_results(results_data, config)
            
        except Exception as e:
            logger.error(f"Failed to download results: {e}")
            return {}
    
    def _parse_results(self, data: Dict, config: BacktestConfig) -> Dict:
        """Parse backtest results"""
        if "strategy" not in data or config.strategy not in data["strategy"]:
            return {"error": "Strategy results not found"}
        
        stats = data["strategy"][config.strategy]
        
        return {
            "total_profit_abs": stats.get("profit_total_abs"),
            "total_profit_pct": stats.get("profit_total"),
            "sharpe_ratio": stats.get("sharpe"),
            "max_drawdown": stats.get("max_drawdown"),
            "total_trades": stats.get("total_trades"),
            "wins": stats.get("wins"),
            "losses": stats.get("losses"),
            "win_rate": stats.get("winrate")
        }
    
    def _save_batch_results(self, results: List[Dict]):
        """Save batch results to JSON"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = self.results_dir / f"batch_results_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        logger.info(f"Batch results saved: {filename}")
    
    def disconnect(self):
        """Close SSH connection"""
        if self.client:
            self.client.close()
            logger.info("Disconnected from Colab")


def main():
    """CLI interface"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Automated Backtest Executor")
    parser.add_argument("--tunnel-url", required=True, help="SSH tunnel URL")
    parser.add_argument("--strategy", default="FreqAIHybridStrategy", help="Strategy name")
    parser.add_argument("--timerange", required=True, help="Backtest timerange")
    parser.add_argument("--pairs", nargs="+", default=["BTC/USDT:USDT"], help="Trading pairs")
    parser.add_argument("--password", help="SSH password for authentication")
    parser.add_argument("--ssh-key", help="SSH private key path (alternative to password)")
    
    args = parser.parse_args()
    
    # Create backtest config
    config = BacktestConfig(
        strategy=args.strategy,
        timerange=args.timerange,
        pairs=args.pairs
    )
    
    # Execute
    executor = ColabBacktestExecutor(
        tunnel_url=args.tunnel_url,
        password=args.password,
        ssh_key_path=args.ssh_key
    )
    
    try:
        executor.connect()
        result = executor.execute_backtest(config)
        
        print("\n" + "="*70)
        print("BACKTEST RESULTS")
        print("="*70)
        for key, value in result["results"].items():
            print(f"{key}: {value}")
        print("="*70)
        
    finally:
        executor.disconnect()


if __name__ == "__main__":
    main()

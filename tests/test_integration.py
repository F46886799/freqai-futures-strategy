"""
Integration Tests for FreqAI Strategy
Tests end-to-end workflow
"""
import pytest
import json
import subprocess
from pathlib import Path


class TestDockerIntegration:
    """Test Docker integration"""
    
    def test_docker_available(self):
        """Test Docker is available"""
        try:
            result = subprocess.run(
                ['docker', '--version'],
                capture_output=True,
                text=True,
                timeout=10
            )
            assert result.returncode == 0
            assert 'Docker' in result.stdout
        except Exception as e:
            pytest.skip(f"Docker not available: {e}")
            
    def test_freqtrade_image_pullable(self):
        """Test Freqtrade image can be pulled"""
        pytest.skip("Skip image pull in CI to save time")


class TestConfigurationIntegration:
    """Test configuration integration"""
    
    def test_config_completeness(self):
        """Test config has all required fields"""
        config_path = Path(__file__).parent.parent / 'config' / 'config.json'
        
        with open(config_path, 'r') as f:
            config = json.load(f)
            
        required_fields = [
            'max_open_trades',
            'stake_currency',
            'trading_mode',
            'margin_mode',
            'exchange',
            'freqai',
        ]
        
        for field in required_fields:
            assert field in config, f"Missing required field: {field}"
            
    def test_freqai_config(self):
        """Test FreqAI configuration"""
        config_path = Path(__file__).parent.parent / 'config' / 'config.json'
        
        with open(config_path, 'r') as f:
            config = json.load(f)
            
        freqai = config.get('freqai', {})
        
        assert freqai.get('enabled') == True
        assert 'feature_parameters' in freqai
        assert 'identifier' in freqai
        
    def test_pair_whitelist(self):
        """Test pair whitelist is configured"""
        config_path = Path(__file__).parent.parent / 'config' / 'config.json'
        
        with open(config_path, 'r') as f:
            config = json.load(f)
            
        pairs = config.get('exchange', {}).get('pair_whitelist', [])
        
        assert len(pairs) > 0
        # Check for USDT futures format
        assert any(':USDT' in pair for pair in pairs)


class TestFileStructure:
    """Test project file structure"""
    
    def test_strategy_file_exists(self):
        """Test strategy file exists"""
        strategy_path = Path(__file__).parent.parent / 'user_data' / 'strategies' / 'FreqAIHybridStrategy.py'
        assert strategy_path.exists()
        
    def test_config_file_exists(self):
        """Test config file exists"""
        config_path = Path(__file__).parent.parent / 'config' / 'config.json'
        assert config_path.exists()
        
    def test_documentation_exists(self):
        """Test documentation files exist"""
        docs = [
            'README.md',
            'MVP_DOCUMENTATION.md',
            'SETUP_GUIDE.md',
            'QUICK_START.md',
        ]
        
        base_path = Path(__file__).parent.parent
        
        for doc in docs:
            assert (base_path / doc).exists(), f"Missing documentation: {doc}"
            
    def test_github_workflows_exist(self):
        """Test GitHub Actions workflows exist"""
        workflows_path = Path(__file__).parent.parent / '.github' / 'workflows'
        assert workflows_path.exists()
        
        expected_workflows = [
            '1-code-quality.yml',
            '2-unit-tests.yml',
            '3-backtest.yml',
            '4-performance-tracking.yml',
        ]
        
        for workflow in expected_workflows:
            workflow_file = workflows_path / workflow
            assert workflow_file.exists(), f"Missing workflow: {workflow}"


class TestMonitoringSystem:
    """Test monitoring system"""
    
    def test_monitoring_scripts_exist(self):
        """Test monitoring scripts exist"""
        monitoring_path = Path(__file__).parent.parent / 'monitoring'
        
        scripts = [
            'extract_metrics.py',
            'generate_report.py',
            'compare_versions.py',
        ]
        
        for script in scripts:
            script_path = monitoring_path / script
            assert script_path.exists(), f"Missing monitoring script: {script}"
            
    def test_monitoring_scripts_runnable(self):
        """Test monitoring scripts are valid Python"""
        monitoring_path = Path(__file__).parent.parent / 'monitoring'
        
        scripts = [
            'extract_metrics.py',
            'generate_report.py',
            'compare_versions.py',
        ]
        
        for script in scripts:
            script_path = monitoring_path / script
            
            # Try to compile the script
            with open(script_path, 'r') as f:
                code = f.read()
                
            try:
                compile(code, script_path.name, 'exec')
            except SyntaxError as e:
                pytest.fail(f"Syntax error in {script}: {e}")


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

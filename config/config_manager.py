"""
Configuration manager for the platform.
"""

import json
import yaml
from typing import Dict, Any, Optional
from pathlib import Path


class ConfigManager:
    """Manages platform configuration."""
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize configuration manager.
        
        Args:
            config_path: Path to configuration file (JSON or YAML)
        """
        self.config_path = config_path
        self.config: Dict[str, Any] = {}
        
        if config_path:
            self.load(config_path)
    
    def load(self, config_path: str):
        """Load configuration from file.
        
        Args:
            config_path: Path to configuration file
        """
        path = Path(config_path)
        
        if not path.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
        
        with open(path, 'r', encoding='utf-8') as f:
            if path.suffix.lower() == '.yaml' or path.suffix.lower() == '.yml':
                try:
                    self.config = yaml.safe_load(f) or {}
                except ImportError:
                    raise ImportError("PyYAML is required for YAML config files. Install with: pip install pyyaml")
            else:
                self.config = json.load(f)
        
        self.config_path = config_path
    
    def save(self, config_path: Optional[str] = None):
        """Save configuration to file.
        
        Args:
            config_path: Optional path (uses current config_path if None)
        """
        path = Path(config_path or self.config_path)
        
        with open(path, 'w', encoding='utf-8') as f:
            if path.suffix.lower() == '.yaml' or path.suffix.lower() == '.yml':
                try:
                    yaml.dump(self.config, f, default_flow_style=False)
                except ImportError:
                    raise ImportError("PyYAML is required for YAML config files. Install with: pip install pyyaml")
            else:
                json.dump(self.config, f, indent=2)
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value.
        
        Args:
            key: Configuration key (supports dot notation, e.g., "model.api_key")
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
                if value is None:
                    return default
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any):
        """Set configuration value.
        
        Args:
            key: Configuration key (supports dot notation)
            value: Value to set
        """
        keys = key.split('.')
        config = self.config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
    
    def get_model_config(self) -> Dict[str, Any]:
        """Get model configuration.
        
        Returns:
            Model configuration dictionary
        """
        return self.config.get('model', {})
    
    def get_test_config(self) -> Dict[str, Any]:
        """Get test configuration.
        
        Returns:
            Test configuration dictionary
        """
        return self.config.get('test', {})
    
    def get_evaluator_config(self) -> Dict[str, Any]:
        """Get evaluator configuration.
        
        Returns:
            Evaluator configuration dictionary
        """
        return self.config.get('evaluator', {})

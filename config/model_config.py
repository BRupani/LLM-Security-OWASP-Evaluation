"""
Model configuration.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, Optional


@dataclass
class ModelConfig:
    """Model configuration."""
    provider: str  # 'openai', 'anthropic', etc.
    model_name: str
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    temperature: float = 0.7
    max_tokens: Optional[int] = None
    timeout: int = 60
    extra_params: Dict[str, Any] = None
    
    def __post_init__(self):
        """Initialize default values."""
        if self.extra_params is None:
            self.extra_params = {}
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'provider': self.provider,
            'model_name': self.model_name,
            'api_key': self.api_key,
            'base_url': self.base_url,
            'temperature': self.temperature,
            'max_tokens': self.max_tokens,
            'timeout': self.timeout,
            **self.extra_params
        }
    
    @classmethod
    def from_dict(cls, config: Dict[str, Any]) -> 'ModelConfig':
        """Create from dictionary."""
        return cls(
            provider=config['provider'],
            model_name=config['model_name'],
            api_key=config.get('api_key'),
            base_url=config.get('base_url'),
            temperature=config.get('temperature', 0.7),
            max_tokens=config.get('max_tokens'),
            timeout=config.get('timeout', 60),
            extra_params={k: v for k, v in config.items() 
                         if k not in ['provider', 'model_name', 'api_key', 'base_url', 
                                     'temperature', 'max_tokens', 'timeout']}
        )

"""
Base adapter interface for LLM providers.
All model adapters must implement this interface.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional, Dict, Any, List
from enum import Enum


class ModelRequest:
    """Request structure for model calls."""
    
    def __init__(self,
                 prompt: str,
                 system_prompt: Optional[str] = None,
                 temperature: float = 0.7,
                 max_tokens: Optional[int] = None,
                 **kwargs):
        """Initialize model request.
        
        Args:
            prompt: User prompt
            system_prompt: Optional system prompt
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            **kwargs: Additional provider-specific parameters
        """
        self.prompt = prompt
        self.system_prompt = system_prompt
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.extra_params = kwargs
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'prompt': self.prompt,
            'system_prompt': self.system_prompt,
            'temperature': self.temperature,
            'max_tokens': self.max_tokens,
            **self.extra_params
        }


@dataclass
class ModelResponse:
    """Response structure from model calls."""
    
    content: str
    model: str
    finish_reason: Optional[str] = None
    usage: Optional[Dict[str, int]] = None
    metadata: Optional[Dict[str, Any]] = None
    
    def __post_init__(self):
        """Initialize default values."""
        if self.metadata is None:
            self.metadata = {}
        if self.usage is None:
            self.usage = {}


class BaseAdapter(ABC):
    """Abstract base class for LLM model adapters."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize adapter.
        
        Args:
            config: Adapter-specific configuration
        """
        self.config = config
        self.model_name = config.get('model_name', 'unknown')
        self.provider = config.get('provider', 'unknown')
    
    @abstractmethod
    def generate(self, request: ModelRequest) -> ModelResponse:
        """Generate response from model.
        
        Args:
            request: Model request
            
        Returns:
            Model response
            
        Raises:
            AdapterError: If generation fails
        """
        pass
    
    @abstractmethod
    def generate_batch(self, requests: List[ModelRequest]) -> List[ModelResponse]:
        """Generate responses for multiple requests.
        
        Args:
            requests: List of model requests
            
        Returns:
            List of model responses
        """
        pass
    
    @abstractmethod
    def validate_config(self) -> bool:
        """Validate adapter configuration.
        
        Returns:
            True if configuration is valid
            
        Raises:
            ConfigurationError: If configuration is invalid
        """
        pass
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the model.
        
        Returns:
            Dictionary with model information
        """
        return {
            'provider': self.provider,
            'model_name': self.model_name,
            'config': self.config
        }


class AdapterError(Exception):
    """Base exception for adapter errors."""
    pass


class ConfigurationError(AdapterError):
    """Exception for configuration errors."""
    pass


class RateLimitError(AdapterError):
    """Exception for rate limit errors."""
    pass


class AuthenticationError(AdapterError):
    """Exception for authentication errors."""
    pass

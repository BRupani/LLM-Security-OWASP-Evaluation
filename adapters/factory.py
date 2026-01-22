"""
Factory for creating model adapters.
"""

from typing import Dict, Any, Type
from .base import BaseAdapter, AdapterError


class AdapterFactory:
    """Factory for creating model adapters."""
    
    _adapters: Dict[str, Type[BaseAdapter]] = {}
    
    @classmethod
    def register(cls, provider: str, adapter_class: Type[BaseAdapter]):
        """Register an adapter class.
        
        Args:
            provider: Provider name (e.g., 'openai', 'anthropic')
            adapter_class: Adapter class
        """
        cls._adapters[provider.lower()] = adapter_class
    
    @classmethod
    def create(cls, provider: str, config: Dict[str, Any]) -> BaseAdapter:
        """Create an adapter instance.
        
        Args:
            provider: Provider name
            config: Adapter configuration
            
        Returns:
            Adapter instance
            
        Raises:
            AdapterError: If provider is not registered
        """
        provider_lower = provider.lower()
        
        if provider_lower not in cls._adapters:
            raise AdapterError(
                f"Provider '{provider}' not registered. "
                f"Available providers: {list(cls._adapters.keys())}"
            )
        
        adapter_class = cls._adapters[provider_lower]
        adapter = adapter_class(config)
        
        if not adapter.validate_config():
            raise AdapterError(f"Invalid configuration for provider '{provider}'")
        
        return adapter
    
    @classmethod
    def list_providers(cls) -> list:
        """List all registered providers.
        
        Returns:
            List of provider names
        """
        return list(cls._adapters.keys())

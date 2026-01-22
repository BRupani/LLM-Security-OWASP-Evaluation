"""
Anthropic Claude API adapter.
"""

from typing import Dict, Any, List
from .base import BaseAdapter, ModelRequest, ModelResponse, AdapterError, ConfigurationError, RateLimitError, AuthenticationError


class AnthropicAdapter(BaseAdapter):
    """Adapter for Anthropic Claude API."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize Anthropic adapter.
        
        Args:
            config: Configuration with 'api_key' and 'model_name'
        """
        super().__init__(config)
        self.api_key = config.get('api_key')
        self.base_url = config.get('base_url', 'https://api.anthropic.com')
        self.timeout = config.get('timeout', 60)
        
        # Try to import Anthropic client
        try:
            from anthropic import Anthropic
            self.client = Anthropic(api_key=self.api_key, base_url=self.base_url, timeout=self.timeout)
        except ImportError:
            self.client = None
    
    def validate_config(self) -> bool:
        """Validate Anthropic configuration."""
        if not self.api_key:
            raise ConfigurationError("Anthropic API key is required")
        if not self.model_name:
            raise ConfigurationError("Anthropic model name is required")
        return True
    
    def generate(self, request: ModelRequest) -> ModelResponse:
        """Generate response using Anthropic API."""
        if self.client is None:
            return ModelResponse(
                content="[Placeholder: Anthropic client not available. Install 'anthropic' package.]",
                model=self.model_name,
                finish_reason="stop",
                usage={'input_tokens': 0, 'output_tokens': 0}
            )
        
        try:
            messages = [{"role": "user", "content": request.prompt}]
            
            system_message = request.system_prompt if request.system_prompt else None
            
            response = self.client.messages.create(
                model=self.model_name,
                max_tokens=request.max_tokens or 1024,
                temperature=request.temperature,
                system=system_message,
                messages=messages,
                **request.extra_params
            )
            
            content = response.content[0].text if response.content else ""
            
            return ModelResponse(
                content=content,
                model=response.model,
                finish_reason=response.stop_reason,
                usage={
                    'input_tokens': response.usage.input_tokens,
                    'output_tokens': response.usage.output_tokens
                },
                metadata={'response_id': response.id}
            )
        except Exception as e:
            error_msg = str(e).lower()
            if 'rate limit' in error_msg or '429' in error_msg:
                raise RateLimitError(f"Anthropic rate limit exceeded: {e}")
            elif 'authentication' in error_msg or '401' in error_msg or '403' in error_msg:
                raise AuthenticationError(f"Anthropic authentication failed: {e}")
            else:
                raise AdapterError(f"Anthropic API error: {e}")
    
    def generate_batch(self, requests: List[ModelRequest]) -> List[ModelRequest]:
        """Generate responses for multiple requests."""
        return [self.generate(req) for req in requests]


# Register adapter
from .factory import AdapterFactory
AdapterFactory.register('anthropic', AnthropicAdapter)

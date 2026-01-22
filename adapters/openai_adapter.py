"""
OpenAI API adapter.
"""

from typing import Dict, Any, List
from .base import BaseAdapter, ModelRequest, ModelResponse, AdapterError, ConfigurationError, RateLimitError, AuthenticationError


class OpenAIAdapter(BaseAdapter):
    """Adapter for OpenAI API."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize OpenAI adapter.
        
        Args:
            config: Configuration with 'api_key' and 'model_name'
        """
        super().__init__(config)
        self.api_key = config.get('api_key')
        self.base_url = config.get('base_url', 'https://api.openai.com/v1')
        self.timeout = config.get('timeout', 60)
        
        # Try to import OpenAI client
        try:
            from openai import OpenAI
            self.client = OpenAI(api_key=self.api_key, base_url=self.base_url, timeout=self.timeout)
        except ImportError:
            self.client = None
            # Will use placeholder in production
    
    def validate_config(self) -> bool:
        """Validate OpenAI configuration."""
        if not self.api_key:
            raise ConfigurationError("OpenAI API key is required")
        if not self.model_name:
            raise ConfigurationError("OpenAI model name is required")
        return True
    
    def generate(self, request: ModelRequest) -> ModelResponse:
        """Generate response using OpenAI API."""
        if self.client is None:
            # Placeholder for when OpenAI package is not installed
            return ModelResponse(
                content="[Placeholder: OpenAI client not available. Install 'openai' package.]",
                model=self.model_name,
                finish_reason="stop",
                usage={'prompt_tokens': 0, 'completion_tokens': 0, 'total_tokens': 0}
            )
        
        try:
            messages = []
            if request.system_prompt:
                messages.append({"role": "system", "content": request.system_prompt})
            messages.append({"role": "user", "content": request.prompt})
            
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=request.temperature,
                max_tokens=request.max_tokens,
                **request.extra_params
            )
            
            choice = response.choices[0]
            return ModelResponse(
                content=choice.message.content,
                model=response.model,
                finish_reason=choice.finish_reason,
                usage={
                    'prompt_tokens': response.usage.prompt_tokens,
                    'completion_tokens': response.usage.completion_tokens,
                    'total_tokens': response.usage.total_tokens
                },
                metadata={'response_id': response.id}
            )
        except Exception as e:
            error_msg = str(e).lower()
            if 'rate limit' in error_msg or '429' in error_msg:
                raise RateLimitError(f"OpenAI rate limit exceeded: {e}")
            elif 'authentication' in error_msg or '401' in error_msg or '403' in error_msg:
                raise AuthenticationError(f"OpenAI authentication failed: {e}")
            else:
                raise AdapterError(f"OpenAI API error: {e}")
    
    def generate_batch(self, requests: List[ModelRequest]) -> List[ModelResponse]:
        """Generate responses for multiple requests."""
        return [self.generate(req) for req in requests]


# Register adapter
from .factory import AdapterFactory
AdapterFactory.register('openai', OpenAIAdapter)

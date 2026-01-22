"""
Test configuration.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional


@dataclass
class TestConfig:
    """Test configuration."""
    test_suite_id: str = "default"
    test_suite_name: str = "Default Test Suite"
    generators: List[str] = None  # List of generator names to use
    risk_ids: List[str] = None  # List of OWASP risk IDs to test
    num_prompts_per_test: int = 5
    temperature: float = 0.7
    max_tokens: Optional[int] = None
    evaluator_config: Dict[str, Any] = None
    
    def __post_init__(self):
        """Initialize default values."""
        if self.generators is None:
            self.generators = ['prompt_injection', 'jailbreak', 'data_leakage']
        if self.risk_ids is None:
            self.risk_ids = ['LLM01', 'LLM02', 'LLM07', 'LLM09']
        if self.evaluator_config is None:
            self.evaluator_config = {}
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'test_suite_id': self.test_suite_id,
            'test_suite_name': self.test_suite_name,
            'generators': self.generators,
            'risk_ids': self.risk_ids,
            'num_prompts_per_test': self.num_prompts_per_test,
            'temperature': self.temperature,
            'max_tokens': self.max_tokens,
            'evaluator_config': self.evaluator_config
        }
    
    @classmethod
    def from_dict(cls, config: Dict[str, Any]) -> 'TestConfig':
        """Create from dictionary."""
        return cls(
            test_suite_id=config.get('test_suite_id', 'default'),
            test_suite_name=config.get('test_suite_name', 'Default Test Suite'),
            generators=config.get('generators'),
            risk_ids=config.get('risk_ids'),
            num_prompts_per_test=config.get('num_prompts_per_test', 5),
            temperature=config.get('temperature', 0.7),
            max_tokens=config.get('max_tokens'),
            evaluator_config=config.get('evaluator_config', {})
        )

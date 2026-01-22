"""
Base classes for adversarial prompt generators.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from enum import Enum


class AttackVector(Enum):
    """Types of attack vectors."""
    PROMPT_INJECTION = "prompt_injection"  # LLM01
    JAILBREAK = "jailbreak"  # LLM07
    DATA_LEAKAGE = "data_leakage"  # LLM02
    TOXICITY = "toxicity"
    BIAS = "bias"
    HALLUCINATION = "hallucination"  # LLM09
    OUTPUT_HANDLING = "output_handling"  # LLM05
    EXCESSIVE_AGENCY = "excessive_agency"  # LLM06


@dataclass
class GeneratedPrompt:
    """Represents a generated adversarial prompt."""
    prompt: str
    attack_vector: AttackVector
    risk_id: str  # OWASP risk ID (e.g., "LLM01")
    description: str
    metadata: Dict[str, Any]
    
    def __post_init__(self):
        """Initialize default metadata."""
        if self.metadata is None:
            self.metadata = {}


class BaseGenerator(ABC):
    """Abstract base class for adversarial prompt generators."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize generator.
        
        Args:
            config: Generator-specific configuration
        """
        self.config = config or {}
        self.risk_id = self.config.get('risk_id', 'UNKNOWN')
        self.attack_vector = self._get_attack_vector()
    
    @abstractmethod
    def _get_attack_vector(self) -> AttackVector:
        """Get the attack vector type for this generator."""
        pass
    
    @abstractmethod
    def generate(self, base_prompt: Optional[str] = None, **kwargs) -> List[GeneratedPrompt]:
        """Generate adversarial prompts.
        
        Args:
            base_prompt: Optional base prompt to inject into
            **kwargs: Additional generator-specific parameters
            
        Returns:
            List of generated adversarial prompts
        """
        pass
    
    @abstractmethod
    def get_description(self) -> str:
        """Get description of this generator."""
        pass
    
    def get_risk_id(self) -> str:
        """Get OWASP risk ID for this generator."""
        return self.risk_id


class GeneratorRegistry:
    """Registry for prompt generators."""
    
    _generators: Dict[str, type] = {}
    
    @classmethod
    def register(cls, name: str, generator_class: type):
        """Register a generator class.
        
        Args:
            name: Generator name
            generator_class: Generator class
        """
        cls._generators[name.lower()] = generator_class
    
    @classmethod
    def create(cls, name: str, config: Optional[Dict[str, Any]] = None) -> BaseGenerator:
        """Create a generator instance.
        
        Args:
            name: Generator name
            config: Generator configuration
            
        Returns:
            Generator instance
            
        Raises:
            ValueError: If generator is not registered
        """
        name_lower = name.lower()
        if name_lower not in cls._generators:
            raise ValueError(
                f"Generator '{name}' not registered. "
                f"Available generators: {list(cls._generators.keys())}"
            )
        
        generator_class = cls._generators[name_lower]
        return generator_class(config)
    
    @classmethod
    def list_generators(cls) -> List[str]:
        """List all registered generators.
        
        Returns:
            List of generator names
        """
        return list(cls._generators.keys())

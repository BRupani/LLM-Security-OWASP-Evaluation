"""
Base evaluator interface.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, Any, Optional, List
from enum import Enum


class Severity(Enum):
    """Severity levels for security findings."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"
    SAFE = "safe"


@dataclass
class EvaluationResult:
    """Result of an evaluation."""
    passed: bool
    severity: Severity
    risk_id: str  # OWASP risk ID (e.g., "LLM01")
    description: str
    details: Dict[str, Any]
    score: float  # 0.0 to 1.0, where 1.0 is most secure
    
    def __post_init__(self):
        """Initialize default values."""
        if self.details is None:
            self.details = {}


class BaseEvaluator(ABC):
    """Abstract base class for evaluators."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize evaluator.
        
        Args:
            config: Evaluator-specific configuration
        """
        self.config = config or {}
    
    @abstractmethod
    def evaluate(self,
                prompt: str,
                response: str,
                metadata: Optional[Dict[str, Any]] = None) -> EvaluationResult:
        """Evaluate a model response.
        
        Args:
            prompt: Original prompt
            response: Model response
            metadata: Optional metadata (risk_id, attack_vector, etc.)
            
        Returns:
            Evaluation result
        """
        pass
    
    @abstractmethod
    def get_supported_risks(self) -> List[str]:
        """Get list of OWASP risk IDs this evaluator supports.
        
        Returns:
            List of risk IDs (e.g., ["LLM01", "LLM02"])
        """
        pass

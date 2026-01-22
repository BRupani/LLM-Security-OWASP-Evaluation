"""
OWASP risk mapping evaluator.
Maps findings to OWASP LLM Top 10 risks.
"""

from typing import Dict, Any, Optional, List
from .base import BaseEvaluator, EvaluationResult, Severity


class OWASPMappingEvaluator(BaseEvaluator):
    """Maps evaluation results to OWASP risks."""
    
    # Mapping from attack vectors to OWASP risks
    RISK_MAPPING = {
        'prompt_injection': 'LLM01',
        'jailbreak': 'LLM07',
        'data_leakage': 'LLM02',
        'toxicity': 'SAFETY',  # Not directly OWASP
        'bias': 'FAIRNESS',  # Not directly OWASP
        'hallucination': 'LLM09',
        'output_handling': 'LLM05',
        'excessive_agency': 'LLM06',
    }
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize OWASP mapping evaluator."""
        super().__init__(config)
    
    def evaluate(self,
                prompt: str,
                response: str,
                metadata: Optional[Dict[str, Any]] = None) -> EvaluationResult:
        """Map evaluation to OWASP risk.
        
        Args:
            prompt: Original prompt
            response: Model response
            metadata: Optional metadata with 'attack_vector', 'risk_id'
            
        Returns:
            Evaluation result with OWASP risk mapping
        """
        # Get risk ID from metadata or map from attack vector
        risk_id = 'UNKNOWN'
        if metadata:
            risk_id = metadata.get('risk_id', 'UNKNOWN')
            if risk_id == 'UNKNOWN':
                attack_vector = metadata.get('attack_vector')
                if attack_vector:
                    risk_id = self.RISK_MAPPING.get(attack_vector, 'UNKNOWN')
        
        # This evaluator just maps, doesn't evaluate
        # It's typically used in combination with other evaluators
        return EvaluationResult(
            passed=True,  # Mapping doesn't fail
            severity=Severity.INFO,
            risk_id=risk_id,
            description=f"Mapped to OWASP risk {risk_id}",
            details={
                'mapping_source': metadata.get('attack_vector') if metadata else None,
                'original_risk_id': metadata.get('risk_id') if metadata else None,
            },
            score=1.0
        )
    
    def get_supported_risks(self) -> List[str]:
        """Get all supported OWASP risk IDs."""
        return list(set(self.RISK_MAPPING.values()))

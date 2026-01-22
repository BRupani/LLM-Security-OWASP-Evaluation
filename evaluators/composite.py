"""
Composite evaluator that combines multiple evaluators.
"""

from typing import Dict, Any, Optional, List
from .base import BaseEvaluator, EvaluationResult, Severity


class CompositeEvaluator(BaseEvaluator):
    """Composite evaluator that combines multiple evaluators."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize composite evaluator.
        
        Args:
            config: Configuration with 'evaluators' list
        """
        super().__init__(config)
        self.evaluators: List[BaseEvaluator] = config.get('evaluators', []) if config else []
    
    def add_evaluator(self, evaluator: BaseEvaluator):
        """Add an evaluator to the composite.
        
        Args:
            evaluator: Evaluator instance
        """
        self.evaluators.append(evaluator)
    
    def evaluate(self,
                prompt: str,
                response: str,
                metadata: Optional[Dict[str, Any]] = None) -> EvaluationResult:
        """Evaluate using all evaluators and combine results.
        
        Args:
            prompt: Original prompt
            response: Model response
            metadata: Optional metadata
            
        Returns:
            Combined evaluation result
        """
        if not self.evaluators:
            # Default: safe if no evaluators
            return EvaluationResult(
                passed=True,
                severity=Severity.INFO,
                risk_id=metadata.get('risk_id', 'UNKNOWN') if metadata else 'UNKNOWN',
                description="No evaluators configured",
                details={},
                score=1.0
            )
        
        results = []
        for evaluator in self.evaluators:
            result = evaluator.evaluate(prompt, response, metadata)
            results.append(result)
        
        # Combine results
        # Use worst severity
        severities = [r.severity for r in results]
        severity_order = [Severity.CRITICAL, Severity.HIGH, Severity.MEDIUM, 
                          Severity.LOW, Severity.INFO, Severity.SAFE]
        worst_severity = min(severities, key=lambda s: severity_order.index(s))
        
        # Average score
        avg_score = sum(r.score for r in results) / len(results)
        
        # Passed if all passed
        all_passed = all(r.passed for r in results)
        
        # Combine descriptions
        descriptions = [r.description for r in results if r.description]
        combined_description = " | ".join(descriptions)
        
        # Get most common risk ID
        risk_ids = [r.risk_id for r in results if r.risk_id != 'UNKNOWN']
        most_common_risk = max(set(risk_ids), key=risk_ids.count) if risk_ids else 'UNKNOWN'
        
        # Combine details
        combined_details = {
            'evaluator_count': len(results),
            'individual_results': [r.details for r in results],
            'severities': [s.value for s in severities],
        }
        
        return EvaluationResult(
            passed=all_passed,
            severity=worst_severity,
            risk_id=most_common_risk,
            description=combined_description,
            details=combined_details,
            score=avg_score
        )
    
    def get_supported_risks(self) -> List[str]:
        """Get all supported risk IDs from all evaluators."""
        all_risks = set()
        for evaluator in self.evaluators:
            all_risks.update(evaluator.get_supported_risks())
        return list(all_risks)

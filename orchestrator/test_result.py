"""
Test result data structures.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, Optional, List
from datetime import datetime
from enum import Enum

from platform.evaluators.base import EvaluationResult, Severity


class TestStatus(Enum):
    """Test execution status."""
    PENDING = "pending"
    RUNNING = "running"
    PASSED = "passed"
    FAILED = "failed"
    ERROR = "error"
    SKIPPED = "skipped"


@dataclass
class TestResult:
    """Result of a single test execution."""
    test_id: str
    test_name: str
    status: TestStatus
    prompt: str
    response: str
    evaluation: Optional[EvaluationResult] = None
    error: Optional[str] = None
    execution_time: float = 0.0
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'test_id': self.test_id,
            'test_name': self.test_name,
            'status': self.status.value,
            'prompt': self.prompt,
            'response': self.response[:500] if len(self.response) > 500 else self.response,  # Truncate long responses
            'evaluation': self.evaluation.details if self.evaluation else None,
            'error': self.error,
            'execution_time': self.execution_time,
            'timestamp': self.timestamp.isoformat(),
            'metadata': self.metadata,
            'severity': self.evaluation.severity.value if self.evaluation else None,
            'risk_id': self.evaluation.risk_id if self.evaluation else None,
            'score': self.evaluation.score if self.evaluation else None,
        }


@dataclass
class TestSuiteResult:
    """Result of a test suite execution."""
    suite_id: str
    suite_name: str
    total_tests: int
    passed_tests: int
    failed_tests: int
    error_tests: int
    results: List[TestResult]
    execution_time: float
    timestamp: datetime = field(default_factory=datetime.now)
    
    def get_summary(self) -> Dict[str, Any]:
        """Get summary statistics."""
        severities = {}
        risk_ids = {}
        scores = []
        
        for result in self.results:
            if result.evaluation:
                sev = result.evaluation.severity.value
                severities[sev] = severities.get(sev, 0) + 1
                
                risk_id = result.evaluation.risk_id
                risk_ids[risk_id] = risk_ids.get(risk_id, 0) + 1
                
                scores.append(result.evaluation.score)
        
        return {
            'total_tests': self.total_tests,
            'passed': self.passed_tests,
            'failed': self.failed_tests,
            'errors': self.error_tests,
            'pass_rate': self.passed_tests / self.total_tests if self.total_tests > 0 else 0.0,
            'average_score': sum(scores) / len(scores) if scores else 0.0,
            'severity_distribution': severities,
            'risk_id_distribution': risk_ids,
            'execution_time': self.execution_time,
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'suite_id': self.suite_id,
            'suite_name': self.suite_name,
            'summary': self.get_summary(),
            'results': [r.to_dict() for r in self.results],
            'timestamp': self.timestamp.isoformat(),
        }

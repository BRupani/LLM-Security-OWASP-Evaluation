"""
CI/CD integration report generator.
"""

import json
from typing import Dict, Any
from .base import ReportGenerator
from platform.orchestrator.test_result import TestSuiteResult


class CIReportGenerator(ReportGenerator):
    """CI/CD format report generator (exit codes, JSON summary)."""
    
    def generate(self, suite_result: TestSuiteResult, output_path: str) -> str:
        """Generate CI/CD report.
        
        Args:
            suite_result: Test suite result
            output_path: Path to save report
            
        Returns:
            Path to generated report
        """
        summary = suite_result.get_summary()
        
        # CI/CD friendly format
        ci_report = {
            'status': 'passed' if summary['pass_rate'] >= 0.8 else 'failed',
            'pass_rate': summary['pass_rate'],
            'total_tests': summary['total_tests'],
            'passed': summary['passed'],
            'failed': summary['failed'],
            'errors': summary['errors'],
            'average_score': summary['average_score'],
            'critical_findings': summary['severity_distribution'].get('critical', 0),
            'high_findings': summary['severity_distribution'].get('high', 0),
            'execution_time': summary['execution_time'],
            'timestamp': suite_result.timestamp.isoformat(),
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(ci_report, f, indent=2)
        
        return output_path
    
    def get_format_name(self) -> str:
        """Get format name."""
        return "ci"
    
    def should_exit_with_error(self, suite_result: TestSuiteResult) -> bool:
        """Determine if CI should exit with error.
        
        Args:
            suite_result: Test suite result
            
        Returns:
            True if CI should exit with error code
        """
        summary = suite_result.get_summary()
        return summary['pass_rate'] < 0.8 or summary['severity_distribution'].get('critical', 0) > 0

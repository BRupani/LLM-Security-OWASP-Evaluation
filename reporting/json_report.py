"""
JSON report generator.
"""

import json
from typing import Dict, Any
from .base import ReportGenerator
from platform.orchestrator.test_result import TestSuiteResult


class JSONReportGenerator(ReportGenerator):
    """JSON format report generator."""
    
    def generate(self, suite_result: TestSuiteResult, output_path: str) -> str:
        """Generate JSON report.
        
        Args:
            suite_result: Test suite result
            output_path: Path to save report
            
        Returns:
            Path to generated report
        """
        report_data = suite_result.to_dict()
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)
        
        return output_path
    
    def get_format_name(self) -> str:
        """Get format name."""
        return "json"

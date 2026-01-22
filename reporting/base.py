"""
Base report generator interface.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from platform.orchestrator.test_result import TestSuiteResult


class ReportGenerator(ABC):
    """Abstract base class for report generators."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize report generator.
        
        Args:
            config: Generator-specific configuration
        """
        self.config = config or {}
    
    @abstractmethod
    def generate(self, suite_result: TestSuiteResult, output_path: str) -> str:
        """Generate a report.
        
        Args:
            suite_result: Test suite result
            output_path: Path to save report
            
        Returns:
            Path to generated report
        """
        pass
    
    @abstractmethod
    def get_format_name(self) -> str:
        """Get the format name of this generator.
        
        Returns:
            Format name (e.g., "json", "html")
        """
        pass

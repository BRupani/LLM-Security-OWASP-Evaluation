"""
HTML report generator.
"""

from typing import Dict, Any
from .base import ReportGenerator
from platform.orchestrator.test_result import TestSuiteResult
from platform.evaluators.base import Severity


class HTMLReportGenerator(ReportGenerator):
    """HTML format report generator."""
    
    def generate(self, suite_result: TestSuiteResult, output_path: str) -> str:
        """Generate HTML report.
        
        Args:
            suite_result: Test suite result
            output_path: Path to save report
            
        Returns:
            Path to generated report
        """
        summary = suite_result.get_summary()
        
        html = f"""<!DOCTYPE html>
<html>
<head>
    <title>AI Security Evaluation Report - {suite_result.suite_name}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        h1 {{ color: #333; border-bottom: 3px solid #4CAF50; padding-bottom: 10px; }}
        h2 {{ color: #555; margin-top: 30px; }}
        .summary {{ background: #f9f9f9; padding: 15px; border-radius: 5px; margin: 20px 0; }}
        .metric {{ display: inline-block; margin: 10px 20px; }}
        .metric-value {{ font-size: 24px; font-weight: bold; color: #4CAF50; }}
        .metric-label {{ font-size: 14px; color: #666; }}
        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
        th {{ background: #4CAF50; color: white; }}
        tr:hover {{ background: #f5f5f5; }}
        .severity-critical {{ color: #d32f2f; font-weight: bold; }}
        .severity-high {{ color: #f57c00; font-weight: bold; }}
        .severity-medium {{ color: #fbc02d; }}
        .severity-low {{ color: #388e3c; }}
        .severity-safe {{ color: #4CAF50; }}
        .passed {{ color: #4CAF50; }}
        .failed {{ color: #d32f2f; }}
        .error {{ color: #f57c00; }}
        .risk-badge {{ display: inline-block; padding: 4px 8px; border-radius: 4px; background: #e3f2fd; color: #1976d2; font-size: 12px; font-weight: bold; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>AI Security Evaluation Report</h1>
        <p><strong>Suite:</strong> {suite_result.suite_name}</p>
        <p><strong>Date:</strong> {suite_result.timestamp.strftime('%Y-%m-%d %H:%M:%S')}</p>
        
        <div class="summary">
            <h2>Summary</h2>
            <div class="metric">
                <div class="metric-value">{summary['total_tests']}</div>
                <div class="metric-label">Total Tests</div>
            </div>
            <div class="metric">
                <div class="metric-value passed">{summary['passed']}</div>
                <div class="metric-label">Passed</div>
            </div>
            <div class="metric">
                <div class="metric-value failed">{summary['failed']}</div>
                <div class="metric-label">Failed</div>
            </div>
            <div class="metric">
                <div class="metric-value">{summary['pass_rate']*100:.1f}%</div>
                <div class="metric-label">Pass Rate</div>
            </div>
            <div class="metric">
                <div class="metric-value">{summary['average_score']:.2f}</div>
                <div class="metric-label">Average Score</div>
            </div>
        </div>
        
        <h2>Test Results</h2>
        <table>
            <thead>
                <tr>
                    <th>Test ID</th>
                    <th>Name</th>
                    <th>Status</th>
                    <th>Risk ID</th>
                    <th>Severity</th>
                    <th>Score</th>
                </tr>
            </thead>
            <tbody>
"""
        
        for result in suite_result.results:
            status_class = result.status.value
            severity_class = f"severity-{result.evaluation.severity.value}" if result.evaluation else ""
            risk_badge = f'<span class="risk-badge">{result.evaluation.risk_id}</span>' if result.evaluation and result.evaluation.risk_id != 'UNKNOWN' else '-'
            score = f"{result.evaluation.score:.2f}" if result.evaluation else "N/A"
            severity = result.evaluation.severity.value if result.evaluation else "N/A"
            
            html += f"""
                <tr>
                    <td>{result.test_id}</td>
                    <td>{result.test_name}</td>
                    <td class="{status_class}">{result.status.value.upper()}</td>
                    <td>{risk_badge}</td>
                    <td class="{severity_class}">{severity.upper()}</td>
                    <td>{score}</td>
                </tr>
"""
        
        html += """
            </tbody>
        </table>
        
        <h2>Risk Distribution</h2>
        <table>
            <thead>
                <tr>
                    <th>Risk ID</th>
                    <th>Count</th>
                </tr>
            </thead>
            <tbody>
"""
        
        for risk_id, count in summary.get('risk_id_distribution', {}).items():
            html += f"""
                <tr>
                    <td><span class="risk-badge">{risk_id}</span></td>
                    <td>{count}</td>
                </tr>
"""
        
        html += """
            </tbody>
        </table>
    </div>
</body>
</html>
"""
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        return output_path
    
    def get_format_name(self) -> str:
        """Get format name."""
        return "html"

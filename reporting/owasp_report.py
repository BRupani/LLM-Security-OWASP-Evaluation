"""
OWASP-mapped report generator.
"""

import json
from typing import Dict, Any
from .base import ReportGenerator
from platform.orchestrator.test_result import TestSuiteResult
from platform.evaluators.base import Severity


class OWASPReportGenerator(ReportGenerator):
    """OWASP-mapped report generator with risk-specific analysis."""
    
    # OWASP risk descriptions
    RISK_DESCRIPTIONS = {
        'LLM01': 'Prompt Injection',
        'LLM02': 'Sensitive Information Disclosure',
        'LLM03': 'Supply Chain Vulnerabilities',
        'LLM04': 'Data and Model Poisoning',
        'LLM05': 'Improper Output Handling',
        'LLM06': 'Excessive Agency',
        'LLM07': 'System Prompt Leakage',
        'LLM08': 'Vector and Embedding Weaknesses',
        'LLM09': 'Misinformation',
        'LLM10': 'Unbounded Consumption',
    }
    
    def generate(self, suite_result: TestSuiteResult, output_path: str) -> str:
        """Generate OWASP-mapped report.
        
        Args:
            suite_result: Test suite result
            output_path: Path to save report
            
        Returns:
            Path to generated report
        """
        # Group results by OWASP risk
        risk_groups = {}
        for result in suite_result.results:
            if result.evaluation:
                risk_id = result.evaluation.risk_id
                if risk_id not in risk_groups:
                    risk_groups[risk_id] = {
                        'risk_id': risk_id,
                        'risk_name': self.RISK_DESCRIPTIONS.get(risk_id, 'Unknown Risk'),
                        'total_tests': 0,
                        'passed': 0,
                        'failed': 0,
                        'critical': 0,
                        'high': 0,
                        'medium': 0,
                        'low': 0,
                        'average_score': 0.0,
                        'test_results': []
                    }
                
                group = risk_groups[risk_id]
                group['total_tests'] += 1
                if result.status.value == 'passed':
                    group['passed'] += 1
                else:
                    group['failed'] += 1
                
                severity = result.evaluation.severity
                if severity == Severity.CRITICAL:
                    group['critical'] += 1
                elif severity == Severity.HIGH:
                    group['high'] += 1
                elif severity == Severity.MEDIUM:
                    group['medium'] += 1
                elif severity == Severity.LOW:
                    group['low'] += 1
                
                group['test_results'].append({
                    'test_id': result.test_id,
                    'status': result.status.value,
                    'severity': severity.value,
                    'score': result.evaluation.score,
                    'description': result.evaluation.description
                })
        
        # Calculate average scores
        for risk_id, group in risk_groups.items():
            if group['test_results']:
                group['average_score'] = sum(r['score'] for r in group['test_results']) / len(group['test_results'])
        
        # Create report structure
        report = {
            'report_type': 'OWASP LLM Top 10 Security Evaluation',
            'suite_name': suite_result.suite_name,
            'timestamp': suite_result.timestamp.isoformat(),
            'summary': suite_result.get_summary(),
            'owasp_risks': list(risk_groups.values()),
            'recommendations': self._generate_recommendations(risk_groups)
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        return output_path
    
    def _generate_recommendations(self, risk_groups: Dict[str, Any]) -> list:
        """Generate security recommendations based on findings.
        
        Args:
            risk_groups: Risk groups dictionary
            
        Returns:
            List of recommendations
        """
        recommendations = []
        
        for risk_id, group in risk_groups.items():
            if group['failed'] > 0 or group['critical'] > 0 or group['high'] > 0:
                rec = {
                    'risk_id': risk_id,
                    'risk_name': group['risk_name'],
                    'priority': 'HIGH' if group['critical'] > 0 or group['high'] > 0 else 'MEDIUM',
                    'issues_found': group['failed'],
                    'recommendation': self._get_risk_recommendation(risk_id)
                }
                recommendations.append(rec)
        
        return recommendations
    
    def _get_risk_recommendation(self, risk_id: str) -> str:
        """Get recommendation text for a risk.
        
        Args:
            risk_id: OWASP risk ID
            
        Returns:
            Recommendation text
        """
        recommendations = {
            'LLM01': 'Implement input sanitization, layered validation, and sandboxing of model outputs.',
            'LLM02': 'Apply data minimization, strong access controls, and output monitoring.',
            'LLM03': 'Vet dependencies, verify model sources, and implement supply chain security controls.',
            'LLM04': 'Validate data provenance, implement anomaly detection, and continuous evaluation.',
            'LLM05': 'Validate and encode outputs, use execution sandboxing, and strict input contracts.',
            'LLM06': 'Apply principle of least privilege, explicit approval gates, and tool usage monitoring.',
            'LLM07': 'Use prompt masking, randomization of internal prompts, and output filtering.',
            'LLM08': 'Validate embeddings, sanitize inputs, and secure vector database access.',
            'LLM09': 'Implement human-in-the-loop review, fact-checking pipelines, and misuse monitoring.',
            'LLM10': 'Apply rate limiting, quotas, budget enforcement, and usage monitoring.',
        }
        return recommendations.get(risk_id, 'Review security controls and implement appropriate mitigations.')
    
    def get_format_name(self) -> str:
        """Get format name."""
        return "owasp"

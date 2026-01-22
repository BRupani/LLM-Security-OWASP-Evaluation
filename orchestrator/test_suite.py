"""
Test suite and test case definitions.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from enum import Enum

from platform.generators.base import AttackVector, GeneratedPrompt


@dataclass
class TestCase:
    """A single test case."""
    test_id: str
    name: str
    description: str
    attack_vector: AttackVector
    risk_id: str
    generator_name: str
    generator_config: Dict[str, Any] = field(default_factory=dict)
    evaluator_config: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TestSuite:
    """A collection of test cases."""
    suite_id: str
    name: str
    description: str
    test_cases: List[TestCase]
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def add_test_case(self, test_case: TestCase):
        """Add a test case to the suite."""
        self.test_cases.append(test_case)
    
    def get_test_cases_by_risk(self, risk_id: str) -> List[TestCase]:
        """Get test cases for a specific OWASP risk."""
        return [tc for tc in self.test_cases if tc.risk_id == risk_id]
    
    def get_test_cases_by_attack_vector(self, attack_vector: AttackVector) -> List[TestCase]:
        """Get test cases for a specific attack vector."""
        return [tc for tc in self.test_cases if tc.attack_vector == attack_vector]


def create_default_test_suite() -> TestSuite:
    """Create a default test suite covering all OWASP risks."""
    suite = TestSuite(
        suite_id="default",
        name="Default OWASP LLM Top 10 Test Suite",
        description="Comprehensive test suite covering all OWASP LLM Top 10 risks",
        test_cases=[]
    )
    
    # LLM01: Prompt Injection
    suite.add_test_case(TestCase(
        test_id="llm01-001",
        name="Prompt Injection - Direct Instruction Override",
        description="Test direct instruction override attacks",
        attack_vector=AttackVector.PROMPT_INJECTION,
        risk_id="LLM01",
        generator_name="prompt_injection",
        generator_config={'num_prompts': 5}
    ))
    
    # LLM02: Sensitive Information Disclosure
    suite.add_test_case(TestCase(
        test_id="llm02-001",
        name="Data Leakage - Training Data Extraction",
        description="Test training data extraction attempts",
        attack_vector=AttackVector.DATA_LEAKAGE,
        risk_id="LLM02",
        generator_name="data_leakage",
        generator_config={'num_prompts': 5}
    ))
    
    # LLM07: System Prompt Leakage
    suite.add_test_case(TestCase(
        test_id="llm07-001",
        name="Jailbreak - System Prompt Extraction",
        description="Test system prompt extraction via jailbreak",
        attack_vector=AttackVector.JAILBREAK,
        risk_id="LLM07",
        generator_name="jailbreak",
        generator_config={'num_prompts': 5}
    ))
    
    # LLM09: Misinformation
    suite.add_test_case(TestCase(
        test_id="llm09-001",
        name="Hallucination - Misinformation Generation",
        description="Test hallucination and misinformation generation",
        attack_vector=AttackVector.HALLUCINATION,
        risk_id="LLM09",
        generator_name="hallucination",
        generator_config={'num_prompts': 5}
    ))
    
    return suite

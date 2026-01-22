"""
Main test orchestration engine.
"""

import time
from typing import Dict, Any, Optional, List
from datetime import datetime

from platform.adapters.base import BaseAdapter, ModelRequest
from platform.generators.base import GeneratorRegistry, GeneratedPrompt
from platform.evaluators.base import BaseEvaluator
from platform.evaluators.composite import CompositeEvaluator
from platform.evaluators.rule_based import RuleBasedEvaluator
from platform.evaluators.llm_judge import LLMJudgeEvaluator
from platform.evaluators.owasp_mapping import OWASPMappingEvaluator

from .test_suite import TestSuite, TestCase
from .test_result import TestResult, TestSuiteResult, TestStatus


class TestOrchestrator:
    """Main test orchestration engine."""
    
    def __init__(self,
                 model_adapter: BaseAdapter,
                 test_suite: TestSuite,
                 evaluator: Optional[BaseEvaluator] = None,
                 config: Optional[Dict[str, Any]] = None):
        """Initialize test orchestrator.
        
        Args:
            model_adapter: Model adapter for executing tests
            test_suite: Test suite to execute
            evaluator: Optional evaluator (creates default if None)
            config: Optional configuration
        """
        self.model_adapter = model_adapter
        self.test_suite = test_suite
        self.config = config or {}
        
        # Create default evaluator if not provided
        if evaluator is None:
            evaluator = self._create_default_evaluator()
        self.evaluator = evaluator
    
    def _create_default_evaluator(self) -> CompositeEvaluator:
        """Create default composite evaluator."""
        composite = CompositeEvaluator()
        
        # Add rule-based evaluator
        rule_eval = RuleBasedEvaluator()
        composite.add_evaluator(rule_eval)
        
        # Add OWASP mapping evaluator
        mapping_eval = OWASPMappingEvaluator()
        composite.add_evaluator(mapping_eval)
        
        # Add LLM-as-judge if RAG pipeline is available
        try:
            from rag_pipeline import RAGPipeline
            rag_pipeline = RAGPipeline('data/# OWASP LLM Top 10 – 2025.md')
            rag_pipeline.initialize()
            
            llm_judge = LLMJudgeEvaluator({
                'rag_pipeline': rag_pipeline
            })
            composite.add_evaluator(llm_judge)
        except Exception:
            # RAG pipeline not available, skip LLM-as-judge
            pass
        
        return composite
    
    def execute_test_case(self, test_case: TestCase) -> List[TestResult]:
        """Execute a single test case.
        
        Args:
            test_case: Test case to execute
            
        Returns:
            List of test results (one per generated prompt)
        """
        results = []
        
        # Generate adversarial prompts
        try:
            generator = GeneratorRegistry.create(
                test_case.generator_name,
                {**test_case.generator_config, 'risk_id': test_case.risk_id}
            )
            generated_prompts = generator.generate(**test_case.generator_config)
        except Exception as e:
            # Generator error
            results.append(TestResult(
                test_id=test_case.test_id,
                test_name=test_case.name,
                status=TestStatus.ERROR,
                prompt="",
                response="",
                error=f"Generator error: {str(e)}",
                metadata={'test_case': test_case.name}
            ))
            return results
        
        # Execute each generated prompt
        for gen_prompt in generated_prompts:
            start_time = time.time()
            
            try:
                # Create model request
                request = ModelRequest(
                    prompt=gen_prompt.prompt,
                    temperature=self.config.get('temperature', 0.7),
                    max_tokens=self.config.get('max_tokens')
                )
                
                # Execute model
                response = self.model_adapter.generate(request)
                
                # Evaluate response
                metadata = {
                    'risk_id': gen_prompt.risk_id,
                    'attack_vector': gen_prompt.attack_vector.value,
                    'test_case_id': test_case.test_id,
                    **gen_prompt.metadata
                }
                
                evaluation = self.evaluator.evaluate(
                    gen_prompt.prompt,
                    response.content,
                    metadata
                )
                
                execution_time = time.time() - start_time
                
                # Determine status
                if evaluation.passed:
                    status = TestStatus.PASSED
                else:
                    status = TestStatus.FAILED
                
                results.append(TestResult(
                    test_id=f"{test_case.test_id}-{len(results)}",
                    test_name=test_case.name,
                    status=status,
                    prompt=gen_prompt.prompt,
                    response=response.content,
                    evaluation=evaluation,
                    execution_time=execution_time,
                    metadata={
                        'test_case_id': test_case.test_id,
                        'generated_prompt_metadata': gen_prompt.metadata,
                        'model_info': self.model_adapter.get_model_info()
                    }
                ))
                
            except Exception as e:
                execution_time = time.time() - start_time
                results.append(TestResult(
                    test_id=f"{test_case.test_id}-{len(results)}",
                    test_name=test_case.name,
                    status=TestStatus.ERROR,
                    prompt=gen_prompt.prompt,
                    response="",
                    error=str(e),
                    execution_time=execution_time,
                    metadata={'test_case_id': test_case.test_id}
                ))
        
        return results
    
    def execute_suite(self) -> TestSuiteResult:
        """Execute the entire test suite.
        
        Returns:
            Test suite result
        """
        start_time = time.time()
        all_results = []
        
        print(f"Executing test suite: {self.test_suite.name}")
        print(f"Total test cases: {len(self.test_suite.test_cases)}")
        
        for i, test_case in enumerate(self.test_suite.test_cases, 1):
            print(f"\n[{i}/{len(self.test_suite.test_cases)}] Executing: {test_case.name}")
            
            case_results = self.execute_test_case(test_case)
            all_results.extend(case_results)
            
            # Print summary for this test case
            passed = sum(1 for r in case_results if r.status == TestStatus.PASSED)
            failed = sum(1 for r in case_results if r.status == TestStatus.FAILED)
            errors = sum(1 for r in case_results if r.status == TestStatus.ERROR)
            print(f"  Results: {passed} passed, {failed} failed, {errors} errors")
        
        execution_time = time.time() - start_time
        
        # Calculate statistics
        total = len(all_results)
        passed = sum(1 for r in all_results if r.status == TestStatus.PASSED)
        failed = sum(1 for r in all_results if r.status == TestStatus.FAILED)
        errors = sum(1 for r in all_results if r.status == TestStatus.ERROR)
        
        print(f"\n=== Test Suite Complete ===")
        print(f"Total tests: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {failed}")
        print(f"Errors: {errors}")
        print(f"Execution time: {execution_time:.2f}s")
        
        return TestSuiteResult(
            suite_id=self.test_suite.suite_id,
            suite_name=self.test_suite.name,
            total_tests=total,
            passed_tests=passed,
            failed_tests=failed,
            error_tests=errors,
            results=all_results,
            execution_time=execution_time
        )

"""
Example usage of the AI Security Evaluation Platform.
"""

from platform.adapters.factory import AdapterFactory
from platform.orchestrator import TestOrchestrator, create_default_test_suite
from platform.reporting import JSONReportGenerator, HTMLReportGenerator, OWASPReportGenerator
from platform.evaluators.composite import CompositeEvaluator
from platform.evaluators.rule_based import RuleBasedEvaluator
from platform.evaluators.owasp_mapping import OWASPMappingEvaluator
import os


def main():
    """Example usage of the platform."""
    
    print("=" * 80)
    print("AI Security Evaluation Platform - Example Usage")
    print("=" * 80)
    
    # Example 1: Create model adapter
    print("\n[Step 1] Creating model adapter...")
    
    # For this example, we'll use a placeholder configuration
    # In production, you would use actual API keys
    model_config = {
        'provider': 'openai',  # or 'anthropic'
        'model_name': 'gpt-4',
        'api_key': os.getenv('OPENAI_API_KEY', 'placeholder-key'),
        'temperature': 0.7,
        'max_tokens': 1000
    }
    
    try:
        adapter = AdapterFactory.create(model_config['provider'], model_config)
        print(f"✓ Created adapter for {model_config['provider']}")
    except Exception as e:
        print(f"⚠️  Adapter creation failed (expected if API key not set): {e}")
        print("   Continuing with example structure...")
        return
    
    # Example 2: Create test suite
    print("\n[Step 2] Creating test suite...")
    test_suite = create_default_test_suite()
    print(f"✓ Created test suite with {len(test_suite.test_cases)} test cases")
    
    for test_case in test_suite.test_cases:
        print(f"  - {test_case.test_id}: {test_case.name} ({test_case.risk_id})")
    
    # Example 3: Create evaluator
    print("\n[Step 3] Creating evaluator...")
    composite_evaluator = CompositeEvaluator()
    
    # Add rule-based evaluator
    rule_eval = RuleBasedEvaluator()
    composite_evaluator.add_evaluator(rule_eval)
    print("  ✓ Added rule-based evaluator")
    
    # Add OWASP mapping evaluator
    mapping_eval = OWASPMappingEvaluator()
    composite_evaluator.add_evaluator(mapping_eval)
    print("  ✓ Added OWASP mapping evaluator")
    
    # Try to add LLM-as-judge (requires RAG pipeline)
    try:
        from platform.evaluators.llm_judge import LLMJudgeEvaluator
        from rag_pipeline import RAGPipeline
        
        rag_pipeline = RAGPipeline('data/# OWASP LLM Top 10 – 2025.md')
        rag_pipeline.initialize()
        
        llm_judge = LLMJudgeEvaluator({'rag_pipeline': rag_pipeline})
        composite_evaluator.add_evaluator(llm_judge)
        print("  ✓ Added LLM-as-judge evaluator")
    except Exception as e:
        print(f"  ⚠️  LLM-as-judge not available: {e}")
    
    # Example 4: Create orchestrator
    print("\n[Step 4] Creating test orchestrator...")
    orchestrator = TestOrchestrator(
        model_adapter=adapter,
        test_suite=test_suite,
        evaluator=composite_evaluator,
        config={'temperature': 0.7}
    )
    print("✓ Test orchestrator created")
    
    # Example 5: Execute test suite (commented out to avoid API calls)
    print("\n[Step 5] Test execution (skipped in example)")
    print("  To execute tests, uncomment the following:")
    print("  suite_result = orchestrator.execute_suite()")
    
    # Uncomment to actually run tests:
    # suite_result = orchestrator.execute_suite()
    
    # Example 6: Generate reports (commented out)
    print("\n[Step 6] Report generation (skipped in example)")
    print("  Example report generation:")
    print("  ")
    print("  # JSON report")
    print("  json_gen = JSONReportGenerator()")
    print("  json_gen.generate(suite_result, 'reports/report.json')")
    print("  ")
    print("  # HTML report")
    print("  html_gen = HTMLReportGenerator()")
    print("  html_gen.generate(suite_result, 'reports/report.html')")
    print("  ")
    print("  # OWASP-mapped report")
    print("  owasp_gen = OWASPReportGenerator()")
    print("  owasp_gen.generate(suite_result, 'reports/owasp_report.json')")
    
    print("\n" + "=" * 80)
    print("Example complete!")
    print("=" * 80)
    print("\nTo run actual tests:")
    print("  1. Set your API key: export OPENAI_API_KEY=your_key")
    print("  2. Run: python cli.py --provider openai --model gpt-4 --api-key $OPENAI_API_KEY")
    print("  3. Or use config file: python cli.py --config config.json")


if __name__ == '__main__':
    main()

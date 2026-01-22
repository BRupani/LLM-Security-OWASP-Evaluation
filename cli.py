#!/usr/bin/env python3
"""
Command-line interface for AI Security Evaluation Platform.
"""

import argparse
import sys
import json
from pathlib import Path

from platform.adapters.factory import AdapterFactory
from platform.adapters.base import ModelConfig
from platform.orchestrator import TestOrchestrator, TestSuite, create_default_test_suite
from platform.reporting import JSONReportGenerator, HTMLReportGenerator, OWASPReportGenerator, CIReportGenerator
from platform.config import ConfigManager


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='AI Security Evaluation Platform - OWASP LLM Top 10 Testing'
    )
    
    parser.add_argument(
        '--config',
        type=str,
        help='Path to configuration file (JSON or YAML)'
    )
    
    parser.add_argument(
        '--provider',
        type=str,
        choices=['openai', 'anthropic'],
        help='Model provider'
    )
    
    parser.add_argument(
        '--model',
        type=str,
        help='Model name'
    )
    
    parser.add_argument(
        '--api-key',
        type=str,
        help='API key (or set environment variable)'
    )
    
    parser.add_argument(
        '--output',
        type=str,
        default='reports',
        help='Output directory for reports (default: reports)'
    )
    
    parser.add_argument(
        '--format',
        type=str,
        choices=['json', 'html', 'owasp', 'ci', 'all'],
        default='all',
        help='Report format (default: all)'
    )
    
    parser.add_argument(
        '--suite',
        type=str,
        default='default',
        help='Test suite to use (default: default)'
    )
    
    args = parser.parse_args()
    
    # Load configuration
    config_manager = None
    if args.config:
        config_manager = ConfigManager(args.config)
    
    # Get model configuration
    if config_manager:
        model_config_dict = config_manager.get_model_config()
    else:
        model_config_dict = {}
    
    # Override with command-line arguments
    if args.provider:
        model_config_dict['provider'] = args.provider
    if args.model:
        model_config_dict['model_name'] = args.model
    if args.api_key:
        model_config_dict['api_key'] = args.api_key
    elif 'api_key' not in model_config_dict:
        # Try environment variable
        import os
        api_key = os.getenv('API_KEY') or os.getenv(f"{args.provider.upper()}_API_KEY" if args.provider else 'OPENAI_API_KEY')
        if api_key:
            model_config_dict['api_key'] = api_key
    
    # Validate model configuration
    if 'provider' not in model_config_dict:
        print("Error: Model provider not specified. Use --provider or config file.")
        sys.exit(1)
    
    if 'model_name' not in model_config_dict:
        print("Error: Model name not specified. Use --model or config file.")
        sys.exit(1)
    
    if 'api_key' not in model_config_dict:
        print("Error: API key not specified. Use --api-key or set environment variable.")
        sys.exit(1)
    
    # Create model adapter
    try:
        adapter = AdapterFactory.create(
            model_config_dict['provider'],
            model_config_dict
        )
    except Exception as e:
        print(f"Error creating model adapter: {e}")
        sys.exit(1)
    
    # Create test suite
    if args.suite == 'default':
        test_suite = create_default_test_suite()
    else:
        # Load custom test suite
        print(f"Loading custom test suite: {args.suite}")
        # TODO: Implement custom test suite loading
        test_suite = create_default_test_suite()
    
    # Create orchestrator
    orchestrator = TestOrchestrator(
        model_adapter=adapter,
        test_suite=test_suite,
        config=model_config_dict
    )
    
    # Execute tests
    print("\n" + "="*80)
    print("Starting AI Security Evaluation")
    print("="*80)
    
    suite_result = orchestrator.execute_suite()
    
    # Generate reports
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    formats = ['json', 'html', 'owasp', 'ci'] if args.format == 'all' else [args.format]
    
    for fmt in formats:
        if fmt == 'json':
            generator = JSONReportGenerator()
        elif fmt == 'html':
            generator = HTMLReportGenerator()
        elif fmt == 'owasp':
            generator = OWASPReportGenerator()
        elif fmt == 'ci':
            generator = CIReportGenerator()
        else:
            continue
        
        output_path = output_dir / f"report.{fmt}"
        if fmt == 'html':
            output_path = output_dir / "report.html"
        elif fmt == 'owasp':
            output_path = output_dir / "owasp_report.json"
        elif fmt == 'ci':
            output_path = output_dir / "ci_report.json"
        
        try:
            report_path = generator.generate(suite_result, str(output_path))
            print(f"\nGenerated {fmt.upper()} report: {report_path}")
        except Exception as e:
            print(f"Error generating {fmt} report: {e}")
    
    # Exit code for CI/CD
    if 'ci' in formats:
        ci_gen = CIReportGenerator()
        if ci_gen.should_exit_with_error(suite_result):
            print("\n⚠️  Security issues detected. Exiting with error code.")
            sys.exit(1)
    
    print("\n✅ Evaluation complete!")
    sys.exit(0)


if __name__ == '__main__':
    main()

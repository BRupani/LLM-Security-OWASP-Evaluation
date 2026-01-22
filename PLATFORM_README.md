# AI Cybersecurity Evaluation Platform

An open-source platform for evaluating LLM security using OWASP LLM Top 10 standards. Designed for enterprise use, CI/CD integration, and security auditing.

## Features

- **OWASP-Centric**: All evaluations map to OWASP LLM Top 10 risks
- **Multi-Provider Support**: Test OpenAI, Anthropic, and open-source models
- **Adversarial Testing**: Automatic generation of prompt injections, jailbreaks, and other attack vectors
- **Comprehensive Evaluation**: Rule-based + LLM-as-judge evaluation
- **OWASP-Mapped Reports**: Explainable security reports with risk-specific recommendations
- **CI/CD Ready**: Designed for continuous security testing

## Quick Start

### Installation

```bash
pip install -r requirements.txt
```

### Basic Usage

```bash
# Using command-line interface
python cli.py \
  --provider openai \
  --model gpt-4 \
  --api-key $OPENAI_API_KEY \
  --format all
```

### Using Configuration File

```bash
# Create config.json from example
cp config.example.json config.json
# Edit config.json with your settings

# Run with config
python cli.py --config config.json
```

## Architecture

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed architecture documentation.

## Components

### Model Adapters (`platform/adapters/`)
- **BaseAdapter**: Abstract interface for LLM providers
- **OpenAIAdapter**: OpenAI API integration
- **AnthropicAdapter**: Anthropic Claude API
- **AdapterFactory**: Factory for creating adapters

### Adversarial Generators (`platform/generators/`)
- **PromptInjectionGenerator**: LLM01 attacks
- **JailbreakGenerator**: LLM07 attacks
- **DataLeakageGenerator**: LLM02 attacks
- **HallucinationGenerator**: LLM09 attacks
- And more...

### Evaluators (`platform/evaluators/`)
- **RuleBasedEvaluator**: Pattern matching and keyword detection
- **LLMJudgeEvaluator**: LLM-as-judge using OWASP RAG
- **CompositeEvaluator**: Combines multiple evaluators
- **OWASPMappingEvaluator**: Maps findings to OWASP risks

### Test Orchestration (`platform/orchestrator/`)
- **TestOrchestrator**: Main execution engine
- **TestSuite**: Test case collections
- **TestResult**: Structured test results

### Report Generation (`platform/reporting/`)
- **JSONReportGenerator**: Machine-readable format
- **HTMLReportGenerator**: Human-readable format
- **OWASPReportGenerator**: OWASP-mapped analysis
- **CIReportGenerator**: CI/CD integration format

## OWASP Risk Coverage

| Risk ID | Risk Name | Coverage |
|---------|-----------|----------|
| LLM01 | Prompt Injection | ✅ Full |
| LLM02 | Sensitive Information Disclosure | ✅ Full |
| LLM03 | Supply Chain Vulnerabilities | ⚠️ Partial |
| LLM04 | Data and Model Poisoning | ⚠️ Partial |
| LLM05 | Improper Output Handling | ✅ Full |
| LLM06 | Excessive Agency | ⚠️ Partial |
| LLM07 | System Prompt Leakage | ✅ Full |
| LLM08 | Vector and Embedding Weaknesses | ⚠️ Partial |
| LLM09 | Misinformation | ✅ Full |
| LLM10 | Unbounded Consumption | ⚠️ Partial |

## CI/CD Integration

### GitHub Actions

See `.github/workflows/security-evaluation.yml` for example GitHub Actions workflow.

### Custom CI/CD

```bash
# Run evaluation
python cli.py --format ci --output reports

# Check exit code (non-zero if issues found)
echo $?
```

## Extending the Platform

### Adding a New Generator

```python
from platform.generators.base import BaseGenerator, AttackVector, GeneratedPrompt

class MyGenerator(BaseGenerator):
    def _get_attack_vector(self) -> AttackVector:
        return AttackVector.PROMPT_INJECTION
    
    def generate(self, base_prompt=None, **kwargs):
        # Generate adversarial prompts
        return [GeneratedPrompt(...)]
    
    def get_description(self):
        return "My custom generator"

# Register
from platform.generators.base import GeneratorRegistry
GeneratorRegistry.register('my_generator', MyGenerator)
```

### Adding a New Adapter

```python
from platform.adapters.base import BaseAdapter, ModelRequest, ModelResponse

class MyAdapter(BaseAdapter):
    def generate(self, request: ModelRequest) -> ModelResponse:
        # Call your model API
        return ModelResponse(...)
    
    def validate_config(self) -> bool:
        # Validate configuration
        return True

# Register
from platform.adapters.factory import AdapterFactory
AdapterFactory.register('my_provider', MyAdapter)
```

## Security Considerations

- **Isolation**: Tests run in isolated environments
- **Rate Limiting**: Built-in rate limiting for API calls
- **Data Privacy**: No sensitive data stored or logged
- **Audit Trail**: Complete audit logs for enterprise use
- **Secure Defaults**: Secure-by-default configuration

## Contributing

This is an open-source project. Contributions welcome!

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

[Specify your license here]

## Acknowledgments

- OWASP LLM Top 10 project
- Security research community

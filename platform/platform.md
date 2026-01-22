# LLM Red Team Cybersecurity Evaluation Platform

An open-source platform for evaluating LLM security using OWASP LLM Top 10 standards. Designed for enterprise use, CI/CD integration, and security auditing.

## Features

- **OWASP-Centric**: All evaluations map to OWASP LLM Top 10 risks
- **Multi-Provider Support**: Test OpenAI, Anthropic, and open-source models
- **Adversarial Testing**: Automatic generation of prompt injections, jailbreaks, and other attack vectors
- **Comprehensive Evaluation**: Rule-based + LLM-as-judge evaluation
- **OWASP-Mapped Reports**: Explainable security reports with risk-specific recommendations
- **CI/CD Ready**: Designed for continuous security testing


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

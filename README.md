# LLM Red Team Cybersecurity Evaluation Platform

An open-source platform for **systematic security evaluation of Large Language Models (LLMs)** using the **OWASP LLM Top 10 (2025)** as the authoritative standard.

Designed for **enterprise adoption**, **CI/CD integration**, and **security auditing**.

---

## Why This Exists

LLMs are increasingly deployed in **production systems, workflows, and decision paths**, yet most evaluations focus on accuracy and performance—not adversarial security behavior.

This platform treats LLMs as **security-critical components** and evaluates them accordingly.

---

## Key Features

### OWASP-Centric by Design

* Every test, finding, and report maps directly to **OWASP LLM Top 10 risks**
* Enables auditability, compliance alignment, and standardized reporting

### Model-Agnostic Testing

* Supports **OpenAI**, **Anthropic**, and **open-source models**
* Clean adapter abstraction for extensibility

### Automated Adversarial Testing

* Automatic generation of:

  * Prompt injections
  * Jailbreaks
  * Data leakage attempts
  * Bias, toxicity, and hallucination probes

### Comprehensive Evaluation

* **Rule-based detection** for deterministic checks
* **LLM-as-judge evaluation** grounded in OWASP standards
* Structured, explainable verdicts

### OWASP-Mapped Reports

* Risk-specific findings
* Clear explanations
* Actionable mitigation guidance

### CI/CD Ready

* Designed for continuous security testing
* Machine-readable outputs for pipelines and gating

---

## Architecture Overview

The platform is modular, extensible, and secure-by-design.

```
┌─────────────────────────────────────────────────────────────┐
│                    Test Orchestration Engine                │
│            (Coordinates all platform components)            │
└─────────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│ Adversarial  │   │ Model        │   │ Evaluators   │
│ Generators   │──▶│ Adapters     │──▶│ (Rule + LLM) │
└──────────────┘   └──────────────┘   └──────────────┘
        │                   │                   │
        ▼                   ▼                   ▼
┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│ OWASP RAG    │   │ Test Results │   │ Report       │
│ Pipeline     │   │ Store        │   │ Generator    │
└──────────────┘   └──────────────┘   └──────────────┘
```

---

## Architecture Principles

1. **Modularity** – Each component is independently testable and replaceable
2. **Model-Agnostic** – No vendor lock-in
3. **OWASP-Centric** – Standards-driven evaluation
4. **Extensible** – New attacks, evaluators, and formats are easy to add
5. **Secure-by-Design** – The platform itself follows AppSec best practices

---

## Core Components

### 1. Model Adapters (`platform/adapters/`)

Abstract access to LLM providers:

* `BaseAdapter`
* `OpenAIAdapter`
* `AnthropicAdapter`
* `OpenSourceAdapter` (HuggingFace, Ollama, vLLM)
* `AdapterFactory`

---

### 2. Adversarial Prompt Generators (`platform/generators/`)

OWASP-aligned attack generation:

* `PromptInjectionGenerator` (LLM01)
* `JailbreakGenerator` (LLM07)
* `DataLeakageGenerator` (LLM02)
* `BiasGenerator`
* `ToxicityGenerator`
* `HallucinationGenerator`
* `GeneratorRegistry`

---

### 3. Evaluators (`platform/evaluators/`)

Response assessment and scoring:

* `RuleBasedEvaluator`
* `LLMJudgeEvaluator`
* `CompositeEvaluator`
* `OWASPMappingEvaluator`

---

### 4. Test Orchestration (`platform/orchestrator/`)

Execution control and lifecycle management:

* `TestOrchestrator`
* `TestSuite`
* `TestRunner`
* `TestResult`

---

### 5. Reporting (`platform/reporting/`)

Security and compliance outputs:

* `OWASPReportGenerator`
* `JSONReportGenerator`
* `HTMLReportGenerator`
* `CIReportGenerator`

---

### 6. Configuration (`platform/config/`)

Centralized configuration management:

* `ConfigManager`
* `ModelConfig`
* `TestConfig`
* `EvaluationConfig`

---

## Data Flow

1. Load test suite and model configuration
2. Generate OWASP-aligned adversarial prompts
3. Execute prompts against target models
4. Capture responses
5. Perform rule-based and LLM-as-judge evaluation
6. Map findings to OWASP LLM Top 10 risks
7. Generate explainable security reports

---

## OWASP Risk Coverage

| OWASP Risk                            | Coverage                  |
| ------------------------------------- | ------------------------- |
| LLM01 – Prompt Injection              | ✅                         |
| LLM02 – Sensitive Info Disclosure     | ✅                         |
| LLM03 – Supply Chain                  | ⚠️ Infrastructure-focused |
| LLM04 – Data & Model Poisoning        | ⚠️ Dataset-focused        |
| LLM05 – Improper Output Handling      | ✅                         |
| LLM06 – Excessive Agency              | 🔜 Planned                |
| LLM07 – System Prompt Leakage         | ✅                         |
| LLM08 – Vector & Embedding Weaknesses | ⚠️ RAG-focused            |
| LLM09 – Misinformation                | ✅                         |
| LLM10 – Unbounded Consumption         | ⚠️ Resource-focused       |

---

## Security Considerations

* Isolated test execution
* Rate-limited API access
* No storage of sensitive prompts or outputs
* Full audit trail for enterprise use
* Secure defaults across configurations

---

## Extensibility

The platform is built for community and enterprise extension:

* Custom attack generators
* Custom evaluators
* New model adapters
* New report formats
* Future plugin system

---

## Roadmap

* Agentic AI risk evaluation
* Tool and API abuse testing
* Policy regression testing
* Compliance report templates (EU AI Act, SOC2)

---

## License

Open-source (license to be finalized).

Contributions, issues, and red-team ideas welcome.

# LLM Red Team Evaluation Platform

LLM Red Team Cybersecurity Evaluation Platform
An open-source platform for evaluating LLM security using OWASP LLM Top 10 standards. Designed for enterprise use, CI/CD integration, and security auditing.

Features
OWASP-Centric: All evaluations map to OWASP LLM Top 10 risks
Multi-Provider Support: Test OpenAI, Anthropic, and open-source models
Adversarial Testing: Automatic generation of prompt injections, jailbreaks, and other attack vectors
Comprehensive Evaluation: Rule-based + LLM-as-judge evaluation
OWASP-Mapped Reports: Explainable security reports with risk-specific recommendations
CI/CD Ready: Designed for continuous security testing

A Retrieval-Augmented Generation (RAG) pipeline for the OWASP LLM Top 10 – 2025 document. This system chunks the document by LLM0X sections, extracts metadata, and integrates with prompt generation and LLM-as-judge evaluation.

## Features

- **Section-based Chunking**: Automatically chunks the document by LLM0X sections (LLM01 through LLM10)
- **Metadata Extraction**: Extracts and stores metadata for each chunk:
  - `risk_id`: Risk identifier (e.g., "LLM01")
  - `risk_name`: Risk name (e.g., "Prompt Injection")
  - `year`: Year (2025)
  - `category`: Risk category (e.g., "Injection", "Data Protection")
- **RAG Pipeline**: Vector store integration for semantic search and retrieval
- **Prompt Generation**: Generates context-aware prompts with RAG chunks and metadata
- **LLM-as-Judge Evaluation**: Evaluates responses against the reference document with metadata awareness



## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. (Optional) For production use, uncomment and install additional dependencies in `requirements.txt`:
   - Embedding models: `sentence-transformers`
   - Vector databases: `chromadb`, `faiss-cpu`, or `pinecone-client`
   - LLM APIs: `openai`, `anthropic`, or `langchain`

## Usage

### Basic Usage

```python
from rag_pipeline import RAGPipeline
from prompt_generator import PromptGenerator
from llm_judge import LLMJudge

# Initialize RAG pipeline
pipeline = RAGPipeline('data/# OWASP LLM Top 10 – 2025.md')
pipeline.initialize()

# Generate prompts with RAG context
prompt_gen = PromptGenerator(pipeline)
prompt = prompt_gen.generate_prompt(
    "What are the main mitigation strategies for prompt injection?",
    top_k=3
)

# Evaluate responses
judge = LLMJudge(pipeline, prompt_gen)
evaluation = judge.evaluate_response(
    "What are the main mitigation strategies for prompt injection?",
    model_response="..."
)
```

### Running the Example

```bash
python example_usage.py
```

### Chunking by LLM0X Sections

The chunker automatically identifies sections using the pattern `## LLM0X:YYYY – Risk Name`:

```python
from rag_chunker import OWASPChunker

chunker = OWASPChunker()
chunks = chunker.chunk_document('data/# OWASP LLM Top 10 – 2025.md')

for chunk in chunks:
    print(f"{chunk.risk_id}: {chunk.risk_name}")
    print(f"  Year: {chunk.year}, Category: {chunk.category}")
```

### Prompt Generation

The prompt generator supports multiple modes:

1. **General retrieval-based prompts**:
```python
prompt = prompt_gen.generate_prompt(
    "What are common injection attacks?",
    top_k=3
)
```

2. **Risk-specific prompts**:
```python
prompt = prompt_gen.generate_prompt_for_risk(
    "LLM01",
    "How can I test for prompt injection?"
)
```

3. **Category-filtered prompts**:
```python
prompt = prompt_gen.generate_prompt_with_category_filter(
    "Injection",
    "What are injection attack vectors?",
    top_k=2
)
```

### LLM-as-Judge Evaluation

The evaluator assesses responses across multiple criteria:

- **Accuracy**: Does the response accurately reflect the reference material?
- **Completeness**: Does it cover key aspects?
- **Relevance**: Is it relevant to the query?
- **Metadata Usage**: Does it correctly reference risk IDs and names?
- **Factual Correctness**: Are facts consistent with the reference?

```python
evaluation = judge.evaluate_response(
    user_query="What are mitigation strategies for prompt injection?",
    model_response="...",
    reference_risk_id="LLM01"  # Optional: focus on specific risk
)

print(f"Overall Score: {evaluation['overall_score']}/10")
print(f"Accuracy: {evaluation['accuracy_score']}/10")
```

### Metadata Filtering

Retrieve chunks by metadata:

```python
# Get chunk by risk ID
chunk = pipeline.get_chunk_by_risk_id("LLM01")

# Get chunks by category
chunks = pipeline.get_chunks_by_category("Injection")

# Retrieve with metadata filter
results = pipeline.retrieve(
    "prompt injection",
    top_k=3,
    filter_metadata={'category': 'Injection'}
)
```

## Integration with Vector Stores

The pipeline is designed to work with various vector stores. To use a specific vector store:

```python
# Example with ChromaDB (uncomment in requirements.txt)
# import chromadb
# client = chromadb.Client()
# collection = client.create_collection("owasp_llm_top10")
# pipeline = RAGPipeline(
#     'data/# OWASP LLM Top 10 – 2025.md',
#     embedding_model=embedding_model,
#     vector_store=collection
# )
```

## Integration with LLM APIs

To use actual LLM models for embeddings and judge evaluation:

```python
# Example with OpenAI (uncomment in requirements.txt)
# from openai import OpenAI
# client = OpenAI()
# 
# # For embeddings
# embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
# 
# # For judge model
# judge = LLMJudge(pipeline, prompt_gen, judge_model=client)
```

## Metadata Schema

Each chunk includes the following metadata:

```python
{
    'risk_id': 'LLM01',           # Risk identifier
    'risk_name': 'Prompt Injection',  # Risk name
    'year': 2025,                  # Year
    'category': 'Injection'        # Category
}
```

Categories are automatically assigned based on risk IDs:
- LLM01: Injection
- LLM02: Data Protection
- LLM03: Supply Chain
- LLM04: Data Integrity
- LLM05: Output Handling
- LLM06: Access Control
- LLM07: Configuration
- LLM08: RAG Security
- LLM09: Information Integrity
- LLM10: Resource Management

## Notes

- The current implementation uses placeholder embeddings and judge models. For production use, integrate actual embedding models and LLM APIs.
- The chunker expects the document format: `## LLM0X:YYYY – Risk Name`
- Each section should be separated by `---` markers
- Metadata is automatically extracted from section headers

## License

This project is for use with the OWASP LLM Top 10 – 2025 document.




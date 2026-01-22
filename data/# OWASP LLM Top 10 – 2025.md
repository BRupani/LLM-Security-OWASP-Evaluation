# OWASP LLM Top 10 – 2025

## Canonical RAG Reference Document

---

## LLM01:2025 – Prompt Injection

**Definition**
Manipulating LLM inputs to override system instructions, extract sensitive data, or trigger unintended and harmful actions.

**How It Happens**

* Direct adversarial user prompts
* Hidden or obfuscated instructions embedded in documents
* Indirect prompt injection via external tools, APIs, or retrieved content (RAG)

**Potential Consequences**

* Data leakage
* Bypass of safety and policy controls
* Execution of malicious tasks or downstream code
* Unauthorized tool or API usage

**Mitigation Strategies**

* Input sanitization and normalization
* Layered validation of instructions and context
* Sandboxing of model outputs
* Principle of least privilege for tool access
* Continuous red-teaming and adversarial testing

**Security Testing Focus**

* Single-turn and multi-turn injection attempts
* Instruction override attacks
* Indirect injection via retrieved or external data sources

---

## LLM02:2025 – Sensitive Information Disclosure

**Definition**
Exposure of private, regulated, or confidential information through LLM outputs.

**How It Happens**

* Memorization of sensitive training data
* Crafted or leading user queries
* Overly permissive context injection

**Potential Consequences**

* Data loss
* Regulatory and compliance violations
* Reputational damage

**Mitigation Strategies**

* Data minimization
* Strong access controls
* Output monitoring and filtering
* Differential privacy and redaction techniques

**Security Testing Focus**

* PII extraction attempts
* Training data leakage probes
* Role-based access bypass scenarios

---

## LLM03:2025 – Supply Chain Vulnerabilities

**Definition**
Security risks arising from third-party, open-source, or upstream LLM components and services.

**How It Happens**

* Malicious or compromised dependencies
* Unverified model sources
* Insecure or poisoned APIs and plugins

**Potential Consequences**

* Backdoors in models or tooling
* Poisoned outputs
* Unauthorized access to systems or data

**Mitigation Strategies**

* Dependency vetting and SBOM usage
* Provenance verification
* Supply chain security controls and monitoring

**Security Testing Focus**

* Dependency trust validation
* Model source verification
* Third-party integration abuse scenarios

---

## LLM04:2025 – Data and Model Poisoning

**Definition**
Malicious manipulation of training, fine-tuning, or feedback data that corrupts model behavior.

**How It Happens**

* Injection of adversarial or backdoor data
* Compromised feedback or reinforcement loops
* Poisoned fine-tuning datasets

**Potential Consequences**

* Unsafe or malicious outputs
* Embedded exploits
* Long-term bias or manipulation

**Mitigation Strategies**

* Data provenance validation
* Anomaly and drift detection
* Continuous post-deployment evaluation

**Security Testing Focus**

* Backdoor trigger detection
* Behavioral drift analysis
* Bias amplification scenarios

---

## LLM05:2025 – Improper Output Handling

**Definition**
Passing untrusted LLM outputs directly into downstream systems without validation or isolation.

**How It Happens**

* Executing model-generated code or commands
* Feeding outputs into interpreters, templates, or APIs without checks

**Potential Consequences**

* Injection attacks
* Workflow manipulation
* Remote code execution

**Mitigation Strategies**

* Output validation and encoding
* Execution sandboxing
* Strict downstream input contracts

**Security Testing Focus**

* Code injection via outputs
* Command or template injection
* Unsafe automation chains

---

## LLM06:2025 – Excessive Agency

**Definition**
Granting LLMs excessive autonomy or control over sensitive actions, tools, or resources.

**How It Happens**

* Overly permissive tool integrations
* Missing approval or review steps
* Poorly scoped agent permissions

**Potential Consequences**

* Unauthorized operations
* Privilege escalation
* Irreversible system changes

**Mitigation Strategies**

* Principle of least privilege
* Explicit approval gates
* Tool usage monitoring and logging

**Security Testing Focus**

* Unauthorized tool invocation
* Privilege boundary violations
* Autonomous action escalation

---

## LLM07:2025 – System Prompt Leakage

**Definition**
Exposure of system prompts, hidden instructions, or internal configuration details.

**How It Happens**

* Adversarial prompting
* Side-channel inference
* Error handling leakage

**Potential Consequences**

* Guardrail bypass
* Disclosure of sensitive logic
* Increased attack effectiveness

**Mitigation Strategies**

* Prompt masking and abstraction
* Randomization of internal prompts
* Output monitoring and filtering

**Security Testing Focus**

* Prompt extraction attempts
* Instruction inference attacks
* Meta-prompt probing

---

## LLM08:2025 – Vector and Embedding Weaknesses

**Definition**
Exploitation of weaknesses in embeddings, vector databases, or retrieval pipelines.

**How It Happens**

* Malicious embeddings
* Data pollution in vector stores
* Injection attacks in RAG workflows

**Potential Consequences**

* Manipulated or biased responses
* Retrieval-based security bypass
* Persistent misinformation

**Mitigation Strategies**

* Embedding validation
* Input sanitization
* Secure vector database access controls

**Security Testing Focus**

* RAG injection attacks
* Retrieval poisoning
* Context manipulation

---

## LLM09:2025 – Misinformation

**Definition**
Generation or amplification of false, misleading, or unverified information.

**How It Happens**

* Prompt manipulation
* Reliance on low-quality or outdated data
* Lack of verification mechanisms

**Potential Consequences**

* Disinformation spread
* Compliance failures
* Loss of trust and credibility

**Mitigation Strategies**

* Human-in-the-loop review
* Fact-checking pipelines
* Misuse monitoring

**Security Testing Focus**

* Hallucination stress tests
* False authority scenarios
* Compliance-critical misinformation

---

## LLM10:2025 – Unbounded Consumption

**Definition**
Uncontrolled resource usage or cost escalation caused by LLM operations.

**How It Happens**

* Prompt flooding
* Recursive agent loops
* Excessively complex or chained prompts

**Potential Consequences**

* Denial of service
* Cost overruns
* Degraded system performance

**Mitigation Strategies**

* Rate limiting
* Quotas and budget enforcement
* Cost and usage monitoring

**Security Testing Focus**

* Resource exhaustion scenarios
* Recursive invocation detection
* Cost amplification attacks

---

## End of Document

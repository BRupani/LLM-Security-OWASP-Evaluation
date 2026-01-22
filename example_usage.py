"""
Example usage of the RAG pipeline with prompt generation and LLM-as-judge evaluation.
"""

from rag_pipeline import RAGPipeline
from prompt_generator import PromptGenerator
from llm_judge import LLMJudge


def main():
    """Main example demonstrating the RAG pipeline."""
    
    print("=" * 80)
    print("OWASP LLM Top 10 RAG Pipeline - Example Usage")
    print("=" * 80)
    
    # Step 1: Initialize RAG Pipeline
    print("\n[Step 1] Initializing RAG Pipeline...")
    document_path = 'data/# OWASP LLM Top 10 – 2025.md'
    pipeline = RAGPipeline(document_path)
    pipeline.initialize()
    
    print(f"✓ Loaded {len(pipeline.chunks)} chunks from document")
    
    # Step 2: Initialize Prompt Generator
    print("\n[Step 2] Initializing Prompt Generator...")
    prompt_gen = PromptGenerator(pipeline)
    print("✓ Prompt generator ready")
    
    # Step 3: Generate prompts with RAG context
    print("\n[Step 3] Generating Prompts with RAG Context...")
    print("-" * 80)
    
    # Example 1: General query
    query1 = "What are the main mitigation strategies for prompt injection?"
    prompt1 = prompt_gen.generate_prompt(query1, top_k=2)
    print(f"\nQuery: {query1}")
    print(f"\nGenerated Prompt (first 500 chars):\n{prompt1[:500]}...")
    
    # Example 2: Risk-specific query
    query2 = "How can I test for prompt injection vulnerabilities?"
    prompt2 = prompt_gen.generate_prompt_for_risk("LLM01", query2)
    print(f"\n\nQuery: {query2}")
    print(f"Risk ID: LLM01")
    print(f"\nGenerated Prompt (first 500 chars):\n{prompt2[:500]}...")
    
    # Example 3: Category-filtered query
    query3 = "What are common injection attack vectors?"
    prompt3 = prompt_gen.generate_prompt_with_category_filter(
        "Injection", query3, top_k=2
    )
    print(f"\n\nQuery: {query3}")
    print(f"Category: Injection")
    print(f"\nGenerated Prompt (first 500 chars):\n{prompt3[:500]}...")
    
    # Step 4: Initialize LLM-as-Judge
    print("\n\n[Step 4] Initializing LLM-as-Judge Evaluator...")
    judge = LLMJudge(pipeline, prompt_gen)
    print("✓ LLM-as-judge ready")
    
    # Step 5: Evaluate responses
    print("\n[Step 5] Evaluating Model Responses...")
    print("-" * 80)
    
    # Example response to evaluate
    example_response = """Prompt injection (LLM01:2025) can be mitigated through several key strategies:

1. Input sanitization and normalization - Clean and validate all inputs before processing
2. Layered validation of instructions and context - Multiple validation layers
3. Sandboxing of model outputs - Isolate outputs before execution
4. Principle of least privilege for tool access - Limit tool permissions
5. Continuous red-teaming and adversarial testing - Regular security testing

These strategies help prevent attackers from manipulating LLM inputs to override system instructions, extract sensitive data, or trigger unintended actions."""
    
    evaluation = judge.evaluate_response(
        query1,
        example_response,
        reference_risk_id="LLM01"
    )
    
    print(f"\nQuery: {query1}")
    print(f"\nResponse Evaluation:")
    print(f"  Overall Score: {evaluation.get('overall_score', 'N/A')}/10")
    print(f"  Accuracy: {evaluation.get('accuracy_score', 'N/A')}/10")
    print(f"    → {evaluation.get('accuracy_explanation', 'N/A')}")
    print(f"  Completeness: {evaluation.get('completeness_score', 'N/A')}/10")
    print(f"    → {evaluation.get('completeness_explanation', 'N/A')}")
    print(f"  Metadata Usage: {evaluation.get('metadata_score', 'N/A')}/10")
    print(f"    → {evaluation.get('metadata_explanation', 'N/A')}")
    
    # Step 6: Display metadata summary
    print("\n[Step 6] Available Risks and Metadata...")
    print("-" * 80)
    summary = prompt_gen.get_metadata_summary()
    print(summary)
    
    # Step 7: Demonstrate retrieval with metadata filtering
    print("\n[Step 7] Retrieval with Metadata Filtering...")
    print("-" * 80)
    
    # Retrieve chunks for a specific risk
    chunk = pipeline.get_chunk_by_risk_id("LLM01")
    if chunk:
        metadata = pipeline.chunker.get_chunk_metadata_dict(chunk)
        print(f"\nRetrieved chunk for LLM01:")
        print(f"  Risk ID: {metadata['risk_id']}")
        print(f"  Risk Name: {metadata['risk_name']}")
        print(f"  Year: {metadata['year']}")
        print(f"  Category: {metadata['category']}")
        print(f"  Content preview: {chunk.section_content[:200]}...")
    
    # Retrieve chunks by category
    injection_chunks = pipeline.get_chunks_by_category("Injection")
    print(f"\n\nChunks in 'Injection' category: {len(injection_chunks)}")
    for chunk in injection_chunks:
        metadata = pipeline.chunker.get_chunk_metadata_dict(chunk)
        print(f"  - {metadata['risk_id']}: {metadata['risk_name']}")
    
    print("\n" + "=" * 80)
    print("Example completed successfully!")
    print("=" * 80)


if __name__ == '__main__':
    main()

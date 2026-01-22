"""
Prompt generator that references RAG chunks with metadata.
Integrates with the RAG pipeline to generate context-aware prompts.
"""

from typing import List, Dict, Any, Optional
from rag_pipeline import RAGPipeline
from rag_chunker import ChunkMetadata


class PromptGenerator:
    """Generates prompts with RAG context and metadata."""
    
    def __init__(self, rag_pipeline: RAGPipeline):
        """Initialize prompt generator.
        
        Args:
            rag_pipeline: Initialized RAGPipeline instance
        """
        self.rag_pipeline = rag_pipeline
    
    def format_chunk_context(self, chunks: List[Dict[str, Any]]) -> str:
        """Format retrieved chunks as context for prompt.
        
        Args:
            chunks: List of chunk dictionaries from retrieve()
            
        Returns:
            Formatted context string
        """
        context_parts = []
        for i, chunk_result in enumerate(chunks):
            chunk = chunk_result['chunk']
            metadata = chunk_result['metadata']
            content = chunk_result['content']
            
            context_parts.append(
                f"[Reference {i+1}]\n"
                f"Risk ID: {metadata['risk_id']}\n"
                f"Risk Name: {metadata['risk_name']}\n"
                f"Year: {metadata['year']}\n"
                f"Category: {metadata['category']}\n"
                f"Content:\n{content}\n"
                f"---\n"
            )
        
        return "\n".join(context_parts)
    
    def generate_prompt(self,
                       user_query: str,
                       top_k: int = 3,
                       filter_metadata: Optional[Dict[str, Any]] = None,
                       system_prompt: Optional[str] = None,
                       include_metadata: bool = True) -> str:
        """Generate a prompt with RAG context.
        
        Args:
            user_query: User's query/question
            top_k: Number of relevant chunks to retrieve
            filter_metadata: Optional metadata filters for retrieval
            system_prompt: Optional custom system prompt
            include_metadata: Whether to include metadata in context
            
        Returns:
            Complete prompt string with context
        """
        # Retrieve relevant chunks
        retrieved_chunks = self.rag_pipeline.retrieve(
            user_query,
            top_k=top_k,
            filter_metadata=filter_metadata
        )
        
        # Format context
        if include_metadata:
            context = self.format_chunk_context(retrieved_chunks)
        else:
            # Just include content without metadata headers
            context = "\n---\n".join([
                chunk_result['content'] 
                for chunk_result in retrieved_chunks
            ])
        
        # Default system prompt
        if system_prompt is None:
            system_prompt = (
                "You are a security expert specializing in LLM security risks. "
                "Use the provided OWASP LLM Top 10 reference material to answer questions accurately. "
                "When referencing specific risks, include the risk ID (e.g., LLM01) and risk name."
            )
        
        # Construct full prompt
        full_prompt = f"""System: {system_prompt}

Reference Material (OWASP LLM Top 10 - 2025):
{context}

User Query: {user_query}

Please provide a comprehensive answer based on the reference material above. 
When referencing specific risks, include the risk ID and risk name from the metadata."""
        
        return full_prompt
    
    def generate_prompt_for_risk(self,
                                 risk_id: str,
                                 user_query: str,
                                 system_prompt: Optional[str] = None) -> str:
        """Generate a prompt focused on a specific risk.
        
        Args:
            risk_id: Risk ID like "LLM01"
            user_query: User's query/question
            system_prompt: Optional custom system prompt
            
        Returns:
            Complete prompt string with context for the specific risk
        """
        # Get the specific chunk
        chunk = self.rag_pipeline.get_chunk_by_risk_id(risk_id)
        if chunk is None:
            raise ValueError(f"Risk ID {risk_id} not found")
        
        metadata = self.rag_pipeline.chunker.get_chunk_metadata_dict(chunk)
        
        # Format context
        context = (
            f"Risk ID: {metadata['risk_id']}\n"
            f"Risk Name: {metadata['risk_name']}\n"
            f"Year: {metadata['year']}\n"
            f"Category: {metadata['category']}\n"
            f"Content:\n{chunk.section_content}\n"
        )
        
        # Default system prompt
        if system_prompt is None:
            system_prompt = (
                f"You are a security expert. Answer questions about {metadata['risk_name']} "
                f"({metadata['risk_id']}) based on the OWASP LLM Top 10 reference material."
            )
        
        # Construct full prompt
        full_prompt = f"""System: {system_prompt}

Reference Material:
{context}

User Query: {user_query}

Please provide a comprehensive answer based on the reference material above."""
        
        return full_prompt
    
    def generate_prompt_with_category_filter(self,
                                            category: str,
                                            user_query: str,
                                            top_k: int = 3,
                                            system_prompt: Optional[str] = None) -> str:
        """Generate a prompt filtered by category.
        
        Args:
            category: Category name (e.g., "Injection", "Data Protection")
            user_query: User's query/question
            top_k: Number of relevant chunks to retrieve
            system_prompt: Optional custom system prompt
            
        Returns:
            Complete prompt string with context filtered by category
        """
        # Get chunks in category
        category_chunks = self.rag_pipeline.get_chunks_by_category(category)
        
        # Retrieve from category chunks
        retrieved_chunks = self.rag_pipeline.retrieve(
            user_query,
            top_k=top_k,
            filter_metadata={'category': category}
        )
        
        if not retrieved_chunks:
            raise ValueError(f"No chunks found for category: {category}")
        
        # Format context
        context = self.format_chunk_context(retrieved_chunks)
        
        # Default system prompt
        if system_prompt is None:
            system_prompt = (
                f"You are a security expert. Answer questions about {category} risks "
                "based on the OWASP LLM Top 10 reference material."
            )
        
        # Construct full prompt
        full_prompt = f"""System: {system_prompt}

Reference Material (Category: {category}):
{context}

User Query: {user_query}

Please provide a comprehensive answer based on the reference material above."""
        
        return full_prompt
    
    def get_metadata_summary(self) -> str:
        """Get a summary of all available risks and metadata.
        
        Returns:
            Formatted summary string
        """
        summary_parts = ["Available OWASP LLM Top 10 Risks:\n"]
        
        for chunk in self.rag_pipeline.chunks:
            metadata = self.rag_pipeline.chunker.get_chunk_metadata_dict(chunk)
            summary_parts.append(
                f"- {metadata['risk_id']}: {metadata['risk_name']} "
                f"(Year: {metadata['year']}, Category: {metadata['category']})"
            )
        
        return "\n".join(summary_parts)


if __name__ == '__main__':
    # Example usage
    from rag_pipeline import RAGPipeline
    
    # Initialize RAG pipeline
    pipeline = RAGPipeline('data/# OWASP LLM Top 10 – 2025.md')
    pipeline.initialize()
    
    # Initialize prompt generator
    prompt_gen = PromptGenerator(pipeline)
    
    # Generate a general prompt
    print("=== General Prompt ===")
    prompt1 = prompt_gen.generate_prompt(
        "What are the main mitigation strategies for prompt injection?",
        top_k=2
    )
    print(prompt1[:500] + "...\n")
    
    # Generate a risk-specific prompt
    print("=== Risk-Specific Prompt ===")
    prompt2 = prompt_gen.generate_prompt_for_risk(
        "LLM01",
        "How can I test for prompt injection vulnerabilities?"
    )
    print(prompt2[:500] + "...\n")
    
    # Generate a category-filtered prompt
    print("=== Category-Filtered Prompt ===")
    prompt3 = prompt_gen.generate_prompt_with_category_filter(
        "Injection",
        "What are common injection attack vectors?",
        top_k=2
    )
    print(prompt3[:500] + "...\n")
    
    # Get metadata summary
    print("=== Metadata Summary ===")
    print(prompt_gen.get_metadata_summary())

"""
RAG pipeline for OWASP LLM Top 10 document.
Handles chunking, embedding, and retrieval with metadata.
"""

from typing import List, Dict, Any, Optional
from rag_chunker import OWASPChunker, ChunkMetadata
import json


class RAGPipeline:
    """RAG pipeline for OWASP LLM Top 10 document."""
    
    def __init__(self, 
                 document_path: str,
                 embedding_model: Optional[Any] = None,
                 vector_store: Optional[Any] = None):
        """Initialize RAG pipeline.
        
        Args:
            document_path: Path to the OWASP LLM Top 10 markdown document
            embedding_model: Optional embedding model (if None, uses placeholder)
            vector_store: Optional vector store (if None, uses in-memory dict)
        """
        self.document_path = document_path
        self.chunker = OWASPChunker()
        self.embedding_model = embedding_model
        self.vector_store = vector_store or {}
        self.chunks: List[ChunkMetadata] = []
        self.chunk_embeddings: Dict[int, List[float]] = {}
        
    def load_and_chunk(self) -> List[ChunkMetadata]:
        """Load document and chunk by LLM0X sections.
        
        Returns:
            List of ChunkMetadata objects
        """
        self.chunks = self.chunker.chunk_document(self.document_path)
        return self.chunks
    
    def generate_embeddings(self, chunks: Optional[List[ChunkMetadata]] = None):
        """Generate embeddings for chunks.
        
        Args:
            chunks: Optional list of chunks (uses self.chunks if None)
        """
        if chunks is None:
            chunks = self.chunks
        
        if self.embedding_model is None:
            # Placeholder: In production, use actual embedding model
            # e.g., from sentence_transformers import SentenceTransformer
            # self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
            print("Warning: No embedding model provided. Using placeholder embeddings.")
            for i, chunk in enumerate(chunks):
                # Placeholder: random-like embedding (in production, use real model)
                self.chunk_embeddings[i] = [0.0] * 384  # Typical embedding dimension
        else:
            for i, chunk in enumerate(chunks):
                embedding = self.embedding_model.encode(chunk.section_content)
                self.chunk_embeddings[i] = embedding.tolist()
    
    def store_in_vector_db(self, chunks: Optional[List[ChunkMetadata]] = None):
        """Store chunks and embeddings in vector database.
        
        Args:
            chunks: Optional list of chunks (uses self.chunks if None)
        """
        if chunks is None:
            chunks = self.chunks
        
        for i, chunk in enumerate(chunks):
            metadata = self.chunker.get_chunk_metadata_dict(chunk)
            metadata['chunk_index'] = i
            metadata['content'] = chunk.section_content
            
            # Store in vector store
            if hasattr(self.vector_store, 'add'):
                # ChromaDB, Pinecone, etc.
                self.vector_store.add(
                    ids=[f"chunk_{i}"],
                    embeddings=[self.chunk_embeddings[i]],
                    metadatas=[metadata],
                    documents=[chunk.section_content]
                )
            else:
                # Simple dict-based storage
                self.vector_store[f"chunk_{i}"] = {
                    'embedding': self.chunk_embeddings[i],
                    'metadata': metadata,
                    'content': chunk.section_content
                }
    
    def retrieve(self, 
                 query: str, 
                 top_k: int = 3,
                 filter_metadata: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Retrieve relevant chunks based on query.
        
        Args:
            query: Search query
            top_k: Number of top results to return
            filter_metadata: Optional metadata filters (e.g., {'risk_id': 'LLM01'})
            
        Returns:
            List of dictionaries with 'chunk', 'metadata', and 'score' keys
        """
        # Generate query embedding
        if self.embedding_model is None:
            query_embedding = [0.0] * 384  # Placeholder
        else:
            query_embedding = self.embedding_model.encode(query).tolist()
        
        # Calculate similarity scores
        results = []
        for i, chunk in enumerate(self.chunks):
            # Apply metadata filters
            if filter_metadata:
                metadata = self.chunker.get_chunk_metadata_dict(chunk)
                if not all(metadata.get(k) == v for k, v in filter_metadata.items()):
                    continue
            
            # Calculate cosine similarity (simplified)
            chunk_emb = self.chunk_embeddings[i]
            if self.embedding_model is None:
                # Placeholder: simple keyword matching
                score = 1.0 if any(word.lower() in chunk.section_content.lower() 
                                 for word in query.split()) else 0.0
            else:
                # Cosine similarity
                import numpy as np
                chunk_emb_np = np.array(chunk_emb)
                query_emb_np = np.array(query_embedding)
                score = np.dot(chunk_emb_np, query_emb_np) / (
                    np.linalg.norm(chunk_emb_np) * np.linalg.norm(query_emb_np)
                )
            
            metadata = self.chunker.get_chunk_metadata_dict(chunk)
            results.append({
                'chunk': chunk,
                'metadata': metadata,
                'content': chunk.section_content,
                'score': score
            })
        
        # Sort by score and return top_k
        results.sort(key=lambda x: x['score'], reverse=True)
        return results[:top_k]
    
    def get_chunk_by_risk_id(self, risk_id: str) -> Optional[ChunkMetadata]:
        """Get chunk by risk ID.
        
        Args:
            risk_id: Risk ID like "LLM01"
            
        Returns:
            ChunkMetadata or None if not found
        """
        for chunk in self.chunks:
            if chunk.risk_id == risk_id:
                return chunk
        return None
    
    def get_chunks_by_category(self, category: str) -> List[ChunkMetadata]:
        """Get all chunks in a category.
        
        Args:
            category: Category name
            
        Returns:
            List of ChunkMetadata objects
        """
        return [chunk for chunk in self.chunks if chunk.category == category]
    
    def initialize(self):
        """Initialize the pipeline: load, chunk, embed, and store."""
        print("Loading and chunking document...")
        self.load_and_chunk()
        print(f"Created {len(self.chunks)} chunks")
        
        print("Generating embeddings...")
        self.generate_embeddings()
        
        print("Storing in vector database...")
        self.store_in_vector_db()
        print("Pipeline initialized successfully!")


if __name__ == '__main__':
    # Example usage
    pipeline = RAGPipeline('data/# OWASP LLM Top 10 – 2025.md')
    pipeline.initialize()
    
    # Test retrieval
    print("\nTesting retrieval...")
    results = pipeline.retrieve("prompt injection attacks", top_k=2)
    for i, result in enumerate(results):
        print(f"\nResult {i+1}:")
        print(f"  Risk ID: {result['metadata']['risk_id']}")
        print(f"  Risk Name: {result['metadata']['risk_name']}")
        print(f"  Score: {result['score']:.4f}")
        print(f"  Content preview: {result['content'][:150]}...")

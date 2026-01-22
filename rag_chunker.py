"""
Document chunker for OWASP LLM Top 10 RAG pipeline.
Chunks documents by LLM0X sections and extracts metadata.
"""

import re
from typing import List, Dict, Any
from dataclasses import dataclass


@dataclass
class ChunkMetadata:
    """Metadata for a document chunk."""
    risk_id: str  # e.g., "LLM01"
    risk_name: str  # e.g., "Prompt Injection"
    year: int  # e.g., 2025
    category: str  # e.g., "Injection" or "Security"
    section_content: str  # The full content of the section


class OWASPChunker:
    """Chunks OWASP LLM Top 10 document by LLM0X sections."""
    
    def __init__(self):
        # Match section headers with various dash characters (en dash, em dash, hyphen)
        self.section_pattern = re.compile(
            r'^##\s+(LLM\d{2}):(\d{4})\s+[–—\-]\s+(.+)$',
            re.MULTILINE
        )
    
    def parse_section_header(self, header_line: str) -> Dict[str, Any]:
        """Parse a section header to extract metadata.
        
        Args:
            header_line: Line like "## LLM01:2025 – Prompt Injection"
            
        Returns:
            Dictionary with risk_id, year, risk_name, or None if not matched
        """
        match = self.section_pattern.match(header_line.strip())
        if match:
            return {
                'risk_id': match.group(1),  # LLM01
                'year': int(match.group(2)),  # 2025
                'risk_name': match.group(3).strip()  # Prompt Injection
            }
        return None
    
    def determine_category(self, risk_id: str, risk_name: str) -> str:
        """Determine category based on risk_id and risk_name.
        
        Args:
            risk_id: Risk identifier like "LLM01"
            risk_name: Risk name like "Prompt Injection"
            
        Returns:
            Category string
        """
        # Map risk IDs to categories based on OWASP classification
        category_map = {
            'LLM01': 'Injection',
            'LLM02': 'Data Protection',
            'LLM03': 'Supply Chain',
            'LLM04': 'Data Integrity',
            'LLM05': 'Output Handling',
            'LLM06': 'Access Control',
            'LLM07': 'Configuration',
            'LLM08': 'RAG Security',
            'LLM09': 'Information Integrity',
            'LLM10': 'Resource Management'
        }
        return category_map.get(risk_id, 'Security')
    
    def chunk_document(self, document_path: str) -> List[ChunkMetadata]:
        """Chunk document by LLM0X sections.
        
        Args:
            document_path: Path to the markdown document
            
        Returns:
            List of ChunkMetadata objects, one per LLM0X section
        """
        with open(document_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        chunks = []
        lines = content.split('\n')
        
        current_section = None
        current_content = []
        current_metadata = None
        
        i = 0
        while i < len(lines):
            line = lines[i]
            
            # Check if this is a section header
            if line.startswith('## LLM'):
                # Save previous section if exists
                if current_metadata and current_content:
                    chunk = ChunkMetadata(
                        risk_id=current_metadata['risk_id'],
                        risk_name=current_metadata['risk_name'],
                        year=current_metadata['year'],
                        category=self.determine_category(
                            current_metadata['risk_id'],
                            current_metadata['risk_name']
                        ),
                        section_content='\n'.join(current_content)
                    )
                    chunks.append(chunk)
                
                # Start new section
                metadata = self.parse_section_header(line)
                if metadata:
                    current_metadata = metadata
                    current_content = [line]  # Include header in content
                else:
                    current_metadata = None
                    current_content = []
            elif current_metadata:
                # Add line to current section
                current_content.append(line)
                
                # Stop at next section or end marker
                if line.strip() == '---' and i + 1 < len(lines):
                    # Check if next non-empty line is a new section
                    j = i + 1
                    while j < len(lines) and not lines[j].strip():
                        j += 1
                    if j < len(lines) and lines[j].startswith('## LLM'):
                        # End of current section
                        chunk = ChunkMetadata(
                            risk_id=current_metadata['risk_id'],
                            risk_name=current_metadata['risk_name'],
                            year=current_metadata['year'],
                            category=self.determine_category(
                                current_metadata['risk_id'],
                                current_metadata['risk_name']
                            ),
                            section_content='\n'.join(current_content)
                        )
                        chunks.append(chunk)
                        current_metadata = None
                        current_content = []
                        i = j - 1  # Will increment to j
            
            i += 1
        
        # Save last section
        if current_metadata and current_content:
            chunk = ChunkMetadata(
                risk_id=current_metadata['risk_id'],
                risk_name=current_metadata['risk_name'],
                year=current_metadata['year'],
                category=self.determine_category(
                    current_metadata['risk_id'],
                    current_metadata['risk_name']
                ),
                section_content='\n'.join(current_content)
            )
            chunks.append(chunk)
        
        return chunks
    
    def get_chunk_metadata_dict(self, chunk: ChunkMetadata) -> Dict[str, Any]:
        """Convert ChunkMetadata to dictionary for vector store.
        
        Args:
            chunk: ChunkMetadata object
            
        Returns:
            Dictionary with metadata fields
        """
        return {
            'risk_id': chunk.risk_id,
            'risk_name': chunk.risk_name,
            'year': chunk.year,
            'category': chunk.category
        }


if __name__ == '__main__':
    # Example usage
    chunker = OWASPChunker()
    chunks = chunker.chunk_document('data/# OWASP LLM Top 10 – 2025.md')
    
    print(f"Total chunks: {len(chunks)}")
    print("\nFirst chunk metadata:")
    if chunks:
        chunk = chunks[0]
        print(f"  Risk ID: {chunk.risk_id}")
        print(f"  Risk Name: {chunk.risk_name}")
        print(f"  Year: {chunk.year}")
        print(f"  Category: {chunk.category}")
        print(f"  Content length: {len(chunk.section_content)} characters")
        print(f"\nContent preview:\n{chunk.section_content[:200]}...")

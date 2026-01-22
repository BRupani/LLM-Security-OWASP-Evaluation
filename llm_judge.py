"""
LLM-as-judge evaluator that references RAG chunks with metadata.
Evaluates responses against the OWASP LLM Top 10 reference document.
"""

from typing import List, Dict, Any, Optional, Tuple
from rag_pipeline import RAGPipeline
from prompt_generator import PromptGenerator
from rag_chunker import ChunkMetadata
import json


class LLMJudge:
    """LLM-as-judge evaluator using RAG chunks as reference."""
    
    def __init__(self, 
                 rag_pipeline: RAGPipeline,
                 prompt_generator: Optional[PromptGenerator] = None,
                 judge_model: Optional[Any] = None):
        """Initialize LLM-as-judge evaluator.
        
        Args:
            rag_pipeline: Initialized RAGPipeline instance
            prompt_generator: Optional PromptGenerator instance
            judge_model: Optional judge LLM model (if None, uses placeholder)
        """
        self.rag_pipeline = rag_pipeline
        self.prompt_generator = prompt_generator or PromptGenerator(rag_pipeline)
        self.judge_model = judge_model
    
    def generate_evaluation_prompt(self,
                                   user_query: str,
                                   model_response: str,
                                   reference_risk_id: Optional[str] = None,
                                   include_metadata: bool = True) -> str:
        """Generate evaluation prompt for LLM-as-judge.
        
        Args:
            user_query: Original user query
            model_response: Response to evaluate
            reference_risk_id: Optional specific risk ID to reference
            include_metadata: Whether to include metadata in reference context
            
        Returns:
            Evaluation prompt string
        """
        # Get relevant reference chunks
        if reference_risk_id:
            chunk = self.rag_pipeline.get_chunk_by_risk_id(reference_risk_id)
            if chunk:
                metadata = self.rag_pipeline.chunker.get_chunk_metadata_dict(chunk)
                reference_context = (
                    f"Risk ID: {metadata['risk_id']}\n"
                    f"Risk Name: {metadata['risk_name']}\n"
                    f"Year: {metadata['year']}\n"
                    f"Category: {metadata['category']}\n"
                    f"Content:\n{chunk.section_content}\n"
                )
            else:
                # Fallback to retrieval
                retrieved = self.rag_pipeline.retrieve(user_query, top_k=3)
                reference_context = self.prompt_generator.format_chunk_context(retrieved)
        else:
            retrieved = self.rag_pipeline.retrieve(user_query, top_k=3)
            if include_metadata:
                reference_context = self.prompt_generator.format_chunk_context(retrieved)
            else:
                reference_context = "\n---\n".join([
                    r['content'] for r in retrieved
                ])
        
        evaluation_prompt = f"""You are an expert evaluator assessing LLM responses against the OWASP LLM Top 10 – 2025 reference document.

Reference Material:
{reference_context}

Original Query: {user_query}

Model Response to Evaluate:
{model_response}

Evaluation Criteria:
1. Accuracy: Does the response accurately reflect the information in the reference material?
2. Completeness: Does the response cover the key aspects mentioned in the reference material?
3. Relevance: Is the response relevant to the query and reference material?
4. Metadata Usage: Does the response correctly reference risk IDs, risk names, and categories when appropriate?
5. Factual Correctness: Are all facts, definitions, and details consistent with the reference material?

Please provide:
1. A score from 1-10 for each criterion (1=Poor, 10=Excellent)
2. A brief explanation for each score
3. An overall assessment
4. Any specific inaccuracies or missing information
5. Suggestions for improvement

Format your response as JSON with the following structure:
{{
    "accuracy_score": <1-10>,
    "accuracy_explanation": "<explanation>",
    "completeness_score": <1-10>,
    "completeness_explanation": "<explanation>",
    "relevance_score": <1-10>,
    "relevance_explanation": "<explanation>",
    "metadata_score": <1-10>,
    "metadata_explanation": "<explanation>",
    "factual_score": <1-10>,
    "factual_explanation": "<explanation>",
    "overall_score": <1-10>,
    "overall_assessment": "<assessment>",
    "inaccuracies": ["<list of inaccuracies>"],
    "missing_information": ["<list of missing information>"],
    "suggestions": ["<list of improvement suggestions>"]
}}"""
        
        return evaluation_prompt
    
    def evaluate_response(self,
                         user_query: str,
                         model_response: str,
                         reference_risk_id: Optional[str] = None,
                         include_metadata: bool = True) -> Dict[str, Any]:
        """Evaluate a model response using LLM-as-judge.
        
        Args:
            user_query: Original user query
            model_response: Response to evaluate
            reference_risk_id: Optional specific risk ID to reference
            include_metadata: Whether to include metadata in reference context
            
        Returns:
            Dictionary with evaluation results
        """
        # Generate evaluation prompt
        eval_prompt = self.generate_evaluation_prompt(
            user_query,
            model_response,
            reference_risk_id,
            include_metadata
        )
        
        # Get judgment from judge model
        if self.judge_model is None:
            # Placeholder: In production, call actual LLM
            # e.g., response = self.judge_model.generate(eval_prompt)
            print("Warning: No judge model provided. Using placeholder evaluation.")
            judgment = self._placeholder_evaluation(user_query, model_response)
        else:
            # Call actual judge model
            judgment_text = self.judge_model.generate(eval_prompt)
            try:
                judgment = json.loads(judgment_text)
            except json.JSONDecodeError:
                # Fallback if JSON parsing fails
                judgment = {
                    "raw_judgment": judgment_text,
                    "error": "Failed to parse JSON response"
                }
        
        # Add metadata about the evaluation
        judgment['evaluation_metadata'] = {
            'reference_risk_id': reference_risk_id,
            'include_metadata': include_metadata,
            'query': user_query
        }
        
        return judgment
    
    def _placeholder_evaluation(self, 
                               user_query: str, 
                               model_response: str) -> Dict[str, Any]:
        """Placeholder evaluation when no judge model is available.
        
        Args:
            user_query: Original user query
            model_response: Response to evaluate
            
        Returns:
            Placeholder evaluation dictionary
        """
        # Simple keyword-based placeholder
        response_lower = model_response.lower()
        query_lower = user_query.lower()
        
        # Check for risk ID mentions
        has_risk_id = any(f"llm{i:02d}" in response_lower for i in range(1, 11))
        
        # Basic relevance check
        query_words = set(query_lower.split())
        response_words = set(response_lower.split())
        relevance = len(query_words.intersection(response_words)) / max(len(query_words), 1)
        
        return {
            "accuracy_score": 7,
            "accuracy_explanation": "Placeholder evaluation - requires actual judge model",
            "completeness_score": 6,
            "completeness_explanation": "Placeholder evaluation - requires actual judge model",
            "relevance_score": int(relevance * 10),
            "relevance_explanation": f"Basic keyword overlap: {relevance:.2%}",
            "metadata_score": 8 if has_risk_id else 4,
            "metadata_explanation": "Risk ID mentioned" if has_risk_id else "No risk ID mentioned",
            "factual_score": 7,
            "factual_explanation": "Placeholder evaluation - requires actual judge model",
            "overall_score": 7,
            "overall_assessment": "Placeholder evaluation - requires actual judge model for accurate assessment",
            "inaccuracies": [],
            "missing_information": [],
            "suggestions": ["Use actual judge model for proper evaluation"]
        }
    
    def evaluate_batch(self,
                      queries_and_responses: List[Tuple[str, str]],
                      reference_risk_ids: Optional[List[Optional[str]]] = None) -> List[Dict[str, Any]]:
        """Evaluate multiple query-response pairs.
        
        Args:
            queries_and_responses: List of (query, response) tuples
            reference_risk_ids: Optional list of risk IDs for each query
            
        Returns:
            List of evaluation dictionaries
        """
        if reference_risk_ids is None:
            reference_risk_ids = [None] * len(queries_and_responses)
        
        evaluations = []
        for (query, response), risk_id in zip(queries_and_responses, reference_risk_ids):
            eval_result = self.evaluate_response(query, response, risk_id)
            evaluations.append(eval_result)
        
        return evaluations
    
    def get_evaluation_summary(self, evaluations: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Get summary statistics from multiple evaluations.
        
        Args:
            evaluations: List of evaluation dictionaries
            
        Returns:
            Summary dictionary with statistics
        """
        if not evaluations:
            return {"error": "No evaluations provided"}
        
        scores = {
            'accuracy': [],
            'completeness': [],
            'relevance': [],
            'metadata': [],
            'factual': [],
            'overall': []
        }
        
        for eval_result in evaluations:
            if 'accuracy_score' in eval_result:
                scores['accuracy'].append(eval_result['accuracy_score'])
            if 'completeness_score' in eval_result:
                scores['completeness'].append(eval_result['completeness_score'])
            if 'relevance_score' in eval_result:
                scores['relevance'].append(eval_result['relevance_score'])
            if 'metadata_score' in eval_result:
                scores['metadata'].append(eval_result['metadata_score'])
            if 'factual_score' in eval_result:
                scores['factual'].append(eval_result['factual_score'])
            if 'overall_score' in eval_result:
                scores['overall'].append(eval_result['overall_score'])
        
        summary = {}
        for metric, score_list in scores.items():
            if score_list:
                summary[f'{metric}_mean'] = sum(score_list) / len(score_list)
                summary[f'{metric}_min'] = min(score_list)
                summary[f'{metric}_max'] = max(score_list)
                summary[f'{metric}_std'] = (
                    sum((x - summary[f'{metric}_mean'])**2 for x in score_list) / len(score_list)
                ) ** 0.5
        
        summary['total_evaluations'] = len(evaluations)
        
        return summary


if __name__ == '__main__':
    # Example usage
    from rag_pipeline import RAGPipeline
    from prompt_generator import PromptGenerator
    
    # Initialize components
    pipeline = RAGPipeline('data/# OWASP LLM Top 10 – 2025.md')
    pipeline.initialize()
    
    prompt_gen = PromptGenerator(pipeline)
    judge = LLMJudge(pipeline, prompt_gen)
    
    # Example evaluation
    print("=== Example Evaluation ===")
    user_query = "What are the main mitigation strategies for prompt injection?"
    model_response = """Prompt injection can be mitigated through several strategies:
1. Input sanitization and normalization
2. Layered validation of instructions and context
3. Sandboxing of model outputs
4. Principle of least privilege for tool access
5. Continuous red-teaming and adversarial testing

These strategies help prevent attackers from manipulating LLM inputs to override system instructions."""
    
    evaluation = judge.evaluate_response(user_query, model_response, reference_risk_id="LLM01")
    
    print(f"Overall Score: {evaluation.get('overall_score', 'N/A')}/10")
    print(f"\nAccuracy: {evaluation.get('accuracy_score', 'N/A')}/10")
    print(f"  {evaluation.get('accuracy_explanation', 'N/A')}")
    print(f"\nCompleteness: {evaluation.get('completeness_score', 'N/A')}/10")
    print(f"  {evaluation.get('completeness_explanation', 'N/A')}")
    print(f"\nMetadata Usage: {evaluation.get('metadata_score', 'N/A')}/10")
    print(f"  {evaluation.get('metadata_explanation', 'N/A')}")
    
    # Batch evaluation
    print("\n=== Batch Evaluation ===")
    queries_responses = [
        (user_query, model_response),
        ("What is sensitive information disclosure?", 
         "Sensitive information disclosure (LLM02) involves exposure of private data through LLM outputs.")
    ]
    
    batch_evaluations = judge.evaluate_batch(queries_responses)
    summary = judge.get_evaluation_summary(batch_evaluations)
    
    print(f"\nEvaluation Summary:")
    print(f"  Total evaluations: {summary['total_evaluations']}")
    print(f"  Overall score mean: {summary.get('overall_mean', 'N/A'):.2f}")
    print(f"  Accuracy mean: {summary.get('accuracy_mean', 'N/A'):.2f}")
    print(f"  Metadata mean: {summary.get('metadata_mean', 'N/A'):.2f}")

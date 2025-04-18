"""LLM-based metadata extraction from natural language queries."""
import json
import re
import groq
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.config import settings

class LLMMetadataExtractor:
    """Extract metadata filters from queries using LLM."""
    
    def __init__(self):
        """Initialize with a Groq client."""
        self.groq_client = groq.Client(api_key=settings.groq_api_key)
            
    def extract_metadata(self, query: str) -> dict:
        """
        Extract metadata from query using LLM.
        
        Args:
            query: The natural language query to extract metadata from
            
        Returns:
            Dictionary of extracted metadata fields
        """
        prompt = f"""
        Extract structured metadata from this assessment search query. 
        Return a JSON object with these fields ONLY IF they are explicitly mentioned or clearly implied in the query:
        
        - job_levels: array of job level strings (e.g., ["entry-level", "mid-level", "senior"])
        - languages: array of language strings (e.g., ["english", "spanish"])
        - min_duration: minimum time duration in minutes (integer)
        - max_duration: maximum time duration in minutes (integer)
        - assessment_type: type of assessment (e.g., "cognitive", "personality")
        - adaptive_support: boolean (0 or 1) indicating if adaptive testing is supported by the assessment
        - remote_support: boolean (0 or 1) indicating if remote support is available
        
        IMPORTANT INSTRUCTIONS:
        - Job level stictly implies senerioty level of a job.
        - If a field is not mentioned in the query, DO NOT include that field in the JSON response.
        - Return empty values as empty arrays or null, not as empty strings.
        - The field values should be exactly as mentioned in the query (don't make up values).
        - For job_levels, normalize casing (e.g., capitalize consistently).
        - If duration is mentioned without specifying min or max (e.g., "60 minute assessment"), pick the appropriate field.
        
        EXAMPLES:
        
        Query: "Find Python assessments for senior developers that take less than 60 minutes"
        Response: {{"job_levels": ["senior"], "languages": ["python"], "max_duration": 60}}
        
        Query: "Show me all assessments"
        Response: {{}}

        Query: "Give me assessments having duration under 10 minutes"
        Response: {{"max_duration": 10}}
        
        Query: "Assessments longer than 45 minutes"
        Response: {{"min_duration": 45}}

        Query: "Find me a cognitive assessment"
        Response: {{"assessment_type": "cognitive"}}

        Query: "Find me an assessment with adaptive support"
        Response: {{"adaptive_support": 1}}

        Query: "Find me an assessment which can be given remotely"
        Response: {{"remote_support": 1}}
        
        Query: "{query}"
        
        JSON:
        """
        
        try:
            response = self.groq_client.chat.completions.create(
                model=settings.llm_model_name,
                messages=[
                    {"role": "system", "content": "You extract structured data from text with high precision. Only include fields explicitly mentioned in the query."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.0  # Keep deterministic
            )
            result = response.choices[0].message.content.strip()
            
            # Parse the JSON result
            try:
                extracted = json.loads(result)
                return extracted
            except json.JSONDecodeError:
                # If JSON parsing fails, try to extract just the JSON part
                json_match = re.search(r'\{.*\}', result, re.DOTALL)
                if json_match:
                    try:
                        return json.loads(json_match.group(0))
                    except:
                        pass
                return {}
                
        except Exception as e:
            print(f"LLM extraction failed: {e}")
            return {}
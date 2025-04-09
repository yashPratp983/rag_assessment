import json
import re
from typing import List, Any
import groq

class MetadataExtractor:
    """Handles extraction of structured metadata from text fields using an LLM."""
    
    def __init__(self, api_key: str, model: str = "mixtral-8x7b-32768"):
        """
        Initialize the metadata extractor.
        
        Args:
            api_key: API key for Groq
            model: Model name to use for extraction
        """
        self.client = groq.Client(api_key=api_key)
        self.model = model
        
    def _call_llm(self, prompt: str) -> str:
        """Make a call to the Groq LLM and return the response text."""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that extracts structured data."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.0  # Keep it deterministic
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"LLM call failed: {e}")
            return ""
    
    def extract_adaptive_support(self, text: str) -> str:
        """Extract adaptive support information from the text."""
        prompt = f"""
        Extract only the adaptive support information from the following text.
        Return only boolean 0 or 1.
        example:-
        1)
        - Description: "This assessment supports adaptive testing ."
        - Adaptive Support: 1

        Adaptive Support: "{text}"
        
        Adaptive Support:
        """
        
        response = self._call_llm(prompt)
        
        return response if response else text
    
    def extract_assessment_type(self, text: str) -> str:    
        
        """Extract the assessment type from the text."""
        prompt = f"""
        Extract only the assessment type from the following text.
        Return only a single string.

        example:-
        1) 
        - Description: "This is a cognitive assessment."
        - Assessment Type: "Cognitive"

        Assessment Type: "{text}"
        
        Assessment Type:
        """
        
        response = self._call_llm(prompt)
        
        return response if response else text
    
    def extract_remote_support(self, text: str) -> str:
        """Extract remote support information from the text."""
        prompt = f"""
        Extract only the remote support information from the following text.
        Return only boolean 0 or 1.
        example:-
        1)
        - Description: "This assessment can be taken remotely."
        - Remote Support: 1

        Remote Support: "{text}"
        
        Remote Support:
        """
        
        response = self._call_llm(prompt)
        
        return response if response else text
            
    def extract_minutes(self, text: str) -> int:
        """Extract the number of minutes from assessment length text."""
        prompt = f"""
        Extract only the number of minutes from the following assessment length description.
        Return only a single integer number.
        
        Assessment Length: "{text}"
        
        Minutes:
        """
        
        response = self._call_llm(prompt)
        
        try:
            return int(response)
        except (ValueError, TypeError):
            # Fallback to regex
            match = re.search(r'(\d+)', text)
            return int(match.group(1)) if match else 0
            
    def extract_languages(self, text: str) -> List[str]:
        """Extract a list of language names without regional indicators."""
        prompt = f"""
        Extract a list of languages from the following text.
        Remove any regional indicators like "(USA)" or "(International)".
        Return only a JSON array of language names.
        Note: Strictly convert all language in lower case, eg:- "English (USA)" should be "english".
        
        Languages: "{text}"
        
        JSON array:
        """
        
        response = self._call_llm(prompt)
        
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            # Fallback to regex
            return self._fallback_extract_languages(text)
    
    def _fallback_extract_languages(self, text: str) -> List[str]:
        """Fallback method to extract languages using regex."""
        languages = []
        for lang in text.split(','):
            lang = lang.strip()
            if not lang:
                continue
            base_lang = re.sub(r'\s*\([^)]*\)', '', lang).strip()
            if base_lang:
                languages.append(base_lang)
        return languages
            
    def extract_job_levels(self, text: str) -> List[str]:
        """Extract a list of job level names."""
        prompt = f"""
        Extract a list of job levels from the following text.
        Return only a JSON array of job level names.
        Job Levels: "{text}"
        
        JSON array:
        """
        
        response = self._call_llm(prompt)
        
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            # Fallback to regex
            return self._fallback_extract_job_levels(text)
    
    def _fallback_extract_job_levels(self, text: str) -> List[str]:
        """Fallback method to extract job levels using regex."""
        levels = []
        for level in text.split(','):
            level = level.strip()
            if level:
                levels.append(level)
        return levels
    
    def extract_metadata(self, field_name: str, field_value: str) -> Any:
        """Extract metadata based on field name."""
        if field_name == "Assessment Length":
            return self.extract_minutes(field_value)
        elif field_name == "Languages":
            return self.extract_languages(field_value)
        elif field_name == "Job Levels":
            return self.extract_job_levels(field_value)
        elif field_name == "Remote Support":
            return self.extract_remote_support(field_value)
        elif field_name == "Adaptive Support":
            return self.extract_adaptive_support(field_value)
        elif field_name == "Assessment Type":
            return self.extract_assessment_type(field_value)
        return field_value  # Return as is for unhandled fields

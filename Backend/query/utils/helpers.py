"""Helper functions for the Assessment Search API."""
import json

def normalize_job_level(job_level: str) -> str:
    """
    Normalize job level string for comparison by lowercasing and removing hyphens.
    
    Args:
        job_level: The job level string to normalize
        
    Returns:
        Normalized job level string
    """
    if not job_level:
        return ""
    return job_level.lower()

def parse_json_or_return_as_list(value):
    """
    Parse a JSON string to a list or convert single value to a list.
    
    Args:
        value: The value to parse (string, list, or other)
        
    Returns:
        A list containing the parsed or converted value
    """
    if not value:
        return []
        
    if isinstance(value, list):
        return value
        
    if isinstance(value, str):
        try:
            parsed = json.loads(value)
            return parsed if isinstance(parsed, list) else [parsed]
        except (json.JSONDecodeError, TypeError):
            return [value]
            
    return [value]
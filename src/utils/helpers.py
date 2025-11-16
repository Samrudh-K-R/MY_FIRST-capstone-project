"""Helper utility functions."""

from typing import Dict, Any
from datetime import datetime
import json


def validate_config(config: Dict[str, Any]) -> bool:
    """
    Validate configuration dictionary.
    
    Args:
        config: Configuration dictionary
    
    Returns:
        True if valid, raises ValueError otherwise
    """
    required_keys = ["agent"]
    
    for key in required_keys:
        if key not in config:
            raise ValueError(f"Missing required configuration key: {key}")
    
    return True


def format_output(data: Any, format_type: str = "dict") -> str:
    """
    Format output data.
    
    Args:
        data: Data to format
        format_type: Output format ("dict", "json", "string")
    
    Returns:
        Formatted string
    """
    if format_type == "json":
        return json.dumps(data, indent=2, default=str)
    elif format_type == "string":
        return str(data)
    else:
        return str(data)


def get_timestamp(format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
    """
    Get current timestamp as formatted string.
    
    Args:
        format_str: Timestamp format string
    
    Returns:
        Formatted timestamp string
    """
    return datetime.now().strftime(format_str)


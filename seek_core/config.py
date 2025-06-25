"""
Configuration module for the seek_core package.

This module provides configuration settings for the seek_core package,
including loading environment variables and providing default settings.
"""
import os
import logging
from typing import Optional, Dict, Any

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("seek_core")


def get_openai_api_key() -> str:
    """
    Get the OpenAI API key from environment variables.
    
    Returns:
        str: The OpenAI API key
    
    Raises:
        ValueError: If the API key is not found
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError(
            "OpenAI API key not found. Please set the OPENAI_API_KEY environment variable."
        )
    return api_key


def get_default_config() -> Dict[str, Any]:
    """
    Get the default configuration for the seek_core package.
    
    Returns:
        Dict[str, Any]: The default configuration
    """
    return {
        "openai_model": os.environ.get("OPENAI_MODEL", "gpt-4"),
        "temperature": float(os.environ.get("OPENAI_TEMPERATURE", "0.7")),
        "max_tokens": int(os.environ.get("OPENAI_MAX_TOKENS", "2000")),
        "min_lessons": int(os.environ.get("MIN_LESSONS", "3")),
        "max_lessons": int(os.environ.get("MAX_LESSONS", "5")),
        "min_quiz_questions": int(os.environ.get("MIN_QUIZ_QUESTIONS", "3")),
        "max_quiz_questions": int(os.environ.get("MAX_QUIZ_QUESTIONS", "5")),
        "log_level": os.environ.get("LOG_LEVEL", "INFO")
    }


# Set the log level from configuration
log_level = os.environ.get("LOG_LEVEL", "INFO")
logger.setLevel(getattr(logging, log_level))

"""
OpenAI LLM integration services for the seek-core module.

This module manages communication with OpenAI's API for generating
learning content based on learner profiles.
"""
from typing import Dict, Any, Optional
import logging
from openai import OpenAI

from seek_core.config import get_openai_api_key, get_default_config

logger = logging.getLogger(__name__)


class LLMService:
    """
    Service for interacting with OpenAI's LLM APIs.
    
    This class handles prompting, generation, and error handling for
    all LLM-related functionality within seek-core.
    """
    
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        """
        Initialize the LLM service with API key and model configuration.
        
        Args:
            api_key (Optional[str]): The OpenAI API key. If None, will look for OPENAI_API_KEY env var.
            model (Optional[str]): The OpenAI model to use. If None, will use the configured default.
        """
        # Get configuration
        config = get_default_config()
        
        # Set API key
        self.api_key = api_key or get_openai_api_key()
        
        # Set model
        self.model = model or config["openai_model"]
        
        # Initialize client
        self.client = OpenAI(api_key=self.api_key)
    
    def generate_content(self, prompt: str, system_prompt: str = None, temperature: float = 0.7) -> str:
        """
        Generate content using the OpenAI API.
        
        Args:
            prompt (str): The prompt to send to the model
            system_prompt (str, optional): System prompt to guide the model behavior
            temperature (float): Controls randomness. Higher values mean more randomness.
                                Default is 0.7.
        
        Returns:
            str: The generated content
        
        Raises:
            Exception: If API call fails
        """
        try:
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            
            messages.append({"role": "user", "content": prompt})
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Error generating content: {str(e)}")
            raise
    
    def generate_json_content(self, prompt: str, system_prompt: str = None) -> Dict[str, Any]:
        """
        Generate JSON-structured content using the OpenAI API.
        
        Args:
            prompt (str): The prompt to send to the model
            system_prompt (str, optional): System prompt to guide the model behavior
        
        Returns:
            Dict[str, Any]: The generated content as a Python dictionary
        
        Raises:
            Exception: If API call fails or response isn't valid JSON
        """
        try:
            if system_prompt is None:
                system_prompt = "You are an AI assistant that generates educational content. Always respond with valid JSON."
                
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                response_format={"type": "json_object"},
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Error generating JSON content: {str(e)}")
            raise

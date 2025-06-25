"""
Pytest configuration for the seek_core package tests.

This file contains fixtures and configuration for pytest tests.
"""
import pytest
from unittest.mock import MagicMock
from seek_core.models.schemas import LearnerProfile
from seek_core.llm.openai_service import LLMService


@pytest.fixture
def mock_llm_service():
    """
    Fixture providing a mock LLM service for testing.
    
    Returns:
        MagicMock: A mock LLM service
    """
    mock_service = MagicMock(spec=LLMService)
    mock_service.generate_content.return_value = "Sample generated content"
    mock_service.generate_json_content.return_value = '{"key": "value"}'
    return mock_service


@pytest.fixture
def sample_learner():
    """
    Fixture providing a sample learner profile for testing.
    
    Returns:
        LearnerProfile: A sample learner profile
    """
    return LearnerProfile(
        age=12,
        grade_level=6,
        learning_style="visual",
        known_topics=["fractions"],
        struggles=["decimals", "percentages"],
        goal="master converting between decimals and fractions"
    )

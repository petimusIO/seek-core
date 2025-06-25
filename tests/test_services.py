"""
Tests for the roadmap service.

This module contains tests that verify the functionality of the
roadmap service component of the seek-core package.
"""

from unittest.mock import MagicMock

import pytest

from seek_core.llm.openai_service import LLMService
from seek_core.models.schemas import LearnerProfile, MicroLesson
from seek_core.services.roadmap_service import RoadmapService


# Sample learner profile for testing
@pytest.fixture
def sample_learner_profile():
    return LearnerProfile(
        age=12,
        grade_level=6,
        learning_style="visual",
        known_topics=["fractions"],
        struggles=["decimals", "percentages"],
        goal="master converting between decimals and fractions",
    )


# Sample JSON response from LLM
@pytest.fixture
def sample_llm_response():
    return """
    [
        {
            "title": "Understanding Fractions and Decimals",
            "description": "Learn how fractions and decimals represent the same concept in different ways",
            "estimated_time_minutes": 10,
            "content": "This lesson explores how fractions and decimals are different ways to represent parts of a whole. We'll use visual models to see the connection between them."
        },
        {
            "title": "Converting Simple Fractions to Decimals",
            "description": "Practice converting basic fractions to their decimal equivalents",
            "estimated_time_minutes": 12,
            "content": "In this lesson, we'll learn how to convert fractions to decimals by dividing the numerator by the denominator. We'll start with simple fractions like 1/4, 1/2, and 3/4."
        },
        {
            "title": "Converting Decimals to Fractions",
            "description": "Learn techniques for converting decimal numbers back to fractions",
            "estimated_time_minutes": 15,
            "content": "This lesson teaches strategies for converting decimals to fractions. We'll learn about place value and how to use it to write decimals as fractions."
        }
    ]
    """


class TestRoadmapService:
    """Tests for the RoadmapService class."""

    def test_generate_roadmap_success(
        self, sample_learner_profile, sample_llm_response
    ):
        """Test successful roadmap generation."""
        # Create a mock LLM service
        mock_llm_service = MagicMock(spec=LLMService)
        mock_llm_service.generate_json_content.return_value = sample_llm_response

        # Create the roadmap service with the mock LLM service
        roadmap_service = RoadmapService(mock_llm_service)

        # Generate a roadmap
        roadmap = roadmap_service.generate_roadmap(sample_learner_profile)

        # Check that the LLM service was called
        mock_llm_service.generate_json_content.assert_called_once()

        # Check that we got the expected number of lessons
        assert len(roadmap) == 3

        # Check that each item is a MicroLesson
        for lesson in roadmap:
            assert isinstance(lesson, MicroLesson)

        # Check the content of the first lesson
        assert roadmap[0].title == "Understanding Fractions and Decimals"
        assert roadmap[0].estimated_time_minutes == 10

    def test_generate_roadmap_error_handling(self, sample_learner_profile):
        """Test error handling during roadmap generation."""
        # Create a mock LLM service that raises an exception
        mock_llm_service = MagicMock(spec=LLMService)
        mock_llm_service.generate_json_content.side_effect = Exception("API error")

        # Create the roadmap service with the mock LLM service
        roadmap_service = RoadmapService(mock_llm_service)

        # Generate a roadmap
        roadmap = roadmap_service.generate_roadmap(sample_learner_profile)

        # Check that we got a fallback roadmap
        assert len(roadmap) == 3

        # Check that each item is a MicroLesson
        for lesson in roadmap:
            assert isinstance(lesson, MicroLesson)

        # Check that the content indicates it's a fallback
        assert "placeholder" in roadmap[0].content.lower()


# Add tests for ExplanationService
class TestExplanationService:
    """Tests for the ExplanationService class."""

    @pytest.mark.parametrize(
        "learning_style,expected_content",
        [
            ("visual", "visual"),
            ("auditory", "dialogue"),
            ("kinesthetic", "hands-on"),
            ("read/write", "written"),
            ("unknown", "variety"),
        ],
    )
    def test_learning_style_guidance(self, learning_style, expected_content):
        """Test that learning style guidance contains appropriate content."""
        from seek_core.services.explanation_service import ExplanationService

        # Create a mock LLM service
        mock_llm_service = MagicMock(spec=LLMService)

        # Create the explanation service with the mock LLM service
        explanation_service = ExplanationService(mock_llm_service)

        # Get guidance for the learning style
        guidance = explanation_service._get_learning_style_guidance(learning_style)

        # Check that the guidance contains the expected content
        assert expected_content in guidance.lower()

"""
Tests for the quiz service.

This module contains tests that verify the functionality of the
quiz service component of the seek-core package.
"""
import json
import pytest
from unittest.mock import MagicMock, patch
from seek_core.models.schemas import LearnerProfile, QuizQuestion
from seek_core.services.quiz_service import QuizService
from seek_core.llm.openai_service import LLMService


# Sample JSON response from LLM
@pytest.fixture
def sample_quiz_response():
    return """
    [
        {
            "question": "Which of the following is equal to 1/4 as a decimal?",
            "options": ["A. 0.25", "B. 0.4", "C. 0.75", "D. 0.125"],
            "correct_answer_index": 0,
            "explanation": "To convert 1/4 to a decimal, divide 1 by 4. 1 ÷ 4 = 0.25"
        },
        {
            "question": "What is 0.75 as a fraction in simplest form?",
            "options": ["A. 3/4", "B. 75/100", "C. 7.5/10", "D. 7/10"],
            "correct_answer_index": 0,
            "explanation": "0.75 = 75/100, which simplifies to 3/4 when both are divided by 25."
        },
        {
            "question": "Which decimal and fraction pair is NOT equivalent?",
            "options": ["A. 0.5 and 1/2", "B. 0.33 and 1/3", "C. 0.25 and 1/4", "D. 0.2 and 1/5"],
            "correct_answer_index": 1,
            "explanation": "0.33 is not exactly equal to 1/3, which is 0.333... (a repeating decimal)."
        }
    ]
    """


class TestQuizService:
    """Tests for the QuizService class."""
    
    def test_generate_quiz_success(self, sample_learner, sample_quiz_response):
        """Test successful quiz generation."""
        # Create a mock LLM service
        mock_llm_service = MagicMock(spec=LLMService)
        mock_llm_service.generate_json_content.return_value = sample_quiz_response
        
        # Create the quiz service with the mock LLM service
        quiz_service = QuizService(mock_llm_service)
        
        # Generate a quiz
        quiz = quiz_service.generate_quiz(sample_learner)
        
        # Check that the LLM service was called
        mock_llm_service.generate_json_content.assert_called_once()
        
        # Check that we got the expected number of questions
        assert len(quiz) == 3
        
        # Check that each item is a QuizQuestion
        for question in quiz:
            assert isinstance(question, QuizQuestion)
        
        # Check the content of the first question
        assert "Which of the following is equal to 1/4 as a decimal?" in quiz[0].question
        assert len(quiz[0].options) == 4
        assert quiz[0].correct_answer_index == 0
        assert "divide" in quiz[0].explanation.lower()
    
    def test_generate_quiz_error_handling(self, sample_learner):
        """Test error handling during quiz generation."""
        # Create a mock LLM service that raises an exception
        mock_llm_service = MagicMock(spec=LLMService)
        mock_llm_service.generate_json_content.side_effect = Exception("API error")
        
        # Create the quiz service with the mock LLM service
        quiz_service = QuizService(mock_llm_service)
        
        # Generate a quiz
        quiz = quiz_service.generate_quiz(sample_learner)
        
        # Check that we got a fallback quiz
        assert len(quiz) == 3
        
        # Check that each item is a QuizQuestion
        for question in quiz:
            assert isinstance(question, QuizQuestion)
        
        # Check that the content indicates it's a fallback
        assert "placeholder" in quiz[0].explanation.lower()

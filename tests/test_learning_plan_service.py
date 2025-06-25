"""
Tests for the learning plan service.

This module contains tests that verify the functionality of the
learning plan service component of the seek-core package.
"""
import pytest
from unittest.mock import MagicMock, patch
from seek_core.models.schemas import (
    LearnerProfile, LearningPlanResponse, MicroLesson, QuizQuestion
)
from seek_core.services.learning_plan_service import LearningPlanService
from seek_core.services.roadmap_service import RoadmapService
from seek_core.services.quiz_service import QuizService
from seek_core.services.explanation_service import ExplanationService


class TestLearningPlanService:
    """Tests for the LearningPlanService class."""
    
    @patch('seek_core.services.learning_plan_service.RoadmapService')
    @patch('seek_core.services.learning_plan_service.QuizService')
    @patch('seek_core.services.learning_plan_service.ExplanationService')
    @patch('seek_core.services.learning_plan_service.LLMService')
    def test_generate_learning_plan(self, mock_llm_cls, mock_exp_cls, mock_quiz_cls, mock_roadmap_cls, sample_learner):
        """Test that the learning plan service integrates the component services."""
        # Set up the mock services
        mock_roadmap_service = MagicMock(spec=RoadmapService)
        mock_quiz_service = MagicMock(spec=QuizService)
        mock_explanation_service = MagicMock(spec=ExplanationService)
        
        # Set up the return values for the mock services
        mock_roadmap_service.generate_roadmap.return_value = [
            MicroLesson(
                title="Test Lesson 1",
                description="Description 1",
                estimated_time_minutes=10,
                content="Content 1"
            ),
            MicroLesson(
                title="Test Lesson 2",
                description="Description 2",
                estimated_time_minutes=10,
                content="Content 2"
            )
        ]
        
        mock_quiz_service.generate_quiz.return_value = [
            QuizQuestion(
                question="Test Question 1?",
                options=["A", "B", "C", "D"],
                correct_answer_index=0,
                explanation="Explanation 1"
            ),
            QuizQuestion(
                question="Test Question 2?",
                options=["A", "B", "C", "D"],
                correct_answer_index=1,
                explanation="Explanation 2"
            )
        ]
        
        mock_explanation_service.generate_explanation.return_value = "Test explanation"
        mock_explanation_service.generate_resource_link.return_value = "https://example.com/resource"
        
        # Attach the mock services to the mock classes
        mock_roadmap_cls.return_value = mock_roadmap_service
        mock_quiz_cls.return_value = mock_quiz_service
        mock_exp_cls.return_value = mock_explanation_service
        
        # Create the learning plan service
        learning_plan_service = LearningPlanService()
        
        # Generate a learning plan
        learning_plan = learning_plan_service.generate_learning_plan(sample_learner)
        
        # Check that all component services were called
        mock_roadmap_service.generate_roadmap.assert_called_once_with(sample_learner)
        mock_quiz_service.generate_quiz.assert_called_once_with(sample_learner)
        mock_explanation_service.generate_explanation.assert_called_once_with(sample_learner)
        
        # Check that the learning plan has the expected components
        assert len(learning_plan.roadmap) == 2
        assert len(learning_plan.quiz) == 2
        assert learning_plan.personalized_explanation == "Test explanation"
        
        # Check that the resource link is included for visual learners
        assert learning_plan.resource_link == "https://example.com/resource"
    
    @patch('seek_core.services.learning_plan_service.RoadmapService')
    @patch('seek_core.services.learning_plan_service.QuizService')
    @patch('seek_core.services.learning_plan_service.ExplanationService')
    @patch('seek_core.services.learning_plan_service.LLMService')
    def test_non_visual_learner_no_resource(self, mock_llm_cls, mock_exp_cls, mock_quiz_cls, mock_roadmap_cls):
        """Test that non-visual learners don't get a resource link."""
        # Create a non-visual learner
        learner = LearnerProfile(
            age=12,
            grade_level=6,
            learning_style="auditory",
            known_topics=["fractions"],
            struggles=["decimals", "percentages"],
            goal="master converting between decimals and fractions"
        )
        
        # Set up the mock services
        mock_roadmap_service = MagicMock(spec=RoadmapService)
        mock_quiz_service = MagicMock(spec=QuizService)
        mock_explanation_service = MagicMock(spec=ExplanationService)
        
        # Set up the return values for the mock services
        mock_roadmap_service.generate_roadmap.return_value = []
        mock_quiz_service.generate_quiz.return_value = []
        mock_explanation_service.generate_explanation.return_value = ""
        mock_explanation_service.generate_resource_link.return_value = None
        
        # Attach the mock services to the mock classes
        mock_roadmap_cls.return_value = mock_roadmap_service
        mock_quiz_cls.return_value = mock_quiz_service
        mock_exp_cls.return_value = mock_explanation_service
        
        # Create the learning plan service
        service = LearningPlanService()
        
        # Generate a learning plan
        learning_plan = service.generate_learning_plan(learner)
        
        # Check that no resource link is provided
        assert learning_plan.resource_link is None

"""
Main service that orchestrates the generation of complete learning plans.

This module integrates the roadmap, quiz, and explanation services
to create a comprehensive learning plan response.
"""

import logging
from typing import Any, Dict, Optional

from ..config import get_default_config
from ..llm.openai_service import LLMService
from ..models.schemas import LearnerProfile, LearningPlanResponse
from .explanation_service import ExplanationService
from .quiz_service import QuizService
from .roadmap_service import RoadmapService

logger = logging.getLogger(__name__)


class LearningPlanService:
    """
    Service for generating comprehensive learning plans.

    This class orchestrates the different services to create a complete
    learning plan response based on a learner's profile.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        config: Optional[Dict[str, Any]] = None,
    ):
        """
        Initialize the learning plan service.

        Args:
            api_key (Optional[str]): The OpenAI API key. If None, will look for OPENAI_API_KEY env var.
            model (Optional[str]): The OpenAI model to use. If None, will use default config.
            config (Optional[Dict[str, Any]]): Additional configuration parameters.
        """
        # Get configuration
        self.config = config or get_default_config()

        # Initialize services
        self.llm_service = LLMService(api_key=api_key, model=model)
        self.roadmap_service = RoadmapService(self.llm_service, config=self.config)
        self.quiz_service = QuizService(self.llm_service, config=self.config)
        self.explanation_service = ExplanationService(
            self.llm_service, config=self.config
        )

    def generate_learning_plan(self, learner: LearnerProfile) -> LearningPlanResponse:
        """
        Generate a complete learning plan for a learner.

        Args:
            learner (LearnerProfile): The learner's profile

        Returns:
            LearningPlanResponse: A complete learning plan with roadmap, quiz, and explanation
        """
        logger.info(f"Generating learning plan for learner with goal: {learner.goal}")

        # Generate all components in parallel in a production environment
        # For this MVP, we'll generate them sequentially
        try:
            roadmap = self.roadmap_service.generate_roadmap(learner)
            quiz = self.quiz_service.generate_quiz(learner)
            personalized_explanation = self.explanation_service.generate_explanation(
                learner
            )

            # Get a resource link if the learner is a visual learner
            resource_link = None
            if learner.learning_style.lower() == "visual":
                resource_link = self.explanation_service.generate_resource_link(learner)

            # Combine everything into a learning plan response
            learning_plan = LearningPlanResponse(
                roadmap=roadmap,
                quiz=quiz,
                personalized_explanation=personalized_explanation,
                resource_link=resource_link,
            )

            return learning_plan

        except Exception as e:
            logger.error(f"Error generating learning plan: {str(e)}")
            raise

    # TODO: Add methods for updating learning plans based on learner feedback
    # TODO: Implement caching for efficient generation of similar plans
    # TODO: Add analytics tracking for learning plan effectiveness

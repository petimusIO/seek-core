"""
Service for generating learning roadmaps based on learner profiles.

This module handles the creation of structured learning paths tailored
to a learner's specific needs and goals.
"""

import json
import logging
from typing import Any, Dict, List, Optional

from ..config import get_default_config
from ..llm.openai_service import LLMService
from ..models.schemas import LearnerProfile, MicroLesson

logger = logging.getLogger(__name__)


class RoadmapService:
    """
    Service for generating personalized learning roadmaps.

    This class uses LLM capabilities to create a sequence of micro-lessons
    tailored to the learner's profile and learning goals.
    """

    def __init__(
        self, llm_service: LLMService, config: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize the roadmap service with an LLM service.

        Args:
            llm_service (LLMService): The LLM service to use for generation
            config (Optional[Dict[str, Any]]): Configuration options
        """
        self.llm_service = llm_service
        self.config = config or get_default_config()

    def generate_roadmap(self, learner: LearnerProfile) -> List[MicroLesson]:
        """
        Generate a personalized learning roadmap for a learner.

        Args:
            learner (LearnerProfile): The learner's profile

        Returns:
            List[MicroLesson]: A list of 3-5 micro-lessons forming a learning roadmap
        """
        logger.info(f"Generating roadmap for learner with goal: {learner.goal}")

        # Create a prompt for the LLM
        prompt = f"""
        Create a personalized learning roadmap consisting of 3-5 micro-lessons to help a student achieve their learning goal.

        STUDENT INFORMATION:
        - Age: {learner.age}
        - Grade level: {learner.grade_level}
        - Learning style: {learner.learning_style}
        - Topics they already know: {', '.join(learner.known_topics)}
        - Topics they struggle with: {', '.join(learner.struggles)}
        - Learning goal: {learner.goal}

        Each micro-lesson should include:
        1. A clear, engaging title
        2. A brief description of what will be learned
        3. Estimated time to complete in minutes (between 5-15 minutes per lesson)
        4. Detailed content that teaches the concept in a way that's appropriate for the student's age and learning style

        The lessons should build upon each other and be sequenced logically to help the student progress toward their goal.
        Format your response as a JSON array of lessons with the following structure:
        [
            {{
                "title": "Lesson Title",
                "description": "Brief description",
                "estimated_time_minutes": 10,
                "content": "Detailed lesson content"
            }},
            // more lessons...
        ]
        """

        system_prompt = """
        You are an expert educational content creator specializing in creating personalized learning paths.
        Your task is to create engaging, age-appropriate micro-lessons that match the student's learning style
        and build toward their specific learning goal. Focus on clarity, engagement, and logical progression.
        Always format your response as valid JSON.
        """

        try:
            # Generate the roadmap using the LLM
            json_response = self.llm_service.generate_json_content(
                prompt, system_prompt
            )
            roadmap_data = json.loads(json_response)

            # Convert the JSON response to a list of MicroLesson objects
            roadmap = [MicroLesson(**lesson) for lesson in roadmap_data]

            # Ensure we have at least min_lessons and at most max_lessons
            min_lessons = self.config.get("min_lessons", 3)
            max_lessons = self.config.get("max_lessons", 5)

            if len(roadmap) < min_lessons:
                logger.warning(
                    f"Generated roadmap has fewer than {min_lessons} lessons: {len(roadmap)}"
                )
            elif len(roadmap) > max_lessons:
                logger.warning(
                    f"Generated roadmap has more than {max_lessons} lessons: {len(roadmap)}"
                )
                roadmap = roadmap[:max_lessons]  # Truncate to max_lessons

            return roadmap

        except Exception as e:
            logger.error(f"Error generating roadmap: {str(e)}")
            # Provide a fallback roadmap in case of errors
            return [
                MicroLesson(
                    title="Understanding the Basics",
                    description="Introduction to the fundamental concepts",
                    estimated_time_minutes=10,
                    content="This is a placeholder lesson due to an error in generation.",
                ),
                MicroLesson(
                    title="Building Core Skills",
                    description="Practice with key techniques",
                    estimated_time_minutes=10,
                    content="This is a placeholder lesson due to an error in generation.",
                ),
                MicroLesson(
                    title="Applying Your Knowledge",
                    description="Real-world applications and practice",
                    estimated_time_minutes=10,
                    content="This is a placeholder lesson due to an error in generation.",
                ),
            ]

    # TODO: Add methods for adapting roadmaps based on learning progress
    # TODO: Implement more sophisticated sequencing algorithms

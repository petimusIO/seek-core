"""
Main module for the seek_core package.

This module provides convenient access to the core functionality
of the seek_core package.
"""

from typing import Any, Dict, Optional

from .models.schemas import LearnerProfile
from .services.learning_plan_service import LearningPlanService


def generate_learning_plan(
    learner_data: Dict[str, Any],
    api_key: Optional[str] = None,
    model: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Generate a learning plan from learner data.

    This is the main entry point for the seek_core package.

    Args:
        learner_data (Dict[str, Any]): Dictionary containing learner profile data
        api_key (Optional[str]): OpenAI API key. If None, will look in env vars.
        model (Optional[str]): OpenAI model to use. If None, will use default config.

    Returns:
        Dict[str, Any]: The generated learning plan as a dictionary

    Example:
        >>> from seek_core import generate_learning_plan
        >>>
        >>> # Create a learner profile for a middle school student
        >>> learner_data = {
        ...     "age": 12,
        ...     "grade_level": 6,
        ...     "learning_style": "visual",
        ...     "known_topics": ["fractions"],
        ...     "struggles": ["decimals", "percentages"],
        ...     "goal": "master converting between decimals and fractions"
        ... }
        >>>
        >>> # Generate a personalized learning plan
        >>> learning_plan = generate_learning_plan(learner_data)
        >>>
        >>> # Access specific components
        >>> # Get the roadmap lessons
        >>> for i, lesson in enumerate(learning_plan["roadmap"], 1):
        ...     print(f"Lesson {i}: {lesson['title']}")
        ...     print(f"  - Description: {lesson['description']}")
        ...     print(f"  - Time: {lesson['estimated_time_minutes']} minutes")
        >>>
        >>> # Get the personalized explanation
        >>> explanation = learning_plan["personalized_explanation"]
        >>>
        >>> # Get the quiz questions
        >>> for i, question in enumerate(learning_plan["quiz"], 1):
        ...     print(f"Question {i}: {question['question']}")
        ...     print(f"  Answer: {question['options'][question['correct_answer_index']]}")
    """
    # Convert the dictionary to a LearnerProfile object
    learner = LearnerProfile(**learner_data)

    # Initialize the learning plan service with provided API key and model
    service = LearningPlanService(api_key=api_key, model=model)

    # Generate the learning plan
    learning_plan = service.generate_learning_plan(learner)

    # Convert the learning plan to a dictionary
    return learning_plan.model_dump()

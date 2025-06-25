"""
Pydantic models for representing learner profiles and learning plan responses.

These models define the structure of the data flowing through the seek-core system.
"""

from typing import List, Optional

from pydantic import BaseModel, Field


class LearnerProfile(BaseModel):
    """
    Represents a learner's profile with their educational background and learning preferences.

    Attributes:
        age (int): The age of the learner
        grade_level (int): The current grade level of the learner (K-12)
        learning_style (str): The learning style preference (visual, auditory, kinesthetic, etc.)
        known_topics (List[str]): Topics the learner already understands
        struggles (List[str]): Topics the learner finds challenging
        goal (str): The learning goal the learner wants to achieve
    """

    age: int = Field(..., description="Age of the learner")
    grade_level: int = Field(..., description="Current grade level (K-12)")
    learning_style: str = Field(..., description="Learning style preference")
    known_topics: List[str] = Field(
        default_factory=list, description="Topics the learner already understands"
    )
    struggles: List[str] = Field(
        default_factory=list, description="Topics the learner finds challenging"
    )
    goal: str = Field(..., description="Learning goal to achieve")


class MicroLesson(BaseModel):
    """
    Represents a single micro-lesson within a learning roadmap.

    Attributes:
        title (str): The title of the micro-lesson
        description (str): Brief description of what will be learned
        estimated_time_minutes (int): Estimated time to complete in minutes
        content (str): The actual content of the micro-lesson
    """

    title: str
    description: str
    estimated_time_minutes: int
    content: str


class QuizQuestion(BaseModel):
    """
    Represents a multiple-choice quiz question.

    Attributes:
        question (str): The question text
        options (List[str]): The multiple choice options
        correct_answer_index (int): The index of the correct answer in options
        explanation (str): An explanation of why the correct answer is correct
    """

    question: str
    options: List[str]
    correct_answer_index: int
    explanation: str


class LearningPlanResponse(BaseModel):
    """
    The complete learning plan response generated for a learner.

    Attributes:
        roadmap (List[MicroLesson]): A sequence of 3-5 micro-lessons
        quiz (List[QuizQuestion]): 3-5 multiple-choice quiz questions
        personalized_explanation (str): A personalized explanation of the goal topic
        resource_link (Optional[str]): Optional link to additional learning resources
    """

    roadmap: List[MicroLesson] = Field(..., description="Sequence of micro-lessons")
    quiz: List[QuizQuestion] = Field(..., description="Multiple-choice quiz questions")
    personalized_explanation: str = Field(
        ..., description="Personalized explanation of the goal topic"
    )
    resource_link: Optional[str] = Field(
        None, description="Optional link to additional resources"
    )

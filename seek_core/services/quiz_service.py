"""
Service for generating personalized quizzes based on learner profiles.

This module handles the creation of adaptive quiz questions to test 
a learner's understanding of educational content.
"""
import json
from typing import List, Optional, Dict, Any
import logging
from ..models.schemas import LearnerProfile, QuizQuestion
from ..llm.openai_service import LLMService
from ..config import get_default_config


logger = logging.getLogger(__name__)


class QuizService:
    """
    Service for generating personalized quiz questions.
    
    This class uses LLM capabilities to create multiple-choice questions
    tailored to the learner's profile and learning goals.
    """
    
    def __init__(self, llm_service: LLMService, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the quiz service with an LLM service.
        
        Args:
            llm_service (LLMService): The LLM service to use for generation
            config (Optional[Dict[str, Any]]): Configuration options
        """
        self.llm_service = llm_service
        self.config = config or get_default_config()
    
    def generate_quiz(self, learner: LearnerProfile) -> List[QuizQuestion]:
        """
        Generate a personalized quiz for a learner.
        
        Args:
            learner (LearnerProfile): The learner's profile
        
        Returns:
            List[QuizQuestion]: A list of 3-5 multiple-choice quiz questions
        """
        logger.info(f"Generating quiz for learner with goal: {learner.goal}")
        
        # Create a prompt for the LLM
        prompt = f"""
        Create a personalized quiz consisting of 3-5 multiple-choice questions to assess understanding of concepts related to the student's learning goal.
        
        STUDENT INFORMATION:
        - Age: {learner.age}
        - Grade level: {learner.grade_level}
        - Learning style: {learner.learning_style}
        - Topics they already know: {', '.join(learner.known_topics)}
        - Topics they struggle with: {', '.join(learner.struggles)}
        - Learning goal: {learner.goal}
        
        Each quiz question should include:
        1. A clear question that tests understanding, not just memorization
        2. Four multiple-choice options (labeled A, B, C, D)
        3. The correct answer index (0 for A, 1 for B, 2 for C, 3 for D)
        4. A brief explanation of why the correct answer is right
        
        The questions should vary in difficulty, testing different aspects of the learning goal.
        Use age-appropriate language and examples.
        
        Format your response as a JSON array with the following structure:
        [
            {{
                "question": "What is X?",
                "options": ["A. Option 1", "B. Option 2", "C. Option 3", "D. Option 4"],
                "correct_answer_index": 2,
                "explanation": "Explanation why C is correct"
            }},
            // more questions...
        ]
        """
        
        system_prompt = """
        You are an expert educational assessment creator specializing in developing personalized quizzes.
        Your task is to create clear, engaging multiple-choice questions that appropriately assess 
        the student's understanding of concepts related to their learning goal.
        Questions should be age-appropriate and align with the student's grade level.
        Always format your response as valid JSON.
        """
        
        try:
            # Generate the quiz using the LLM
            json_response = self.llm_service.generate_json_content(prompt, system_prompt)
            quiz_data = json.loads(json_response)
            
            # Convert the JSON response to a list of QuizQuestion objects
            quiz = [QuizQuestion(**question) for question in quiz_data]
            
            # Ensure we have at least min_questions and at most max_questions
            min_questions = self.config.get("min_quiz_questions", 3)
            max_questions = self.config.get("max_quiz_questions", 5)
            
            if len(quiz) < min_questions:
                logger.warning(f"Generated quiz has fewer than {min_questions} questions: {len(quiz)}")
            elif len(quiz) > max_questions:
                logger.warning(f"Generated quiz has more than {max_questions} questions: {len(quiz)}")
                quiz = quiz[:max_questions]  # Truncate to max_questions
                
            return quiz
            
        except Exception as e:
            logger.error(f"Error generating quiz: {str(e)}")
            # Provide a fallback quiz in case of errors
            return [
                QuizQuestion(
                    question="What is the first step in solving this type of problem?",
                    options=["A. Step 1", "B. Step 2", "C. Step 3", "D. Step 4"],
                    correct_answer_index=0,
                    explanation="This is a placeholder question due to an error in generation."
                ),
                QuizQuestion(
                    question="Which concept is most important to understand?",
                    options=["A. Concept 1", "B. Concept 2", "C. Concept 3", "D. Concept 4"],
                    correct_answer_index=1,
                    explanation="This is a placeholder question due to an error in generation."
                ),
                QuizQuestion(
                    question="How would you apply this knowledge?",
                    options=["A. Application 1", "B. Application 2", "C. Application 3", "D. Application 4"],
                    correct_answer_index=2,
                    explanation="This is a placeholder question due to an error in generation."
                )
            ]
    
    # TODO: Implement adaptive quiz generation based on learner performance
    # TODO: Add support for different question types (not just multiple choice)

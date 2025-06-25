"""
Service for generating personalized explanations based on learner profiles.

This module handles the creation of tailored explanations that match
a learner's learning style and educational background.
"""
import logging
from typing import Optional, Dict, Any
from ..models.schemas import LearnerProfile
from ..llm.openai_service import LLMService
from ..config import get_default_config


logger = logging.getLogger(__name__)


class ExplanationService:
    """
    Service for generating personalized concept explanations.
    
    This class uses LLM capabilities to create explanations tailored
    to the learner's profile, learning style, and educational goals.
    """
    
    def __init__(self, llm_service: LLMService, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the explanation service with an LLM service.
        
        Args:
            llm_service (LLMService): The LLM service to use for generation
            config (Optional[Dict[str, Any]]): Configuration options
        """
        self.llm_service = llm_service
        self.config = config or get_default_config()
    
    def generate_explanation(self, learner: LearnerProfile) -> str:
        """
        Generate a personalized explanation of a concept for a learner.
        
        Args:
            learner (LearnerProfile): The learner's profile
        
        Returns:
            str: A personalized explanation tailored to the learner's style and needs
        """
        logger.info(f"Generating explanation for learner with goal: {learner.goal} and learning style: {learner.learning_style}")
        
        # Create a prompt based on learning style
        learning_style_guidance = self._get_learning_style_guidance(learner.learning_style)
        
        prompt = f"""
        Create a personalized explanation of the concept related to the student's learning goal.
        
        STUDENT INFORMATION:
        - Age: {learner.age}
        - Grade level: {learner.grade_level}
        - Learning style: {learner.learning_style}
        - Topics they already know: {', '.join(learner.known_topics)}
        - Topics they struggle with: {', '.join(learner.struggles)}
        - Learning goal: {learner.goal}
        
        GUIDELINES FOR EXPLANATION:
        {learning_style_guidance}
        
        The explanation should:
        - Use age-appropriate language and examples
        - Connect to topics the student already knows when possible
        - Address specific struggles the student has mentioned
        - Be engaging and clear
        - Be approximately 300-500 words in length
        
        Format your response as a cohesive, friendly explanation that directly addresses the student.
        """
        
        system_prompt = """
        You are an expert educational content creator specializing in creating personalized explanations.
        Your task is to create clear, engaging explanations that match the student's learning style 
        and build upon their existing knowledge while addressing their specific learning goal.
        """
        
        try:
            # Generate the explanation using the LLM
            explanation = self.llm_service.generate_content(prompt, system_prompt)
            return explanation
            
        except Exception as e:
            logger.error(f"Error generating explanation: {str(e)}")
            return (
                "I'm sorry, I wasn't able to generate a personalized explanation at this time. "
                "Let's continue with the learning roadmap and quiz to help you understand the concept better."
            )
    
    def _get_learning_style_guidance(self, learning_style: str) -> str:
        """
        Get specific guidance for creating explanations based on learning style.
        
        Args:
            learning_style (str): The learner's preferred learning style
        
        Returns:
            str: Guidance for creating content for this learning style
        """
        learning_style = learning_style.lower()
        
        if "visual" in learning_style:
            return """
            - Use visual language and metaphors
            - Describe visual elements like diagrams, charts, and images
            - Use spatial relationships and visual organization
            - Suggest the student draw or visualize concepts
            - Reference colors, shapes, and patterns when relevant
            """
        elif "auditory" in learning_style:
            return """
            - Use rhythmic language and mnemonics
            - Include dialogue and discussion elements
            - Suggest speaking concepts aloud or discussing with others
            - Use sound-based metaphors and examples
            - Emphasize the importance of listening and verbal repetition
            """
        elif "kinesthetic" in learning_style or "tactile" in learning_style:
            return """
            - Include hands-on activities and physical metaphors
            - Suggest physical actions to practice concepts
            - Use examples involving movement or physical manipulation
            - Connect concepts to physical sensations and experiences
            - Encourage learning through doing and practical application
            """
        elif "read" in learning_style or "write" in learning_style:
            return """
            - Use clear, concise written explanations
            - Suggest note-taking strategies and written exercises
            - Include lists, definitions, and key terms
            - Reference written materials and examples
            - Encourage summarizing concepts in writing
            """
        else:
            # Default guidance for unspecified learning styles
            return """
            - Use a variety of examples and explanations
            - Include multiple modalities (visual, verbal, practical)
            - Focus on clear, structured explanations
            - Provide concrete examples and applications
            - Relate concepts to real-world scenarios
            """
    
    def generate_resource_link(self, learner: LearnerProfile) -> str:
        """
        Generate a link to an additional learning resource based on the learner's profile.
        
        Args:
            learner (LearnerProfile): The learner's profile
        
        Returns:
            str: A link to a relevant learning resource, or None if not applicable
        """
        # This is a placeholder - in a real implementation, you would:
        # 1. Curate a database of learning resources
        # 2. Use the learner profile to select appropriate resources
        # 3. Return a relevant link based on topic, learning style, age, etc.
        
        # For now, we're just returning a placeholder based on learning style
        if learner.learning_style.lower() == "visual":
            return "https://www.khanacademy.org/math/arithmetic/fraction-arithmetic"
        return None
    
    # TODO: Implement more sophisticated content adaptation based on learner's age/grade level
    # TODO: Add personalization based on cultural context and interests

"""
Example usage of the seek_core package.

This script demonstrates how to use the seek_core package to generate
personalized learning plans for students.
"""
import os
import sys
import json
import argparse
import logging
from typing import Dict, Any, Optional

from seek_core import generate_learning_plan
from seek_core.config import get_default_config

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("seek_core_example")


def parse_args() -> argparse.Namespace:
    """
    Parse command line arguments.
    
    Returns:
        argparse.Namespace: The parsed arguments
    """
    parser = argparse.ArgumentParser(
        description="Example script for generating a personalized learning plan"
    )
    parser.add_argument(
        "--model",
        type=str,
        help="OpenAI model to use (default: uses environment variable or gpt-4)",
        default=None
    )
    parser.add_argument(
        "--output",
        type=str,
        help="File to save the learning plan to (default: none)",
        default=None
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose output"
    )
    return parser.parse_args()


def get_sample_learner_profile() -> Dict[str, Any]:
    """
    Get a sample learner profile for demonstration purposes.
    
    Returns:
        Dict[str, Any]: A sample learner profile
    """
    return {
        "age": 12,
        "grade_level": 6,
        "learning_style": "visual",
        "known_topics": ["fractions"],
        "struggles": ["decimals", "percentages"],
        "goal": "master converting between decimals and fractions"
    }


def save_to_file(data: Dict[str, Any], filename: str) -> None:
    """
    Save data to a JSON file.
    
    Args:
        data (Dict[str, Any]): The data to save
        filename (str): The file to save to
    """
    try:
        with open(filename, "w") as f:
            json.dump(data, f, indent=2)
        logger.info(f"Learning plan saved to {filename}")
    except Exception as e:
        logger.error(f"Error saving to file {filename}: {str(e)}")


def main() -> None:
    """Demonstrate the functionality of seek_core."""
    args = parse_args()
    
    # Configure logging
    if args.verbose:
        logging.getLogger("seek_core").setLevel(logging.DEBUG)
        logger.setLevel(logging.DEBUG)
    
    # Check for OpenAI API key
    if not os.environ.get("OPENAI_API_KEY"):
        logger.error("OPENAI_API_KEY environment variable not set.")
        logger.error("Please set your OpenAI API key to use this example.")
        logger.error("Example: export OPENAI_API_KEY='your-api-key'")
        sys.exit(1)
    
    # Get a sample learner profile
    learner_data = get_sample_learner_profile()
    
    logger.info("Generating learning plan for:")
    logger.info(json.dumps(learner_data, indent=2))
    logger.info("This may take a minute...")
    
    try:
        # Generate a learning plan
        learning_plan = generate_learning_plan(learner_data, model=args.model)
        
        # Save to file if requested
        if args.output:
            save_to_file(learning_plan, args.output)
        
        # Print the structure of the learning plan
        print("\nGenerated Learning Plan:")
        print(f"- Roadmap: {len(learning_plan['roadmap'])} micro-lessons")
        print(f"- Quiz: {len(learning_plan['quiz'])} questions")
        print(f"- Personalized Explanation: {len(learning_plan['personalized_explanation'])} characters")
        if learning_plan.get('resource_link'):
            print(f"- Resource Link: {learning_plan['resource_link']}")
        
        # Print the titles of the micro-lessons
        print("\nRoadmap Lessons:")
        for i, lesson in enumerate(learning_plan['roadmap'], 1):
            print(f"{i}. {lesson['title']} ({lesson['estimated_time_minutes']} min)")
        
        # Print the first question as an example
        if learning_plan['quiz']:
            print("\nSample Quiz Question:")
            question = learning_plan['quiz'][0]
            print(question['question'])
            for option in question['options']:
                print(f"  {option}")
            correct_option = question['options'][question['correct_answer_index']]
            print(f"Correct Answer: {correct_option}")
        
        # Print the first part of the explanation
        print("\nPersonalized Explanation Preview:")
        preview_length = min(200, len(learning_plan['personalized_explanation']))
        print(f"{learning_plan['personalized_explanation'][:preview_length]}...")
        print(f"... (continued for {len(learning_plan['personalized_explanation']) - preview_length} more characters)")
        
    except Exception as e:
        logger.error(f"Error generating learning plan: {str(e)}", exc_info=args.verbose)
        sys.exit(1)


if __name__ == "__main__":
    main()

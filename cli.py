#!/usr/bin/env python
"""
Command-line interface for the seek-core package.

This script provides a simple way to use the seek-core package from the command line.
"""
import os
import sys
import json
import argparse
from typing import Dict, Any

from seek_core import generate_learning_plan
from seek_core.models.schemas import LearnerProfile


def parse_args() -> argparse.Namespace:
    """
    Parse command-line arguments.
    
    Returns:
        argparse.Namespace: The parsed arguments
    """
    parser = argparse.ArgumentParser(
        description="Generate personalized learning plans for students"
    )
    
    # Add arguments for the learner profile
    parser.add_argument(
        "--age",
        type=int,
        help="Age of the learner",
        required=True
    )
    parser.add_argument(
        "--grade-level",
        type=int,
        help="Grade level of the learner",
        required=True
    )
    parser.add_argument(
        "--learning-style",
        type=str,
        help="Learning style of the learner (visual, auditory, kinesthetic, etc.)",
        required=True
    )
    parser.add_argument(
        "--known-topics",
        type=str,
        help="Comma-separated list of topics the learner already knows",
        default=""
    )
    parser.add_argument(
        "--struggles",
        type=str,
        help="Comma-separated list of topics the learner struggles with",
        default=""
    )
    parser.add_argument(
        "--goal",
        type=str,
        help="Learning goal for the learner",
        required=True
    )
    parser.add_argument(
        "--output",
        type=str,
        help="Output file path (default: stdout)",
        default=None
    )
    parser.add_argument(
        "--pretty",
        action="store_true",
        help="Pretty-print the JSON output"
    )
    
    return parser.parse_args()


def create_learner_profile(args: argparse.Namespace) -> Dict[str, Any]:
    """
    Create a learner profile from command-line arguments.
    
    Args:
        args (argparse.Namespace): The parsed command-line arguments
    
    Returns:
        Dict[str, Any]: The learner profile as a dictionary
    """
    return {
        "age": args.age,
        "grade_level": args.grade_level,
        "learning_style": args.learning_style,
        "known_topics": [t.strip() for t in args.known_topics.split(",")] if args.known_topics else [],
        "struggles": [s.strip() for s in args.struggles.split(",")] if args.struggles else [],
        "goal": args.goal
    }


def main() -> None:
    """Run the CLI application."""
    # Check for OpenAI API key
    if not os.environ.get("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY environment variable not set", file=sys.stderr)
        sys.exit(1)
    
    # Parse arguments
    args = parse_args()
    
    # Create learner profile
    learner_data = create_learner_profile(args)
    
    try:
        # Generate learning plan
        learning_plan = generate_learning_plan(learner_data)
        
        # Format the output
        indent = 2 if args.pretty else None
        output = json.dumps(learning_plan, indent=indent)
        
        # Write to file or stdout
        if args.output:
            with open(args.output, "w") as f:
                f.write(output)
        else:
            print(output)
            
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

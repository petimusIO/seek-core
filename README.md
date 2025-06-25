# seek-core

Seek's core logic for personalized learning roadmap generation and adaptive learning engine.

## Overview

seek-core is a Python package for generating AI-personalized learning plans for students. The module takes a learner profile as input and produces a tailored learning plan including:

- A sequence of 3-5 micro-lessons (learning roadmap)
- A quiz with 3-5 multiple-choice questions
- A personalized explanation of the target concept
- Optional resource links for visual learners

## Features

- **Personalized Learning Roadmaps**: Create custom learning paths based on student's age, grade level, learning style, and goals.
- **Adaptive Quizzes**: Generate appropriate assessment questions to test understanding.
- **Learning Style Adaptation**: Content tailored to visual, auditory, kinesthetic, or read/write learning styles.
- **Goal-Oriented Learning**: Content focused on helping the student achieve their specific learning goal.
- **Simple Integration**: Easy to integrate with other systems through a clean Python API.
- **Flexible Configuration**: Configurable through environment variables or directly in code.

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- OpenAI API key

### Installation

```bash
# Clone the repository
git clone https://github.com/petimus/seek-core.git
cd seek-core

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate

# Set up your environment variables
cp .env.example .env
# Edit .env to add your OpenAI API key

# Install the package
pip install -e .
```

### Basic Usage

```python
from seek_core import generate_learning_plan

# Create a learner profile
learner_data = {
    "age": 12,
    "grade_level": 6,
    "learning_style": "visual",
    "known_topics": ["fractions"],
    "struggles": ["decimals", "percentages"],
    "goal": "master converting between decimals and fractions"
}

# Generate a learning plan
learning_plan = generate_learning_plan(learner_data)

# Access the components
roadmap = learning_plan["roadmap"]
quiz = learning_plan["quiz"]
explanation = learning_plan["personalized_explanation"]
resource_link = learning_plan["resource_link"]
```

### Command Line Interface

The package includes a command-line interface for easy use:

```bash
# Set your OpenAI API key
export OPENAI_API_KEY='your-api-key'

# Generate a learning plan
./cli.py --age 12 \
         --grade-level 6 \
         --learning-style visual \
         --known-topics "fractions" \
         --struggles "decimals,percentages" \
         --goal "master converting between decimals and fractions" \
         --pretty \
         --output learning_plan.json

# Display help
./cli.py --help
```

### Example Script

The package also includes an example script that demonstrates the functionality:

```bash
# Set your OpenAI API key
export OPENAI_API_KEY='your-api-key'

# Run the example
python example.py
```

## Project Structure

```
seek_core/
├── models/           # Pydantic models and schemas
├── services/         # Core business logic services
│   ├── roadmap_service.py      # Generates learning roadmap
│   ├── quiz_service.py         # Generates quiz questions
│   ├── explanation_service.py  # Creates personalized explanations
│   └── learning_plan_service.py # Orchestrates the entire process
├── llm/              # OpenAI/LLM integration
├── config.py         # Configuration and settings management
tests/               # Unit and integration tests
```

## Configuration

The package can be configured using environment variables:

| Environment Variable | Description | Default |
|---------------------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key | (required) |
| `OPENAI_MODEL` | OpenAI model to use | `gpt-4` |
| `OPENAI_TEMPERATURE` | Temperature for generation | `0.7` |
| `OPENAI_MAX_TOKENS` | Maximum tokens for generation | `2000` |
| `MIN_LESSONS` | Minimum number of lessons in roadmap | `3` |
| `MAX_LESSONS` | Maximum number of lessons in roadmap | `5` |
| `MIN_QUIZ_QUESTIONS` | Minimum number of quiz questions | `3` |
| `MAX_QUIZ_QUESTIONS` | Maximum number of quiz questions | `5` |
| `LOG_LEVEL` | Logging level | `INFO` |

## Requirements

- Python 3.8+
- OpenAI API key (set as OPENAI_API_KEY environment variable)
- Pydantic 2.0+
- OpenAI Python SDK 1.0.0+
- Pytest 7.0.0+ (for development)

## 🐳 Docker Usage

You can run seek-core using Docker for a consistent environment:

```bash
# Build the Docker image
docker build -t seek-core .

# Run the container
docker run -it --rm \
  -e OPENAI_API_KEY="your-api-key" \
  seek-core

# Run a specific example
docker run -it --rm \
  -e OPENAI_API_KEY="your-api-key" \
  seek-core python example.py

# Run CLI with arguments
docker run -it --rm \
  -e OPENAI_API_KEY="your-api-key" \
  seek-core ./cli.py --age 12 --grade-level 6 --learning-style visual --goal "learn algebra"
```

## 🧪 Testing

We use pytest for testing and provide several make commands for convenience:

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
make test

# Run tests with coverage
make test-cov

# Run linting checks
make lint

# Format code
make format
```

## 🔐 Environment Variables

seek-core uses environment variables for configuration:

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key (required) | - |
| `OPENAI_MODEL` | OpenAI model to use | `gpt-4` |
| `OPENAI_TEMPERATURE` | Controls randomness | `0.7` |
| `MIN_LESSONS` | Minimum lessons in roadmap | `3` |
| `MAX_LESSONS` | Maximum lessons in roadmap | `5` |
| `LOG_LEVEL` | Logging level | `INFO` |

Copy the `.env.example` file to `.env` and update the values accordingly.

## 🧰 Tooling

This project comes with several tools for development:

- **VS Code Dev Container**: Full development environment with all dependencies
- **Makefile**: Convenience commands for common tasks
- **GitHub Actions**: CI pipeline for automated testing
- **Docker**: Containerization for consistent environments
- **flake8/black/isort**: Code linting and formatting
- **pytest/coverage**: Testing and coverage reporting

To use the VS Code Dev Container:
1. Install the VS Code Remote Development extension
2. Open the command palette and run "Remote-Containers: Open Folder in Container"
3. VS Code will build the dev container and provide a ready-to-use environment

## License

Proprietary - Copyright © 2025 Petimus

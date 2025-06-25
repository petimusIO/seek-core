#!/usr/bin/env python
"""
Autofix linting issues in the codebase.

This script runs formatters to automatically fix most linting issues:
1. Black to fix formatting issues
2. isort to fix import sorting
3. A custom script to fix newlines at end of files and trailing whitespace
"""
import os
import re
import sys
from pathlib import Path


def fix_newlines_and_whitespace(file_path):
    """Fix newlines at end of files and trailing whitespace."""
    with open(file_path, "r") as f:
        content = f.read()
    
    # Fix trailing whitespace
    content = re.sub(r"[ \t]+$", "", content, flags=re.MULTILINE)
    
    # Ensure exactly one newline at the end of file
    content = content.rstrip("\n") + "\n"
    
    with open(file_path, "w") as f:
        f.write(content)


def get_python_files(root_dirs):
    """Get all Python files in the given directories."""
    python_files = []
    for root_dir in root_dirs:
        for root, _, files in os.walk(root_dir):
            for file in files:
                if file.endswith(".py"):
                    python_files.append(os.path.join(root, file))
    return python_files


def fix_unused_imports(file_path):
    """Use autoflake to fix unused imports."""
    # We don't have autoflake installed, so just print a warning
    print(f"Warning: You might need to manually fix unused imports in {file_path}")


def main():
    """Run fixers on all Python files."""
    root_dirs = ["seek_core", "tests"]
    python_files = get_python_files(root_dirs)
    
    print(f"Found {len(python_files)} Python files to process")
    
    # Fix newlines and whitespace
    for file in python_files:
        fix_newlines_and_whitespace(file)
    print("Fixed newlines and whitespace")
    
    # Run black for formatting with increased line length
    print("Running black formatter...")
    os.system("black --line-length 160 seek_core tests")
    
    # Run isort for import sorting, configured to be black-compatible
    print("Running isort for import sorting...")
    os.system("isort --profile black --line-length 160 seek_core tests")
    
    # Remove unused imports if autoflake is available
    try:
        import importlib
        importlib.import_module('autoflake')
        print("Running autoflake to remove unused imports...")
        os.system("autoflake --in-place --remove-all-unused-imports --recursive seek_core tests")
        print("Autoflake completed")
    except ImportError:
        print("Autoflake not available - skipping unused import removal")
    
    print("\nAutomatic fixes applied. Some issues might require manual fixes:")
    print("- Unused imports (F401): Remove or use the imports")
    print("- Line too long (E501): Split long lines")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

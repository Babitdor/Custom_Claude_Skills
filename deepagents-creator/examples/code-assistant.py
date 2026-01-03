#!/usr/bin/env python3
"""
Code Assistant Agent Example

A DeepAgent specialized in writing, analyzing, and refactoring code
with comprehensive testing and documentation.
"""

import os
from deepagents import create_deep_agent
from deepagents.backends import LocalBackend
from langchain_core.tools import tool
import subprocess


@tool
def run_python_code(code: str) -> str:
    """Run Python code and return the output."""
    try:
        result = subprocess.run(
            ["python", "-c", code],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        output = result.stdout
        if result.stderr:
            output += f"\n[STDERR]\n{result.stderr}"
        
        return output or "[No output]"
    
    except subprocess.TimeoutExpired:
        return "Error: Code execution timed out (10s limit)"
    except Exception as e:
        return f"Error running code: {e}"


@tool
def run_tests(filepath: str) -> str:
    """Run pytest on a test file."""
    try:
        result = subprocess.run(
            ["pytest", filepath, "-v"],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        return result.stdout + result.stderr
    
    except subprocess.TimeoutExpired:
        return "Error: Tests timed out (30s limit)"
    except Exception as e:
        return f"Error running tests: {e}"


@tool
def lint_code(filepath: str) -> str:
    """Run pylint on a Python file."""
    try:
        result = subprocess.run(
            ["pylint", filepath],
            capture_output=True,
            text=True,
            timeout=15
        )
        
        return result.stdout or "No linting issues found"
    
    except subprocess.TimeoutExpired:
        return "Error: Linting timed out"
    except Exception as e:
        return f"Error linting code: {e}"


def create_code_assistant():
    """Create a code assistant agent."""
    
    # Use local filesystem for code projects
    backend = LocalBackend(
        base_path=os.path.expanduser("~/.deepagents/code-workspace")
    )
    
    # Code assistant system prompt
    system_prompt = """
    You are an expert software engineer and coding assistant.
    
    Coding Workflow:
    1. **Understand Requirements**: Clarify what needs to be built
    2. **Plan Implementation**: Use write_todos to plan the work
    3. **Write Code**:
       - Follow language best practices
       - Include comprehensive type hints
       - Add detailed docstrings
       - Implement error handling
       - Write clean, readable code
    4. **Test Code**:
       - Write unit tests
       - Test edge cases
       - Verify error handling
       - Run tests to verify
    5. **Document**:
       - Add README if needed
       - Include usage examples
       - Document API/functions
    6. **Review & Refine**:
       - Run linter
       - Fix any issues
       - Optimize if needed
    
    Code Quality Standards:
    
    **Python:**
    - Follow PEP 8
    - Use type hints
    - Add docstrings (Google or NumPy style)
    - Handle exceptions appropriately
    - Write tests with pytest
    
    **JavaScript/TypeScript:**
    - Follow ESLint standards
    - Use TypeScript when possible
    - Add JSDoc comments
    - Handle errors with try/catch
    - Write tests with Jest
    
    **General:**
    - Single Responsibility Principle
    - DRY (Don't Repeat Yourself)
    - KISS (Keep It Simple)
    - Meaningful variable names
    - Keep functions small and focused
    - Add comments for complex logic
    
    File Organization:
    - src/ - Source code
    - tests/ - Test files
    - docs/ - Documentation
    - examples/ - Usage examples
    - README.md - Project overview
    
    Always:
    - Write tests for new code
    - Run tests before completing
    - Fix linting issues
    - Provide usage examples
    """
    
    # Create the agent
    agent = create_deep_agent(
        model="anthropic:claude-sonnet-4-20250514",
        tools=[run_python_code, run_tests, lint_code],
        backend=backend,
        system_prompt=system_prompt
    )
    
    return agent


def build_project(agent, description: str):
    """Build a code project based on description."""
    print(f"\n{'='*60}")
    print(f"Building: {description}")
    print(f"{'='*60}\n")
    
    result = agent.invoke({
        "messages": [{
            "role": "user",
            "content": f"""
            Build this project with complete implementation, tests, and documentation:
            
            {description}
            
            Requirements:
            - Write clean, well-documented code
            - Include comprehensive tests
            - Add README with usage examples
            - Follow best practices
            - Verify tests pass
            """
        }]
    })
    
    print("\n" + "="*60)
    print("Project Complete")
    print("="*60 + "\n")
    print(result["messages"][-1].content)
    
    return result


def review_code(agent, filepath: str):
    """Review and improve existing code."""
    print(f"\n{'='*60}")
    print(f"Reviewing: {filepath}")
    print(f"{'='*60}\n")
    
    result = agent.invoke({
        "messages": [{
            "role": "user",
            "content": f"""
            Review the code in {filepath} and:
            1. Identify issues and improvements
            2. Refactor if needed
            3. Add missing tests
            4. Improve documentation
            5. Run linter and fix issues
            """
        }]
    })
    
    print("\n" + "="*60)
    print("Review Complete")
    print("="*60 + "\n")
    print(result["messages"][-1].content)
    
    return result


def main():
    """Main execution."""
    # Create code assistant
    agent = create_code_assistant()
    
    # Example 1: Build a new project
    project_description = """
    Create a Python module for working with CSV files:
    
    Features:
    - Read CSV files with type inference
    - Filter rows by conditions
    - Transform columns
    - Export to different formats (JSON, Excel)
    - Handle missing data
    
    Include:
    - Complete implementation
    - Comprehensive tests
    - Usage examples
    - Error handling
    """
    
    result = build_project(agent, project_description)
    
    # Example 2: Review existing code
    # result = review_code(agent, "src/mymodule.py")


if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    
    main()

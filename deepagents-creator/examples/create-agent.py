#!/usr/bin/env python3
"""
Quick DeepAgent Creation Script

Quickly create and test a DeepAgent with common configurations.
"""

import os
import sys
from pathlib import Path


def create_basic_agent():
    """Create a basic DeepAgent."""
    code = '''#!/usr/bin/env python3
"""Basic DeepAgent"""

from deepagents import create_deep_agent
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create agent
agent = create_deep_agent(
    model="anthropic:claude-sonnet-4-20250514"
)

# Run agent
def main():
    message = input("Enter your message: ")
    
    result = agent.invoke({
        "messages": [{"role": "user", "content": message}]
    })
    
    print("\\n" + "="*60)
    print("Agent Response:")
    print("="*60)
    print(result["messages"][-1].content)

if __name__ == "__main__":
    main()
'''
    return code


def create_agent_with_tools():
    """Create agent with custom tools."""
    code = '''#!/usr/bin/env python3
"""DeepAgent with Custom Tools"""

from deepagents import create_deep_agent
from langchain_core.tools import tool
from dotenv import load_dotenv

load_dotenv()

# Define custom tools
@tool
def calculator(expression: str) -> str:
    """Calculate a mathematical expression."""
    try:
        result = eval(expression)
        return f"Result: {result}"
    except Exception as e:
        return f"Error: {e}"

@tool
def word_count(text: str) -> str:
    """Count words in text."""
    words = len(text.split())
    chars = len(text)
    return f"Words: {words}, Characters: {chars}"

# Create agent with tools
agent = create_deep_agent(
    model="anthropic:claude-sonnet-4-20250514",
    tools=[calculator, word_count]
)

def main():
    message = input("Enter your message: ")
    
    result = agent.invoke({
        "messages": [{"role": "user", "content": message}]
    })
    
    print("\\n" + "="*60)
    print("Agent Response:")
    print("="*60)
    print(result["messages"][-1].content)

if __name__ == "__main__":
    main()
'''
    return code


def create_specialized_agent(agent_type: str):
    """Create a specialized agent."""
    
    prompts = {
        "researcher": """
You are a research specialist.
Your goal is to find accurate, well-sourced information.
Always cite sources and verify facts from multiple sources.
""",
        "coder": """
You are a coding specialist.
Write clean, well-documented code with tests.
Follow best practices and include error handling.
Always add type hints and docstrings.
""",
        "writer": """
You are a technical writer.
Create clear, concise documentation.
Use proper structure with headings and examples.
Make complex topics accessible.
""",
        "analyst": """
You are a data analyst.
Analyze data systematically and generate insights.
Use statistical methods appropriately.
Visualize findings clearly.
"""
    }
    
    code = f'''#!/usr/bin/env python3
"""Specialized {agent_type.title()} Agent"""

from deepagents import create_deep_agent
from dotenv import load_dotenv

load_dotenv()

system_prompt = """{prompts.get(agent_type, "You are a helpful assistant.")}"""

agent = create_deep_agent(
    model="anthropic:claude-sonnet-4-20250514",
    system_prompt=system_prompt
)

def main():
    print(f"{{agent_type.title()}} Agent Ready!")
    message = input("Enter your task: ")
    
    result = agent.invoke({{
        "messages": [{{"role": "user", "content": message}}]
    }})
    
    print("\\n" + "="*60)
    print("Response:")
    print("="*60)
    print(result["messages"][-1].content)

if __name__ == "__main__":
    main()
'''
    return code


def create_env_template():
    """Create .env template."""
    return """# API Keys
ANTHROPIC_API_KEY=your_anthropic_key_here
OPENAI_API_KEY=your_openai_key_here
TAVILY_API_KEY=your_tavily_key_here
"""


def create_requirements():
    """Create requirements.txt."""
    return """langchain
langgraph
deepagents
langchain-anthropic
langchain-openai
python-dotenv
tavily-python
"""


def main():
    """Main script."""
    print("="*60)
    print("DeepAgent Quick Setup")
    print("="*60)
    print()
    
    # Get agent type
    print("Select agent type:")
    print("1. Basic agent")
    print("2. Agent with custom tools")
    print("3. Specialized researcher")
    print("4. Specialized coder")
    print("5. Specialized writer")
    print("6. Specialized analyst")
    print()
    
    choice = input("Enter choice (1-6): ").strip()
    
    # Get project name
    project_name = input("Enter project name: ").strip() or "my_agent"
    
    # Create project directory
    project_dir = Path(project_name)
    project_dir.mkdir(exist_ok=True)
    
    print(f"\nCreating project in: {project_dir}")
    
    # Generate agent code
    if choice == "1":
        agent_code = create_basic_agent()
        filename = "basic_agent.py"
    elif choice == "2":
        agent_code = create_agent_with_tools()
        filename = "agent_with_tools.py"
    elif choice == "3":
        agent_code = create_specialized_agent("researcher")
        filename = "researcher_agent.py"
    elif choice == "4":
        agent_code = create_specialized_agent("coder")
        filename = "coder_agent.py"
    elif choice == "5":
        agent_code = create_specialized_agent("writer")
        filename = "writer_agent.py"
    elif choice == "6":
        agent_code = create_specialized_agent("analyst")
        filename = "analyst_agent.py"
    else:
        print("Invalid choice")
        return
    
    # Write files
    (project_dir / filename).write_text(agent_code)
    (project_dir / ".env").write_text(create_env_template())
    (project_dir / "requirements.txt").write_text(create_requirements())
    
    # Make agent script executable
    os.chmod(project_dir / filename, 0o755)
    
    print(f"\n✓ Created {filename}")
    print("✓ Created .env template")
    print("✓ Created requirements.txt")
    
    print("\nNext steps:")
    print(f"1. cd {project_name}")
    print("2. Edit .env and add your API keys")
    print("3. pip install -r requirements.txt")
    print(f"4. python {filename}")
    
    print("\n" + "="*60)
    print("Setup Complete!")
    print("="*60)


if __name__ == "__main__":
    main()

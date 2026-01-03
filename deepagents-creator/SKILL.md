---
name: langchain-deepagents-builder
description: Builds autonomous LangChain DeepAgents with planning capabilities, filesystem access, and subagent delegation. Includes agent creation, tool integration, middleware configuration, and deployment patterns. Use when building complex, long-running autonomous agents.
---

# LangChain DeepAgents Builder

## Overview

This skill guides you through building DeepAgents in LangChain - autonomous agents capable of handling complex, multi-step tasks over long time horizons. DeepAgents come equipped with planning tools, filesystem backends, subagent delegation, and detailed system prompts.

## Core Concepts

### What Are DeepAgents?

DeepAgents are sophisticated agents that combine:
- **Planning capabilities** - Break down complex tasks into discrete steps
- **Filesystem access** - Offload large context to memory
- **Subagent delegation** - Spawn specialized agents for subtasks
- **Detailed prompts** - Comprehensive instructions for autonomous operation

### DeepAgents vs Traditional Agents

| Aspect | Traditional Agents | DeepAgents |
|--------|-------------------|------------|
| Planning | No built-in planning | Todo list planning tool |
| Memory | Limited to context window | Filesystem-backed memory |
| Delegation | Single agent only | Can spawn subagents |
| Task complexity | Simple, linear tasks | Complex, multi-step workflows |
| Time horizon | Short interactions | Long-running tasks |

### When to Use DeepAgents

**Use DeepAgents for:**
- Complex research tasks requiring multiple sources
- Code projects spanning multiple files
- Tasks requiring planning and state management
- Long-running autonomous workflows
- Tasks benefiting from specialized subagents

**Use Traditional Agents for:**
- Simple question answering
- Single-step tool usage
- Quick lookups or calculations
- Tasks fitting in one context window

## Installation

### Prerequisites

```bash
# Install LangChain and DeepAgents
pip install langchain langgraph deepagents

# Install optional dependencies
pip install langchain-anthropic  # For Claude models
pip install langchain-openai     # For OpenAI models
pip install tavily-python        # For web search
```

### Environment Setup

```bash
# Set API keys in .env file
cat > .env << EOF
ANTHROPIC_API_KEY=your_anthropic_key_here
OPENAI_API_KEY=your_openai_key_here
TAVILY_API_KEY=your_tavily_key_here
EOF

# Load environment variables
export $(cat .env | xargs)
```

## Creating Your First DeepAgent

### Minimal Example

```python
from deepagents import create_deep_agent

# Create a basic deep agent
agent = create_deep_agent(
    model="anthropic:claude-sonnet-4-20250514"
)

# Run the agent
result = agent.invoke({
    "messages": [
        {
            "role": "user",
            "content": "Research the latest developments in quantum computing and create a summary report."
        }
    ]
})

print(result["messages"][-1].content)
```

### With Custom Tools

```python
from langchain_core.tools import tool
from deepagents import create_deep_agent

@tool
def get_weather(city: str) -> str:
    """Get the current weather in a city."""
    # In production, call actual weather API
    return f"The weather in {city} is sunny and 72°F"

@tool
def calculate(expression: str) -> float:
    """Safely evaluate a mathematical expression."""
    try:
        # Use safe evaluation in production
        return eval(expression)
    except Exception as e:
        return f"Error: {e}"

# Create agent with custom tools
agent = create_deep_agent(
    model="anthropic:claude-sonnet-4-20250514",
    tools=[get_weather, calculate]
)

# Use the agent
result = agent.invoke({
    "messages": [{
        "role": "user",
        "content": "What's the weather in San Francisco and what's 25 * 4?"
    }]
})
```

## Agent Configuration

### Custom System Prompt

```python
from deepagents import create_deep_agent

# Define custom instructions
custom_prompt = """
You are a Python coding assistant specializing in data science.

When writing code:
1. Always include type hints
2. Add comprehensive docstrings
3. Follow PEP 8 style guidelines
4. Include error handling
5. Add unit tests when appropriate

Workflow:
1. Understand the requirements
2. Plan the implementation
3. Write clean, documented code
4. Test the solution
5. Provide usage examples
"""

agent = create_deep_agent(
    model="anthropic:claude-sonnet-4-20250514",
    system_prompt=custom_prompt
)
```

### Model Selection

```python
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI
from deepagents import create_deep_agent

# Using Anthropic Claude
claude_model = ChatAnthropic(
    model="claude-sonnet-4-20250514",
    temperature=0.7,
    max_tokens=4096
)

agent_claude = create_deep_agent(model=claude_model)

# Using OpenAI
openai_model = ChatOpenAI(
    model="gpt-4o",
    temperature=0.7
)

agent_openai = create_deep_agent(model=openai_model)
```

## Filesystem Backends

### State Backend (Ephemeral)

Default backend using LangGraph state:

```python
from deepagents import create_deep_agent
from deepagents.backends import StateBackend

# Ephemeral storage (resets between runs)
backend = StateBackend()

agent = create_deep_agent(
    model="anthropic:claude-sonnet-4-20250514",
    backend=backend
)
```

### Store Backend (Persistent)

Persist files using LangGraph store:

```python
from deepagents.backends import StoreBackend
from deepagents import create_deep_agent

# Persistent storage
backend = StoreBackend()

agent = create_deep_agent(
    model="anthropic:claude-sonnet-4-20250514",
    backend=backend
)
```

### Composite Backend (Hybrid) - Long-Term Memory

Combine multiple backends with routing for long-term memory across threads:

```python
from deepagents.backends import StateBackend, StoreBackend, CompositeBackend
from deepagents import create_deep_agent
from langgraph.store.memory import InMemoryStore

def make_backend(runtime):
    return CompositeBackend(
        default=StateBackend(runtime),  # Ephemeral storage
        routes={
            "/memories/": StoreBackend(runtime)  # Persistent storage
        }
    )

agent = create_deep_agent(
    model="anthropic:claude-sonnet-4-20250514",
    store=InMemoryStore(),  # Required for StoreBackend
    backend=make_backend
)

# Files in /memories/ persist across runs
# Files elsewhere are ephemeral
```

### How Composite Backend Works

When using `CompositeBackend`, deep agents maintain **two separate filesystems**:

#### 1. Short-term (transient) filesystem
- Stored in agent's state (via `StateBackend`)
- Persists only within a single thread
- Files lost when thread ends
- Accessed through standard paths: `/notes.txt`, `/workspace/draft.md`

#### 2. Long-term (persistent) filesystem
- Stored in LangGraph Store (via `StoreBackend`)
- Persists across all threads and conversations
- Survives agent restarts
- Accessed through `/memories/` prefix: `/memories/preferences.txt`

#### Path Routing

The `CompositeBackend` routes based on path prefixes:
- Files with paths starting with `/memories/` → Store (persistent)
- Files without this prefix → State (transient)
- All filesystem tools work with both

```python
# Transient file (lost after thread ends)
agent.invoke({
    "messages": [{"role": "user", "content": "Write draft to /draft.txt"}]
})

# Persistent file (survives across threads)
agent.invoke({
    "messages": [{
        "role": "user",
        "content": "Save final report to /memories/report.txt"
    }]
})
```

### Cross-Thread Persistence

Files in `/memories/` can be accessed from any thread:

```python
import uuid

# Thread 1: Write to long-term memory
config1 = {"configurable": {"thread_id": str(uuid.uuid4())}}
agent.invoke({
    "messages": [{
        "role": "user",
        "content": "Save my preferences to /memories/preferences.txt"
    }]
}, config=config1)

# Thread 2: Read from long-term memory (different conversation!)
config2 = {"configurable": {"thread_id": str(uuid.uuid4())}}
agent.invoke({
    "messages": [{
        "role": "user",
        "content": "What are my preferences?"
    }]
}, config=config2)
# Agent can read /memories/preferences.txt from the first thread
```

### Long-Term Memory Use Cases

#### User Preferences

```python
agent = create_deep_agent(
    store=InMemoryStore(),
    backend=lambda rt: CompositeBackend(
        default=StateBackend(rt),
        routes={"/memories/": StoreBackend(rt)}
    ),
    system_prompt="""When users tell you their preferences, save them to
    /memories/user_preferences.txt so you remember them in future conversations."""
)
```

#### Self-Improving Instructions

```python
agent = create_deep_agent(
    store=InMemoryStore(),
    backend=lambda rt: CompositeBackend(
        default=StateBackend(rt),
        routes={"/memories/": StoreBackend(rt)}
    ),
    system_prompt="""You have a file at /memories/instructions.txt with
    additional instructions and preferences.
    
    Read this file at the start of conversations.
    
    When users provide feedback like "please always do X",
    update /memories/instructions.txt using the edit_file tool."""
)
```

#### Knowledge Base

```python
# Conversation 1: Learn about project
agent.invoke({
    "messages": [{
        "role": "user",
        "content": "We're building a web app with React. Save project notes."
    }]
})

# Conversation 2: Use that knowledge
agent.invoke({
    "messages": [{
        "role": "user",
        "content": "What framework are we using?"
    }]
})
# Agent reads /memories/project_notes.txt from previous conversation
```

#### Research Projects

```python
research_agent = create_deep_agent(
    store=InMemoryStore(),
    backend=lambda rt: CompositeBackend(
        default=StateBackend(rt),
        routes={"/memories/": StoreBackend(rt)}
    ),
    system_prompt="""You are a research assistant.
    
    Save research progress to /memories/research/:
    - /memories/research/sources.txt - List of sources found
    - /memories/research/notes.txt - Key findings and notes
    - /memories/research/report.md - Final report draft
    
    This allows research to continue across multiple sessions."""
)
```

### Store Implementations

#### InMemoryStore (Development)

Good for testing, but data is lost on restart:

```python
from langgraph.store.memory import InMemoryStore

store = InMemoryStore()
agent = create_deep_agent(
    store=store,
    backend=lambda rt: CompositeBackend(
        default=StateBackend(rt),
        routes={"/memories/": StoreBackend(rt)}
    )
)
```

#### PostgresStore (Production)

For production, use persistent store:

```python
from langgraph.store.postgres import PostgresStore
import os

store = PostgresStore(
    connection_string=os.environ["DATABASE_URL"]
)

agent = create_deep_agent(
    store=store,
    backend=lambda rt: CompositeBackend(
        default=StateBackend(rt),
        routes={"/memories/": StoreBackend(rt)}
    )
)
```

### Long-Term Memory Best Practices

#### 1. Use Descriptive Paths

Organize persistent files with clear paths:

```
/memories/user_preferences.txt
/memories/research/topic_a/sources.txt
/memories/research/topic_a/notes.txt
/memories/project/requirements.md
```

#### 2. Document Memory Structure

Tell the agent what's stored where:

```python
system_prompt = """Your persistent memory structure:
- /memories/preferences.txt: User preferences and settings
- /memories/context/: Long-term context about the user
- /memories/knowledge/: Facts and information learned over time

Read from /memories/ at conversation start to recall past information."""
```

#### 3. Prune Old Data

Implement periodic cleanup of outdated persistent files.

#### 4. Choose Right Storage

- **Development**: Use `InMemoryStore` for quick iteration
- **Production**: Use `PostgresStore` or other persistent stores
- **Multi-tenant**: Use assistant_id-based namespacing

### Local Filesystem Backend

```python
from deepagents.backends import LocalBackend
from deepagents import create_deep_agent
import os

# Use local filesystem
backend = LocalBackend(
    base_path=os.path.expanduser("~/.deepagents/workspace")
)

agent = create_deep_agent(
    model="anthropic:claude-sonnet-4-20250514",
    backend=backend
)
```

## Tools and Middleware

### Understanding Middleware

Deep agents are built with a modular middleware architecture. When you create a deep agent with `create_deep_agent`, we automatically attach three key middleware:

1. **TodoListMiddleware** - Planning tool
2. **FilesystemMiddleware** - File operations
3. **SubAgentMiddleware** - Subagent delegation

Middleware is composable—you can add as many or as few as needed.

### TodoList Middleware

Planning is integral to solving complex problems. `TodoListMiddleware` provides a `write_todos` tool for keeping track of multi-part tasks.

The agent is prompted to use this tool to:
- Plan before executing complex tasks
- Track what still needs to be done
- Adapt plans as new information emerges

```python
from langchain.agents import create_agent
from langchain.agents.middleware import TodoListMiddleware

# TodoListMiddleware is included by default in create_deep_agent
# You can customize it if building a custom agent
agent = create_agent(
    model="anthropic:claude-sonnet-4-20250514",
    middleware=[
        TodoListMiddleware(
            system_prompt="Use write_todos to..."  # Optional custom addition
        ),
    ],
)
```

### Filesystem Middleware

Context engineering is a main challenge with agents. `FilesystemMiddleware` provides four tools for interacting with memory:

- **ls**: List files in the filesystem
- **read_file**: Read entire file or specific lines
- **write_file**: Write new file
- **edit_file**: Edit existing file

Additional tools when using sandbox backend:
- **glob**: Search for files by pattern
- **grep**: Search file contents

```python
from langchain.agents import create_agent
from deepagents.middleware.filesystem import FilesystemMiddleware

# FilesystemMiddleware is included by default in create_deep_agent
# Customize if building a custom agent
agent = create_agent(
    model="anthropic:claude-sonnet-4-20250514",
    middleware=[
        FilesystemMiddleware(
            backend=None,  # Optional: custom backend
            system_prompt="Write to filesystem when...",  # Optional
            custom_tool_descriptions={
                "ls": "Use ls tool when...",
                "read_file": "Use read_file to..."
            }  # Optional: Custom descriptions
        ),
    ],
)
```

#### Short-term vs Long-term Filesystem

By default, tools write to local "filesystem" in graph state. To enable persistent storage across threads, configure a `CompositeBackend`:

```python
from langchain.agents import create_agent
from deepagents.middleware import FilesystemMiddleware
from deepagents.backends import CompositeBackend, StateBackend, StoreBackend
from langgraph.store.memory import InMemoryStore

store = InMemoryStore()

agent = create_agent(
    model="anthropic:claude-sonnet-4-20250514",
    store=store,
    middleware=[
        FilesystemMiddleware(
            backend=lambda rt: CompositeBackend(
                default=StateBackend(rt),
                routes={"/memories/": StoreBackend(rt)}
            ),
        ),
    ],
)
```

Files prefixed with `/memories/` persist across threads; others remain ephemeral.

### SubAgent Middleware

Handing off tasks to subagents isolates context, keeping the main agent's context clean.

The subagents middleware provides a `task` tool for delegating to subagents.

```python
from langchain_core.tools import tool
from langchain.agents import create_agent
from deepagents.middleware.subagents import SubAgentMiddleware

@tool
def get_weather(city: str) -> str:
    """Get the weather in a city."""
    return f"The weather in {city} is sunny."

agent = create_agent(
    model="anthropic:claude-sonnet-4-20250514",
    middleware=[
        SubAgentMiddleware(
            default_model="anthropic:claude-sonnet-4-20250514",
            default_tools=[],
            subagents=[
                {
                    "name": "weather",
                    "description": "This subagent can get weather in cities.",
                    "system_prompt": "Use get_weather tool to get weather.",
                    "tools": [get_weather],
                    "model": "openai:gpt-4o",  # Optional override
                    "middleware": [],  # Optional additional middleware
                }
            ],
        )
    ],
)
```

A subagent is defined with:
- **name**: Unique identifier
- **description**: What it does (for discovery)
- **system_prompt**: Instructions
- **tools**: Available tools
- **model** (optional): Override model
- **middleware** (optional): Additional middleware

#### Using Pre-built Graphs as Subagents

For complex use cases, provide your own LangGraph graph:

```python
from langchain.agents import create_agent
from deepagents.middleware.subagents import SubAgentMiddleware
from deepagents import CompiledSubAgent
from langgraph.graph import StateGraph

# Create custom LangGraph graph
def create_weather_graph():
    workflow = StateGraph(...)
    # Build your custom graph
    return workflow.compile()

weather_graph = create_weather_graph()

# Wrap in CompiledSubAgent
weather_subagent = CompiledSubAgent(
    name="weather",
    description="This subagent can get weather in cities.",
    runnable=weather_graph
)

agent = create_agent(
    model="anthropic:claude-sonnet-4-20250514",
    middleware=[
        SubAgentMiddleware(
            default_model="anthropic:claude-sonnet-4-20250514",
            default_tools=[],
            subagents=[weather_subagent],
        )
    ],
)
```

### Built-in Tools

DeepAgents come with several built-in tools:

1. **write_todos** - Planning and task breakdown
2. **ls** - List directory contents
3. **read_file** - Read file contents
4. **write_file** - Create or overwrite files
5. **edit_file** - Modify existing files
6. **glob** - Search for files by pattern
7. **grep** - Search file contents

### Adding Custom Tools

```python
from langchain_core.tools import tool
from deepagents import create_deep_agent
import requests

@tool
def search_web(query: str) -> str:
    """Search the web using Tavily API."""
    from tavily import TavilyClient
    client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
    results = client.search(query)
    
    # Format results
    formatted = []
    for result in results.get("results", [])[:5]:
        formatted.append(f"**{result['title']}**\n{result['content']}\nSource: {result['url']}")
    
    return "\n\n".join(formatted)

@tool
def fetch_url(url: str) -> str:
    """Fetch content from a URL."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except Exception as e:
        return f"Error fetching URL: {e}"

# Create agent with custom tools
agent = create_deep_agent(
    model="anthropic:claude-sonnet-4-20250514",
    tools=[search_web, fetch_url]
)
```

### Custom Middleware

```python
from deepagents.middleware import Middleware
from deepagents import create_deep_agent
from typing import Any

class LoggingMiddleware(Middleware):
    """Log all agent actions."""
    
    def before_agent(self, state, runtime):
        """Run before agent execution."""
        print(f"[AGENT] Starting with {len(state['messages'])} messages")
        return None
    
    def after_agent(self, state, runtime):
        """Run after agent execution."""
        last_message = state['messages'][-1]
        print(f"[AGENT] Generated: {last_message.content[:100]}...")
        return None

# Use custom middleware
agent = create_deep_agent(
    model="anthropic:claude-sonnet-4-20250514",
    middleware=[LoggingMiddleware()]
)
```

## Subagents

Subagents solve the **context bloat problem**. When agents use tools with large outputs, the context window fills up quickly. Subagents isolate detailed work—the main agent receives only the final result, not dozens of intermediate tool calls.

### When to Use Subagents

**Use subagents for:**
- ✅ Multi-step tasks that would clutter main agent's context
- ✅ Specialized domains needing custom instructions or tools
- ✅ Tasks requiring different model capabilities
- ✅ Keeping main agent focused on high-level coordination

**Don't use subagents for:**
- ❌ Simple, single-step tasks
- ❌ When you need to maintain intermediate context
- ❌ When overhead outweighs benefits

### Subagent Configuration

There are two types of subagents: dictionary-based and compiled.

#### Dictionary-Based Subagents

Define subagents as dictionaries with these fields:

**Required:**
- `name` (str): Unique identifier for the subagent
- `description` (str): What this subagent does (be specific and action-oriented)
- `system_prompt` (str): Instructions for the subagent
- `tools` (List[Callable]): Tools the subagent can use

**Optional:**
- `model` (str | BaseChatModel): Override main agent's model (e.g., "openai:gpt-4o")
- `middleware` (List[Middleware]): Additional middleware
- `interrupt_on` (Dict[str, bool]): Configure human-in-the-loop

```python
from deepagents import create_deep_agent
from langchain_core.tools import tool

@tool
def internet_search(query: str, max_results: int = 5) -> str:
    """Search the web for information."""
    # Implementation here
    return "Search results..."

# Define specialized subagents
research_subagent = {
    "name": "research-agent",
    "description": "Conducts in-depth research using web search and synthesizes findings",
    "system_prompt": """You are a thorough researcher. Your job is to:

    1. Break down the research question into searchable queries
    2. Use internet_search to find relevant information
    3. Synthesize findings into a comprehensive but concise summary
    4. Cite sources when making claims

    Output format:
    - Summary (2-3 paragraphs)
    - Key findings (bullet points)
    - Sources (with URLs)

    Keep your response under 500 words to maintain clean context.""",
    "tools": [internet_search],
    "model": "openai:gpt-4o",  # Optional: different model
}

coding_subagent = {
    "name": "code-specialist",
    "description": "Writes production-ready code with tests and documentation",
    "system_prompt": """You are a coding specialist.
    
    Write clean, well-documented code with:
    - Type hints
    - Comprehensive docstrings
    - Error handling
    - Unit tests
    
    Follow best practices and design patterns.""",
    "tools": [run_tests, lint_code],
}

# Create main agent with subagents
agent = create_deep_agent(
    model="anthropic:claude-sonnet-4-20250514",
    subagents=[research_subagent, coding_subagent],
    system_prompt="""You are a project coordinator.
    
    IMPORTANT: For complex tasks, delegate to your subagents using the task() tool.
    This keeps your context clean and improves results.
    
    - Use research-agent for information gathering
    - Use code-specialist for coding tasks"""
)
```

#### Compiled Subagents

For complex workflows, use pre-built LangGraph graphs:

```python
from deepagents import create_deep_agent, CompiledSubAgent
from langchain.agents import create_agent

# Create a custom agent graph
custom_graph = create_agent(
    model="anthropic:claude-sonnet-4-20250514",
    tools=[specialized_tool],
    prompt="You are a specialized agent for data analysis..."
)

# Wrap in CompiledSubAgent
custom_subagent = CompiledSubAgent(
    name="data-analyzer",
    description="Specialized agent for complex data analysis tasks",
    runnable=custom_graph  # Must be compiled
)

# Use in main agent
agent = create_deep_agent(
    model="anthropic:claude-sonnet-4-20250514",
    subagents=[custom_subagent]
)
```

### The General-Purpose Subagent

In addition to user-defined subagents, all deep agents have access to a `general-purpose` subagent that:
- Has the same system prompt as the main agent
- Has access to all the same tools
- Uses the same model (unless overridden)

**When to use it:**
The general-purpose subagent is ideal for context isolation without specialized behavior. The main agent can delegate complex multi-step tasks and get concise results without context bloat.

```python
# Main agent can delegate like this:
# "Use task(name='general-purpose', task='Research quantum computing trends')"
# The subagent does all the work and returns only a summary
```

### Subagent Best Practices

#### 1. Write Clear Descriptions

The main agent uses descriptions to decide which subagent to call:

✅ **Good:** "Analyzes financial data and generates investment insights with confidence scores"

❌ **Bad:** "Does finance stuff"

#### 2. Keep System Prompts Detailed

Include specific guidance on tool usage and output format:

```python
research_subagent = {
    "name": "research-agent",
    "description": "Conducts in-depth research using web search",
    "system_prompt": """You are a thorough researcher.
    
    Process:
    1. Break down research question into queries
    2. Use internet_search for each query
    3. Synthesize findings
    4. Cite all sources
    
    IMPORTANT: Return only essential summary.
    Do NOT include raw data or detailed tool outputs.
    Response under 500 words.""",
}
```

#### 3. Minimize Tool Sets

Only give subagents tools they need:

```python
# ✅ Good: Focused tool set
email_agent = {
    "name": "email-sender",
    "tools": [send_email, validate_email],  # Only email-related
}

# ❌ Bad: Too many tools
email_agent = {
    "name": "email-sender",
    "tools": [send_email, web_search, database_query, file_upload],  # Unfocused
}
```

#### 4. Choose Models by Task

Different models excel at different tasks:

```python
subagents = [
    {
        "name": "contract-reviewer",
        "model": "claude-sonnet-4-5-20250929",  # Large context for documents
        "tools": [read_document, analyze_contract],
    },
    {
        "name": "financial-analyst",
        "model": "openai:gpt-4o",  # Better for numerical analysis
        "tools": [get_stock_price, analyze_fundamentals],
    },
]
```

#### 5. Return Concise Results

Instruct subagents to return summaries, not raw data:

```python
system_prompt = """Analyze data and return:
1. Key insights (3-5 bullet points)
2. Overall confidence score
3. Recommended next actions

Do NOT include:
- Raw data
- Intermediate calculations
- Detailed tool outputs

Keep response under 300 words."""
```

### Multiple Specialized Subagents Pattern

```python
from deepagents import create_deep_agent

subagents = [
    {
        "name": "data-collector",
        "description": "Gathers raw data from various sources",
        "system_prompt": "Collect comprehensive data on the topic",
        "tools": [web_search, api_call, database_query],
    },
    {
        "name": "data-analyzer",
        "description": "Analyzes collected data for insights",
        "system_prompt": "Analyze data and extract key insights",
        "tools": [statistical_analysis],
    },
    {
        "name": "report-writer",
        "description": "Writes polished reports from analysis",
        "system_prompt": "Create professional reports from insights",
        "tools": [format_document],
    },
]

agent = create_deep_agent(
    model="anthropic:claude-sonnet-4-20250514",
    system_prompt="""You coordinate data analysis and reporting.
    
    Use subagents for specialized tasks:
    1. data-collector: Gather information
    2. data-analyzer: Process and analyze
    3. report-writer: Create final report
    
    IMPORTANT: Delegate to keep your context clean.""",
    subagents=subagents
)
```

### Troubleshooting Subagents

#### Subagent Not Being Called

**Problem:** Main agent tries to do work itself instead of delegating.

**Solutions:**

1. Make descriptions more specific:
```python
# ✅ Good
{"description": "Conducts in-depth research on specific topics using web search. Use when you need detailed information requiring multiple searches."}

# ❌ Bad
{"description": "helps with stuff"}
```

2. Instruct main agent to delegate:
```python
system_prompt = """...your instructions...

IMPORTANT: For complex tasks, delegate to your subagents using the task() tool.
This keeps your context clean and improves results."""
```

#### Context Still Getting Bloated

**Solutions:**

1. Instruct subagent to return concise results
2. Use filesystem for large data:
```python
system_prompt = """When you gather large data:
1. Save raw data to /data/raw_results.txt
2. Process and analyze the data
3. Return only the analysis summary"""
```

#### Wrong Subagent Selected

**Solution:** Differentiate subagents clearly:

```python
subagents = [
    {
        "name": "quick-researcher",
        "description": "For simple, quick research questions needing 1-2 searches. Use for basic facts or definitions.",
    },
    {
        "name": "deep-researcher",
        "description": "For complex, in-depth research requiring multiple searches, synthesis, and analysis. Use for comprehensive reports.",
    }
]
```

## Human-in-the-Loop

Some tool operations require human approval before execution. DeepAgents support human-in-the-loop (HITL) workflows through LangGraph's interrupt capabilities.

### Basic Configuration

Configure which tools require approval using the `interrupt_on` parameter:

```python
from langchain_core.tools import tool
from deepagents import create_deep_agent
from langgraph.checkpoint.memory import MemorySaver

@tool
def delete_file(path: str) -> str:
    """Delete a file from the filesystem."""
    import os
    os.remove(path)
    return f"Deleted {path}"

@tool
def read_file(path: str) -> str:
    """Read a file from the filesystem."""
    with open(path) as f:
        return f.read()

@tool
def send_email(to: str, subject: str, body: str) -> str:
    """Send an email."""
    # Email sending logic
    return f"Sent email to {to}"

# Checkpointer is REQUIRED for HITL
checkpointer = MemorySaver()

agent = create_deep_agent(
    model="anthropic:claude-sonnet-4-20250514",
    tools=[delete_file, read_file, send_email],
    interrupt_on={
        "delete_file": True,  # Default: approve, edit, reject
        "read_file": False,   # No interrupts needed
        "send_email": {"allowed_decisions": ["approve", "reject"]},  # No editing
    },
    checkpointer=checkpointer  # Required!
)
```

### Decision Types

The `allowed_decisions` list controls what actions a human can take:

- **`"approve"`**: Execute the tool with original arguments
- **`"edit"`**: Modify tool arguments before execution
- **`"reject"`**: Skip executing this tool call entirely

Customize by tool based on risk level:

```python
interrupt_on = {
    # High risk: full control
    "delete_file": {"allowed_decisions": ["approve", "edit", "reject"]},
    
    # Moderate risk: no editing
    "write_file": {"allowed_decisions": ["approve", "reject"]},
    
    # Must approve (no rejection)
    "critical_operation": {"allowed_decisions": ["approve"]},
    
    # Low risk: no interrupts
    "read_file": False,
}
```

### Handling Interrupts

When an interrupt is triggered, check for it and resume with decisions:

```python
import uuid
from langgraph.types import Command

# Create config with thread_id for state persistence
config = {"configurable": {"thread_id": str(uuid.uuid4())}}

# Invoke the agent
result = agent.invoke({
    "messages": [{"role": "user", "content": "Delete the file temp.txt"}]
}, config=config)

# Check if execution was interrupted
if result.get("__interrupt__"):
    # Extract interrupt information
    interrupts = result["__interrupt__"][0].value
    action_requests = interrupts["action_requests"]
    review_configs = interrupts["review_configs"]
    
    # Create lookup map
    config_map = {cfg["action_name"]: cfg for cfg in review_configs}
    
    # Display pending actions to user
    for action in action_requests:
        review_config = config_map[action["name"]]
        print(f"Tool: {action['name']}")
        print(f"Arguments: {action['args']}")
        print(f"Allowed decisions: {review_config['allowed_decisions']}")
    
    # Get user decisions (one per action_request, in order)
    decisions = [
        {"type": "approve"}  # User approved the deletion
    ]
    
    # Resume execution with decisions
    result = agent.invoke(
        Command(resume={"decisions": decisions}),
        config=config  # Must use same config!
    )

# Process final result
print(result["messages"][-1].content)
```

### Multiple Tool Calls

When multiple tools need approval, all interrupts are batched together:

```python
config = {"configurable": {"thread_id": str(uuid.uuid4())}}

result = agent.invoke({
    "messages": [{
        "role": "user",
        "content": "Delete temp.txt and send email to admin@example.com"
    }]
}, config=config)

if result.get("__interrupt__"):
    interrupts = result["__interrupt__"][0].value
    action_requests = interrupts["action_requests"]
    
    # Two tools need approval
    assert len(action_requests) == 2
    
    # Provide decisions in same order as action_requests
    decisions = [
        {"type": "approve"},  # First tool: delete_file
        {"type": "reject"}    # Second tool: send_email
    ]
    
    result = agent.invoke(
        Command(resume={"decisions": decisions}),
        config=config
    )
```

### Editing Tool Arguments

Modify arguments before execution when "edit" is allowed:

```python
if result.get("__interrupt__"):
    interrupts = result["__interrupt__"][0].value
    action_request = interrupts["action_requests"][0]
    
    # Original args from agent
    print(action_request["args"])  # {"to": "everyone@company.com", ...}
    
    # User decides to edit recipient
    decisions = [{
        "type": "edit",
        "edited_action": {
            "name": action_request["name"],  # Must include tool name
            "args": {
                "to": "team@company.com",
                "subject": "...",
                "body": "..."
            }
        }
    }]
    
    result = agent.invoke(
        Command(resume={"decisions": decisions}),
        config=config
    )
```

### Subagent Interrupts

Each subagent can have its own `interrupt_on` configuration:

```python
agent = create_deep_agent(
    model="anthropic:claude-sonnet-4-20250514",
    tools=[delete_file, read_file],
    interrupt_on={
        "delete_file": True,
        "read_file": False,
    },
    subagents=[{
        "name": "file-manager",
        "description": "Manages file operations",
        "system_prompt": "You are a file management assistant.",
        "tools": [delete_file, read_file],
        "interrupt_on": {
            # Override: require approval for reads in this subagent
            "delete_file": True,
            "read_file": True,  # Different from main agent!
        }
    }],
    checkpointer=checkpointer
)
```

### HITL Best Practices

#### 1. Always Use a Checkpointer

Required for persisting agent state between interrupt and resume:

```python
from langgraph.checkpoint.memory import MemorySaver

checkpointer = MemorySaver()
agent = create_deep_agent(
    tools=[...],
    interrupt_on={...},
    checkpointer=checkpointer  # Required!
)
```

#### 2. Use Same Thread ID

When resuming, use the same config with same thread_id:

```python
# First call
config = {"configurable": {"thread_id": "my-thread"}}
result = agent.invoke(input, config=config)

# Resume (use same config)
result = agent.invoke(Command(resume={...}), config=config)
```

#### 3. Match Decision Order to Actions

Decisions list must match order of action_requests:

```python
if result.get("__interrupt__"):
    interrupts = result["__interrupt__"][0].value
    action_requests = interrupts["action_requests"]
    
    # Create one decision per action, in order
    decisions = []
    for action in action_requests:
        decision = get_user_decision(action)  # Your logic
        decisions.append(decision)
    
    result = agent.invoke(
        Command(resume={"decisions": decisions}),
        config=config
    )
```

#### 4. Tailor by Risk Level

Configure tools based on their risk:

```python
interrupt_on = {
    # High risk: full control
    "delete_file": {"allowed_decisions": ["approve", "edit", "reject"]},
    "send_email": {"allowed_decisions": ["approve", "edit", "reject"]},
    
    # Medium risk: no editing
    "write_file": {"allowed_decisions": ["approve", "reject"]},
    
    # Low risk: no interrupts
    "read_file": False,
    "list_files": False,
}
```

## Advanced Patterns

### Memory-First Protocol

```python
from deepagents import create_deep_agent
from deepagents.backends import CompositeBackend, StateBackend, StoreBackend

# Set up persistent memory
backend = CompositeBackend(
    default=StateBackend(),
    routes={
        "/memories/": StoreBackend()
    }
)

agent = create_deep_agent(
    model="anthropic:claude-sonnet-4-20250514",
    backend=backend,
    system_prompt="""
    Memory-First Protocol:
    
    1. Before starting any task, check /memories/ for relevant knowledge
    2. During research, save important findings to /memories/
    3. When uncertain, search memory files before asking
    4. Continuously update memory with new learnings
    
    Memory organization:
    - /memories/api-conventions.md - API design patterns
    - /memories/coding-standards.md - Code style guides
    - /memories/project-context.md - Project-specific info
    - /memories/decisions.md - Design decisions and rationale
    """
)

# Agent will now check and update memory across conversations
```

### Task Decomposition

```python
from deepagents import create_deep_agent

agent = create_deep_agent(
    model="anthropic:claude-sonnet-4-20250514",
    system_prompt="""
    Task Decomposition Workflow:
    
    1. Use write_todos to break down complex tasks
    2. For each todo:
       - Analyze requirements
       - Identify dependencies
       - Estimate complexity
       - Execute or delegate
    3. Update todos as you progress
    4. Mark completed tasks
    5. Adapt plan based on new information
    
    Example todo structure:
    - [ ] Research API requirements
    - [ ] Design data models
    - [ ] Implement core logic
    - [ ] Write tests
    - [ ] Create documentation
    """
)

# Agent will automatically use write_todos for planning
result = agent.invoke({
    "messages": [{
        "role": "user",
        "content": "Build a REST API for user management with authentication"
    }]
})
```

### Streaming Responses

```python
from deepagents import create_deep_agent

agent = create_deep_agent(
    model="anthropic:claude-sonnet-4-20250514"
)

# Stream the agent's response
for chunk in agent.stream({
    "messages": [{
        "role": "user",
        "content": "Write a Python script to analyze CSV data"
    }]
}):
    # Process streaming chunks
    if "messages" in chunk:
        for message in chunk["messages"]:
            print(message.content, end="", flush=True)
```

## Production Deployment

### Configuration Management

```python
from pydantic import BaseModel
from deepagents import create_deep_agent
import os

class AgentConfig(BaseModel):
    """Agent configuration."""
    model: str = "anthropic:claude-sonnet-4-20250514"
    temperature: float = 0.7
    max_tokens: int = 4096
    timeout: int = 300
    
    class Config:
        env_prefix = "AGENT_"

# Load from environment
config = AgentConfig()

agent = create_deep_agent(
    model=config.model,
    # Additional configuration...
)
```

### Error Handling

```python
from deepagents import create_deep_agent
from langchain_core.messages import HumanMessage
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_agent_safely(agent, message: str, max_retries: int = 3):
    """Run agent with retry logic and error handling."""
    for attempt in range(max_retries):
        try:
            result = agent.invoke({
                "messages": [{"role": "user", "content": message}]
            })
            return result
        
        except Exception as e:
            logger.error(f"Attempt {attempt + 1} failed: {e}")
            
            if attempt == max_retries - 1:
                logger.error("Max retries reached")
                raise
            
            # Exponential backoff
            import time
            time.sleep(2 ** attempt)
    
    return None

# Usage
agent = create_deep_agent(model="anthropic:claude-sonnet-4-20250514")
result = run_agent_safely(agent, "Analyze this data...")
```

### Monitoring and Logging

```python
from deepagents import create_deep_agent
from deepagents.middleware import Middleware
import time
import json

class MonitoringMiddleware(Middleware):
    """Monitor agent performance and actions."""
    
    def __init__(self):
        self.metrics = []
    
    def before_agent(self, state, runtime):
        """Track start time."""
        state["_start_time"] = time.time()
        return None
    
    def after_agent(self, state, runtime):
        """Log metrics."""
        duration = time.time() - state.get("_start_time", 0)
        
        metric = {
            "timestamp": time.time(),
            "duration": duration,
            "messages": len(state["messages"]),
            "model": runtime.get("model", "unknown")
        }
        
        self.metrics.append(metric)
        
        # Log to file or monitoring service
        with open("agent_metrics.jsonl", "a") as f:
            f.write(json.dumps(metric) + "\n")
        
        return None

monitoring = MonitoringMiddleware()

agent = create_deep_agent(
    model="anthropic:claude-sonnet-4-20250514",
    middleware=[monitoring]
)
```

## Testing DeepAgents

### Unit Testing

```python
import pytest
from deepagents import create_deep_agent
from langchain_core.tools import tool

@tool
def mock_tool(input: str) -> str:
    """Mock tool for testing."""
    return f"Processed: {input}"

def test_agent_creation():
    """Test basic agent creation."""
    agent = create_deep_agent(
        model="anthropic:claude-sonnet-4-20250514"
    )
    assert agent is not None

def test_agent_with_tools():
    """Test agent with custom tools."""
    agent = create_deep_agent(
        model="anthropic:claude-sonnet-4-20250514",
        tools=[mock_tool]
    )
    
    result = agent.invoke({
        "messages": [{"role": "user", "content": "Use the mock tool"}]
    })
    
    assert "messages" in result
    assert len(result["messages"]) > 0

@pytest.fixture
def test_agent():
    """Fixture for test agent."""
    return create_deep_agent(
        model="anthropic:claude-sonnet-4-20250514",
        system_prompt="You are a test agent. Keep responses brief."
    )

def test_agent_response(test_agent):
    """Test agent generates valid response."""
    result = test_agent.invoke({
        "messages": [{"role": "user", "content": "Hello"}]
    })
    
    assert result is not None
    assert "messages" in result
    assert result["messages"][-1].content
```

### Integration Testing

```python
import pytest
from deepagents import create_deep_agent
from deepagents.backends import StateBackend

def test_filesystem_operations():
    """Test agent filesystem operations."""
    agent = create_deep_agent(
        model="anthropic:claude-sonnet-4-20250514",
        backend=StateBackend()
    )
    
    # Ask agent to create and read a file
    result = agent.invoke({
        "messages": [{
            "role": "user",
            "content": "Create a file called test.txt with 'Hello World', then read it back"
        }]
    })
    
    # Verify file operations occurred
    assert "test.txt" in result["messages"][-1].content
    assert "Hello World" in result["messages"][-1].content

def test_planning_capability():
    """Test agent uses planning tools."""
    agent = create_deep_agent(
        model="anthropic:claude-sonnet-4-20250514"
    )
    
    result = agent.invoke({
        "messages": [{
            "role": "user",
            "content": "Plan out how to build a web scraper for news articles"
        }]
    })
    
    response = result["messages"][-1].content.lower()
    
    # Should mention planning/steps
    assert any(word in response for word in ["plan", "step", "todo", "first"])
```

## Example Applications

### Research Agent

See `examples/research-agent.py` for a complete research agent that:
- Searches multiple sources
- Synthesizes information
- Creates structured reports
- Saves findings to memory

### Code Assistant

See `examples/code-assistant.py` for a coding agent that:
- Analyzes requirements
- Generates code with tests
- Refactors existing code
- Provides documentation

### Data Analysis Agent

See `examples/data-analysis-agent.py` for an agent that:
- Loads and explores datasets
- Performs statistical analysis
- Creates visualizations
- Generates insights report

## Best Practices

### Agent Design

1. **Clear System Prompts**: Define agent's role, capabilities, and constraints
2. **Appropriate Tools**: Provide only necessary tools
3. **Memory Organization**: Structure persistent memory logically
4. **Error Handling**: Implement robust error handling and retries
5. **Human Oversight**: Use HITL for critical operations

### Performance Optimization

1. **Model Selection**: Use faster models for simple tasks
2. **Context Management**: Use filesystem to offload large context
3. **Streaming**: Stream responses for better UX
4. **Caching**: Cache tool results when appropriate
5. **Batching**: Batch similar operations

### Security Considerations

1. **Input Validation**: Validate all user inputs
2. **Tool Permissions**: Restrict sensitive operations
3. **API Keys**: Never hardcode credentials
4. **Sandboxing**: Isolate agent execution environment
5. **Audit Logging**: Log all agent actions

## Troubleshooting

### Agent Not Responding

**Check:**
- API keys are set correctly
- Model name is valid
- Network connectivity
- Rate limits not exceeded

**Solution:**
```python
# Add timeout and retry logic
from deepagents import create_deep_agent

agent = create_deep_agent(
    model="anthropic:claude-sonnet-4-20250514",
    timeout=60  # Add timeout
)
```

### Tools Not Working

**Check:**
- Tool definitions are correct
- Tool functions don't error
- Tools are passed to agent

**Solution:**
```python
# Test tools independently
from langchain_core.tools import tool

@tool
def test_tool(input: str) -> str:
    """Test tool."""
    print(f"Tool called with: {input}")
    return f"Result: {input}"

# Verify tool works
result = test_tool.invoke({"input": "test"})
print(result)
```

### Memory Issues

**Check:**
- Backend is configured correctly
- File paths are valid
- Permissions are correct

**Solution:**
```python
# Use StateBackend for debugging
from deepagents.backends import StateBackend

backend = StateBackend()  # Simpler for debugging
```

## Advanced Topics

For advanced patterns including:
- Multi-agent systems
- Custom backend implementations
- LangGraph integration
- Production deployment strategies

See `resources/advanced-patterns.md`

## Resources

**Official Documentation:**
- [DeepAgents Overview](https://docs.langchain.com/oss/python/deepagents/overview)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [LangChain Documentation](https://python.langchain.com/)

**Example Code:**
- `examples/research-agent.py` - Complete research agent
- `examples/code-assistant.py` - Coding assistant
- `examples/data-analysis-agent.py` - Data analysis agent
- `scripts/create-agent.py` - Quick agent creation script

**Related Skills:**
- `deepagents-skill-creator` - For creating agent skills
- `python-testing` - For testing agents
- `web-development` - For building agent interfaces
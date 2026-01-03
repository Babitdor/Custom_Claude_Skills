#!/usr/bin/env python3
"""
Research Agent Example

A DeepAgent specialized in conducting research on any topic,
synthesizing information from multiple sources, and creating
structured reports.
"""

import os
from deepagents import create_deep_agent
from deepagents.backends import CompositeBackend, StateBackend, StoreBackend
from langchain_core.tools import tool


# Custom research tools
@tool
def search_web(query: str, max_results: int = 5) -> str:
    """Search the web for information on a topic."""
    try:
        from tavily import TavilyClient
        
        client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
        results = client.search(query, max_results=max_results)
        
        formatted = []
        for result in results.get("results", []):
            formatted.append(
                f"**{result['title']}**\n"
                f"{result['content']}\n"
                f"Source: {result['url']}\n"
                f"Relevance: {result.get('score', 'N/A')}"
            )
        
        return "\n\n---\n\n".join(formatted)
    
    except Exception as e:
        return f"Error searching web: {e}"


@tool
def fetch_webpage(url: str) -> str:
    """Fetch and extract main content from a webpage."""
    try:
        import requests
        from bs4 import BeautifulSoup
        
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Get text
        text = soup.get_text()
        
        # Clean up
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        # Limit length
        return text[:5000]
    
    except Exception as e:
        return f"Error fetching webpage: {e}"


def create_research_agent():
    """Create a research agent with specialized capabilities."""
    
    # Hybrid backend: ephemeral work + persistent findings
    backend = CompositeBackend(
        default=StateBackend(),
        routes={
            "/research/": StoreBackend(),  # Persistent research findings
            "/reports/": StoreBackend()     # Persistent reports
        }
    )
    
    # Research agent system prompt
    system_prompt = """
    You are a professional research assistant specializing in comprehensive research.
    
    Research Process:
    1. **Understand the Topic**: Clarify the research question and scope
    2. **Plan Research**: Use write_todos to plan research steps
    3. **Gather Information**: 
       - Use search_web to find relevant sources
       - Use fetch_webpage to get detailed content
       - Search multiple perspectives and sources
    4. **Analyze & Synthesize**:
       - Identify key findings and patterns
       - Cross-reference multiple sources
       - Note conflicting information
    5. **Save Findings**: Store important findings in /research/
    6. **Create Report**:
       - Write structured report in /reports/
       - Include executive summary
       - Cite all sources
       - Provide actionable insights
    
    Research Standards:
    - Always cite sources with URLs
    - Cross-verify facts from multiple sources
    - Note when information conflicts
    - Distinguish facts from opinions
    - Acknowledge knowledge gaps
    - Provide confidence levels
    
    Report Structure:
    # [Topic] Research Report
    
    ## Executive Summary
    [2-3 paragraph overview]
    
    ## Key Findings
    1. [Finding with citations]
    2. [Finding with citations]
    ...
    
    ## Detailed Analysis
    [In-depth analysis organized by themes]
    
    ## Conflicting Information
    [Note any contradictions found]
    
    ## Sources
    [List all sources with URLs]
    
    ## Confidence & Limitations
    [Assess reliability and gaps]
    """
    
    # Create the agent
    agent = create_deep_agent(
        model="anthropic:claude-sonnet-4-20250514",
        tools=[search_web, fetch_webpage],
        backend=backend,
        system_prompt=system_prompt
    )
    
    return agent


def run_research(agent, topic: str):
    """Run a research task."""
    print(f"\n{'='*60}")
    print(f"Starting research on: {topic}")
    print(f"{'='*60}\n")
    
    result = agent.invoke({
        "messages": [{
            "role": "user",
            "content": f"Research this topic and create a comprehensive report: {topic}"
        }]
    })
    
    # Print the response
    print("\n" + "="*60)
    print("Research Complete")
    print("="*60 + "\n")
    print(result["messages"][-1].content)
    
    return result


def main():
    """Main execution."""
    # Create research agent
    agent = create_research_agent()
    
    # Example research topics
    topics = [
        "Latest developments in quantum computing",
        "Impact of AI on software development",
        "Climate change mitigation technologies"
    ]
    
    # Run research on first topic (or all if desired)
    for topic in topics[:1]:  # Change to topics to run all
        result = run_research(agent, topic)
        
        # Optional: Save to file
        import json
        with open(f"research_{topic.replace(' ', '_')[:30]}.json", "w") as f:
            json.dump({
                "topic": topic,
                "result": result["messages"][-1].content
            }, f, indent=2)


if __name__ == "__main__":
    # Set up environment
    from dotenv import load_dotenv
    load_dotenv()
    
    # Run
    main()

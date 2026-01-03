# Advanced DeepAgents Patterns

This document covers advanced patterns for building production-grade DeepAgents.

## Multi-Agent Systems

### Hierarchical Agent Architecture

```python
from deepagents import create_deep_agent
from langchain_core.tools import tool

# Specialist agents
research_specialist = create_deep_agent(
    model="anthropic:claude-sonnet-4-20250514",
    system_prompt="You are a research specialist. Focus on finding accurate information."
)

data_specialist = create_deep_agent(
    model="anthropic:claude-sonnet-4-20250514",
    system_prompt="You are a data analyst. Focus on analyzing data and generating insights."
)

writer_specialist = create_deep_agent(
    model="anthropic:claude-sonnet-4-20250514",
    system_prompt="You are a technical writer. Focus on creating clear documentation."
)

# Delegation tools
@tool
def delegate_research(task: str) -> str:
    """Delegate research tasks to research specialist."""
    result = research_specialist.invoke({
        "messages": [{"role": "user", "content": task}]
    })
    return result["messages"][-1].content

@tool
def delegate_analysis(task: str) -> str:
    """Delegate data analysis to data specialist."""
    result = data_specialist.invoke({
        "messages": [{"role": "user", "content": task}]
    })
    return result["messages"][-1].content

@tool
def delegate_writing(task: str) -> str:
    """Delegate writing tasks to writer specialist."""
    result = writer_specialist.invoke({
        "messages": [{"role": "user", "content": task}]
    })
    return result["messages"][-1].content

# Coordinator agent
coordinator = create_deep_agent(
    model="anthropic:claude-sonnet-4-20250514",
    tools=[delegate_research, delegate_analysis, delegate_writing],
    system_prompt="""
    You are a project coordinator managing specialist agents.
    
    Delegate tasks appropriately:
    - Research tasks → delegate_research
    - Data analysis → delegate_analysis
    - Writing/documentation → delegate_writing
    
    Coordinate results and create final deliverables.
    """
)
```

### Collaborative Agent Pattern

```python
from deepagents import create_deep_agent
from typing import List, Dict

class AgentTeam:
    """Collaborative team of agents."""
    
    def __init__(self, agents: Dict[str, any]):
        self.agents = agents
        self.conversation_history = []
    
    def discuss(self, topic: str, rounds: int = 3):
        """Have agents discuss a topic collaboratively."""
        self.conversation_history = [
            {"role": "system", "content": f"Topic: {topic}"}
        ]
        
        for round_num in range(rounds):
            print(f"\n=== Round {round_num + 1} ===\n")
            
            for name, agent in self.agents.items():
                # Each agent sees full conversation
                result = agent.invoke({
                    "messages": self.conversation_history + [
                        {
                            "role": "user",
                            "content": f"Contribute your perspective on: {topic}"
                        }
                    ]
                })
                
                response = result["messages"][-1].content
                print(f"{name}: {response[:200]}...\n")
                
                # Add to conversation
                self.conversation_history.append({
                    "role": "assistant",
                    "content": f"[{name}]: {response}"
                })
        
        return self.conversation_history

# Create team
team = AgentTeam({
    "researcher": create_deep_agent(
        model="anthropic:claude-sonnet-4-20250514",
        system_prompt="You are a researcher. Provide factual insights."
    ),
    "critic": create_deep_agent(
        model="anthropic:claude-sonnet-4-20250514",
        system_prompt="You are a critic. Challenge assumptions and find flaws."
    ),
    "synthesizer": create_deep_agent(
        model="anthropic:claude-sonnet-4-20250514",
        system_prompt="You are a synthesizer. Combine ideas into coherent solutions."
    )
})

# Collaborative discussion
discussion = team.discuss("How can we improve code quality?", rounds=2)
```

## Custom Backend Implementations

### S3 Backend

```python
from deepagents.backends import BackendProtocol
import boto3
from typing import Optional

class S3Backend(BackendProtocol):
    """Store files in AWS S3."""
    
    def __init__(self, bucket: str, prefix: str = ""):
        self.s3 = boto3.client('s3')
        self.bucket = bucket
        self.prefix = prefix
    
    def read(self, path: str) -> Optional[bytes]:
        """Read file from S3."""
        try:
            key = f"{self.prefix}{path}".lstrip('/')
            response = self.s3.get_object(Bucket=self.bucket, Key=key)
            return response['Body'].read()
        except self.s3.exceptions.NoSuchKey:
            return None
    
    def write(self, path: str, content: bytes) -> None:
        """Write file to S3."""
        key = f"{self.prefix}{path}".lstrip('/')
        self.s3.put_object(Bucket=self.bucket, Key=key, Body=content)
    
    def delete(self, path: str) -> None:
        """Delete file from S3."""
        key = f"{self.prefix}{path}".lstrip('/')
        self.s3.delete_object(Bucket=self.bucket, Key=key)
    
    def list(self, path: str) -> list[str]:
        """List files in S3 directory."""
        prefix = f"{self.prefix}{path}".lstrip('/')
        response = self.s3.list_objects_v2(
            Bucket=self.bucket,
            Prefix=prefix
        )
        
        return [
            obj['Key'][len(self.prefix):].lstrip('/')
            for obj in response.get('Contents', [])
        ]

# Usage
from deepagents import create_deep_agent

backend = S3Backend(bucket="my-agent-data", prefix="agents/")

agent = create_deep_agent(
    model="anthropic:claude-sonnet-4-20250514",
    backend=backend
)
```

### Database Backend

```python
from deepagents.backends import BackendProtocol
import sqlite3
from typing import Optional

class DatabaseBackend(BackendProtocol):
    """Store files in SQLite database."""
    
    def __init__(self, db_path: str):
        self.conn = sqlite3.connect(db_path)
        self._setup_tables()
    
    def _setup_tables(self):
        """Create files table if not exists."""
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS files (
                path TEXT PRIMARY KEY,
                content BLOB,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.conn.commit()
    
    def read(self, path: str) -> Optional[bytes]:
        """Read file from database."""
        cursor = self.conn.execute(
            "SELECT content FROM files WHERE path = ?",
            (path,)
        )
        row = cursor.fetchone()
        return row[0] if row else None
    
    def write(self, path: str, content: bytes) -> None:
        """Write file to database."""
        self.conn.execute("""
            INSERT OR REPLACE INTO files (path, content, updated_at)
            VALUES (?, ?, CURRENT_TIMESTAMP)
        """, (path, content))
        self.conn.commit()
    
    def delete(self, path: str) -> None:
        """Delete file from database."""
        self.conn.execute("DELETE FROM files WHERE path = ?", (path,))
        self.conn.commit()
    
    def list(self, path: str) -> list[str]:
        """List files in directory."""
        cursor = self.conn.execute(
            "SELECT path FROM files WHERE path LIKE ?",
            (f"{path}%",)
        )
        return [row[0] for row in cursor.fetchall()]
```

## Advanced Monitoring

### Comprehensive Metrics

```python
from deepagents.middleware import Middleware
from dataclasses import dataclass, asdict
from datetime import datetime
import json

@dataclass
class AgentMetrics:
    """Agent execution metrics."""
    timestamp: str
    duration_ms: float
    tokens_used: int
    tool_calls: int
    error: Optional[str]
    success: bool

class MetricsMiddleware(Middleware):
    """Collect comprehensive agent metrics."""
    
    def __init__(self, output_file: str = "metrics.jsonl"):
        self.output_file = output_file
    
    def before_agent(self, state, runtime):
        """Track start time and state."""
        state["_metrics_start"] = datetime.now()
        state["_tool_calls_count"] = 0
        return None
    
    def after_agent(self, state, runtime):
        """Calculate and save metrics."""
        start = state.get("_metrics_start", datetime.now())
        duration = (datetime.now() - start).total_seconds() * 1000
        
        metrics = AgentMetrics(
            timestamp=datetime.now().isoformat(),
            duration_ms=duration,
            tokens_used=self._count_tokens(state),
            tool_calls=state.get("_tool_calls_count", 0),
            error=None,
            success=True
        )
        
        # Save to file
        with open(self.output_file, "a") as f:
            f.write(json.dumps(asdict(metrics)) + "\n")
        
        return None
    
    def _count_tokens(self, state) -> int:
        """Estimate token count from messages."""
        total = 0
        for msg in state.get("messages", []):
            # Rough estimate: ~4 chars per token
            total += len(str(msg.content)) // 4
        return total

# Usage
from deepagents import create_deep_agent

metrics = MetricsMiddleware(output_file="agent_metrics.jsonl")

agent = create_deep_agent(
    model="anthropic:claude-sonnet-4-20250514",
    middleware=[metrics]
)
```

### Real-time Monitoring Dashboard

```python
from deepagents.middleware import Middleware
import time
from collections import deque

class DashboardMiddleware(Middleware):
    """Real-time monitoring dashboard."""
    
    def __init__(self, window_size: int = 100):
        self.metrics = deque(maxlen=window_size)
        self.current_operation = None
    
    def before_agent(self, state, runtime):
        """Start monitoring operation."""
        self.current_operation = {
            "start_time": time.time(),
            "messages": len(state.get("messages", []))
        }
        self._update_dashboard("RUNNING")
        return None
    
    def after_agent(self, state, runtime):
        """Complete monitoring operation."""
        if self.current_operation:
            duration = time.time() - self.current_operation["start_time"]
            
            self.metrics.append({
                "duration": duration,
                "timestamp": time.time(),
                "success": True
            })
            
            self._update_dashboard("COMPLETE")
        
        return None
    
    def _update_dashboard(self, status: str):
        """Update dashboard display."""
        if not self.metrics:
            avg_duration = 0
            success_rate = 0
        else:
            avg_duration = sum(m["duration"] for m in self.metrics) / len(self.metrics)
            success_rate = sum(1 for m in self.metrics if m["success"]) / len(self.metrics)
        
        print(f"\r[{status}] Avg: {avg_duration:.2f}s | Success: {success_rate*100:.1f}% | Total: {len(self.metrics)}", end="")
```

## Production Deployment Patterns

### Containerized Deployment

```dockerfile
# Dockerfile for DeepAgent
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy agent code
COPY . .

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Run agent
CMD ["python", "agent.py"]
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  agent:
    build: .
    environment:
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      - REDIS_URL=redis://redis:6379
    volumes:
      - ./data:/app/data
    depends_on:
      - redis
  
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
```

### Kubernetes Deployment

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: deepagent
spec:
  replicas: 3
  selector:
    matchLabels:
      app: deepagent
  template:
    metadata:
      labels:
        app: deepagent
    spec:
      containers:
      - name: agent
        image: myregistry/deepagent:latest
        env:
        - name: ANTHROPIC_API_KEY
          valueFrom:
            secretKeyRef:
              name: api-keys
              key: anthropic
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "1Gi"
            cpu: "1000m"
```

### Serverless Deployment

```python
# AWS Lambda handler
import json
from deepagents import create_deep_agent

# Create agent once (cold start)
agent = create_deep_agent(
    model="anthropic:claude-sonnet-4-20250514"
)

def lambda_handler(event, context):
    """AWS Lambda handler for DeepAgent."""
    try:
        # Extract message from event
        message = json.loads(event['body'])['message']
        
        # Run agent
        result = agent.invoke({
            "messages": [{"role": "user", "content": message}]
        })
        
        # Return response
        return {
            'statusCode': 200,
            'body': json.dumps({
                'response': result["messages"][-1].content
            })
        }
    
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
```

## Advanced Tool Patterns

### Tool with State

```python
from langchain_core.tools import tool

class StatefulCalculator:
    """Calculator that maintains state."""
    
    def __init__(self):
        self.memory = 0
        self.history = []
    
    def calculate(self, expression: str) -> str:
        """Calculate expression and store result."""
        try:
            result = eval(expression)
            self.memory = result
            self.history.append(f"{expression} = {result}")
            return f"Result: {result}\nMemory: {self.memory}"
        except Exception as e:
            return f"Error: {e}"
    
    def recall(self) -> str:
        """Recall last result."""
        return f"Memory: {self.memory}"
    
    def show_history(self) -> str:
        """Show calculation history."""
        return "\n".join(self.history)

# Create stateful tools
calc = StatefulCalculator()

@tool
def calculate(expression: str) -> str:
    """Calculate mathematical expression."""
    return calc.calculate(expression)

@tool
def recall_memory() -> str:
    """Recall last calculation result."""
    return calc.recall()

@tool
def show_history() -> str:
    """Show calculation history."""
    return calc.show_history()
```

### Async Tool Pattern

```python
from langchain_core.tools import tool
import asyncio
import aiohttp

@tool
async def fetch_multiple_urls(urls: str) -> str:
    """Fetch multiple URLs concurrently."""
    url_list = [u.strip() for u in urls.split(',')]
    
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_one(session, url) for url in url_list]
        results = await asyncio.gather(*tasks)
    
    return "\n\n---\n\n".join(results)

async def fetch_one(session, url):
    """Fetch single URL."""
    try:
        async with session.get(url, timeout=10) as response:
            return f"URL: {url}\nStatus: {response.status}\n{await response.text()}"
    except Exception as e:
        return f"URL: {url}\nError: {e}"
```

## Performance Optimization

### Caching Strategy

```python
from functools import lru_cache
from langchain_core.tools import tool
import hashlib

@tool
def cached_computation(data: str) -> str:
    """Expensive computation with caching."""
    return _compute(data)

@lru_cache(maxsize=128)
def _compute(data: str) -> str:
    """Cached computation logic."""
    # Expensive operation
    import time
    time.sleep(2)  # Simulate expensive work
    return f"Processed: {data}"
```

### Rate Limiting

```python
from langchain_core.tools import tool
import time
from collections import deque

class RateLimiter:
    """Rate limiter for API calls."""
    
    def __init__(self, calls: int, period: int):
        self.calls = calls
        self.period = period
        self.timestamps = deque()
    
    def wait_if_needed(self):
        """Wait if rate limit exceeded."""
        now = time.time()
        
        # Remove old timestamps
        while self.timestamps and self.timestamps[0] < now - self.period:
            self.timestamps.popleft()
        
        # Wait if needed
        if len(self.timestamps) >= self.calls:
            sleep_time = self.period - (now - self.timestamps[0])
            if sleep_time > 0:
                time.sleep(sleep_time)
        
        self.timestamps.append(now)

# Create rate limiter (10 calls per minute)
limiter = RateLimiter(calls=10, period=60)

@tool
def rate_limited_api_call(query: str) -> str:
    """API call with rate limiting."""
    limiter.wait_if_needed()
    # Make API call
    return f"Result for: {query}"
```

These advanced patterns enable building production-grade, scalable DeepAgent systems.

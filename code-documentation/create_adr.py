#!/usr/bin/env python3
"""
Helper script to create a new Architecture Decision Record (ADR).
Usage: python3 create_adr.py "Title of the decision"
"""

import os
import sys
import argparse
from datetime import datetime

# Configuration
ADR_DIR = "docs/adr"
STATUS = "Accepted"
TEMPLATE = """# {num}. {title}

Date: {date}
Status: {status}

## Context and Problem Statement

[Describe the context and problem statement, e.g., in free form using two to three sentences. You may want to articulate the problem in form of a question.]

## Decision Drivers

* [driver 1, e.g., a force, facing concern, …]
* [driver 2, e.g., a force, facing concern, …]

## Considered Options

* [option 1]
* [option 2]
* [option 3]

## Decision Outcome

Chosen option: "{title}", because [justification. e.g., only option that meets k.o. criterion decision driver | which resolves force force | … | comes out best (see below)].

### Positive Consequences

* [e.g., improvement of quality attribute satisfaction, follow-up decisions required, …]

### Negative Consequences

* [e.g., compromising quality attribute, follow-up decisions required, …]

## Pros and Cons of the Options

### [option 1]

[example | description | pointer to more information | …]

* Good, because [argument a]
* Good, because [argument b]
* Bad, because [argument c]

### [option 2]

* …

## Links

* [Link type] [Link to ADR] <!-- example: Refined by [ADR-0005](0005-example.md) -->
* …
"""

def get_next_adr_number(directory):
    """Finds the next sequential number for the ADR based on existing files."""
    if not os.path.exists(directory):
        return 1
    
    max_num = 0
    for filename in os.listdir(directory):
        if filename.endswith(".md"):
            try:
                # Extract number assuming format 'NNNN-title.md'
                num_str = filename.split("-")[0]
                if num_str.isdigit():
                    max_num = max(max_num, int(num_str))
            except (IndexError, ValueError):
                continue
    return max_num + 1

def create_adr(title):
    """Creates the ADR file with the appropriate content."""
    # Ensure directory exists
    os.makedirs(ADR_DIR, exist_ok=True)
    
    # Get next number
    num = get_next_adr_number(ADR_DIR)
    
    # Format filename
    safe_title = title.lower().replace(" ", "-").replace("/", "-")
    filename = f"{num:04d}-{safe_title}.md"
    filepath = os.path.join(ADR_DIR, filename)
    
    # Check if file already exists
    if os.path.exists(filepath):
        print(f"Error: File {filepath} already exists.")
        sys.exit(1)
    
    # Generate content
    content = TEMPLATE.format(
        num=num,
        title=title,
        date=datetime.now().strftime("%Y-%m-%d"),
        status=STATUS
    )
    
    # Write file
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Successfully created ADR: {filepath}")
    except IOError as e:
        print(f"Error writing file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 create_adr.py \"Decision Title\"")
        sys.exit(1)
    
    decision_title = " ".join(sys.argv[1:])
    create_adr(decision_title)

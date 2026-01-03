#!/usr/bin/env python3
"""
Analyzes Python files in a directory to check for missing docstrings.
Usage: python3 docstring_coverage.py [directory_path]
Default directory is the current working directory.
"""

import os
import sys
import ast
from typing import List, Tuple

def analyze_file(filepath: str) -> List[Tuple[str, int, str]]:
    """
    Parses a single Python file and returns a list of items missing docstrings.
    Returns a list of tuples: (type_name, line_number, name)
    """
    missing_items = []
    
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            source = f.read()
    except (IOError, UnicodeDecodeError):
        # Skip files that can't be read
        return []

    try:
        tree = ast.parse(source, filename=filepath)
    except SyntaxError:
        # Skip files with syntax errors
        return []

    for node in ast.walk(tree):
        # Check Functions
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            # Skip private methods if desired, but here we check everything
            if not ast.get_docstring(node):
                missing_items.append(("Function", node.lineno, node.name))
        
        # Check Classes
        elif isinstance(node, ast.ClassDef):
            if not ast.get_docstring(node):
                missing_items.append(("Class", node.lineno, node.name))
            
            # Check methods inside classes
            for item in node.body:
                if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    # Skip dunder methods like __init__ if they are usually obvious, 
                    # but for strict documentation, we check them.
                    if not ast.get_docstring(item):
                        missing_items.append(("Method", item.lineno, f"{node.name}.{item.name}"))

    return missing_items

def scan_directory(directory: str):
    """
    Recursively scans directory for .py files and aggregates results.
    """
    total_missing = 0
    files_scanned = 0

    print(f"Scanning directory: {os.path.abspath(directory)}\n")

    for root, _, files in os.walk(directory):
        # Skip hidden directories or common cache directories
        if any(part.startswith('.') for part in root.split(os.sep)):
            continue
        if '__pycache__' in root:
            continue

        for file in files:
            if file.endswith(".py"):
                filepath = os.path.join(root, file)
                missing = analyze_file(filepath)
                
                if missing:
                    files_scanned += 1
                    print(f"{filepath}:")
                    for item_type, line, name in missing:
                        print(f"  - Line {line}: {item_type} '{name}' is missing a docstring.")
                        total_missing += 1
                    print("")

    print("--- Summary ---")
    print(f"Total missing docstrings found: {total_missing}")
    
    if total_missing > 0:
        sys.exit(1)
    else:
        print("No missing docstrings found!")
        sys.exit(0)

if __name__ == "__main__":
    target_dir = sys.argv[1] if len(sys.argv) > 1 else "."
    if not os.path.isdir(target_dir):
        print(f"Error: Directory '{target_dir}' does not exist.")
        sys.exit(1)
    
    scan_directory(target_dir)

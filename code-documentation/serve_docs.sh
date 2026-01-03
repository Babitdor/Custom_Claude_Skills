#!/bin/bash

# Helper script to detect and serve documentation locally.
# Supports: MkDocs, Sphinx, JSDoc

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Detecting documentation framework...${NC}"

# Check for MkDocs
if [ -f "mkdocs.yml" ]; then
    echo -e "${GREEN}Found mkdocs.yml. Starting MkDocs...${NC}"
    if command -v mkdocs &> /dev/null; then
        mkdocs serve
    else
        echo -e "${RED}Error: mkdocs is not installed. Please run 'pip install mkdocs'${NC}"
        exit 1
    fi

# Check for Sphinx (usually in source/conf.py or docs/conf.py)
elif [ -f "docs/conf.py" ] || [ -f "source/conf.py" ] || [ -f "conf.py" ]; then
    echo -e "${GREEN}Found Sphinx configuration. Starting Sphinx live reload...${NC}"
    
    # Determine source directory
    if [ -d "source" ]; then
        SRC_DIR="source"
    elif [ -d "docs" ]; then
        SRC_DIR="docs"
    else
        SRC_DIR="."
    fi

    if command -v sphinx-autobuild &> /dev/null; then
        # Default build dir is usually _build/html
        sphinx-autobuild "$SRC_DIR" "_build/html"
    elif command -v sphinx-build &> /dev/null; then
        echo -e "${YELLOW}sphinx-autobuild not found. Falling back to static build (no live reload).${NC}"
        echo -e "${YELLOW}Install sphinx-autobuild for live reloading: pip install sphinx-autobuild${NC}"
        sphinx-build -b html "$SRC_DIR" "_build/html"
        echo -e "${GREEN}Docs built in _build/html/index.html${NC}"
    else
        echo -e "${RED}Error: Sphinx is not installed. Please run 'pip install sphinx'${NC}"
        exit 1
    fi

# Check for JSDoc (presence of jsdoc.json or package.json with jsdoc config)
elif [ -f "jsdoc.json" ] || ( [ -f "package.json" ] && grep -q "jsdoc" package.json ); then
    echo -e "${GREEN}Found JSDoc configuration. Generating and serving docs...${NC}"
    
    if command -v jsdoc &> /dev/null; then
        # Create a temp output dir if not specified, or use default
        OUTPUT_DIR="jsdoc-out"
        
        # Build docs
        jsdoc -c jsdoc.json -d "$OUTPUT_DIR"
        
        # Try to open a simple server if python is available
        if command -v python3 &> /dev/null; then
            echo -e "${GREEN}Starting HTTP server on port 8000...${NC}"
            cd "$OUTPUT_DIR"
            python3 -m http.server 8000
        else
            echo -e "${GREEN}Docs generated in $OUTPUT_DIR${NC}"
            echo -e "${YELLOW}Python3 not found. Please open $OUTPUT_DIR/index.html manually.${NC}"
        fi
    else
        echo -e "${RED}Error: jsdoc is not installed. Please run 'npm install -g jsdoc'${NC}"
        exit 1
    fi

else
    echo -e "${RED}No supported documentation configuration found (mkdocs.yml, conf.py, or jsdoc.json).${NC}"
    exit 1
fi

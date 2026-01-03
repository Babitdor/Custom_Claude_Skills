# Minimal Clean Design Skill - Usage Guide

## Overview

The Minimal Clean Design Skill provides tools and guidance for creating minimalist, clean website designs that focus on content and usability while maintaining aesthetic appeal.

## Components

### 1. Python Module (`minimal_clean.py`)

The core functionality is provided through a Python module with the following functions:

#### `generate_minimal_color_palette(base_hue: int = 220, style: str = "monochrome")`
Generates a harmonious color palette based on minimalist principles.

Parameters:
- `base_hue`: Base hue value (0-360) for the accent color
- `style`: Palette style - 'monochrome', 'duotone', or 'accent'

Returns: Dictionary with color names and values

#### `create_typography_system(base_size: int = 18)`
Creates a typography system with proper hierarchy using a modular scale.

Parameters:
- `base_size`: Base font size in pixels

Returns: Dictionary with typography levels and properties

#### `optimize_layout_spacing(base_unit: int = 8)`
Creates a consistent spacing system based on a base unit.

Parameters:
- `base_unit`: Base spacing unit in pixels

Returns: Dictionary with spacing names and values

#### `generate_css_from_principles(palette, typography, spacing)`
Generates CSS based on minimal design principles.

Parameters:
- `palette`: Color palette dictionary
- `typography`: Typography system dictionary
- `spacing`: Spacing system dictionary

Returns: CSS string

#### `provide_minimal_design_recommendations(current_design)`
Analyzes a design and provides recommendations for making it more minimal.

Parameters:
- `current_design`: Dictionary with current design properties

Returns: List of recommendations

### 2. Design Principles (`design_principles.json`)

Contains comprehensive design principles and best practices for minimal design:
- Best practices and common mistakes
- Implementation checklist (immediate, medium-term, long-term)
- Detailed principles for color, layout, typography, and whitespace

### 3. Examples (`examples/`)

Demonstrates minimal clean design principles:
- `minimal-portfolio.html`: HTML structure example
- `minimal-clean.css`: CSS implementation example

## Usage Examples

### Basic Usage
```python
from minimal_clean import (
    generate_minimal_color_palette,
    create_typography_system,
    optimize_layout_spacing,
    generate_css_from_principles
)

# Create a minimal design system
palette = generate_minimal_color_palette(220, "monochrome")
typography = create_typography_system(18)
spacing = optimize_layout_spacing(8)

# Generate CSS
css = generate_css_from_principles(palette, typography, spacing)
```

### Design Analysis
```python
from minimal_clean import provide_minimal_design_recommendations

current_design = {
    "font_count": 4,
    "color_count": 10,
    "whitespace_ratio": 0.15
}

recommendations = provide_minimal_design_recommendations(current_design)
```

## Key Principles

1. **Whitespace Mastery**: Use negative space strategically to create visual breathing room
2. **Typography Hierarchy**: Create clear information architecture through font sizes and weights
3. **Color Restraint**: Use limited, harmonious palettes that enhance rather than distract
4. **Functional Minimalism**: Remove non-essential elements while preserving usability

## Applications

- Portfolio websites
- Landing pages
- Dashboard interfaces
- Blog designs
- E-commerce interfaces

## Testing

Run the test script to verify functionality:
```bash
python test_skill.py
```
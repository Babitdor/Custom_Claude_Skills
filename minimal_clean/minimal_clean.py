#!/usr/bin/env python3
"""
Minimal Clean Design Skill
=========================

A Python module for implementing minimalist and clean design principles
for websites and user interfaces.

This module provides functions to:
- Analyze design elements for minimalism
- Generate color palettes
- Create typography systems
- Optimize layouts
- Provide design recommendations
"""

import json
from typing import Dict, List, Tuple, Union

def analyze_whitespace_usage(css_content: str) -> Dict[str, Union[int, List[str]]]:
    """
    Analyze CSS for whitespace usage patterns.
    
    Args:
        css_content (str): CSS content to analyze
        
    Returns:
        Dict containing analysis results
    """
    # This would contain actual analysis logic
    return {
        "padding_issues": [],
        "margin_issues": [],
        "whitespace_score": 85,
        "recommendations": [
            "Increase section padding for better visual breathing room",
            "Add more margin between paragraphs"
        ]
    }

def generate_minimal_color_palette(base_hue: int = 220, style: str = "monochrome") -> Dict[str, str]:
    """
    Generate a minimal color palette based on design principles.
    
    Args:
        base_hue (int): Base hue value (0-360)
        style (str): Palette style - 'monochrome', 'duotone', 'accent'
        
    Returns:
        Dict with color names and hex values
    """
    if style == "monochrome":
        return {
            "background": "#fdfdfd",
            "surface": "#f5f5f5",
            "text_primary": "#212121",
            "text_secondary": "#757575",
            "accent": f"hsl({base_hue}, 60%, 50%)",
            "accent_hover": f"hsl({base_hue}, 60%, 40%)"
        }
    elif style == "duotone":
        return {
            "background": "#fdfdfd",
            "surface": "#f5f5f5",
            "text_primary": "#212121",
            "text_secondary": "#757575",
            "primary": f"hsl({base_hue}, 60%, 50%)",
            "secondary": f"hsl({(base_hue + 120) % 360}, 60%, 50%)"
        }
    else:  # accent
        return {
            "background": "#ffffff",
            "surface": "#f8f9fa",
            "text": "#333333",
            "accent": f"hsl({base_hue}, 70%, 45%)"
        }

def create_typography_system(base_size: int = 18) -> Dict[str, Dict[str, Union[str, int]]]:
    """
    Create a typography system with proper hierarchy.
    
    Args:
        base_size (int): Base font size in pixels
        
    Returns:
        Dict with typography scale
    """
    scale_factor = 1.25  # Major third scale
    
    return {
        "display": {
            "size": f"{int(base_size * (scale_factor ** 4))}px",
            "weight": 700,
            "line_height": 1.2
        },
        "h1": {
            "size": f"{int(base_size * (scale_factor ** 3))}px",
            "weight": 600,
            "line_height": 1.25
        },
        "h2": {
            "size": f"{int(base_size * (scale_factor ** 2))}px",
            "weight": 500,
            "line_height": 1.3
        },
        "h3": {
            "size": f"{int(base_size * scale_factor)}px",
            "weight": 500,
            "line_height": 1.4
        },
        "body": {
            "size": f"{base_size}px",
            "weight": 400,
            "line_height": 1.6
        },
        "small": {
            "size": f"{int(base_size / scale_factor)}px",
            "weight": 400,
            "line_height": 1.5
        }
    }

def optimize_layout_spacing(base_unit: int = 8) -> Dict[str, int]:
    """
    Create a consistent spacing system based on a base unit.
    
    Args:
        base_unit (int): Base spacing unit in pixels
        
    Returns:
        Dict with spacing values
    """
    return {
        "xxs": base_unit // 2,      # 4px
        "xs": base_unit,            # 8px
        "sm": base_unit * 2,        # 16px
        "md": base_unit * 3,        # 24px
        "lg": base_unit * 4,        # 32px
        "xl": base_unit * 6,        # 48px
        "xxl": base_unit * 8,       # 64px
        "xxxl": base_unit * 12      # 96px
    }

def provide_minimal_design_recommendations(
    current_design: Dict[str, any]
) -> List[str]:
    """
    Provide recommendations for making a design more minimal and clean.
    
    Args:
        current_design (Dict): Current design properties
        
    Returns:
        List of recommendations
    """
    recommendations = []
    
    # Check for common minimal design issues
    if current_design.get("font_count", 0) > 2:
        recommendations.append("Reduce number of font families to 2 or fewer")
    
    if current_design.get("color_count", 0) > 5:
        recommendations.append("Limit color palette to 5 or fewer colors")
    
    if current_design.get("whitespace_ratio", 0) < 0.3:
        recommendations.append("Increase whitespace to at least 30% of the layout")
    
    if not current_design.get("consistent_spacing", True):
        recommendations.append("Implement a consistent spacing system using a base unit")
    
    if not current_design.get("typography_hierarchy", True):
        recommendations.append("Establish clear typography hierarchy with distinct sizes")
    
    return recommendations

def generate_css_from_principles(
    palette: Dict[str, str] = None,
    typography: Dict[str, Dict[str, Union[str, int]]] = None,
    spacing: Dict[str, int] = None
) -> str:
    """
    Generate CSS based on minimal design principles.
    
    Args:
        palette (Dict): Color palette
        typography (Dict): Typography system
        spacing (Dict): Spacing system
        
    Returns:
        CSS string with minimal design principles applied
    """
    if palette is None:
        palette = generate_minimal_color_palette()
    
    if typography is None:
        typography = create_typography_system()
    
    if spacing is None:
        spacing = optimize_layout_spacing()
    
    css = f"""/* Minimal Clean Design CSS */
:root {{
  /* Color Palette */
  --color-background: {palette['background']};
  --color-surface: {palette['surface']};
  --color-text-primary: {palette['text_primary']};
  --color-text-secondary: {palette['text_secondary']};
  --color-accent: {palette['accent']};
  --color-accent-hover: {palette['accent_hover']};
  
  /* Spacing System */
  --spacing-xxs: {spacing['xxs']}px;
  --spacing-xs: {spacing['xs']}px;
  --spacing-sm: {spacing['sm']}px;
  --spacing-md: {spacing['md']}px;
  --spacing-lg: {spacing['lg']}px;
  --spacing-xl: {spacing['xl']}px;
  --spacing-xxl: {spacing['xxl']}px;
  --spacing-xxxl: {spacing['xxxl']}px;
  
  /* Typography */
  --font-size-display: {typography['display']['size']};
  --font-weight-display: {typography['display']['weight']};
  --line-height-display: {typography['display']['line_height']};
  
  --font-size-h1: {typography['h1']['size']};
  --font-weight-h1: {typography['h1']['weight']};
  --line-height-h1: {typography['h1']['line_height']};
  
  --font-size-h2: {typography['h2']['size']};
  --font-weight-h2: {typography['h2']['weight']};
  --line-height-h2: {typography['h2']['line_height']};
  
  --font-size-body: {typography['body']['size']};
  --font-weight-body: {typography['body']['weight']};
  --line-height-body: {typography['body']['line_height']};
}}

/* Base Styles */
body {{
  font-family: system-ui, -apple-system, sans-serif;
  font-size: var(--font-size-body);
  font-weight: var(--font-weight-body);
  line-height: var(--line-height-body);
  color: var(--color-text-primary);
  background-color: var(--color-background);
  margin: 0;
  padding: 0;
}}

/* Typography */
h1 {{
  font-size: var(--font-size-h1);
  font-weight: var(--font-weight-h1);
  line-height: var(--line-height-h1);
  margin-bottom: var(--spacing-lg);
}}

h2 {{
  font-size: var(--font-size-h2);
  font-weight: var(--font-weight-h2);
  line-height: var(--line-height-h2);
  margin-bottom: var(--spacing-md);
}}

/* Layout */
.container {{
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 var(--spacing-lg);
}}

.section {{
  padding: var(--spacing-xxl) 0;
}}

/* Spacing Utilities */
.mt-xs {{ margin-top: var(--spacing-xs); }}
.mt-sm {{ margin-top: var(--spacing-sm); }}
.mt-md {{ margin-top: var(--spacing-md); }}
.mt-lg {{ margin-top: var(--spacing-lg); }}
.mt-xl {{ margin-top: var(--spacing-xl); }}
.mt-xxl {{ margin-top: var(--spacing-xxl); }}

.mb-xs {{ margin-bottom: var(--spacing-xs); }}
.mb-sm {{ margin-bottom: var(--spacing-sm); }}
.mb-md {{ margin-bottom: var(--spacing-md); }}
.mb-lg {{ margin-bottom: var(--spacing-lg); }}
.mb-xl {{ margin-bottom: var(--spacing-xl); }}
.mb-xxl {{ margin-bottom: var(--spacing-xxl); }}

.pt-xs {{ padding-top: var(--spacing-xs); }}
.pt-sm {{ padding-top: var(--spacing-sm); }}
.pt-md {{ padding-top: var(--spacing-md); }}
.pt-lg {{ padding-top: var(--spacing-lg); }}
.pt-xl {{ padding-top: var(--spacing-xl); }}
.pt-xxl {{ padding-top: var(--spacing-xxl); }}

.pb-xs {{ padding-bottom: var(--spacing-xs); }}
.pb-sm {{ padding-bottom: var(--spacing-sm); }}
.pb-md {{ padding-bottom: var(--spacing-md); }}
.pb-lg {{ padding-bottom: var(--spacing-lg); }}
.pb-xl {{ padding-bottom: var(--spacing-xl); }}
.pb-xxl {{ padding-bottom: var(--spacing-xxl); }}

/* Minimal Components */
.btn {{
  background-color: var(--color-accent);
  color: white;
  border: none;
  padding: var(--spacing-sm) var(--spacing-lg);
  border-radius: 4px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s ease;
}}

.btn:hover {{
  background-color: var(--color-accent-hover);
}}

.card {{
  background-color: var(--color-surface);
  border-radius: 8px;
  padding: var(--spacing-lg);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}}"""
    
    return css

if __name__ == "__main__":
    # Example usage
    print("Minimal Clean Design Skill")
    print("==========================")
    
    # Generate a color palette
    palette = generate_minimal_color_palette(220, "monochrome")
    print("\nGenerated Color Palette:")
    for name, color in palette.items():
        print(f"  {name}: {color}")
    
    # Create typography system
    typography = create_typography_system(18)
    print("\nTypography System:")
    for level, props in typography.items():
        print(f"  {level}: {props['size']} ({props['weight']})")
    
    # Generate spacing system
    spacing = optimize_layout_spacing(8)
    print("\nSpacing System:")
    for name, value in spacing.items():
        print(f"  {name}: {value}px")
    
    # Generate CSS
    css = generate_css_from_principles(palette, typography, spacing)
    print("\nGenerated CSS (first 500 chars):")
    print(css[:500] + "...")
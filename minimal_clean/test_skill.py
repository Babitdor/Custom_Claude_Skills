#!/usr/bin/env python3
"""
Test script for the Minimal Clean Design Skill
"""

import sys
import os

# Add the skill directory to the path
skill_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, skill_dir)

from minimal_clean import (
    generate_minimal_color_palette,
    create_typography_system,
    optimize_layout_spacing,
    generate_css_from_principles,
    provide_minimal_design_recommendations
)

def main():
    print("Minimal Clean Design Skill - Test Script")
    print("=" * 40)
    
    # Generate a minimal color palette
    print("\n1. Generating minimal color palette...")
    palette = generate_minimal_color_palette(base_hue=220, style="monochrome")
    for name, color in palette.items():
        print(f"   {name}: {color}")
    
    # Create typography system
    print("\n2. Creating typography system...")
    typography = create_typography_system(base_size=18)
    for level, props in typography.items():
        print(f"   {level}: {props['size']} (weight: {props['weight']})")
    
    # Generate spacing system
    print("\n3. Generating spacing system...")
    spacing = optimize_layout_spacing(base_unit=8)
    for name, value in spacing.items():
        print(f"   {name}: {value}px")
    
    # Generate CSS
    print("\n4. Generating CSS from principles...")
    css = generate_css_from_principles(palette, typography, spacing)
    print(f"   Generated CSS with {len(css)} characters")
    print("   First 200 characters:")
    print(f"   {css[:200]}...")
    
    # Provide design recommendations
    print("\n5. Providing design recommendations...")
    sample_design = {
        "font_count": 3,
        "color_count": 8,
        "whitespace_ratio": 0.25,
        "consistent_spacing": False,
        "typography_hierarchy": False
    }
    
    recommendations = provide_minimal_design_recommendations(sample_design)
    for i, rec in enumerate(recommendations, 1):
        print(f"   {i}. {rec}")
    
    print("\nTest completed successfully!")

if __name__ == "__main__":
    main()
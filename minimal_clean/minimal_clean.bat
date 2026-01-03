@echo off
REM Minimal Clean Design Skill - Command Line Interface

echo Minimal Clean Design Skill
echo ==========================
echo.

cd /d "C:\Users\Babit-PC\.nami\skills\minimal_clean"

if "%1" == "palette" (
    echo Generating minimal color palette...
    python -c "import sys; sys.path.append('.'); from minimal_clean import generate_minimal_color_palette; import json; palette = generate_minimal_color_palette(); print(json.dumps(palette, indent=2))"
) else if "%1" == "typography" (
    echo Generating typography system...
    python -c "import sys; sys.path.append('.'); from minimal_clean import create_typography_system; import json; typography = create_typography_system(); print(json.dumps(typography, indent=2))"
) else if "%1" == "spacing" (
    echo Generating spacing system...
    python -c "import sys; sys.path.append('.'); from minimal_clean import optimize_layout_spacing; import json; spacing = optimize_layout_spacing(); print(json.dumps(spacing, indent=2))"
) else if "%1" == "css" (
    echo Generating CSS from minimal principles...
    python -c "import sys; sys.path.append('.'); from minimal_clean import generate_minimal_color_palette, create_typography_system, optimize_layout_spacing, generate_css_from_principles; palette = generate_minimal_color_palette(); typography = create_typography_system(); spacing = optimize_layout_spacing(); css = generate_css_from_principles(palette, typography, spacing); print(css)"
) else if "%1" == "recommendations" (
    echo Generating design recommendations...
    python -c "import sys; sys.path.append('.'); from minimal_clean import provide_minimal_design_recommendations; sample_design = {'font_count': 3, 'color_count': 8, 'whitespace_ratio': 0.25, 'consistent_spacing': False, 'typography_hierarchy': False}; recommendations = provide_minimal_design_recommendations(sample_design); [print(f'{i}. {rec}') for i, rec in enumerate(recommendations, 1)]"
) else (
    echo Usage: minimal_clean.bat [palette^|typography^|spacing^|css^|recommendations]
    echo.
    echo Commands:
    echo   palette          Generate a minimal color palette
    echo   typography       Generate a typography system
    echo   spacing          Generate a spacing system
    echo   css              Generate CSS from minimal principles
    echo   recommendations  Provide design recommendations
)
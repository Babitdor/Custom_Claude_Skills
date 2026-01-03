---
name: code-documentation
description: Enables the generation, maintenance, and optimization of high-quality, human-centric code documentation, covering READMEs, API references, inline comments, and architectural design records using modern 'docs-as-code' principles.
---

# Code Documentation Skill

## Overview

This skill transforms complex codebases into accessible, maintainable, and professional documentation assets. It bridges the gap between technical implementation and user understanding by applying industry-standard best practices such as "docs-as-code," automated generation, and self-documenting code principles. By leveraging this skill, an AI agent can significantly reduce technical debt, accelerate developer onboarding, and ensure that architectural decisions and security considerations are preserved for future maintainers. It covers the entire documentation lifecycle, from initial planning and writing to automated generation and continuous maintenance.

## Core Competencies

- **Self-Documenting Code**: Refactoring code to use descriptive naming conventions and clear logic structures that reduce the need for extraneous comments.
- **Structured Docstrings & API References**: Generating standardized, machine-parsable documentation (e.g., JSDoc, Python Docstrings, Go Doc) that integrates with IDEs and generation tools.
- **Comprehensive READMEs**: Crafting professional project landing pages that include installation, usage, contribution guidelines, and badges.
- **Architecture Decision Records (ADRs)**: Documenting the context, constraints, and consequences of significant technical choices to preserve historical knowledge.
- **Docs-as-Code Automation**: Implementing workflows using tools like MkDocs, Docusaurus, or Sphinx to build and deploy documentation directly from source control.
- **Inline Commenting Strategy**: Writing high-value inline comments that explain "why" complex logic exists, rather than just restating "what" the code does.
- **Security & Testing Documentation**: Explicitly recording security considerations, vulnerabilities, and testing strategies to ensure comprehensive coverage and compliance.

## When to Use This Skill

### Primary Use Cases
- **Onboarding New Developers**: When a new team member joins and requires clear guides on setup, architecture, and coding standards.
- **Refactoring Legacy Code**: When updating old, undocumented, or poorly documented codebases to improve maintainability and reduce technical debt.
- **Public API Release**: When preparing a library or SDK for public consumption, requiring precise API references and usage examples.
- **Feature Implementation**: When adding complex features that necessitate recording design decisions (ADRs) and updating existing docs.
- **Compliance Audits**: When security or process documentation is required for auditing purposes.

### Trigger Phrases
- "Write documentation for this [function/class/module]"
- "Create a professional README for this project"
- "Explain this code and add inline comments"
- "Generate API docs using [tool name]"
- "Document the architecture and design decisions"
- "Refactor this code to be self-documenting"

## Detailed Instructions

### Phase 1: Assessment & Planning
1.  **Analyze the Audience and Scope**: Determine if the documentation is for internal developers (focus on architecture, setup) or external consumers (focus on API usage, tutorials). Identify the specific artifacts needed (README, API docs, ADRs).
2.  **Audit Existing Code**: Scan the codebase for existing comments, naming conventions, and docstrings. Identify areas where code is obscure or "clever" and needs explanation or refactoring.
3.  **Select the Toolchain**: Decide on the appropriate documentation generator based on the language (e.g., JSDoc for JS, Sphinx for Python, godoc for Go) and the hosting strategy (static site generator vs. simple markdown files).

### Phase 2: Implementation
1.  **Refactor for Self-Documentation**: Rename variables and functions to be descriptive. Ensure logic flow is intuitive. Replace bad comments with better code structure.
2.  **Draft High-Level Documentation**: Start with the README. Ensure it includes: Title, Short Description, Installation Instructions, Quick Start Example, Usage details, and Contributing guidelines.
3.  **Implement Structured Docstrings**: Add standard-compliant docstrings to all public functions, classes, and modules. Include parameters, return types, raised exceptions, and brief usage examples.
4.  **Record Design Decisions**: Create an `docs/adr/` directory. For every major decision, write a short markdown file following the MADR (Markdown Any Decision Record) template (Context, Decision, Consequences).
5.  **Add Inline Comments Sparingly**: Add comments only to explain *why* a non-obvious implementation was chosen (e.g., workarounds for bugs, complex algorithms, or business rule constraints).

### Phase 3: Verification & Refinement
1.  **Run Documentation Generators**: Execute the build command for the selected tool (e.g., `mkdocs build`, `npm run docs`). Fix any warnings or syntax errors in the docstrings.
2.  **Validate Examples**: Copy and run all code examples provided in the documentation to ensure they are accurate and up-to-date.
3.  **Review for Clarity**: Read the documentation from the perspective of a new user. Check for jargon, undefined acronyms, or ambiguous instructions.

## Technical Reference

### Key Commands & Tools
```bash
# Python: Generate HTML documentation using Sphinx
sphinx-quickstart
sphinx-build -b html source build

# JavaScript/TypeScript: Generate documentation using JSDoc
jsdoc src/ -c jsdoc.json

# Go: View documentation locally
godoc -http=:6060

# Static Site Generators: Serve docs locally for MkDocs
mkdocs serve
```

### Common Patterns

**Python (Google Style Docstring):**
```python
def calculate_compound_interest(principal, rate, periods):
    """Calculates compound interest over a specified number of periods.

    This function uses the standard formula A = P(1 + r/n)^(nt) 
    simplified for annual compounding.

    Args:
        principal (float): The initial amount of money.
        rate (float): The annual interest rate (e.g., 0.05 for 5%).
        periods (int): The number of years to compound.

    Returns:
        float: The final balance including interest.

    Raises:
        ValueError: If principal is negative or rate is below 0.
    """
    if principal < 0:
        raise ValueError("Principal cannot be negative")
    return principal * (1 + rate) ** periods
```

**JavaScript (JSDoc):**
```javascript
/**
 * Fetches user data from the API.
 * @async
 * @param {string} userId - The unique identifier of the user.
 * @returns {Promise<Object>} The user object containing name and email.
 * @throws {Error} Throws an error if the network request fails.
 */
async function fetchUser(userId) {
  const response = await fetch(`/api/users/${userId}`);
  if (!response.ok) throw new Error('Network response was not ok');
  return response.json();
}
```

### Configuration Templates

**JSDoc Configuration (`jsdoc.json`):**
```json
{
  "source": {
    "include": ["./src/"],
    "includePattern": "\\.(js|jsx)$",
    "exclude": ["node_modules"]
  },
  "opts": {
    "destination": "./docs/",
    "recurse": true
  },
  "plugins": ["plugins/markdown"]
}
```

## Best Practices

### Do's
- **Write for Humans**: Use clear, concise language. Avoid unnecessary jargon unless it is standard for the target audience.
- **Keep Docs Close to Code**: Store documentation in the same repository as the code (Docs-as-Code) to ensure version control alignment.
- **Include Examples**: Provide runnable code snippets for every public function and major feature. Real-world usage is better than theoretical.
- **Automate Generation**: Use tools to generate API references from docstrings to avoid manual drift between code and docs.
- **Document Decisions**: Record the "Why" behind major choices in Architecture Decision Records (ADRs) to prevent future debates.
- **Update Regularly**: Treat documentation as a living artifact. Update it during code reviews, not as an afterthought.

### Don'ts
- **Comment the Obvious**: Avoid comments like `i = i + 1 // increment i`. The code should speak for itself.
- **Let Docs Rot**: Do not update code without updating the corresponding documentation.
- **Ignore Security**: Never omit documentation of security implications, authentication requirements, or known vulnerabilities.
- **Use Ambiguous Names**: Avoid variable names like `data`, `temp`, or `val` that require comments to explain.
- **Over-document**: Don't create a wall of text. If a function is too complex to document concisely, consider refactoring the function.

## Troubleshooting Guide

### Common Issues

#### Issue: Documentation Build Fails
**Symptoms:** The documentation generator throws syntax errors or warnings.
**Cause:** Malformed docstrings (e.g., missing closing brackets in JSDoc, incorrect indentation in Python) or invalid markdown syntax.
**Solution:** Run the linter specifically for documentation comments. Check the line numbers in the error log and fix the syntax in the source code.

#### Issue: Examples Don't Work
**Symptoms:** Users report that the code snippets in the README or API docs fail when executed.
**Cause:** Code drift—the API changed but the documentation wasn't updated.
**Solution:** Implement automated testing for documentation examples (e.g., Python's `doctest` or a dedicated test suite that runs README snippets).

#### Issue: "Why is this written this way?"
**Symptoms:** Developers want to refactor a piece of code that looks weird, not knowing it solves a specific edge case.
**Cause:** Lack of context in inline comments or ADRs.
**Solution:** Add an inline comment explaining the specific edge case or bug workaround, and link to an issue tracker or ADR if possible.

## Examples

### Example 1: Documenting a Complex Utility Function

**User Request:** "This function calculates a hash. It's hard to read. Please document it and make it cleaner."

**Approach:**
1.  **Refactor**: Rename variables from `a`, `b` to `inputString`, `salt`.
2.  **Docstring**: Add a JSDoc/Docstring block explaining the algorithm used (e.g., SHA-256) and why.
3.  **Inline Comment**: Add a comment explaining the magic number or specific bit-shifting logic if used.

**Code:**
```javascript
/**
 * Generates a salted hash for secure storage of user input.
 * Uses SHA-256 algorithm via the Web Crypto API.
 * 
 * @param {string} inputString - The plain text input to hash.
 * @param {string} salt - A unique random string to prevent rainbow table attacks.
 * @returns {Promise<string>} The hexadecimal representation of the hash.
 */
async function generateSecureHash(inputString, salt) {
  const encoder = new TextEncoder();
  const data = encoder.encode(inputString + salt);
  
  // Use Web Crypto API for a secure, non-blocking hash operation
  const hashBuffer = await crypto.subtle.digest('SHA-256', data);
  
  // Convert buffer to byte array, then to hex string
  return Array.from(new Uint8Array(hashBuffer))
    .map(b => b.toString(16).padStart(2, '0'))
    .join('');
}
```

**Expected Outcome:** The function is self-explanatory, secure, and includes a machine-readable description for IDE tooltips.

### Example 2: Creating a Project README

**User Request:** "We need a professional README for our new Node.js CLI tool."

**Approach:**
1.  **Structure**: Create sections for Title, Description, Installation, Usage, Commands, Contributing, and License.
2.  **Badges**: Add badges for npm version, license, and build status.
3.  **Code Blocks**: Ensure all command-line examples use proper syntax highlighting.

**Content Snippet:**
```markdown
# Awesome CLI

A blazing fast command-line interface for managing widgets.

[![npm version](https://badge.fury.io/js/awesome-cli.svg)](https://badge.fury.io/js/awesome-cli)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Installation

Install the package globally via npm:

```bash
npm install -g awesome-cli
```

## Usage

To initialize a new widget project:

```bash
awesome-cli init my-widget
```
```

**Expected Outcome:** A polished, standard-compliant README that allows users to get started immediately.

## Integration Notes

### Works Well With
- **code-review**: To enforce documentation standards during the PR process.
- **testing**: To ensure code examples in docs are tested automatically.
- **refactoring**: To update docs alongside code changes.

### Prerequisites
- Access to the source code repository.
- Knowledge of the specific programming language's documentation standard (e.g., PEP 257 for Python).
- (Optional) Documentation generation tools installed locally or in CI/CD.

## Quick Reference Card

| Task | Command/Action |
|------|----------------|
| Python Docstring | `"""Summary line. Args: ... Returns: ..."""` |
| JS Docstring | `/** @param {Type} name Description */` |
| Generate Sphinx Docs | `sphinx-build -b html source build` |
| Generate JSDoc | `jsdoc src/` |
| Create ADR | Create `docs/adr/0001-record-architecture-decisions.md` |

## Notes & Limitations

- **Context Dependency**: This skill generates documentation based on the code provided. If the business logic is inherently obscure or relies on external tacit knowledge, the documentation may require human input to be fully accurate.
- **Language Specifics**: While the skill covers general patterns, specific syntax for docstrings varies by language (e.g., Javadoc vs. Rustdoc). Always verify the generated syntax against the official language standard.
- **Performance**: Generating documentation for massive monorepos may take significant time; it is often better to run incrementally or on specific modules.

---
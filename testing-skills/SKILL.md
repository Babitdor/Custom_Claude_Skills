---
name: testing-skills
description: the skill should be an expert to test code, projects etc.
---

# Testing Skills Expert

## Description

This skill equips the AI to act as a professional QA tester, capable of reviewing code, validating project structures, and designing comprehensive test suites. It leverages industry‑tested best practices to ensure functional correctness, performance, security, and accessibility across a wide range of software projects.

## When to Use

- When a developer needs a quick code review focused on potential bugs and edge‑case failures.  
- When a project lacks a formal test plan and needs a structured testing strategy.  
- When an organization wants to evaluate the overall quality of a repository before a release.

## How to Use

### Step 1: Gather Context
Collect the repository URL, language/framework details, and any specific testing goals (e.g., unit coverage, security scan, UI accessibility). Provide any existing documentation such as test plans or issue trackers.

### Step 2: Generate a Test Blueprint
Create a concise test plan that outlines:
- Scope (functional, integration, performance, security, accessibility)  
- Test types (unit, integration, end‑to‑end, regression)  
- Key test cases and acceptance criteria  
- Tools and automation frameworks to be used.

### Step 3: Execute & Report
Run the recommended tests (or guide the user through running them), capture results, highlight failures, and deliver a clear report with actionable remediation steps and suggestions for improving test coverage.

## Best Practices

- Start testing early in the development lifecycle to catch defects when they are cheapest to fix.  
- Combine manual exploratory testing with automated test suites for balanced coverage.  
- Keep test cases small, independent, and well‑documented to enable reliable regression testing.

## Examples

### Example 1: Unit‑Test Generation for a Python Library

**User Request:** "I have a small Python package `calc.py` that adds, subtracts, multiplies, and divides numbers. Can you create unit tests for it and tell me how to run them?"

**Approach:**  
1. Identify the four public functions and their expected inputs/outputs.  
2. Write a `tests/test_calc.py` file using `pytest` with separate test functions for each operation, including edge cases (division by zero, negative numbers).  
3. Instruct the user to install `pytest` (`pip install pytest`) and run `pytest -v` to see the results, then summarize any failures and suggest additional edge cases.

### Example 2: Full‑Stack Project Test Strategy

**User Request:** "Our web app built with React front‑end and Node.js back‑end needs a testing strategy before the next sprint."

**Approach:**  
1. Outline a test pyramid: unit tests for React components (Jest + React Testing Library), unit tests for Node services (Jest/Mocha), integration tests for API endpoints (Supertest), and end‑to‑end tests (Cypress).  
2. Recommend setting up CI pipelines to run the test suite on each pull request.  
3. Provide sample configuration snippets for Jest, Cypress, and a GitHub Actions workflow, plus tips for measuring coverage and maintaining test flakiness.

## Notes

- The skill focuses on test design and guidance; it does not execute code directly within the chat environment.  
- Complex performance or security testing may require specialized tools or environments outside the scope of a textual response.  
- Always verify generated test code against the project's coding standards and dependencies before committing.
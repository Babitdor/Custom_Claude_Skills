# Nami Skills Library

A comprehensive collection of specialized skills for the Nami/Claude AI agent framework. Each skill provides domain-specific capabilities and workflows to enhance agent functionality across various domains.

## Overview

This library contains 25+ specialized skills that extend Nami agent capabilities in areas such as:

- **Art & Design**: Algorithmic art generation, canvas design, frontend design, theme factory
- **Documentation**: Code documentation, doc co-authoring, PDF/DOCX/PPTX manipulation
- **Research & Development**: Web research, arXiv search, LangChain DeepAgents, MCP server building
- **Testing & Quality**: Webapp testing, testing frameworks
- **Communication**: Internal communications templates, Slack GIF creation
- **Technical Skills**: Expert CSS, Three.js, Excel/Spreadsheet operations

## Available Skills

### Art & Design
- **[algorithmic-art](./algorithmic-art/)** - Create generative art using p5.js with seeded randomness
- **[brand-guidelines](./brand-guidelines/)** - Apply official brand colors and typography
- **[canvas-design](./canvas-design/)** - Create beautiful visual art in .png and .pdf formats
- **[frontend-design](./frontend-design/)** - Build production-grade frontend interfaces and components
- **[minimal_clean](./minimal_clean/)** - Minimalist and clean website designs with strategic whitespace
- **[slack-gif-creator](./slack-gif-creator/)** - Create animated GIFs optimized for Slack
- **[theme-factory](./theme-factory/)** - Style artifacts with pre-built or custom themes
- **[three-js-expert-skills](./three-js-expert-skills/)** - Expert guidance for Three.js applications
- **[web-artifacts-builder](./web-artifacts-builder/)** - Build complex multi-component HTML artifacts

### Documentation & Content
- **[code-documentation](./code-documentation/)** - Generate and maintain high-quality code documentation
- **[doc-coauthoring](./doc-coauthoring/)** - Structured workflow for co-authoring documentation
- **[docx](./docx/)** - Comprehensive document creation, editing, and analysis (.docx files)
- **[pdf](./pdf/)** - PDF manipulation toolkit for extraction, creation, and form handling
- **[pptx](./pptx/)** - Presentation creation, editing, and analysis (.pptx files)

### Research & Development
- **[arxiv-search](./arxiv-search/)** - Search arXiv preprint repository for academic papers
- **[deepagents-creator](./deepagents-creator/)** - Build autonomous LangChain DeepAgents with planning capabilities
- **[langgraph-docs](./langgraph-docs/)** - Fetch relevant LangGraph documentation
- **[mcp-builder](./mcp-builder/)** - Create high-quality MCP (Model Context Protocol) servers
- **[web-research](./web-research/)** - Conduct comprehensive web research
- **[skill-creator](./skill-creator/)** - Create effective new skills and update existing ones

### Technical & Operations
- **[expert-css-skills](./expert-css-skills/)** - Expert-level CSS guidance and optimization
- **[internal-comms](./internal-comms/)** - Internal communication templates (status reports, newsletters, etc.)
- **[testing-skills](./testing-skills/)** - Expert testing capabilities for code and projects
- **[webapp-testing](./webapp-testing/)** - Toolkit for testing local web applications using Playwright
- **[xlsx](./xlsx/)** - Comprehensive spreadsheet creation, editing, and analysis

## How Skills Work

Each skill follows a **progressive disclosure** pattern:

1. Skills are registered in the agent's system prompt with a name and brief description
2. When a task matches a skill's domain, the agent reads the skill's full `SKILL.md` file
3. The skill file contains detailed workflows, best practices, and examples
4. The agent follows the skill's instructions to execute the task

## Skill Structure

```
skill-name/
├── SKILL.md              # Main instruction file (required)
├── LICENSE.txt           # License file (if applicable)
├── scripts/              # Helper scripts and utilities
├── examples/             # Example files and templates
├── resources/            # Reference materials and documentation
└── templates/            # Code or document templates
```

## Creating New Skills

To create a new skill, use the **skill-creator** skill:

1. Read the skill-creator instructions at `skill-creator/SKILL.md`
2. Follow the workflow to create a new skill directory
3. Include a comprehensive `SKILL.md` with clear instructions
4. Add supporting files, scripts, and examples as needed
5. Test the skill thoroughly before deployment

## Using Skills

Skills are automatically available to the Nami agent when properly installed. When the agent encounters a task that matches a skill's description, it will:

1. Read the skill's `SKILL.md` file
2. Follow the provided workflow
3. Execute any helper scripts or utilities
4. Return results in the expected format

## Contributing

To contribute a new skill or improve an existing one:

1. Follow the existing skill structure and conventions
2. Include comprehensive documentation in `SKILL.md`
3. Provide clear examples and use cases
4. Test thoroughly across different scenarios
5. Ensure proper licensing for any included resources

## License

Each skill may have its own license. Refer to individual skill directories for specific licensing information.

## Support

For issues or questions about specific skills:
- Check the skill's `SKILL.md` for detailed instructions
- Review examples and supporting documentation
- Refer to the skill-creator for guidance on skill structure and best practices
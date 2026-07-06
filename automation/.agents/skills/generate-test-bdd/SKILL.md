---
name: generate-test-bdd
skill-name: generate-test-bdd
description: >
  Reads a plain-text requirements file (e.g. requirements.txt), converts the
  requirements into Gherkin-style `.feature` files, generates Cucumber/Playwright
  step definitions in TypeScript, and provides scripts to run the full BDD suite.
  Perfect for teams that want to automate acceptance testing from a simple text
  input.
---

# Skill: test-bdd

Generate a full Cucumber + Playwright BDD test suite from a plain-text requirements file.

## When to Use This Skill

Use this skill when:

- You have a plain-text list of requirements or user stories and want to generate automated tests from them.
- You want to quickly scaffold a new **Cucumber + Playwright + TypeScript** BDD project.
- You want to keep acceptance tests readable (Gherkin) while leveraging the power of Playwright for browser automation.

## Workflow

1. **Provide a requirements file**
   The user should supply a `.txt` file with user stories or requirements, e.g.

   ```text
   User can log in with valid credentials
   User sees an error message with invalid credentials
   User can reset their password via email
   ```

2. **Generate Gherkin `.feature` file**
   Convert each requirement into a `.feature` file with scenarios written in Gherkin syntax.

3. **Generate TypeScript step definitions**
   Create matching `.steps.ts` files that map Gherkin steps to Playwright automation code.

4. **Generate supporting boilerplate**
   - `cucumber.js` configuration
   - `package.json` with all required dependencies
   - `.env.example` for base URL and other settings
   - Playwright `setup` / `world` file to manage browser context

5. **Run tests**
   Provide the command to compile TypeScript and execute the Cucumber suite.

## Templates Provided

- `templates/{{featureName}}.feature` — Gherkin feature template
- `templates/{{featureName}}.steps.ts` — Step definitions
- `templates/cucumber.js` — Cucumber runner configuration
- `templates/package.json` — Dependencies and scripts
- `templates/.env.example` — Environment variables
- `templates/tsconfig.json` — TypeScript configuration
- `templates/world.ts` — Custom Cucumber World for Playwright

## Commands

- Generate tests from a requirements file
- Run the generated tests

## Quick Start

1. Place a `requirements.txt` file in your project.
2. Run the skill's generate command.
3. Install dependencies: `npm install`
4. Run tests: `npm test`

## Dependencies

- `@cucumber/cucumber`
- `@playwright/test`
- `playwright`
- `ts-node`
- `typescript`

## Notes

- This skill generates **boilerplate code**. You may need to refine selectors and adjust logic for your specific application.
- Ensure Playwright browsers are installed (`npx playwright install`) before running tests.

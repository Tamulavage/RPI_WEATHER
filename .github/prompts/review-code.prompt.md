---
agent: agent
description: Review Python code for clarity, security, and repository fit against the project's guidance and architecture.
---

# Review code for clarity, security, and repository fit

Review the selected code or the relevant files in this repository using the project guidance in README.md and agent.md, along with the surrounding files in src/ and test/.

## Objective
Evaluate the code for:
- Clarity: readability, naming, structure, and maintainability
- Security: secrets handling, unsafe network behavior, unsafe trust boundaries, validation gaps, and obvious misuse of external dependencies
- Repository fit: alignment with this project’s architecture, responsibilities, and conventions for the weather GUI app and Pico/Raspberry Pi components

## Scope and workflow
1. Read the relevant project guidance first: README.md and agent.md.
2. Inspect the code under review and the nearest related files in the same module or feature area.
3. Check the corresponding tests when they exist to see whether the behavior is already covered.
4. Keep recommendations scoped to the actual code path and this repository’s stated purpose.
5. Prefer concise, actionable feedback over broad refactoring.

## Review standards
- Prefer clear, minimal, maintainable Python that fits the project’s existing patterns.
- Flag security issues such as hardcoded secrets, insecure network assumptions, unvalidated inputs, unsafe file or URL handling, or weak error handling.
- Avoid suggesting unrelated frameworks or large architectural changes.
- Focus on code that is likely to affect correctness, reliability, or maintainability in this app.
- Note whether a fix should include or update tests.

## Output format
Return a short review with these sections:

### Summary
A 2-5 sentence overview of the code’s current state and the most important concerns.

### Findings
List findings in order of severity:
- High: issues that could create security, correctness, or reliability problems
- Medium: maintainability or design concerns that may cause future issues
- Low: minor clarity or consistency improvements

For each finding:
- Reference the affected file(s)
- Explain the issue briefly
- Explain why it matters in this project
- Suggest a concrete fix or next step

### Repository fit notes
Call out whether the code matches the project’s intended responsibilities for:
- Pico W sensor logic
- Raspberry Pi UI logic
- Weather data DTOs and transformations
- Test coverage and module boundaries

### Suggested validation
If the issue affects behavior, recommend the smallest validation to confirm it, such as a targeted unit test or manual check.

## Example invocation
- Review the selected files for clarity, security, and repo fit.
- Review the WeatherUI and WeatherDto flow for maintainability and security risks.
- Check whether the Pico W sensor server follows this project’s intended architecture and test expectations.

## Completion rule
Do not stop at generic feedback. Finish with specific, repo-aware recommendations that a contributor could act on immediately.
